import unittest
from unittest.mock import Mock, patch

from serverOOP.db_single import ServerDB


class ServerDBTest(unittest.TestCase):

    def fake_init(obj, db_name="server.db"):
        obj.cursor = Mock()
        obj.cursor.cursor.execute.return_value = None
        print("Call fake init. Args: %s" % db_name)

    @classmethod
    @patch.object(ServerDB, "__init__", fake_init)
    def setUpClass(cls):
        cls.db = ServerDB()

    def test_insert(self):
        self.db.save_to_base({
            "name": "CompanyX", "address": "London", "telephone": "0685930245"
        }, "Companies")

        actual_query = self.db.cursor.execute.call_args[0][0]
        expected_query = "INSERT INTO Companies VALUES ('CompanyX', 'London', '068593024')"
        self.assertEqual(expected_query, actual_query)

    def test_insert_exception(self):
        raise NotImplemented()  # TODO

    def test_update(self):
        self.db.update("fakeID", {
            "name": "CompanyX", "address": "London", "telephone": "0685930244"
        }, "Companies")

        actual_query = self.db.cursor.execute.call_args[0][0]
        expected_query = '''UPDATE Companies SET name=CompanyX, address=London, telephone=0685930244 WHERE id=fakeID'''
        self.assertEqual(expected_query, actual_query)

    def test_update_exception(self):
        self.db.update("fakeID", {
            "name": "CompanyX", "address": "London", "telephone": "0685930244"
        }, "Companies")

        actual_query = self.db.cursor.execute.call_args[0][0]
        expected_query = '''UPDATE Companies SET name=CompanyX, address=London, telephone=0685930244 WHERE id=fakeID'''
        self.assertEqual(expected_query, actual_query)

    def test_remove(self):
        raise NotImplemented()  # TODO

    def test_remove_exception(self):
        raise NotImplemented()  # TODO

    def test_select(self):
        raise NotImplemented()  # TODO

    def test_select_exception(self):
        raise NotImplemented()  # TODO

    def test_create_tables(self):
        raise NotImplemented()  # TODO

    def test_create_tables_exception(self):
        raise NotImplemented()  # TODO


class ServerDBIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = ServerDB()

    def setUp(self):
        test_data = {
            "name": "\"CompanyName\"",
            "address": "\"CompanyAddress\"",
            "telephone": "380991111212"
        }

        self.db.cursor.execute(f"""INSERT INTO Companies ({", ".join(test_data.keys())}) VALUES 
        ({", ".join(test_data.values())})""")
        self.db.conn.commit()

    def test_insert(self):
        res = self.db.cursor.execute('''SELECT * FROM Companies ''').fetchall()
        self.assertEqual(1, len(res))
        expected_data = {
            "name": "CompanyName",
            "address": "CompanyAddress",
            "telephone": 380991111212
        }
        self.assertEqual(tuple(expected_data.values()), res[0][1:])

    def test_save_to_base_insert(self):

        test_data = {
            "name": "'CompanyName'",
            "address": "'CompanyAddress'",
            "telephone": '380991111212'
        }

        self.db.cursor.execute(f"""INSERT INTO Companies ({", ".join(test_data.keys())}) VALUES 
        ({", ".join(test_data.values())})""")
        self.db.conn.commit()

        res = self.db.cursor.execute('''SELECT * FROM Companies''').fetchall()
        self.assertEqual(2, len(res))

        expected_data = {
            "name": "CompanyName",
            "address": "CompanyAddress",
            "telephone": 380991111212
        }

        self.assertEqual(tuple(expected_data.values()), res[0][1:])

    def test_save(self):
        res = self.db.cursor.execute('''SELECT * FROM Companies ''').fetchall()
        self.assertEqual(1, len(res))
        expected_data = {
            "name": "CompanyName",
            "address": "CompanyAddress",
            "telephone": 380991111212
        }
        self.assertEqual(tuple(expected_data.values()), res[0][1:])

        test_data = {
            "name": "'CompanyNameChanged'",
            "address": "'CompanyAddressChanged'",
            "telephone": "380991111212"
        }

        self.db.cursor.execute(f"""UPDATE Companies SET {", ".join("%s = %s" % (k, v) for k, v in test_data.items()) } WHERE id=1""")
        self.db.conn.commit()

        res = self.db.cursor.execute('''SELECT * FROM Companies''').fetchall()

        self.assertEqual(1, len(res))

        expected_data = {
            "name": "CompanyNameChanged",
            "address": "CompanyAddressChanged",
            "telephone": 380991111212
        }

        self.assertEqual(tuple(expected_data.values()), res[0][1:])

    def tearDown(self):
        self.db.cursor.executescript('''
            DELETE FROM Companies;
            DELETE FROM Users;
            UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Companies';
            UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Users';
        ''')
        self.db.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.cursor.execute('''DROP TABLE Companies''')
        cls.db.cursor.execute('''DROP TABLE Users''')
