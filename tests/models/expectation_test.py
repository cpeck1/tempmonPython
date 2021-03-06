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

class ReadingModelTest(unittest.TestCase):
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

        self.session.add(condition)
        self.session.commit()

    def tearDown(self):
        self.session.close()

class ReadingModelTestSuite(ReadingModelTest):
    def test_access(self):
        """Expectation 1 id matches first Expectation entered"""
        test_id = 1

        expectation = self.session.query(Expectation).filter(
            Expectation.id == test_id
        ).one()

        self.assertEqual(expectation.id, test_id)

    def test_violated_by1(self):
        """Expectation 1 not violated by Reading within expected parameters"""
        test_id = 1

        expectation = self.session.query(Expectation).filter(
            Expectation.id == test_id
        ).one()

        r = Reading(units="Test", value=0)

        self.assertFalse(expectation.violated_by(r))

    def test_violated_by2(self):
        """Expectation 1 violated by Reading with value outside parameters"""
        test_id = 1

        expectation = self.session.query(Expectation).filter(
            Expectation.id == test_id
        ).one()

        r = Reading(units="Test", value=1)

        self.assertTrue(expectation.violated_by(r))

    def test_violated_by3(self):
        """Expectation 1 violated by Reading with improper units"""
        test_id = 1

        expectation = self.session.query(Expectation).filter(
            Expectation.id == test_id
        ).one()

        r = Reading(units="FEST", value=0)

        self.assertTrue(expectation.violated_by(r))

    def test_violated_by4(self):
        """Expectation 1 violated by reading with bad units and value"""
        test_id = 1

        expectation = self.session.query(Expectation).filter(
            Expectation.id == test_id
        ).one()

        r = Reading(units="FEST", value=90000)

        self.assertTrue(expectation.violated_by(r))

    def test_delete(self):
        """Expectation 1 properly deleted from system"""
        test_id = 1

        reading = self.session.query(Expectation).filter(
            Expectation.id == test_id
        ).one()

        self.session.delete(reading)
        self.session.commit()

        readings = self.session.query(Reading).filter(
            Reading.id == test_id
        ).all()

        self.assertEqual(readings, [])
