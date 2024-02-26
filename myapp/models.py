from typing import List
from pydantic import BaseModel
class StudentBase(BaseModel):
    full_name: str
    age: int
    faculty_id: int
class FacultyBase(BaseModel):
    name: str

class SubjectBase(BaseModel):
    name: str
class StudentSubjectBase(BaseModel):
    student_id: int
    subject_id: int