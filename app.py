from flask import Flask, jsonify, request
from patient import PatientDB
import string
import random
import datetime

app = Flask(__name__)

patients=PatientDB()

@app.route('/')
def hello_world():
    return 'Patient API!'

# API Routes



# returns paginated list of patient data
# api/patients?page=_
@app.route('/api/v1/patients')
def get_patients():
    page_num=int(request.args.get('page')) if request.args.get('page')!=None else 1
    count=patients.get_count()
    start=10*(int(page_num)-1)
    pag_patients=patients.get_all_patients_page(page_num)
    end=10*(page_num-1)+len(pag_patients)-1
    if pag_patients==None:  pag_patients={}
    return jsonify({
        "count": count, "start": start, "end": end, "limit": 10, "page": page_num,
        "data": pag_patients
    })





# # retursn list of json requested records based on user id
# URL ROUTE:  /api/patient?id=_
# DONE
@app.route('/api/v1/patient')
def get_records():
    record_id = request.args.get('id')
    if record_id!=None:
        patient=patients.get_patient(record_id)
        if patient==None: patient={}
        return jsonify(patient)
    else:
        return jsonify({})






# updates patient records based on user id, dob, email
@app.route('/api/v1/patient/update', methods=['PATCH'])
def update():
    args = request.args
    user_id = args.get('id')

    fname, mname, lname = args.get('fname'), args.get('mname'), args.get('lname')
    email, dob, gender = args.get('email'), args.get('dob'), args.get('gender')
    status, terms, date_accpted = args.get('status'), args.get('terms'), args.get('date_accepted')
    street, state, zip = args.get('street'), args.get('state'), args.get('zip')
    phone=args.get('phone')



    if dob!=None:
        date = dob.split("-")
        year, month, day = int(date[0]), int(date[1]), int(date[2])
        if patients.get_age(year, month, day)<8:
            return jsonify(success=False)
    if valid_date==False:
        return jsonify(success=False)
    if user_id==None:
        return jsonify(success=False)
    else:
        p_data=patients.get_patient(user_id)
        keys=['first_name', 'middle_name', 'last_name', 'email', 'dob', 'gender',
              'status', 'terms_accepted', 'terms_accepted_at', 'address_street',
              'address_city', 'address_state', 'address_zip', 'phone']
        updated_patient=[]
        for key in keys:
            updated_patient.append(p_data[key])
        attributes=[
            fname, mname, lname, email, dob, gender, status, terms,
            date_accpted, street, state, zip, phone
        ]
        for i, value in enumerate(attributes):
            if value!=None: updated_patient[i]=value

        if valid_date(updated_patient[4])==False:
            return jsonify(success=False)

        json=patients.update_patient(user_id, updated_patient)
        return jsonify(success=True)


#


# # deletes existing patient records
# DELETE URL ROUTE:  /api/patient/delete?id=_
@app.route('/api/v1/patient/delete', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('id')
    if user_id==None:
        return jsonify(success=False)
    else:
        patients.delete_patient(user_id)
        return jsonify(success=True)



# # creates new patient record
# working
@app.route('/api/v1/patient/new', methods=['POST'])
def create():
    try:
        id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase+ string.digits, k=7))
        args=request.args
        fname, mname, lname=args.get('fname'), args.get('mname'), args.get('lname')
        email, dob, gender = args.get('email'), args.get('dob'), args.get('gender')
        status, terms, date_accpted=args.get('status'), args.get('terms'), args.get('date_accepted')
        street, state, zip=args.get('street'), args.get('state'), args.get('zip')
        phone = request.args.get('phone')
        new_patient_data=(id, fname, mname, lname, email, dob, gender, status, int(terms), date_accpted, street, state, zip, phone, )

        date = dob.split("-")
        year, month, day = int(date[0]), int(date[1]), int(date[2])
        print(dob)
        if valid_date(dob)==False:
            return jsonify(success=False)
        if patients.get_age(year, month, day) < 8:
            return jsonify(success=False)
        else:
            patients.create_patient(new_patient_data)
            return jsonify(success=True)

    except:
        return jsonify(success=False)




# # returns patient's age based on date of birth
# URL ROUTE:  /api/age?year= &month= &day=
@app.route('/api/v1/patient/age')
def get_age():
    args=request.args
    years= patients.get_age(int(args.get('year')), int(args.get('month')), int(args.get('day')))
    return jsonify({"years": years})


def valid_date(str):
    try:
        datetime.datetime.strptime(str, '%Y-%m-%d')
        return True
    except ValueError:
        return False



if __name__ == '__main__':
    app.run( host='0.0.0.0', debug=True )

