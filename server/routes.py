from flask import Blueprint, jsonify, request
from models import db, Patient, Doctor, Review

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Welcome to MediFinder!"


######################################## REVIEWS ################################


@main.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = [{'rating': review.rating, 'comment': review.comment} for review in reviews]
    return jsonify({'reviews': review_list})


# @main.route('/add_review', methods=['POST'])
# def add_review():
#     data = request.get_json()
#     rating = data.get('rating')
#     comment = data.get('comment')

#     new_review = Review(rating=rating, comment=comment)

#     try:
#         db.session.add(new_review)
#         db.session.commit()
#         return jsonify({"message": "Review added successfully"}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": "Failed to add review", "error": str(e)}), 500

@main.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    patient_id = data.get('patient_id')  # Assuming you pass the patient ID in the request

    # Fetch the patient associated with the provided ID
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found with the provided ID"}), 404

    # Assuming you have a Review model with appropriate fields
    new_review = Review(rating=rating, comment=comment)

    # Associate the review with the patient
    new_review.patient = patient

    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add review", "error": str(e)}), 500

################################ DOCTORS #################################

@main.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    doctor_list = []
    for doctor in doctors:
        doctor_info = {
            'id': doctor.id,
            'name': doctor.name,
            'username': doctor.username,
            'email': doctor.email
        }
        doctor_list.append(doctor_info)
    return jsonify({'doctors': doctor_list})


@main.route('/add_doctor', methods=['POST'])
def add_doctor():
    data = request.get_json()
    new_doctor = Doctor(name=data['name'], username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_doctor)
    db.session.commit()
    return "Doctor added successfully", 201

################################PATIENTS #################################

@main.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    patient_list = []
    
    for patient in patients:
        patient_info = {
            'id': patient.id,
            'name': patient.name,
            'username': patient.username,
            'email': patient.email,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),  # format datess as YYYY-MM-DD
            'phone_numbers': patient.phone_numbers,
            'address': patient.address,
            'medical_history': patient.medical_history,
            'emergency_contact_name': patient.emergency_contact_name,
            'emergency_contact_relationship': patient.emergency_contact_relationship,
            'emergency_contact_phone': patient.emergency_contact_phone,
            'insurance_provider': patient.insurance_provider,
            'policy_number': patient.policy_number,
            'appointment_history': patient.appointment_history,
            'notes_comments': patient.notes_comments,
            'health_goals': patient.health_goals,
            'preferences': patient.preferences,
            'allergies': patient.allergies,
            'current_medications': patient.current_medications
        }
        patient_list.append(patient_info)

    return jsonify({'patients': patient_list})

from datetime import datetime

@main.route('/create_patient', methods=['POST'])
def create_patient():
    data = request.get_json()

    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    #  to convert dateofbirth to a Python date object
    date_of_birth_str = data.get('date_of_birth')
    date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()

    phone_numbers = data.get('phone_numbers')
    address = data.get('address')
    medical_history = data.get('medical_history')
    emergency_contact_name = data.get('emergency_contact_name')
    emergency_contact_relationship = data.get('emergency_contact_relationship')
    emergency_contact_phone = data.get('emergency_contact_phone')
    insurance_provider = data.get('insurance_provider')
    policy_number = data.get('policy_number')
    appointment_history = data.get('appointment_history')
    notes_comments = data.get('notes_comments')
    health_goals = data.get('health_goals')
    preferences = data.get('preferences')
    allergies = data.get('allergies')
    current_medications = data.get('current_medications')

    new_patient = Patient(
        name=name,
        username=username,
        email=email,
        password=password,
        date_of_birth=date_of_birth,
        phone_numbers=phone_numbers,
        address=address,
        medical_history=medical_history,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_relationship=emergency_contact_relationship,
        emergency_contact_phone=emergency_contact_phone,
        insurance_provider=insurance_provider,
        policy_number=policy_number,
        appointment_history=appointment_history,
        notes_comments=notes_comments,
        health_goals=health_goals,
        preferences=preferences,
        allergies=allergies,
        current_medications=current_medications
    )

    db.session.add(new_patient)
    db.session.commit()

    return f"New patient added successfully with ID: {new_patient.id}", 201
