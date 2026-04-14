from fastapi import FastAPI, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import uuid
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------- DATABASE DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- API KEY VALIDATION ----------------
def verify_api_key(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    key = db.query(models.ApiKey).filter(
        models.ApiKey.key == x_api_key
    ).first()

    if not key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return x_api_key


# ---------------- API USAGE TRACKING ----------------
def log_api_usage(api_key: str, endpoint: str, db: Session):
    usage = models.ApiUsage(
        api_key=api_key,
        endpoint=endpoint,
        timestamp=datetime.utcnow()
    )
    db.add(usage)
    db.commit()


# ---------------- GENERATE API KEY ----------------
@app.post("/generate-api-key")
def generate_api_key(owner_name: str, db: Session = Depends(get_db)):
    new_key = str(uuid.uuid4())

    api_key = models.ApiKey(
        key=new_key,
        owner_name=owner_name
    )

    db.add(api_key)
    db.commit()

    return {
        "api_key": new_key,
        "owner": owner_name
    }


# ---------------- STATES ----------------
@app.get("/states")
def get_states(
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    log_api_usage(api_key, "/states", db)

    states = db.query(models.State).all()
    return states


@app.post("/states")
def create_state(
    state_name: str,
    db: Session = Depends(get_db)
):
    state = models.State(state_name=state_name)

    db.add(state)
    db.commit()
    db.refresh(state)

    return state


# ---------------- DISTRICTS ----------------
@app.post("/districts")
def create_district(
    district: dict,
    db: Session = Depends(get_db)
):
    new_district = models.District(
        district_name=district["district_name"],
        state_id=district["state_id"]
    )

    db.add(new_district)
    db.commit()
    db.refresh(new_district)

    return new_district


@app.get("/districts/{state_id}")
def get_districts(
    state_id: int,
    db: Session = Depends(get_db)
):
    districts = db.query(models.District).filter(
        models.District.state_id == state_id
    ).all()

    return districts


# ---------------- SUBDISTRICTS ----------------
@app.post("/subdistricts")
def create_subdistrict(
    subdistrict: dict,
    db: Session = Depends(get_db)
):
    new_subdistrict = models.SubDistrict(
        sub_district_name=subdistrict["sub_district_name"],
        district_id=subdistrict["district_id"]
    )

    db.add(new_subdistrict)
    db.commit()
    db.refresh(new_subdistrict)

    return new_subdistrict


@app.get("/subdistricts/{district_id}")
def get_subdistricts(
    district_id: int,
    db: Session = Depends(get_db)
):
    subdistricts = db.query(models.SubDistrict).filter(
        models.SubDistrict.district_id == district_id
    ).all()

    return subdistricts


# ---------------- VILLAGES ----------------
@app.post("/villages")
def create_village(
    village: dict,
    db: Session = Depends(get_db)
):
    new_village = models.Village(
        village_name=village["village_name"],
        sub_district_id=village["sub_district_id"]
    )

    db.add(new_village)
    db.commit()
    db.refresh(new_village)

    return new_village


@app.get("/villages/{subdistrict_id}")
def get_villages(
    subdistrict_id: int,
    db: Session = Depends(get_db)
):
    villages = db.query(models.Village).filter(
        models.Village.sub_district_id == subdistrict_id
    ).all()

    return villages


# ---------------- SEARCH ----------------
@app.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    states = db.query(models.State).filter(
        models.State.state_name.ilike(f"%{query}%")
    ).all()

    districts = db.query(models.District).filter(
        models.District.district_name.ilike(f"%{query}%")
    ).all()

    subdistricts = db.query(models.SubDistrict).filter(
        models.SubDistrict.sub_district_name.ilike(f"%{query}%")
    ).all()

    villages = db.query(models.Village).filter(
        models.Village.village_name.ilike(f"%{query}%")
    ).all()

    return {
        "states": states,
        "districts": districts,
        "subdistricts": subdistricts,
        "villages": villages
    }


# ---------------- AUTOCOMPLETE (FINAL FIX) ----------------
@app.get("/autocomplete")
def autocomplete(query: str = Query(...), db: Session = Depends(get_db)):
    query_lower = query.lower()

    states = db.query(models.State).filter(
        models.State.state_name.ilike(f"%{query_lower}%")
    ).all()

    districts = db.query(models.District).filter(
        models.District.district_name.ilike(f"%{query_lower}%")
    ).all()

    subdistricts = db.query(models.SubDistrict).filter(
        models.SubDistrict.sub_district_name.ilike(f"%{query_lower}%")
    ).all()

    villages = db.query(models.Village).filter(
        models.Village.village_name.ilike(f"%{query_lower}%")
    ).all()

    suggestions = []

    for s in states:
        suggestions.append(s.state_name)

    for d in districts:
        suggestions.append(d.district_name)

    for sd in subdistricts:
        suggestions.append(sd.sub_district_name)

    for v in villages:
        suggestions.append(v.village_name)

    return {
        "suggestions": suggestions
    }