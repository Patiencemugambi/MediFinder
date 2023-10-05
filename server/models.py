from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    medicines = db.relationship('Medicine', backref='hospital', lazy=True)

    def __repr__(self):
        return f'<Hospital {self.name}>'

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    usage = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)

    def __repr__(self):
        return f'<Medicine {self.name}>'

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)  # Add the hospital_id column

    def __repr__(self):
        return f'<Diagnosis {self.diagnosis}>'