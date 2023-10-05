from flask import Blueprint, jsonify, request, current_app as app
from models import db, Patient, Doctor, Review
from datetime import datetime
from flask import redirect, url_for


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


main = Blueprint('main', __name__)

from flask import jsonify, url_for

@main.route('/', methods=['GET'])
def list_endpoints():
    """List all available endpoints."""
    endpoints = {
        'GET /': url_for('main.list_endpoints', _external=True),
        'GET /reviews': url_for('main.get_reviews', _external=True),
        'GET /reviews/<int:review_id>': url_for('main.get_review', review_id=1, _external=True),
        'POST /add_review': url_for('main.add_review', _external=True),
        'GET /doctors': url_for('main.get_doctors', _external=True),
        'GET /doctors/<int:doctor_id>': url_for('main.get_doctor', doctor_id=1, _external=True),
        'POST /add_doctor': url_for('main.add_doctor', _external=True),
        'DELETE /doctors/<int:doctor_id>': url_for('main.delete_doctor', doctor_id=1, _external=True),
        'PUT /doctors/<int:doctor_id>': url_for('main.update_doctor', doctor_id=1, _external=True),
        'GET /patients': url_for('main.get_patients', _external=True),
        'GET /patients/<int:patient_id>': url_for('main.get_patient', patient_id=1, _external=True),
        'POST /create_patient': url_for('main.create_patient', _external=True),
        'PUT /patients/<int:patient_id>': url_for('main.update_patient', patient_id=1, _external=True)
    }

    return jsonify({'endpoints': endpoints})




######################################## REVIEWS ################################


@main.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = []

    for review in reviews:

        patient_name = review.patient.name if review.patient else "Unknown Patient"

        review_info = {
            'rating': review.rating,
            'comment': review.comment,
            'patient_name': patient_name
        }
        review_list.append(review_info)

    return jsonify({'reviews': review_list})


@main.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get(review_id)

    if review:
        patient_name = review.patient.name if review.patient else "Unknown Patient"

        review_info = {
            'rating': review.rating,
            'comment': review.comment,
            'patient_name': patient_name
        }
        return jsonify({'review': review_info}), 200
    else:
        return 'Review not found', 404




@main.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    patient_id = data.get('patient_id') 

    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found with the provided ID"}), 404

    new_review = Review(rating=rating, comment=comment)

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


@main.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)

    if doctor:
        doctor_info = {
            'id': doctor.id,
            'name': doctor.name,
            'username': doctor.username,
            'email': doctor.email
        }
        return jsonify({'doctor': doctor_info}), 200
    else:
        return 'Doctor not found', 404


@main.route('/add_doctor', methods=['POST'])
def add_doctor():
    data = request.get_json()
    new_doctor = Doctor(name=data['name'], username=data['username'], email=data['email'], password=data['password'])
    new_doctor.role = 'doctor'  
    db.session.add(new_doctor)
    db.session.commit()
    return "Doctor added successfully", 201


@main.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return f'Doctor with ID {doctor_id} deleted successfully', 200
    else:
        return 'Doctor not found', 404

@main.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    data = request.get_json()
    doctor = Doctor.query.get(doctor_id)

    if doctor:
        doctor.name = data.get('name', doctor.name)
        doctor.username = data.get('username', doctor.username)
        doctor.email = data.get('email', doctor.email)
        doctor.password = data.get('password', doctor.password)
        
        db.session.commit()
        return f'Doctor with ID {doctor_id} updated successfully', 200
    else:
        return 'Doctor not found', 404


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


@main.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)

    if patient:
        patient_info = {
            'id': patient.id,
            'name': patient.name,
            'username': patient.username,
            'email': patient.email,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),  # format  YYYY-MM-DD
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
        return jsonify({'patient': patient_info}), 200
    else:
        return 'Patient not found', 404



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
        role='patient' ,
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


@main.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.get(patient_id)

    if patient:
        patient.name = data.get('name', patient.name)
        patient.username = data.get('username', patient.username)
        patient.email = data.get('email', patient.email)
        patient.date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()

        db.session.commit()
        return f'Patient with ID {patient_id} updated successfully', 200
    else:
        return 'Patient not found', 404
