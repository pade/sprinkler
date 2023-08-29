 # type: ignore 
import unittest
from schedule.planning import Planning, SEvent, Days, STime
from uuid import uuid4

class TestPlanning(unittest.TestCase):
    
    def setUp(self) -> None:
        self.planning = Planning()
        return super().setUp()

    def test_addEvent(self):
        event = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event'
        )
        self.planning.addEvent(event)
        self.assertEqual(len(self.planning._data), 1)
        
    def test_addEventWithId(self):
        id = uuid4()
        event = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event',
            id=id
        )
        self.planning.addEvent(event)
        self.assertIsNotNone(self.planning.findById(id))
    
    def test_remove_event(self):
        event1 = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event'
        )
        event2 = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event 2'
        )
        self.planning.addEvent(event1)
        self.planning.addEvent(event2)
        self.assertEqual(len(self.planning._data), 2)
        self.planning.removeEvent(event1.id)
        self.assertEqual(len(self.planning._data), 1)
        self.assertIsNone(self.planning.findById(event1.id))
        self.assertIsNotNone(self.planning.findById(event2.id))

    def test_change_event(self):
        event = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event'
        )
        self.planning.addEvent(event)
        event2 = self.planning.findById(event.id)
        event2.name = 'New name'
        event3 = self.planning.findById(event.id)
        self.assertEqual(event3.name, 'New name')

    def test_iteration(self):
        for name in ('Name 1', 'Name 2', 'Name 3'):
            self.planning.addEvent(SEvent(
                enable=True,
                days=Days.fromValues(False, False, False, False, False, False, False),
                channel=0,
                time=STime(0, 0, 0),
                name=name
            ))
        self.assertEqual(len(self.planning._data), 3)
        for event in self.planning:
            self.assertIn(event.name, ('Name 1', 'Name 2', 'Name 3'))

if __name__ == '__main__':
    unittest.main()