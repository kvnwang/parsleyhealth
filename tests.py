import unittest
import json
import os
import time
import app

BASE_URL = 'http://127.0.0.1:5000/api/v1'


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        # resets db to original
        os.system("cat data/backup.db > data/database.db")
    #
    # def test_get_paginated_id_and_filters(self):
    #     response = self.app.get(BASE_URL+"/patients?page=2")
    #     data = json.loads(response.get_data())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['limit'], 10)
    #     self.assertEqual(data['start'], 10)
    #     self.assertEqual(data['end'], 19)
    #     self.assertEqual(data['data'][0]['id'], '1zsjhd0d')
    #
    #
    # def test_filters(self):
    #     response = self.app.get(BASE_URL+"/patients?page=3")
    #     data = json.loads(response.get_data())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['data'][0]['id'], 'tihh4eri')
    #
    #
    # def test_correct_patient(self):
    #     response = self.app.get(BASE_URL+"/patient?id=1zsjhd0d")
    #     inner_data = json.loads(response.get_data())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(inner_data['id'], '1zsjhd0d')
    #     self.assertEqual(inner_data['first_name'], 'Leola')
    #     self.assertEqual(inner_data['middle_name'], 'Augustus')
    #     self.assertEqual(inner_data['last_name'], 'Crona')
    #     self.assertEqual(inner_data['email'], 'Axel_West@yahoo.com')
    #     self.assertEqual(inner_data['dob'], '1991-03-17')
    #     self.assertEqual(inner_data['gender'], 'female')
    #     self.assertEqual(inner_data['status'], 'inactive')
    #     self.assertEqual(inner_data['terms_accepted'], 1)
    #     self.assertEqual(inner_data['terms_accepted_at'], '2018-05-12T16:59:58.365Z')
    #     self.assertEqual(inner_data['address_street'], '328 Glen Cliffs')
    #     self.assertEqual(inner_data['address_city'], 'Lefflerbury')
    #     self.assertEqual(inner_data['address_state'], 'North Dakota')
    #     self.assertEqual(inner_data['address_zip'], '44064')
    #     self.assertEqual(inner_data['phone'], '270-729-6496 x547')
    #
    # def test_valid_update_email(self):
    #     response = self.app.get(BASE_URL+"/patient?id=uw380vgp")
    #     data_before = json.loads(response.get_data())
    #     response_update = self.app.patch(BASE_URL+"/patient/update?id=uw380vgp&email=test@gmail.com")
    #     response2 = self.app.get(BASE_URL + "/patient?id=uw380vgp")
    #     after = json.loads(response2.get_data())
    #     response_after = self.app.get(BASE_URL + "/patient?id=uw380vgp")
    #     data_after = json.loads(response_after.get_data())
    #     self.assertNotEqual(data_before, data_after)
    #     self.assertNotEqual(data_before['email'], data_after['email'])
    #     after = json.loads(self.app.get(BASE_URL+"/patient?id=uw380vgp").get_data())
    #     self.assertEqual(data_after['first_name'], data_before['first_name'])
    #
    # def test_invalid_update_dob(self):
    #     response = self.app.get(BASE_URL+"/patient?id=x74w6y99")
    #     data_before = json.loads(response.get_data())
    #     response_update = self.app.patch(BASE_URL+"/patient/update?id=uw380vgp&dob=2015-12-12")
    #     response_after = self.app.get(BASE_URL + "/patient?id=x74w6y99")
    #     data_after = json.loads(response_after.get_data())
    #     self.assertEqual(data_before, data_after)
    #
    #
    # def test_delete_success(self):
    #     response = self.app.get(BASE_URL+"/patient?id=x74w6y99")
    #     oldCount= app.patients.get_count()
    #     response_update = self.app.delete(BASE_URL + "/patient/delete?id=x74w6y99")
    #     deleted_data = json.loads(self.app.get(BASE_URL + "/patient?id=x74w6y99").get_data())
    #     newCount= app.patients.get_count()
    #     self.assertGreater(oldCount, newCount)
    #     self.assertNotEqual(response_update, {})
    #     self.assertEqual(deleted_data, {})
    #
    #
    # def test_no_less_than8(self):
    #     all_rows= app.patients.get_all()
    #     for row in all_rows:
    #         dob=row['dob']
    #         date = dob.split("-")
    #         year, month, day = int(date[0]), int(date[1]), int(date[2])
    #         age= app.patients.get_age(year, month, day)
    #         self.assertGreaterEqual(age,8 )
    #
    # def test_create(self):
    #     prev_count= app.patients.get_count()
    #     response = self.app.post(BASE_URL + "/patient/new?fname=fname&lname=lname&"
    #     "&mname=mname&email=test@gmail.com&dob=2000-02-03&gender=Male&status=1&terms=12&date_accepted=2012-11-21"
    #                                         "&street=214 M street&state=NY&zip=10535&phone=456 543 2345")
    #
    #     newCount= app.patients.get_count()
    #     self.assertGreater(newCount, prev_count)
    #     self.assertEqual(newCount-prev_count, 1)
    #
    # def test_server_reponse(self):
    #     start = time.clock()
    #     response = self.app.post(BASE_URL + "/patient/new?fname=fname&lname=lname&"
    #     "&mname=mname&email=tets2t@gmail.com&dob=2000-02-03&gender=Male&status=1&terms=12&date_accepted=12-1-2"
    #                                         "&street=214 M street&state=NY&zip=10535&phone=456 543 2345")
    #     request_time = time.clock() - start
    #     print(request_time)
    #     self.assertLess(request_time, 0.1)
    #     #
    #
    # def test_cache(self):
    #     start = time.clock()
    #     app.patients.get_all_cached()
    #     request_time = time.clock() - start
    #     start_cached=time.clock()
    #     app.patients.get_all_cached()
    #     request_time2=time.clock()-start_cached
    #     # caching should improve second and consecurive api requests
    #     self.assertGreater(request_time, request_time2)

    def test_invalid_date(self):
        response = self.app.post(BASE_URL + "/patient/new?fname=fname&lname=lname&"
        "&mname=mname&email=tets2t@gmail.com&dob=20-2-3&gender=Male&status=1&terms=12&date_accepted=1-2-3"
        "&street=214 M street&state=NY&zip=10535&phone=456 543 2345")
        data = json.loads(response.get_data())
        print(data)
        self.assertEqual(data['success'], False)



if __name__ == "__main__":
    unittest.main()