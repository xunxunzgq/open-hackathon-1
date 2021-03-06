import sys

sys.path.append("../src/hackathon")
import unittest
from hackathon.admin.admin_mgr import AdminManager
from hackathon.database.models import AdminUser, AdminToken, AdminEmail, AdminUserHackathonRel
from hackathon import app
from mock import Mock, ANY
from datetime import datetime, timedelta
from flask import request, g


class AdminManagerTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        pass


    # ---------------------test method: validate_request--------------------------------------
    def test_validate_request_if_token_missing(self):
        am = AdminManager(None)
        '''more args for app.text_request_context:
                 path='/', base_url=None, query_string=None,
                 method='GET', input_stream=None, content_type=None,
                 content_length=None, errors_stream=None, multithread=False,
                 multiprocess=False, run_once=False, headers=None, data=None,
                 environ_base=None, environ_overrides=None, charset='utf-8'
        '''
        with app.test_request_context('/', headers=None):
            self.assertFalse("token" in request.headers)
            self.assertFalse(am.validate_request())

    def test_validate_request_token_not_found(self):
        token_value = "token_value"

        mock_db = Mock()
        mock_db.find_first_object_by.return_value = None
        am = AdminManager(mock_db)

        with app.test_request_context('/api', headers={"token": token_value}):
            self.assertTrue("token" in request.headers)
            self.assertFalse(am.validate_request())
            mock_db.find_first_object_by.assert_called_once_with(AdminToken, token=token_value)

    def test_validate_request_token_expired(self):
        token_value = "token_value"
        token = AdminToken(token=token_value, admin=None, expire_date=datetime.utcnow() - timedelta(seconds=30))

        mock_db = Mock()
        mock_db.find_first_object_by.return_value = token

        am = AdminManager(mock_db)

        with app.test_request_context('/', headers={"token": token_value}):
            self.assertTrue("token" in request.headers)
            self.assertFalse(am.validate_request())
            mock_db.find_first_object_by.assert_called_once_with(AdminToken, token=token_value)

    def test_validate_request_token_valid(self):
        token_value = "token_value"
        admin = AdminUser(name="test_name")
        token = AdminToken(token=token_value, admin=admin, expire_date=datetime.utcnow() + timedelta(seconds=30))

        mock_db = Mock()
        mock_db.find_first_object_by.return_value = token
        am = AdminManager(mock_db)

        with app.test_request_context('/', headers={"token": token_value}):
            self.assertTrue("token" in request.headers)
            self.assertTrue(am.validate_request())
            mock_db.find_first_object_by.assert_called_once_with(AdminToken, token=token_value)
            self.assertEqual(g.admin, admin)


    # ---------------------test method: get_hackid_from_adminid----------------------------------
    def test_get_hackid_by_adminid(self):
        admin_email_test = [AdminEmail(email='test@ms.com')]
        admin_user_hackathon_rel = [AdminUserHackathonRel(hackathon_id=-1)]
        emails = ['test@ms.com']

        mock_db = Mock()
        mock_db.find_all_objects_by.return_value = admin_email_test
        mock_db.find_all_objects.return_value = admin_user_hackathon_rel

        am = AdminManager(mock_db)

        self.assertEqual(am.get_hack_id_by_admin_id(1), [-1L])
        mock_db.find_all_objects_by.assert_called_once_with(AdminEmail, admin_id=1)
        mock_db.find_all_objects.assert_called_once_with(AdminUserHackathonRel, ANY)


    # ---------------------test method:validate_admin_hackathon_request---------------------------
    def test_validate_admin_hackathon_request_token_missing(self):
        am = AdminManager(None)
        with app.test_request_context('/', headers=None):
            g.admin = AdminUser(id=1, name='testadmin')
            self.assertTrue(am.validate_admin_hackathon_request(1))
            self.assertFalse('token' in request.headers)

    def test_validate_admin_hackathon_request_super_admin(self):
        token_value = "token_value"
        admin_email_test = [AdminEmail(email='test@ms.com')]
        admin_user_hackathon_rel = [AdminUserHackathonRel(hackathon_id=-1L)]

        mock_db = Mock()
        mock_db.find_all_objects_by.return_value = admin_email_test
        mock_db.find_all_objects.return_value = admin_user_hackathon_rel

        am = AdminManager(mock_db)
        with app.test_request_context('/', headers={"token": token_value}):
            g.admin = AdminUser(id=1, name='testadmin')
            self.assertTrue(am.validate_admin_hackathon_request(1))
            mock_db.find_all_objects_by.assert_called_once_with(AdminEmail, admin_id=1)
            mock_db.find_all_objects.assert_called_once_with(AdminUserHackathonRel, ANY)

    def test_validate_admin_hackathon_request_have_authority(self):
        token_value = "token_value"
        admin_email_test = [AdminEmail(email='test@ms.com')]
        admin_user_hackathon_rel = [AdminUserHackathonRel(hackathon_id=1L)]

        mock_db = Mock()
        mock_db.find_all_objects_by.return_value = admin_email_test
        mock_db.find_all_objects.return_value = admin_user_hackathon_rel

        am = AdminManager(mock_db)
        with app.test_request_context('/', headers={"token": token_value}):
            g.admin = AdminUser(id=1, name='testadmin')
            self.assertTrue(am.validate_admin_hackathon_request(1))
            mock_db.find_all_objects_by.assert_called_once_with(AdminEmail, admin_id=1)
            mock_db.find_all_objects.assert_called_once_with(AdminUserHackathonRel, ANY)

    def test_validate_admin_hackathon_request_havnt_authority(self):
        token_value = "token_value"
        admin_email_test = [AdminEmail(email='test@ms.com')]
        admin_user_hackathon_rel = [AdminUserHackathonRel(hackathon_id=1L)]

        mock_db = Mock()
        mock_db.find_all_objects_by.return_value = admin_email_test
        mock_db.find_all_objects.return_value = admin_user_hackathon_rel

        am = AdminManager(mock_db)
        with app.test_request_context('/', headers={"token": token_value}):
            g.admin = AdminUser(id=1, name='testadmin')
            self.assertFalse(am.validate_admin_hackathon_request(2))
            mock_db.find_all_objects_by.assert_called_once_with(AdminEmail, admin_id=1)
            mock_db.find_all_objects.assert_called_once_with(AdminUserHackathonRel, ANY)


if __name__ == '__main__':
    unittest.main()

