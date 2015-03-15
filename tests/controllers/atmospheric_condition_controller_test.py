"""
test that things behave the way they ought to
"""
import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from bin.models import base
from sqlalchemy.sql import exists

from bin.models.environment import Environment
from bin.models.atmospheric_condition import AtmosphericCondition
from bin.models.expectation import Expectation
from bin.models.alarm import Alarm
from bin.models.reading import Reading
from bin.models.channel import Channel

from bin.controllers.atmospheric_condition_controller import (
    AtmosphericConditionController
)

class AtmosphericConditionControllerTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        base.Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        conditions = [
            AtmosphericCondition(
                type="Temperature",
                channel_bus=1,
                channel_address=1,
                channel_number=1,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=1,
                channel_address=2,
                channel_number=2,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=1,
                channel_address=3,
                channel_number=3,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=2,
                channel_address=1,
                channel_number=4,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=2,
                channel_address=2,
                channel_number=1,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=3,
                channel_address=1,
                channel_number=2,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=3,
                channel_address=2,
                channel_number=3,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=3,
                channel_address=3,
                channel_number=4,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=4,
                channel_address=1,
                channel_number=5,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            ),
            AtmosphericCondition(
                type="Temperature",
                channel_bus=4,
                channel_address=2,
                channel_number=1,
                rec_freq=15,
                expectation=Expectation(units="Celsius", low=-90, high=-80)
            )
        ]

        for c in conditions:
            self.session.add(c)
        self.session.commit()

        self.condition_controller = AtmosphericConditionController(
            dbsession=self.session,
            conditions=conditions
        )

    def tearDown(self):
        self.session.close()

class AtmosphericConditionControllerTestSuite(
        AtmosphericConditionControllerTest
):
    def test_assign_channels_all_channels_missing(self):
        channels = []
        no_channels = self.condition_controller.assign_channels(channels)

        self.assertEqual(
            set(no_channels), 
            set(self.condition_controller.atmospheric_conditions)
        )
    def test_assign_channels_some_channels_missing(self):
        vchannels = [ 
            Channel( #ac[0]
                bus=1, 
                address=1, 
                channel_number=1, 
                device_handle=None, 
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[1]
                bus=1,
                address=2,
                channel_number=2,
                device_handle=None,
                read_method=None,
                units="Celsius" 
            ),
            Channel( #ac[2]
                bus=1,
                address=3,
                channel_number=3,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[4]
                bus=2,
                address=2,
                channel_number=1,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[5]
                bus=3,
                address=1,
                channel_number=2,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[7]
                bus=3,
                address=3,
                channel_number=4,
                device_handle=None,
                read_method=None,
                units="Celsius"
            )
        ]
        no_channels = self.condition_controller.assign_channels(vchannels)
        no_channels_actual = [
            self.condition_controller.atmospheric_conditions[3],
            self.condition_controller.atmospheric_conditions[6],
            self.condition_controller.atmospheric_conditions[8],
            self.condition_controller.atmospheric_conditions[9],
        ]

        self.assertEqual(
            set(no_channels),
            set(no_channels_actual)
        )

    def test_assign_channels_success(self):
        vchannels = [ 
            Channel( #ac[0]
                bus=1, 
                address=1, 
                channel_number=1, 
                device_handle=None, 
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[1]
                bus=1,
                address=2,
                channel_number=2,
                device_handle=None,
                read_method=None,
                units="Celsius" 
            ),
            Channel( #ac[2]
                bus=1,
                address=3,
                channel_number=3,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[3]
                bus=2,
                address=1,
                channel_number=4,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[4]
                bus=2,
                address=2,
                channel_number=1,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[5]
                bus=3,
                address=1,
                channel_number=2,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[6]
                bus=3,
                address=2,
                channel_number=3,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[7]
                bus=3,
                address=3,
                channel_number=4,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[8]
                bus=4,
                address=1,
                channel_number=5,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ),
            Channel( #ac[5]
                bus=4,
                address=2,
                channel_number=1,
                device_handle=None,
                read_method=None,
                units="Celsius"
            ) 
        ]

        no_channels = self.condition_controller.assign_channels(vchannels)
        no_channels_actual = []

        self.assertEqual(
            set(no_channels),
            set(no_channels_actual)
        )

    def test_gather_readings_many_alarms(self):
        def fake_read(device_handle, channel_number):
            return device_handle

        vchannels = [ 
            Channel( #ac[0]
                bus=1, 
                address=1, 
                channel_number=1, 
                device_handle=0, 
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[1]
                bus=1,
                address=2,
                channel_number=2,
                device_handle=0,
                read_method=fake_read,
                units="Celsius" 
            ),
            Channel( #ac[2]
                bus=1,
                address=3,
                channel_number=3,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[3]
                bus=2,
                address=1,
                channel_number=4,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[4]
                bus=2,
                address=2,
                channel_number=1,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[5]
                bus=3,
                address=1,
                channel_number=2,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[6]
                bus=3,
                address=2,
                channel_number=3,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[7]
                bus=3,
                address=3,
                channel_number=4,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[8]
                bus=4,
                address=1,
                channel_number=5,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[9]
                bus=4,
                address=2,
                channel_number=1,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ) 
        ]
        self.condition_controller.assign_channels(vchannels)
        alarms = self.condition_controller.gather_readings()

        self.assertEqual(len(alarms), 9)

    def test_gather_readings_few_alarms(self):
        def fake_read(device_handle, channel_number):
            return device_handle

        vchannels = [ 
            Channel( #ac[0]
                bus=1, 
                address=1, 
                channel_number=1, 
                device_handle=-85, 
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[1]
                bus=1,
                address=2,
                channel_number=2,
                device_handle=0,
                read_method=fake_read,
                units="Celsius" 
            ),
            Channel( #ac[2]
                bus=1,
                address=3,
                channel_number=3,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[3]
                bus=2,
                address=1,
                channel_number=4,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[4]
                bus=2,
                address=2,
                channel_number=1,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[5]
                bus=3,
                address=1,
                channel_number=2,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[6]
                bus=3,
                address=2,
                channel_number=3,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[7]
                bus=3,
                address=3,
                channel_number=4,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[8]
                bus=4,
                address=1,
                channel_number=5,
                device_handle=0,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[9]
                bus=4,
                address=2,
                channel_number=1,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ) 
        ]
        self.condition_controller.assign_channels(vchannels)
        alarms = self.condition_controller.gather_readings()

        self.assertEqual(len(alarms), 5)

    def test_gather_readings_no_alarms(self):
        def fake_read(device_handle, channel_number):
            return device_handle

        vchannels = [ 
            Channel( #ac[0]
                bus=1, 
                address=1, 
                channel_number=1, 
                device_handle=-85, 
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[1]
                bus=1,
                address=2,
                channel_number=2,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius" 
            ),
            Channel( #ac[2]
                bus=1,
                address=3,
                channel_number=3,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[3]
                bus=2,
                address=1,
                channel_number=4,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[4]
                bus=2,
                address=2,
                channel_number=1,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[5]
                bus=3,
                address=1,
                channel_number=2,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[6]
                bus=3,
                address=2,
                channel_number=3,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[7]
                bus=3,
                address=3,
                channel_number=4,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[8]
                bus=4,
                address=1,
                channel_number=5,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ),
            Channel( #ac[9]
                bus=4,
                address=2,
                channel_number=1,
                device_handle=-85,
                read_method=fake_read,
                units="Celsius"
            ) 
        ]
        self.condition_controller.assign_channels(vchannels)
        alarms = self.condition_controller.gather_readings()

        self.assertEqual(len(alarms), 0)
