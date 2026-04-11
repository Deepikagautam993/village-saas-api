from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List
from sqlalchemy import func

from database import engine, Base, SessionLocal
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- API KEY ----------------
def verify_api_key(x_api_key: str = Header(None), db: Session = Depends(get_db)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key missing")

    key = db.query(models.ApiKey).filter(models.ApiKey.key == x_api_key).first()

    if not key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return key


# ---------------- SCHEMAS ----------------
class StateCreate(BaseModel):
    state_name: str


class StateResponse(BaseModel):
    id: int
    state_name: str

    class Config:
        from_attributes = True


class DistrictCreate(BaseModel):
    district_name: str
    state_id: int


class SubDistrictCreate(BaseModel):
    sub_district_name: str
    district_id: int


class VillageCreate(BaseModel):
    village_name: str
    sub_district_id: int


# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "Village SaaS API Running"}


# ---------------- API KEY GENERATION ----------------
@app.post("/generate-api-key")
def generate_api_key(owner_name: str, db: Session = Depends(get_db)):
    new_key = models.ApiKey(owner_name=owner_name)
    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    return {
        "api_key": new_key.key,
        "owner": new_key.owner_name
    }


# ---------------- USAGE TRACKING FUNCTION ----------------
def track_usage(db: Session, api_key: str, endpoint: str):
    log = models.ApiUsage(
        api_key=api_key,
        endpoint=endpoint
    )
    db.add(log)
    db.commit()


# ---------------- STATES ----------------
@app.post("/states")
def create_state(state: StateCreate, db: Session = Depends(get_db)):
    try:
        new_state = models.State(state_name=state.state_name)
        db.add(new_state)
        db.commit()
        db.refresh(new_state)
        return new_state

    except IntegrityError:
        db.rollback()
        return {"message": "State already exists"}


@app.get("/states", response_model=List[StateResponse])
def get_states(
    db: Session = Depends(get_db),
    api_key=Depends(verify_api_key)
):
    track_usage(db, api_key.key, "/states")
    return db.query(models.State).all()


@app.put("/states/{state_id}")
def update_state(state_id: int, state: StateCreate, db: Session = Depends(get_db)):
    existing = db.query(models.State).filter(models.State.id == state_id).first()

    if not existing:
        return {"message": "State not found"}

    existing.state_name = state.state_name
    db.commit()
    db.refresh(existing)

    return existing


@app.delete("/states/{state_id}")
def delete_state(state_id: int, db: Session = Depends(get_db)):
    state = db.query(models.State).filter(models.State.id == state_id).first()

    if not state:
        return {"message": "State not found"}

    db.delete(state)
    db.commit()

    return {"message": "State deleted"}


# ---------------- DISTRICTS ----------------
@app.post("/districts")
def create_district(district: DistrictCreate, db: Session = Depends(get_db)):
    new = models.District(
        district_name=district.district_name,
        state_id=district.state_id
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get("/districts")
def get_districts(db: Session = Depends(get_db)):
    return db.query(models.District).all()


@app.get("/states/{state_id}/districts")
def get_districts_by_state(state_id: int, db: Session = Depends(get_db)):
    return db.query(models.District).filter(models.District.state_id == state_id).all()


# ---------------- SUBDISTRICTS ----------------
@app.post("/subdistricts")
def create_subdistrict(sub: SubDistrictCreate, db: Session = Depends(get_db)):
    new = models.SubDistrict(
        sub_district_name=sub.sub_district_name,
        district_id=sub.district_id
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get("/subdistricts")
def get_subdistricts(db: Session = Depends(get_db)):
    return db.query(models.SubDistrict).all()


# ---------------- VILLAGES ----------------
@app.post("/villages")
def create_village(v: VillageCreate, db: Session = Depends(get_db)):
    new = models.Village(
        village_name=v.village_name,
        sub_district_id=v.sub_district_id
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get("/villages")
def get_villages(db: Session = Depends(get_db)):
    return db.query(models.Village).all()


# ---------------- SEARCH ----------------
@app.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    states = db.query(models.State).filter(models.State.state_name.contains(query)).all()
    districts = db.query(models.District).filter(models.District.district_name.contains(query)).all()
    villages = db.query(models.Village).filter(models.Village.village_name.contains(query)).all()

    return {
        "states": states,
        "districts": districts,
        "villages": villages
    }


# ---------------- AUTOCOMPLETE ----------------
@app.get("/autocomplete")
def autocomplete(query: str, db: Session = Depends(get_db)):
    states = db.query(models.State.state_name)\
        .filter(func.lower(models.State.state_name).contains(query.lower()))\
        .limit(5).all()

    districts = db.query(models.District.district_name)\
        .filter(func.lower(models.District.district_name).contains(query.lower()))\
        .limit(5).all()

    villages = db.query(models.Village.village_name)\
        .filter(func.lower(models.Village.village_name).contains(query.lower()))\
        .limit(5).all()

    results = [s[0] for s in states] + [d[0] for d in districts] + [v[0] for v in villages]

    return {"suggestions": results}


# ---------------- USAGE API ----------------
@app.get("/usage")
def get_usage(api_key=Depends(verify_api_key)):
    return {
        "api_key": api_key.key,
        "status": "tracking enabled (database based SaaS ready)"
    }