from flask import Flask
from models import Hospital, Medicine, Diagnosis, db
from faker import Faker
import random

app = Flask(__name__)
# Initialize your Flask app and database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
fake = Faker()

def seed_data():
    with app.app_context():
        # Sample towns in Nairobi, Kisumu, and Mombasa
        towns_nairobi = ['Karen', 'Westlands', 'Kileleshwa', 'Runda', 'CBD']
        towns_kisumu = ['Kisumu Central', 'Nyalenda', 'Mamboleo', 'Nyamasaria', 'Kisian']
        towns_mombasa = ['Nyali', 'Mombasa Island', 'Bamburi', 'Likoni', 'Kiembeni']
        print("Seeding hospitals...")
        # Generate sample hospitals with related details
        for i in range(5):
            # Randomly select a town from Nairobi, Kisumu, or Mombasa
            if i < 2:
                location = random.choice(towns_nairobi)
            elif i < 4:
                location = random.choice(towns_kisumu)
            else:
                location = random.choice(towns_mombasa)
            # Generate the hospital object
            hospital = Hospital(
                name=fake.company(),
                location=location,
                contact=fake.phone_number()
            )
            db.session.add(hospital)
            # Generate sample medicines associated with the hospital
            for _ in range(3):
                medicine = Medicine(
                    name=fake.word(),
                    description=fake.text(),
                    usage=fake.sentence(),
                    dosage=fake.sentence(),
                    hospital=hospital
                )
                db.session.add(medicine)
                # Commit the changes for each medicine
                db.session.commit()
            print(f"Seeding diagnoses for hospital: {hospital.name} in {hospital.location}")
            # Generate sample diagnoses associated with the hospital
            for _ in range(2):
                medicine = random.choice(hospital.medicines)
                diagnosis = Diagnosis(
                    patient_id=fake.random_int(min=100, max=999),
                    diagnosis=fake.sentence(),
                    medicine_id=medicine.id,
                    hospital_id=hospital.id  # Set the hospital_id value
                )
                db.session.add(diagnosis)
                # Commit the changes for each diagnosis
                db.session.commit()
            # ... rest of the seeding logic ...
            print(f"Generated hospital: {hospital.name} in {hospital.location}")
        print("Committing changes...")
        db.session.commit()
        print("Data seeding completed.")

if __name__ == '__main__':
    with app.app_context():
        try:
            seed_data()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Rollback the session in case of an error
            db.session.rollback()