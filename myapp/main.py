from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import database
import dbentities
from database import engine, session
from models import FacultyBase, StudentBase

app = FastAPI();

database.Base.metadata.create_all(bind=engine)
def get_db():
    sessionDb = session();
    try:
        yield sessionDb
    finally:
        sessionDb.close();

db_dependency = Depends(get_db)

faculty_tag = "Faculty";
student_tag = "Student";

# Faculty #
@app.post("/api/v1/faculty/create",tags=[faculty_tag])
def create_faculty(faculty_base: FacultyBase, db: Session = db_dependency):
    if (faculty_base != None) & (faculty_base.name != ""):
        db_faculty = dbentities.Faculty(name=faculty_base.name);
        db.add(db_faculty);
        db.commit();
        db.refresh(db_faculty);
        return f"Faculty id: {db_faculty.id}";
    raise HTTPException(status_code=400,detail="Faculty base should not be empty")
@app.get("/api/v1/faculties", tags=[faculty_tag])
def get_faculties(db: Session = db_dependency):
    return db.query(dbentities.Faculty).all();
@app.put("/api/v1/faculty/edit/{faculty_id}", tags=[faculty_tag])
def update_faculty(faculty_id: int,faculty_base: FacultyBase ,db: Session = db_dependency):
    db_faculty = db.query(dbentities.Faculty).filter(dbentities.Faculty.id == faculty_id).first();
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty with that id not found!");
    db_faculty.name = faculty_base.name;
    db.commit();
    db.refresh(db_faculty);
    return f"Changed faculty name to {db_faculty.name}";
@app.delete("/api/v1/faculty/delete/{faculty_id}", tags=[faculty_tag])
def delete_faculty(faculty_id: int, db: Session = db_dependency):
    db_faculty = db.query(dbentities.Faculty).filter(dbentities.Faculty.id == faculty_id).first();
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty does not exist!");
    db.delete(db_faculty);
    db.commit();
    return f"Faculty with id: {faculty_id} successfully deleted";

# Student #
@app.get("/api/v1/students",tags=[student_tag])
def get_students(db: Session = db_dependency):
    return db.query(dbentities.Student).all();
@app.post("/api/v1/students/create", tags=[student_tag])
def create_student(student_base: StudentBase,db: Session = db_dependency):
    db_faculty = db.query(dbentities.Faculty).filter(dbentities.Faculty.id == student_base.faculty_id).first();
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db_student = dbentities.Student(full_name=student_base.full_name,age=student_base.age,faculty_id=db_faculty.id);
    db.add(db_student);
    db.commit();
    db.refresh(db_student);
    return f"Student id: {db_student.id}";
@app.put("/api/v1/students/edit/{student_id}",tags=[student_tag])
def update_student(student_id: int,student_base: StudentBase ,db: Session = db_dependency):
    db_student = db.query(dbentities.Student).filter(dbentities.Student.id == student_id).first();
    db_faculty = db.query(dbentities.Faculty).filter(dbentities.Faculty.id == student_base.faculty_id).first();
    if not db_student:
        raise HTTPException(status_code=404, detail="Student with that id does not exist!");
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty with that id does not exist!");
    db_student.full_name=student_base.full_name;
    db_student.age = student_base.age;
    db_student.faculty_id=student_base.faculty_id;
    db.commit();
    db.refresh(db_student)
    return f"Updated student with id {db_student.id}";
@app.delete("/api/v1/students/delete/{student_id}",tags=[student_tag])
def delete_student(student_id: int, db:Session=db_dependency):
    db_student = db.query(dbentities.Student).filter(dbentities.Student.id == student_id).first();
    if not db_student:
        raise HTTPException(status_code=404, detail="Student with that id does not exist!");
    db.delete(db_student);
    db.commit();
    return f"Student with id {student_id} deleted successfully!";
