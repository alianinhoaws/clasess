import unittest
from unittest.mock import Mock, patch
from serverOOP.models import AbstractModels


class TestAbstractModels(unittest.TestCase):

    def fake_init(obj):
        obj.request = Mock()
        obj.db = Mock()

    def test_init_and_validate(self):

            self.request = ['PUT', '/companies/22', 'HTTP/1.1\r\nHost:', 'localhost:8080\r\nUser-Agent:', 'curl/7.64.1\r\nAccept:', '*/*\r\nContent-Length:', '50\r\nContent-Type:', 'application/x-www-form-urlencoded\r\n\r\nname=CoOSTanyX&address=London&telephone=0685930245']
            test = AbstractModels(self.request)
            args = ['CoOSTanyX', 'London', '0685930245']
            actual = test.init_and_validate(args)

            expected = {'name': 'CoOSTanyX', 'address': 'London', 'telephone': '0685930245'}
            self.assertEqual(expected, actual)


    def test__parse_args(self):
        self.fail()

    def test__parse_url(self):
        self.fail()

    def test__parse_id(self):
        self.fail()

    def test_get(self):
        self.fail()

    def test_post(self):
        self.fail()

    def test_put(self):
        self.fail()

    def test_delete(self):
        self.fail()

    def test_return_codes(self):
        self.fail()


class UserProfileTest(unittest.TestCase):

    def test_save(self):
        raise NotImplemented()  # TODO

    def test_save_exception(self):
        raise NotImplemented()  # TODO

    def test_select(self):
        raise NotImplemented()  # TODO

    def test_select_exception(self):
        raise NotImplemented()  # TODO

    def test_update(self):
        raise NotImplemented()  # TODO

    def test_update_exception(self):
        raise NotImplemented()  # TODO

    def test_remove(self):
        raise NotImplemented()  # TODO

    def test_remove_exception(self):
        raise NotImplemented()  # TODO


class CompaniesTest(unittest.TestCase):

    def test_save(self):
        raise NotImplemented()  # TODO

    def test_save_exception(self):
        raise NotImplemented()  # TODO

    def test_select(self):
        raise NotImplemented()  # TODO

    def test_select_exception(self):
        raise NotImplemented()  # TODO

    def test_update(self):
        raise NotImplemented()  # TODO

    def test_update_exception(self):
        raise NotImplemented()  # TODO

    def test_remove(self):
        raise NotImplemented()  # TODO

    def test_remove_exception(self):
        raise NotImplemented()  # TODO
