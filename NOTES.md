# 🚀 Employee Management System - Multi-Cloud Project Notes

## 📋 Project Summary & Status
- **Current State:** Fully operational and deployed live on Render.
- **Backend Fabric:** Python FastAPI running inside a lightweight, compilation-free Linux Docker container on Port 7000.
- **Database Engine:** Multi-cloud agnostic configuration. Currently utilizes a shared-cache, in-memory SQLite setup (`sqlite:///file:mem_employee?mode=memory&cache=shared`) that cleanly synchronizes data across all independent multi-threaded Uvicorn execution paths without requiring heavy local system C++ drivers.
- **Frontend Layer:** Cross-origin relative path structure utilizing modern JavaScript `async/await` syntax to guarantee error-free rendering.

---

## 🐍 1. Final Backend Script (`app.py`)
```python
import os
import logging
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("uvicorn.error")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENGINE SETUP ---
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.info("No cloud database string detected. Spawning shared cache in-memory SQLite engine...")
    DATABASE_URL = "sqlite:///file:mem_employee?mode=memory&cache=shared"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    logger.info("Connecting to external cloud database engine...")
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE TABLE MODEL ---
class EmployeeTable(Base):
    __tablename__ = "tbl_employee"
    __table_args__ = {'schema': 'dbo'} if DATABASE_URL and DATABASE_URL.startswith("mssql") else None

    empcode = Column(String(50), primary_key=True, nullable=False)
    empname = Column(String(150), nullable=False)
    empaddress = Column(String(255), nullable=True)
    empzipcode = Column(String(20), nullable=True)
    empstatus = Column(String(20), nullable=False, default="ACTIVE")

Base.metadata.create_all(bind=engine)

# --- DATA SEED ENGINE ---
def seed_database():
    db = SessionLocal()
    try:
        count = db.query(EmployeeTable).count()
        if count == 0:
            logger.info("Initializing Seed Sequence...")
            sample_employees = [
                EmployeeTable(empcode="101", empname="Alex Mercer M", empaddress="123 Tech Park", empzipcode="560001", empstatus="ACTIVE"),
                EmployeeTable(empcode="102", empname="Sarah Connor", empaddress="456 Skynet Blvd", empzipcode="560036", empstatus="ACTIVE"),
                EmployeeTable(empcode="103", empname="Bruce Wayne", empaddress="1007 Mountain Drive", empzipcode="560099", empstatus="ACTIVE"),
                EmployeeTable(empcode="104", empname="Diana Prince", empaddress="Themyscira Embassy", empzipcode="560012", empstatus="INACTIVE"),
                EmployeeTable(empcode="105", empname="Clark Kent", empaddress="345 Metropolis Way", empzipcode="560045", empstatus="ACTIVE")
            ]
            db.add_all(sample_employees)
            db.commit()
            logger.info("Seed Sequence Completed.")
    except Exception as e:
        logger.error(f"Failed to execute startup database seed: {e}")
    finally:
        db.close()

seed_database()

class EmployeeSchema(BaseModel):
    empcode: str
    empname: str
    empaddress: str
    empzipcode: str
    empstatus: str

    @field_validator("empcode", "empname", "empaddress", "empzipcode")
    @classmethod
    def sanitize_inputs(cls, value: str) -> str:
        clean_value = value.strip()
        clean_value = re.sub(r"<[^>]*>", "", clean_value)
        if not clean_value:
            raise ValueError("Fields cannot consist of blank spaces.")
        return clean_value

@app.get("/")
def read_index():
    return FileResponse("app.html")

@app.get("/employees")
def get_all_employees():
    db = SessionLocal()
    try:
        return db.query(EmployeeTable).order_by(EmployeeTable.empname.asc()).all()
    finally:
        db.close()

@app.post("/employees")
def create_employee(employee: EmployeeSchema):
    db = SessionLocal()
    try:
        existing = db.query(EmployeeTable).filter(EmployeeTable.empcode == employee.empcode).first()
        if existing:
            raise HTTPException(status_code=400, detail="Employee code already exists")
        new_emp = EmployeeTable(
            empcode=employee.empcode, empname=employee.empname,
            empaddress=employee.empaddress, empzipcode=employee.empzipcode, empstatus=employee.empstatus
        )
        db.add(new_emp)
        db.commit()
        return {"message": "Saved successfully!"}
    finally:
        db.close()

@app.put("/employees/{emp_code}")
def update_employee(emp_code: str, employee: EmployeeSchema):
    db = SessionLocal()
    try:
        db_emp = db.query(EmployeeTable).filter(EmployeeTable.empcode == emp_code).first()
        if not db_emp:
            raise HTTPException(status_code=404, detail="Employee not found")
        db_emp.empname = employee.empname
        db_emp.empaddress = employee.empaddress
        db_emp.empzipcode = employee.empzipcode
        db_emp.empstatus = employee.empstatus
        db.commit()
        return {"message": f"Employee {emp_code} updated successfully!"}
    finally:
        db.close()

@app.delete("/employees/{emp_code}")
def delete_employee(emp_code: str):
    db = SessionLocal()
    try:
        db_emp = db.query(EmployeeTable).filter(EmployeeTable.empcode == emp_code).first()
        if not db_emp:
            raise HTTPException(status_code=404, detail="Employee not found to delete")
        db.delete(db_emp)
        db.commit()
        return {"message": f"Employee {emp_code} removed safely!"}
    finally:
        db.close()
```

## 🌐 2. Final UI Script (`app.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Management System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 2.5fr; gap: 30px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: fit-content; }
        h2 { margin-top: 0; color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 600; font-size: 14px; }
        input, select { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #2ecc71; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; }
        button:hover { background-color: #27ae60; }
        .search-wrapper { margin-bottom: 15px; }
        #searchBar { padding: 10px; border: 2px solid #34495e; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box; }
        .table-scroll-container { max-height: 450px; overflow-y: auto; border: 1px solid #ddd; border-radius: 4px; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; font-size: 14px; }
        th { background-color: #34495e; color: white; position: sticky; top: 0; z-index: 1; }
        tr:hover { background-color: #f1f2f6; }
        .btn-delete { background-color: #e74c3c; padding: 5px 10px; width: auto; font-size: 12px; display: inline-block; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .btn-delete:hover { background-color: #c0392b; }
        .btn-edit { background-color: #3498db; width: auto; font-size: 12px; padding: 5px 10px; margin-right: 5px; display: inline-block; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .btn-edit:hover { background-color: #2980b9; }
    </style>
</head>
<body>
    <h1 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">Employee Database Directory</h1>
    <div class="container">
        <div class="card">
            <h2>Add Employee</h2>
            <form id="empForm">
                <div class="form-group"><label>Emp Code</label><input type="text" id="empcode" required></div>
                <div class="form-group"><label>Name</label><input type="text" id="empname" required></div>
                <div class="form-group"><label>Address</label><input type="text" id="empaddress" required></div>
                <div class="form-group"><label>Zip Code</label><input type="text" id="empzipcode" required></div>
                <div class="form-group">
                    <label>Status</label>
                    <select id="empstatus">
                        <option value="ACTIVE">ACTIVE</option>
                        <option value="INACTIVE">INACTIVE</option>
                    </select>
                </div>
                <button type="submit" id="submitBtn">Save Record</button>
            </form>
        </div>
        <div class="card">
            <h2>Employee List</h2>
            <div class="search-wrapper"><input type="text" id="searchBar" placeholder="🔍 Type to search employees..."></div>
            <div class="table-scroll-container">
                <table>
                    <thead>