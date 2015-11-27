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

class QuantitativePropertyModelTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        base.Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        test_expectation = Expectation(units="Test", low=0, high=0)

        conditions = [
            QuantitativeProperty(
                type="Test1",
                channel_bus=0,
                channel_address=0,
                channel_number=0,
                rec_freq=0,
                expectation=test_expectation
            ),
            QuantitativeProperty(
                type="Test2",
                channel_bus=1,
                channel_address=1,
                channel_number=1,
                rec_freq=0,
                expectation=test_expectation
            ),
            QuantitativeProperty(
                type="Test3",
                channel_bus=2,
                channel_address=2,
                channel_number=2,
                rec_freq=2,
                expectation=test_expectation
            ),
            QuantitativeProperty(
                type="Test4",
                channel_bus=3,
                channel_address=3,
                channel_number=3,
                rec_freq=3,
                expectation=test_expectation
            )
        ]

        conditions[1].readings.append(Reading(units="test", value=0))

        conditions[2].readings.append(Reading(units="test", value=0))
        conditions[2].readings.append(Reading(units="test", value=0))
        conditions[2].readings.append(Reading(units="test", value=0))
        conditions[2].readings.append(Reading(units="test", value=0))

        conditions[3].alarms.append(Alarm())
        conditions[3].alarms.append(Alarm())
        conditions[3].alarms.append(Alarm())
        conditions[3].alarms.append(Alarm())


        for c in conditions:
            self.session.add(c)
        self.session.commit()

    def tearDown(self):
        self.session.close()

class QuantitativePropertyModelTestSuite(QuantitativePropertyModelTest):
    def test_access1(self):
        """Quantitative Property 1's ID matches first Quantitative Property entered"""
        test_id = 1
        expected_type = "Test1"
        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertEqual(ac.type, expected_type)

    def test_access2(self):
        """Quantitative Property 2's ID matches second Quantitative Property entered"""
        test_id = 2
        expected_type = "Test2"

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertEqual(ac.type, expected_type)

    def test_access3(self):
        """Quantitative Property 3's ID matches third Quantitative Property entered"""
        test_id = 3
        expected_type = "Test3"

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()
        self.assertEqual(ac.type, expected_type)

    def test_access4(self):
        """Quantitative Property 4's ID Matches fourth Quantitative Property entered"""
        test_id = 4
        expected_type = "Test4"

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertEqual(ac.type, expected_type)


    def test_modify1(self):
        """Quantitative Property's expectation can be properly modified"""
        test_id = 1
        altered_expectation_units = "It's A Test!"
        altered_expectation = Expectation(
            units=altered_expectation_units,
            low=1,
            high=10000
        )

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()
        ac.expectation = altered_expectation

        self.session.add(ac)
        self.session.commit()

        same_ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertEqual(
            same_ac.expectation.units,
            altered_expectation_units
        )

    def test_add_reading(self):
        """Quantitative Propery can have readings added"""
        test_id = 1
        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        ac.readings.append(Reading(units="Test1234", value=123456.789))

        self.session.add(ac)
        self.session.commit()

        same_ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        last_reading = same_ac.most_recent_reading()

        self.assertEqual(
            last_reading.units, "Test1234"
        )

        self.assertEqual(
            last_reading.value, 123456.789
        )

    def test_most_recent_alarm1(self):
        """Quantitative Property's most recent alarm is None"""
        test_id = 1
        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertTrue(ac.most_recent_alarm() is None)

    def test_most_recent_alarm2(self):
        """Quantitative Property's most recent alarm fetches properly"""
        test_id = 1
        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        alarm = Alarm()
        ac.alarms.append(alarm)

        self.session.add(ac)
        self.session.commit()

        actual_most_recent_alarm_id = alarm.id

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertEqual(
            ac.most_recent_alarm().id,
            actual_most_recent_alarm_id
        )

    def test_alarm_active1(self):
        """Quantitative Property properly determines an alarm is active"""
        test_id = 1
        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        alarm = Alarm()
        ac.alarms.append(alarm)

        self.session.add(ac)
        self.session.commit()

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertTrue(ac.alarm_active())

    def test_alarm_active2(self):
        """Quantitative Property properly determines there is no active alarm"""
        test_id = 1
        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        alarm = Alarm()
        alarm.end()
        ac.alarms.append(alarm)

        self.session.add(ac)
        self.session.commit()

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertFalse(
            ac.alarm_active()
        )

    def test_record_due1(self):
        """Quantitative Property 1 properly determines there is a record due"""
        # no record committed for conditions[0]
        test_id = 1

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertTrue(
            ac.record_due()
        )

    def test_record_due2(self):
        """Quantitative Property 2 properly determines there is a record due"""
        test_id = 2

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertTrue(
            ac.record_due()
        )

    def test_record_due3(self):
        """Quantitative Property 3 properly determines there is no record due"""
        test_id = 2

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        ac.recording_frequency = 15
        self.session.add(ac)
        self.session.commit()

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.assertFalse(
            ac.record_due()
        )

    def test_orphanage1(self):
        """Quantitative Property reading orphans are properly deleted"""
        # make sure orphans are removed
        test_id = 3

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        ac.readings = []
        self.session.add(ac)
        self.session.commit()

        q = self.session.query(Reading).filter(
            Reading.quantitative_property_id==test_id
        ).all()

        self.assertEqual(q, [])

    def test_orphanage2(self):
        """Quantitative Property alarm orphans are properly deleted"""
        # make sure orphans are removed
        test_id = 4

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        ac.alarms = []
        self.session.add(ac)
        self.session.commit()

        q = self.session.query(Alarm).filter(
            Alarm.quantitative_property_id==test_id
        ).all()

        self.assertEqual(q, [])


    def test_delete1(self):
        """Quantitative Property can be properly removed from the system"""
        test_id = 3

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.session.delete(ac)
        self.session.commit()

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).all()

        self.assertEqual(ac, [])

    def test_delete2(self):
        """Quantitative Property deletion properly cascades to readings"""
        # make sure delete cascades 1
        test_id = 1

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.session.delete(ac)
        self.session.commit()

        q = self.session.query(Reading).filter(
            Reading.quantitative_property_id==test_id
        ).all()

        self.assertEqual(q, [])

    def test_delete3(self):
        """Quantitative Property deletion properly cascades to alarms"""
        # make sure delete cascades 2
        test_id = 4

        ac = self.session.query(QuantitativeProperty).filter(
            QuantitativeProperty.id == test_id
        ).one()

        self.session.delete(ac)
        self.session.commit()

        q = self.session.query(Alarm).filter(
            Alarm.quantitative_property_id==test_id
        ).all()

        self.assertEqual(q, [])
