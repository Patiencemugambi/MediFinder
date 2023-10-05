from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()
class Patient(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    date_of_birth = Column(Date)
    phone_numbers = Column(String)
    address = Column(String)
    medical_history = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_relationship = Column(String)
    emergency_contact_phone = Column(String)
    insurance_provider = Column(String)
    policy_number = Column(String)
    appointment_history = Column(String)
    notes_comments = Column(String)
    health_goals = Column(String)
    preferences = Column(String)
    allergies = Column(String)
    current_medications = Column(String)



class Doctor(db.Model):
    __tablename__ = 'doctor'  # Specify the table name
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)

class Review(db.Model):
    __tablename__ = 'review'  # Specify the table name
    id = Column(Integer, primary_key=True)
    rating = Column(Float)
    comment = Column(String)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship('Patient', backref='reviews')

    def __repr__(self):
        return f'<Review {self.id}>'
