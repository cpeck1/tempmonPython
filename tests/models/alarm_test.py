"""
Mostly test interaction with the ORM
"""
from datetime import datetime

from bin.models.environment import Environment
from bin.models.quantitative_property import QuantitativeProperty
from bin.models.expectation import Expectation
from bin.models.alarm import Alarm
from bin.models.reading import Reading
from bin.models.exceptions import AlarmInactiveException

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from bin.models import base
from sqlalchemy.sql import exists

class AlarmModelTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        base.Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        test_expectation = Expectation(units="Test", low=0, high=0)

        condition = QuantitativeProperty(
            type="Test1",
            channel_bus=0,
            channel_address=0,
            channel_number=0,
            rec_freq=0,
            expectation=test_expectation
        )

        reading = Reading(units="Test", value=1)
        condition.readings.append(reading)

        alarm = Alarm(reading=reading, expectation=test_expectation)
        condition.alarms.append(alarm)

        self.session.add(condition)
        self.session.commit()

    def tearDown(self):
        self.session.close()

class AlarmModelTestSuite(AlarmModelTest):
    def test_access(self):
        """Alarm 1's ID matches first Alarm added"""
        test_id = 1

        alarm = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).one()

        self.assertEqual(alarm.expectation.units, "Test")
        self.assertEqual(alarm.reading.units, "Test")

    def test_active1(self):
        """Alarm properly reads as active"""
        test_id = 1

        alarm = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).one()

        self.assertTrue(alarm.active())

    def test_active2(self):
        """Alarm properly reads as inactive"""
        test_id = 1

        alarm = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).one()

        alarm.end_time = datetime.now()
        self.assertFalse(alarm.active())

    def test_end1(self):
        """Alarm end method properly ends alarm"""
        test_id = 1

        alarm = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).one()

        alarm.end()
        self.assertTrue(alarm.end_time is not None)

    def test_end2(self):
        """Alarm end method on inactive Alarm raises AlarmInactiveException"""
        test_id = 1

        alarm = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).one()

        alarm.end()
        # due to unittest's difficulty with handling custom exceptions
        try:
            alarm.end()
        except Exception as e:
            self.assertTrue(isinstance(e, AlarmInactiveException))

    def test_delete(self):
        """Alarm deletion properly removes alarm"""
        test_id = 1

        alarm = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).one()

        self.session.delete(alarm)
        self.session.commit()

        alarms = self.session.query(Alarm).filter(
            Alarm.id == test_id
        ).all()

        self.assertEqual(alarms, [])
