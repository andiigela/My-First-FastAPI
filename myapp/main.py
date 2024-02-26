from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import database
import dbentities
from database import engine, session
from models import FacultyBase, StudentBase, SubjectBase, StudentSubjectBase

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
subject_tag = "Subject";
subjectparticipations_tag = "SubjectParticipations";

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


# Subject #
@app.get("/api/v1/subjects",tags=[subject_tag])
def get_subjects(db: Session = db_dependency):
    return db.query(dbentities.Subject).all();
@app.post("/api/v1/subjects/create", tags=[subject_tag])
def create_subject(subject_base: SubjectBase,db: Session = db_dependency):
    if (subject_base == None) | (subject_base.name == ""):
        raise HTTPException(status_code=404, detail="Subject must not be null or empty");
    db_subject = dbentities.Subject(name=subject_base.name);
    db.add(db_subject);
    db.commit();
    db.refresh(db_subject);
    return f"Subject id: {db_subject.id}";
@app.put("/api/v1/subjects/edit/{subject_id}",tags=[subject_tag])
def update_subject(subject_id: int,subject_base: SubjectBase ,db: Session = db_dependency):
    db_subject = db.query(dbentities.Subject).filter(dbentities.Subject.id == subject_id).first();
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject with that id does not exist!");
    db_subject.name = subject_base.name;
    db.commit();
    db.refresh(db_subject)
    return f"Updated subject with id {db_subject.id}";

@app.delete("/api/v1/subjects/delete/{subject_id}",tags=[subject_tag])
def delete_subject(subject_id: int, db:Session=db_dependency):
    db_subject = db.query(dbentities.Subject).filter(dbentities.Subject.id == subject_id).first();
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject with that id does not exist!");
    db.delete(db_subject);
    db.commit();
    return f"Subject with id {db_subject.id} deleted successfully!";

# Student - Subject #
@app.get("/api/v1/subjectparticipations",tags=[subjectparticipations_tag])
def get_subjectparticipations(db: Session = db_dependency):
    return db.query(dbentities.StudentSubject).all();
@app.post("/api/v1/subjectparticipations/create", tags=[subjectparticipations_tag])
def create_participation(studentsubject_base: StudentSubjectBase,db: Session = db_dependency):
    db_student = db.query(dbentities.Student).filter(dbentities.Student.id == studentsubject_base.student_id).first();
    db_subject = db.query(dbentities.Subject).filter(dbentities.Subject.id == studentsubject_base.subject_id).first();
    if (not db_student) | (not db_subject):
        raise HTTPException(status_code=404, detail="Student or Subject does not exist");
    if (studentsubject_base.student_id <= 0) | (studentsubject_base.subject_id <= 0):
        raise HTTPException(status_code=404, detail="id's must be greater than 0");
    db_participation = dbentities.StudentSubject(student_id=studentsubject_base.student_id,subject_id=studentsubject_base.subject_id);
    db.add(db_participation);
    db.commit();
    db.refresh(db_participation);
    return f"Participation created: {db_student.full_name} - {db_subject.name}";
@app.put("/api/v1/subjectparticipations/edit/{student_id}/{subject_id}",tags=[subjectparticipations_tag])
def update_participation(student_id: int,subject_id: int,studentsubject_base: StudentSubjectBase,db: Session = db_dependency):
    db_studentsubject = db.query(dbentities.StudentSubject).filter((dbentities.StudentSubject.student_id == student_id) & (dbentities.StudentSubject.subject_id == subject_id)).first()
    if not db_studentsubject:
        raise HTTPException(status_code=404, detail="Participation does not exist!");
    db_studentsubject.student_id = studentsubject_base.student_id;
    db_studentsubject.subject_id = studentsubject_base.subject_id;
    db.commit();
    db.refresh(db_studentsubject)
    return f"Updated participation from: {student_id} - {subject_id} to {db_studentsubject.student_id} - {db_studentsubject.subject_id}";

@app.delete("/api/v1/subjectparticipations/delete/{student_id}/{subject_id}",tags=[subjectparticipations_tag])
def delete_subject(student_id: int,subject_id: int, db:Session=db_dependency):
    db_studentsubject = db.query(dbentities.StudentSubject).filter((dbentities.StudentSubject.student_id == student_id) & (dbentities.StudentSubject.subject_id == subject_id)).first()
    if not db_studentsubject:
        raise HTTPException(status_code=404, detail="Participation with that id does not exist!");
    db.delete(db_studentsubject);
    db.commit();
    return f"Subject with id {student_id} - {subject_id} deleted successfully!";