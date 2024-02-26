from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base
class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True)
    age = Column(Integer)
    faculty_id = Column(Integer, ForeignKey("faculty.id",ondelete='CASCADE'))
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer,primary_key=True)
    name = Column(String, index=True)

class StudentSubject(Base):
    __tablename__ = "student_subject"
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), primary_key=True)