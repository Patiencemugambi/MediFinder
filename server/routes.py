from flask import Blueprint, jsonify, request
from models import Hospital, Medicine, Diagnosis, db

hospital_routes = Blueprint('hospital_routes', __name__)

# ---- Hospitals ----

@hospital_routes.route('/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = Hospital.query.all()
    hospital_list = [{'id': hospital.id, 'name': hospital.name, 'address': hospital.address, 'contact': hospital.contact} for hospital in hospitals]
    return jsonify({'hospitals': hospital_list})

@hospital_routes.route('/hospitals/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        hospital_data = {'id': hospital.id, 'name': hospital.name, 'address': hospital.address, 'contact': hospital.contact}
        return jsonify({'hospital': hospital_data})
    return jsonify({'message': 'Hospital not found'}), 404

@hospital_routes.route('/hospitals', methods=['POST'])
def add_hospital():
    data = request.form
    name = data.get('name')
    address = data.get('address')
    contact = data.get('contact')

    if not name or not address or not contact:
        return jsonify({'error': 'Incomplete data. Please provide name, address, and contact for the hospital.'}), 400

    new_hospital = Hospital(name=name, address=address, contact=contact)

    try:
        db.session.add(new_hospital)
        db.session.commit()
        return jsonify({'message': 'Hospital added successfully', 'hospital': {'id': new_hospital.id, 'name': new_hospital.name, 'address': new_hospital.address, 'contact': new_hospital.contact}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while adding the hospital: {str(e)}'}), 500

@hospital_routes.route('/hospitals/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    data = request.form
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        hospital.name = data.get('name', hospital.name)
        hospital.address = data.get('address', hospital.address)
        hospital.contact = data.get('contact', hospital.contact)
        db.session.commit()
        return jsonify({'message': 'Hospital updated successfully'})
    return jsonify({'message': 'Hospital not found'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>', methods=['DELETE'])
def delete_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
        return jsonify({'message': 'Hospital deleted successfully'})
    return jsonify({'message': 'Hospital not found'}), 404

# ---- Medicines ----

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines', methods=['GET'])
def get_medicines(hospital_id):
    medicines = Medicine.query.filter_by(hospital_id=hospital_id).all()
    medicine_list = [{'id': medicine.id, 'name': medicine.name, 'description': medicine.description, 'usage': medicine.usage, 'dosage': medicine.dosage} for medicine in medicines]
    return jsonify({'medicines': medicine_list})

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines', methods=['POST'])
def add_medicine(hospital_id):
    data = request.form
    name = data.get('name')
    description = data.get('description')
    usage = data.get('usage')
    dosage = data.get('dosage')

    if not name or not description or not usage or not dosage:
        return jsonify({'error': 'Incomplete data. Please provide name, description, usage, and dosage for the medicine.'}), 400

    new_medicine = Medicine(name=name, description=description, usage=usage, dosage=dosage, hospital_id=hospital_id)

    try:
        db.session.add(new_medicine)
        db.session.commit()
        return jsonify({'message': 'Medicine added successfully', 'medicine': {'id': new_medicine.id, 'name': new_medicine.name, 'description': new_medicine.description, 'usage': new_medicine.usage, 'dosage': new_medicine.dosage}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while adding the medicine: {str(e)}'}), 500

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines/<int:medicine_id>', methods=['PUT'])
def update_medicine(hospital_id, medicine_id):
    data = request.form
    medicine = Medicine.query.filter_by(id=medicine_id, hospital_id=hospital_id).first()
    if medicine:
        medicine.name = data.get('name', medicine.name)
        medicine.description = data.get('description', medicine.description)
        medicine.usage = data.get('usage', medicine.usage)
        medicine.dosage = data.get('dosage', medicine.dosage)
        db.session.commit()
        return jsonify({'message': 'Medicine updated successfully'})
    return jsonify({'message': 'Medicine not found'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(hospital_id, medicine_id):
    medicine = Medicine.query.filter_by(id=medicine_id, hospital_id=hospital_id).first()
    if medicine:
        db.session.delete(medicine)
        db.session.commit()
        return jsonify({'message': 'Medicine deleted successfully'})
    return jsonify({'message': 'Medicine not found'}), 404

# ---- Diagnoses ----

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses', methods=['GET'])
def get_diagnoses(hospital_id):
    diagnoses = Diagnosis.query.filter_by(hospital_id=hospital_id).all()
    diagnosis_list = [{'id': diagnosis.id, 'patient_id': diagnosis.patient_id, 'diagnosis': diagnosis.diagnosis} for diagnosis in diagnoses]
    return jsonify({'diagnoses': diagnosis_list})

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses', methods=['POST'])
def add_diagnosis(hospital_id):
    data = request.form
    patient_id = data.get('patient_id')
    diagnosis_text = data.get('diagnosis')

    if not patient_id or not diagnosis_text:
        return jsonify({'error': 'Incomplete data. Please provide patient_id and diagnosis for the diagnosis.'}), 400

    new_diagnosis = Diagnosis(patient_id=patient_id, diagnosis=diagnosis_text, hospital_id=hospital_id)

    try:
        db.session.add(new_diagnosis)
        db.session.commit()
        return jsonify({'message': 'Diagnosis added successfully', 'diagnosis': {'id': new_diagnosis.id, 'patient_id': new_diagnosis.patient_id, 'diagnosis': new_diagnosis.diagnosis}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while adding the diagnosis: {str(e)}'}), 500

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses/<int:diagnosis_id>', methods=['PUT'])
def update_diagnosis(hospital_id, diagnosis_id):
    data = request.form
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, hospital_id=hospital_id).first()
    if diagnosis:
        diagnosis.patient_id = data.get('patient_id', diagnosis.patient_id)
        diagnosis.diagnosis = data.get('diagnosis', diagnosis.diagnosis)
        db.session.commit()
        return jsonify({'message': 'Diagnosis updated successfully'})
    return jsonify({'message': 'Diagnosis not found'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses/<int:diagnosis_id>', methods=['DELETE'])
def delete_diagnosis(hospital_id, diagnosis_id):
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, hospital_id=hospital_id).first()
    if diagnosis:
        db.session.delete(diagnosis)
        db.session.commit()
        return jsonify({'message': 'Diagnosis deleted successfully'})
    return jsonify({'message': 'Diagnosis not found'}), 404

# ... other routes ...
