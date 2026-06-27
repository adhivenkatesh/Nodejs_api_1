import logging
import re
import urllib.parse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# --- 1. FIXED LOGGING SYSTEM (BOUND TO UVICORN STREAM) ---
# This grabs FastAPI's active running logger so no actions are muted
logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. SQLALCHEMY ENGINE SETUP ---
raw_conn_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=(LocalDb)\\MSSQLLocalDB;"
    "Database=db_employee;"
    "Trusted_Connection=yes;"  
    "TrustServerCertificate=yes;"
)
params = urllib.parse.quote_plus(raw_conn_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 3. DATABASE TABLE MODEL ---
class EmployeeTable(Base):
    __tablename__ = "tbl_employee"
    __table_args__ = {'schema': 'dbo'}

    empcode = Column(String(50), primary_key=True, nullable=False)
    empname = Column(String(150), nullable=False)
    empaddress = Column(String(255), nullable=True)
    empzipcode = Column(String(20), nullable=True)
    empstatus = Column(String(20), nullable=False, default="ACTIVE")

# Programmatically build table layouts
Base.metadata.create_all(bind=engine)

# --- 4. AUTOMATED DATABASE SEED ENGINE ---
def seed_database():
    db = SessionLocal()
    try:
        # Check if any employee entries exist inside the table grid
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

# Fire seed verification query immediately upon application startup context
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
        clean_value = re.sub(r"<[^>]*>", "", clean_value) # Block Cross-Site Scripting (XSS)
        if not clean_value:
            raise ValueError("Fields cannot consist of blank spaces.")
        return clean_value


# --- 6. USER INTERFACE STATIC ROUTER ---
@app.get("/")
def read_index():
    return FileResponse("app.html")


# --- 7. DATABASE OPERATIONS (WITH ACTIVE CONSOLE LOGGING) ---

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
            logger.warning(f"Conflict Blocked: Employee code {employee.empcode} already exists inside SQL Server.")
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