import sqlite3
import sys
from datetime import datetime
import functools
from dateutil.relativedelta import relativedelta


class PatientDB:
    def db_connect(self):
        conn = sqlite3.connect('data/database.db')
        conn.row_factory = sqlite3.Row

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        conn.row_factory = dict_factory
        conn.set_trace_callback(print)
        return conn

    def db_close(self, conn):
        conn.commit()
        conn.close()


    def get_all(self):
        conn = self.db_connect()
        c = conn.cursor()
        rows = []
        for table in c.fetchall():
            rows.append(table)
        return rows

    @functools.lru_cache(maxsize=100, typed=False)
    def get_all_cached(self):
        conn = self.db_connect()
        c = conn.cursor()
        rows = []
        for table in c.fetchall():
            rows.append(table)
        return rows

    def get_all_patients_page(self, page):
        conn = self.db_connect()
        c = conn.cursor()
        c.execute("SELECT * FROM person ORDER BY last_name ASC LIMIT 10 OFFSET ?", ((int(page)-1)*10,))
        return c.fetchall()



    def get_patient(self, select_id):
        conn = self.db_connect()
        c = conn.cursor()
        rows = []
        c.execute("SELECT * FROM person WHERE id = ? ", [select_id])
        return c.fetchone()



    def update_patient(self, select_id, data):
        conn = self.db_connect()
        try:
            data.append(select_id)
            user_data=tuple(data)
            c = conn.cursor()
            new_data = (user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6],
                         user_data[7], user_data[8], user_data[9], user_data[10], user_data[11], user_data[12], user_data[13], user_data[14])
            c.execute('''UPDATE person SET first_name=?, middle_name=?, last_name=?, email=?, dob=?, gender=?, status=?, terms_accepted=?, terms_accepted_at=?, address_street=?, address_city=?, address_state=?, address_zip=?, phone=? WHERE id = ?''',
                      new_data)
            value=c.fetchone()
            conn.commit()
            conn.close()
            return value

        except:
            print(sys.exc_info()[0])
            conn.rollback()




    def delete_patient(self, select_id):
        conn = self.db_connect()
        try:
            c = conn.cursor()
            c.execute("DELETE FROM person WHERE id =?", (select_id,))
            self.db_close(conn)
        except:
            print(sys.exc_info()[0])
            conn.rollback()



    def create_patient(self, data):
        try:
            conn = self.db_connect()
            c = conn.cursor()
            table_names='(id, first_name, middle_name, last_name, email, dob, gender, status, terms_accepted, address_street, address_city, address_state, address_zip, phone)'
            values='(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            c.execute("INSERT INTO person "+ table_names+ "VALUES  "+values, data)
            self.db_close(conn)
        except:
            print(sys.exc_info()[0])
            conn.rollback()

    #
    def get_age(self, year, month, day):
        start_date = datetime(year, month, day)
        end_date = datetime.today()
        difference = end_date - start_date
        difference_in_years = relativedelta(end_date, start_date).years
        return difference_in_years

    def get_count(self):
        conn = self.db_connect()
        conn.row_factory=None
        c = conn.cursor()
        c.execute("SELECT count(*) FROM person")
        return c.fetchone()[0]

