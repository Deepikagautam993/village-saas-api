from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


# ---------------- STATE ----------------
class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String, unique=True, index=True)

    districts = relationship("District", back_populates="state")


# ---------------- DISTRICT ----------------
class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String, index=True)
    state_id = Column(Integer, ForeignKey("states.id"))

    state = relationship("State", back_populates="districts")
    subdistricts = relationship("SubDistrict", back_populates="district")


# ---------------- SUB DISTRICT ----------------
class SubDistrict(Base):
    __tablename__ = "subdistricts"

    id = Column(Integer, primary_key=True, index=True)
    sub_district_name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))

    district = relationship("District", back_populates="subdistricts")
    villages = relationship("Village", back_populates="subdistrict")


# ---------------- VILLAGE ----------------
class Village(Base):
    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    village_name = Column(String, index=True)
    sub_district_id = Column(Integer, ForeignKey("subdistricts.id"))

    subdistrict = relationship("SubDistrict", back_populates="villages")


# ---------------- API KEY ----------------
class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    owner_name = Column(String)


# ---------------- API USAGE ----------------
class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)