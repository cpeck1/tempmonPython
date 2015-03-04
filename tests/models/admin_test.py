"""
Mostly test interaction with the ORM
"""
from bin.models.admin import Admin
from bin.models.address import Address

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from bin.models import base
from sqlalchemy.sql import exists

class AdminModelTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        base.Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        admins = [
            Admin(
                name="Sean Gomez", 
                email_addresses=[
                ]
            ),
            Admin(
                name="Juan Diego",
                email_addresses=[
                    Address(email="juanjuan213949142@gmail.com"),
                ]
            ),
            Admin(
                name="Rachel Dawes",
                email_addresses=[
                    Address(email="rdawg91230213@gmail.com"),
                    Address(email="racheldawes91230124@hotmail.com")
                ]
            ),
            Admin(
                name="This Dude's Got A Very Very Long Name In Particular It Has A Lot Of Words In It And I Suspect He Is Of Some Kind Of Royal Birth",
                email_addresses=[
                    Address(email="test0@testdomain.com"),
                    Address(email="test1@testdomain.com"),
                    Address(email="test2@testdomain.com"),
                    Address(email="test3@testdomain.com"),
                    Address(email="test4@testdomain.com"),
                    Address(email="test5@testdomain.com"),
                    Address(email="test6@testdomain.com"),
                    Address(email="test7@testdomain.com"),
                    Address(email="test8@testdomain.com"),
                    Address(email="test9@testdomain.com"),
                    Address(email="test10@testdomain.com"),
                    Address(email="test11@testdomain.com"),
                    Address(email="test12@testdomain.com"),
                    Address(email="test13@testdomain.com"),
                    Address(email="test14@testdomain.com"),
                    Address(email="test15@testdomain.com"),
                    Address(email="test16@testdomain.com"),
                    Address(email="test17@testdomain.com"),
                    Address(email="test18@testdomain.com"),
                    Address(email="test19@testdomain.com"),
                    Address(email="test20@testdomain.com"),
                    Address(email="test21@testdomain.com"),
                    Address(email="test22@testdomain.com"),
                    Address(email="test23@testdomain.com"),
                    Address(email="test24@testdomain.com"),
                    Address(email="test25@testdomain.com"),
                    Address(email="test26@testdomain.com"),
                    Address(email="test27@testdomain.com"),
                    Address(email="test28@testdomain.com"),
                    Address(email="test29@testdomain.com"),
                ]
            )
        ]
        self.admins = admins
        
        for a in admins:
            self.session.add(a)

        self.session.commit()

    def tearDown(self):
        self.session.close()

    
class AdminModelTestSuite(AdminModelTest):
    # simultaneously test that IDs were assigned in order
    def test_access1(self):
        admin_test_id = 1

        actual_admin_name = "Sean Gomez"
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        self.assertEqual(admin.name, actual_admin_name)

    def test_access2(self):
        admin_test_id = 1

        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        address_strings = [x.email for x in admin.email_addresses]

        self.assertEqual(address_strings, [])

    def test_access3(self):
        admin_test_id = 2

        actual_admin_name = "Juan Diego"
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        self.assertEqual(admin.name, actual_admin_name)

    def test_access4(self):
        admin_test_id = 2

        actual_email_address_strings = ["juanjuan213949142@gmail.com"]
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        address_strings = [x.email for x in admin.email_addresses]

        for actual_address_string in actual_email_address_strings:
                self.assertTrue(actual_address_string in address_strings)

    def test_access5(self):
        admin_test_id = 3

        actual_admin_name = "Rachel Dawes"
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        self.assertEqual(admin.name, actual_admin_name)

    def test_access6(self):
        admin_test_id = 3

        actual_email_address_strings = [
            "rdawg91230213@gmail.com",
            "racheldawes91230124@hotmail.com"
        ]
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        address_strings = [x.email for x in admin.email_addresses]

        for actual_address_string in actual_email_address_strings:
                self.assertTrue(actual_address_string in address_strings)

    def test_access7(self):
        admin_test_id = 4

        actual_admin_name = "This Dude's Got A Very Very Long Name In Particular It Has A Lot Of Words In It And I Suspect He Is Of Some Kind Of Royal Birth"
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        self.assertEqual(admin.name, actual_admin_name)

    def test_access8(self):
        admin_test_id = 4

        actual_email_address_strings = [
            "test"+str(a)+"@testdomain.com" for a in range(30)
        ]
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        address_strings = [x.email for x in admin.email_addresses]

        for actual_address_string in actual_email_address_strings:
                self.assertTrue(actual_address_string in address_strings)

    def test_modify1(self):
        admin_test_id = 1
        admin_name_test_value = "San Diego"
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        
        admin.name = admin_name_test_value
        self.session.commit()

        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        self.assertEqual(admin.name, admin_name_test_value)

    def test_modify2(self):
        admin_test_id = 3
        admin_address_test_value = Address(email="test_value")
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        
        admin.email_addresses = [admin_address_test_value]        
        self.session.commit()

        atest = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        address = atest.email_addresses[0]
        self.assertEqual(address.email, admin_address_test_value.email)

    def test_delete1(self):
        admin_test_id = 1
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        self.session.delete(admin)
        self.session.commit()

        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).all()
        self.assertEqual(admin, [])

    def test_delete2(self):
        # testing cascade
        admin_test_id = 4
        admin = self.session.query(Admin).filter(Admin.id==admin_test_id).one()
        
        self.session.delete(admin)
        self.session.commit()

        addresses = self.session.query(Address).filter(
            Address.email.like('%testdomain%')
        ).all()
        self.assertEqual(addresses, [])

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)
