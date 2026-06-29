import os
import logging
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.responses import HTMLResponse

# --- 1. FIXED LOGGING SYSTEM ---
logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. MULTI-ENVIRONMENT SQLALCHEMY ENGINE SETUP ---
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.info("No cloud database string detected. Spawning free in-memory SQLite engine...")
    DATABASE_URL = "sqlite:///file:mem_employee?mode=memory&cache=shared"
    engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})
else:
    logger.info("Connecting to external cloud database engine...")
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 3. DATABASE TABLE MODEL (CLEAN & UNIQUE) ---
class EmployeeTable(Base):
    __tablename__ = "tbl_employee"
    
    # Safely injects the 'dbo' schema ONLY if you are explicitly targeted on a Microsoft SQL DB
    __table_args__ = {'schema': 'dbo'} if DATABASE_URL and DATABASE_URL.startswith("mssql") else None

    empcode = Column(String(50), primary_key=True, nullable=False)
    empname = Column(String(150), nullable=False)
    empaddress = Column(String(255), nullable=True)
    empzipcode = Column(String(20), nullable=True)
    empstatus = Column(String(20), nullable=False, default="ACTIVE")

# Programmatically build table layouts cleanly
Base.metadata.create_all(bind=engine)

# --- 4. AUTOMATED DATABASE SEED ENGINE ---
def seed_database():
    db = SessionLocal()
    try:
        count = db.query(EmployeeTable).count()
        if count == 0:
            logger.info("Initializing Seed Sequence: 'tbl_employee' is empty. Injecting sample records...")
            sample_employees = [
                EmployeeTable(empcode="101", empname="Alex Mercer", empaddress="123 Tech Park", empzipcode="560001", empstatus="ACTIVE"),
                EmployeeTable(empcode="102", empname="Sarah Connor", empaddress="456 Skynet Blvd", empzipcode="560036", empstatus="ACTIVE"),
                EmployeeTable(empcode="103", empname="Bruce Wayne", empaddress="1007 Mountain Drive", empzipcode="560099", empstatus="ACTIVE"),
                EmployeeTable(empcode="104", empname="Diana Prince", empaddress="Themyscira Embassy", empzipcode="560012", empstatus="INACTIVE"),
                EmployeeTable(empcode="105", empname="Clark Kent", empaddress="345 Metropolis Way", empzipcode="560045", empstatus="ACTIVE")
            ]
            db.add_all(sample_employees)
            db.commit()
            logger.info("Seed Sequence Completed: 5 structural sample records committed to database.")
        else:
            logger.info(f"Database Verification: 'tbl_employee' contains {count} existing rows. Skipping data seed.")
    except Exception as e:
        logger.error(f"Failed to execute startup database seed: {e}")
    finally:
        db.close()

seed_database()

# --- 5. INPUT SANITIZATION VALIDATOR (PYDANTIC) ---
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

# --- 6. USER INTERFACE STATIC ROUTER ---
@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("app.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    # We return it with strict 'No-Cache' headers to force your mobile and desktop browsers 
    # to completely throw away old cached structures and download the fresh JS code block immediately.
    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return HTMLResponse(content=html_content, status_code=200, headers=headers)

# --- 7. DATABASE OPERATIONS ---
@app.get("/employees")
def get_all_employees():
    logger.info("HTTP GET Request: Fetching all active employee profile records.")
    db = SessionLocal()
    try:
        employees = db.query(EmployeeTable).order_by(EmployeeTable.empname.asc()).all()
        return employees
    finally:
        db.close()

@app.post("/employees")
def create_employee(employee: EmployeeSchema):
    logger.info(f"HTTP POST Request: Attempting registration for EmpCode: {employee.empcode}")
    db = SessionLocal()
    try:
        existing = db.query(EmployeeTable).filter(EmployeeTable.empcode == employee.empcode).first()
        if existing:
            logger.warning(f"Conflict Blocked: Employee code {employee.empcode} already exists.")
            raise HTTPException(status_code=400, detail="Employee code already exists")
        
        new_emp = EmployeeTable(
            empcode=employee.empcode,
            empname=employee.empname,
            empaddress=employee.empaddress,
            empzipcode=employee.empzipcode,
            empstatus=employee.empstatus
        )
        db.add(new_emp)
        db.commit()
        logger.info(f"Transaction Committed: Verified record '{employee.empname}' saved using SQLAlchemy.")
        return {"message": "Saved successfully!"}
    finally:
        db.close()

@app.put("/employees/{emp_code}")
def update_employee(emp_code: str, employee: EmployeeSchema):
    logger.info(f"HTTP PUT Request: Attempting database update for trace code: {emp_code}")
    db = SessionLocal()
    try:
        db_emp = db.query(EmployeeTable).filter(EmployeeTable.empcode == emp_code).first()
        if not db_emp:
            logger.warning(f"Update Aborted: Target code {emp_code} not found.")
            raise HTTPException(status_code=404, detail="Employee not found")
        
        db_emp.empname = employee.empname
        db_emp.empaddress = employee.empaddress
        db_emp.empzipcode = employee.empzipcode
        db_emp.empstatus = employee.empstatus
        
        db.commit()
        logger.info(f"Transaction Committed: Target profile code {emp_code} modified successfully.")
        return {"message": f"Employee {emp_code} updated successfully!"}
    finally:
        db.close()

@app.delete("/employees/{emp_code}")
def delete_employee(emp_code: str):
    logger.info(f"HTTP DELETE Request: Initiating purge transaction on entity code: {emp_code}")
    db = SessionLocal()
    try:
        db_emp = db.query(EmployeeTable).filter(EmployeeTable.empcode == emp_code).first()
        if not db_emp:
            logger.warning(f"Delete Aborted: Purge target code {emp_code} missing.")
            raise HTTPException(status_code=404, detail="Employee not found to delete")
        
        db.delete(db_emp)
        db.commit()
        logger.info(f"Transaction Committed: Purged employee code {emp_code} from database storage tables.")
        return {"message": f"Employee {emp_code} removed safely!"}
    finally:
        db.close()