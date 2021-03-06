"""
Mostly test interaction with the ORM
"""
from bin.models.environment import Environment
from bin.models.quantitative_property import QuantitativeProperty
from bin.models.expectation import Expectation
from bin.models.alarm import Alarm
from bin.models.reading import Reading

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from bin.models import base
from sqlalchemy.sql import exists

class EnvironmentModelTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        base.Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        test_expectation = Expectation(units="Test", low=0.0, high=0.0)

        environments = [
            Environment(
                name="Test Environment 1",
                serial="test1",
                quantitative_properties=[]
            ),
            Environment(
                name="Test Environment 2",
                serial="test2",
                quantitative_properties=[
                    QuantitativeProperty(
                        type="test2",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    )
                ]
            ),
            Environment(
                name="Test Environment 3",
                serial="test3",
                quantitative_properties=[
                    QuantitativeProperty(
                        type="test3",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test3",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    )
                ]
            ),
            Environment(
                name="Test Environment 4",
                serial="test4",
                quantitative_properties=[
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    ),
                    QuantitativeProperty(
                        type="test4",
                        channel_bus=0,
                        channel_address=0,
                        channel_number=0,
                        rec_freq=0,
                        expectation=test_expectation
                    )
                ]
            )
        ]

        for e in environments:
            self.session.add(e)
            self.session.commit()

        self.session.commit()

    def tearDown(self):
        self.session.close()

class EnvironmentModelTestSuite(EnvironmentModelTest):
    def test_access1(self):
        """Environment 1 has same name/serial as first Environment entered"""
        test_id = 1
        expected_name = "Test Environment 1"
        expected_serial = "test1"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(env.name, expected_name)
        self.assertEqual(env.serial, expected_serial)

    def test_access2(self):
        """Environment 1 has same properties as first Environment entered"""
        test_id = 1

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(env.quantitative_properties, [])


    def test_access3(self):
        """Environment 2 has same name/serial as second Environment entered"""
        test_id = 2
        expected_name = "Test Environment 2"
        expected_serial = "test2"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(env.name, expected_name)
        self.assertEqual(env.serial, expected_serial)

    def test_access4(self):
        """Environment 2 has same properties as second Environment entered"""
        test_id = 2
        expected_condition_type = "test2"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        for ac in env.quantitative_properties:
            self.assertEqual(ac.type, expected_condition_type)

    def test_access5(self):
        """Environment 3 has same name/serial as third Environment entered"""
        test_id = 3
        expected_name = "Test Environment 3"
        expected_serial = "test3"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(env.name, expected_name)
        self.assertEqual(env.serial, expected_serial)

    def test_access6(self):
        """Environment 3 has same properties as third Environment entered"""
        test_id = 3
        expected_condition_type = "test3"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        for ac in env.quantitative_properties:
            self.assertEqual(ac.type, expected_condition_type)


    def test_access7(self):
        """Environment 4 has same name/serial as fourth Environment entered"""
        test_id = 4
        expected_name = "Test Environment 4"
        expected_serial = "test4"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(env.name, expected_name)
        self.assertEqual(env.serial, expected_serial)

    def test_access8(self):
        """Environment 4 has same properties as fourth Environment entered"""
        test_id = 4
        expected_condition_type = "test4"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        for ac in env.quantitative_properties:
            self.assertEqual(ac.type, expected_condition_type)

    def test_modify1(self):
        """Environment's name can be properly modified"""
        test_id = 1
        new_name_value = "New Test Value!"

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        env.name = new_name_value
        self.session.add(env)
        self.session.commit()

        env2 = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(env2.name, new_name_value)

    def test_modify2(self):
        """Environment's properties can be properly modified"""
        test_id = 3
        new_ac_value = [
            QuantitativeProperty(
                type="New Test AC",
                channel_bus=0,
                channel_address=0,
                channel_number=0,
                rec_freq=0,
                expectation=Expectation(units="test", low=1, high=1)
            )
        ]

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        env.quantitative_properties = new_ac_value
        self.session.add(env)
        self.session.commit()

        env2 = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.assertEqual(
            env2.quantitative_properties[0].type,
            new_ac_value[0].type
        )

    def test_delete1(self):
        """Environment can be properly deleted from the system"""
        # test removal from db
        test_id = 1

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        self.session.delete(env)
        self.session.commit()

        test_env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).all()

        self.assertEqual(
            test_env, []
        )

    def test_delete2(self):
        """Environment can be properly deleted from system, delete cascades"""
        # test cascade delete
        test_id = 4

        env = self.session.query(Environment).filter(
            Environment.id == test_id
        ).one()

        deleted_type = env.quantitative_properties[0].type
        self.session.delete(env)
        self.session.commit()

        atm = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.type.like('%{}%'.format(deleted_type))
        ).all()
        self.assertEqual(atm, [])
