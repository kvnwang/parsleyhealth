from flask import Flask, jsonify, request
from patient import PatientDB
import json
import string
import random
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
    page_num=request.args.get('page') if request.args.get('page')!=None else 1
    pag_patients=patients.get_all_patients_page(page_num)
    print(pag_patients)
    page_num=int(page_num)
    return jsonify({
        "start": 10*(int(page_num)-1),
        "limit": 10,
        "end": 10*(page_num-1)+len(pag_patients)-1,
        "page": page_num,
        "data": pag_patients
    })





# # retursn list of json requested records based on user id
# URL ROUTE:  /api/patient?id=_
# DONE
@app.route('/api/v1/patient')
def get_records():
    record_id = request.args.get('id')
    if record_id!=None:
        records=patients.get_patient(record_id)
        return jsonify(records)
    else:
        return jsonify(success=False)






# updates patient records based on user id, dob, email
# WORKS
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
    if user_id==None:
        return jsonify(success=False)
    else:
        p_data=patients.get_patient(user_id)
        print (p_data)
        keys=['first_name', 'middle_name', 'last_name', 'email', 'dob', 'gender', 'status', 'terms_accepted', 'terms_accepted_at', 'address_street',
              'address_city', 'address_state', 'address_zip', 'phone']
        values=[]
        for key in keys:
            values.append(p_data[key])


        if fname!=None: values[0]=fname
        if mname!=None: values[1]=fname
        if lname!=None: values[2]=lname
        if email!=None: values[3]=email
        if dob!=None: values[4]=dob
        if gender!=None: values[5]=gender
        if status!=None: values[6]=status
        if terms!=None: values[7]=terms
        if date_accpted!=None: values[8]=date_accpted
        if args.get('street')!=None:
            values[9]=street
        if state!=None: values[10]=state
        if zip!=None: values[11]=zip
        if phone!=None: values[12]=phone
        print('values ',values)
        json=patients.update_patient(user_id, values)
        print(json)
        return jsonify(success=True)


#


# # deletes existing patient records
# DELETE URL ROUTE:  /api/patient/delete?id=_
# WORKS
@app.route('/api/v1/patient/delete', methods=['DELETE'])
def delete_user():
    try:
        user_id = request.args.get('id')
        patients.delete_patient(user_id)
        return jsonify(success=True)
    except:
        return jsonify(success=False)




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

        if patients.get_age(year, month, day) < 8:
            return jsonify(success=False)
        else:
            patients.create_patient(new_patient_data)
            return jsonify(success=True)
    except:
        return jsonify(success=False)









# # returns patient's age based on date of birth
# URL ROUTE:  /api/age?year= &month= &day=
# DONE

@app.route('/api/v1/patient/age')
def get_age():
    args=request.args
    years= patients.get_age(int(args.get('year')), int(args.get('month')), int(args.get('day')))
    return jsonify({"years": round(years,2)})




if __name__ == '__main__':
    app.run( host='0.0.0.0', debug=True )

