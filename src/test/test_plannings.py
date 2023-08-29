 # type: ignore 
import unittest
from schedule.planning import Planning, SEvent, Days, STime

class TestPlanning(unittest.TestCase):

    def test_addEvent(self):
        planning = Planning()
        event = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event'
        )
        planning.addEvent(event)
        self.assertEqual(len(planning._data), 1)

    def test_remove_event(self):
        planning = Planning()
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
        planning.addEvent(event1)
        planning.addEvent(event2)
        self.assertEqual(len(planning._data), 2)
        planning.removeEvent(event1.id)
        self.assertEqual(len(planning._data), 1)
        self.assertIsNone(planning.findById(event1.id))
        self.assertIsNotNone(planning.findById(event2.id))

    def test_change_event(self):
        planning = Planning()
        event = SEvent(
            enable=True,
            days=Days.fromValues(False, False, False, False, False, False, False),
            channel=0,
            time=STime(0, 0, 0),
            name='New event'
        )
        planning.addEvent(event)
        event2 = planning.findById(event.id)
        event2.name = 'New name'
        event3 = planning.findById(event.id)
        self.assertEqual(event3.name, 'New name')

    def test_iteration(self):
        planning = Planning()
        for name in ('Name 1', 'Name 2', 'Name 3'):
            planning.addEvent(SEvent(
                enable=True,
                days=Days.fromValues(False, False, False, False, False, False, False),
                channel=0,
                time=STime(0, 0, 0),
                name=name
            ))
        self.assertEqual(len(planning._data), 3)
        for event in planning:
            self.assertIn(event.name, ('Name 1', 'Name 2', 'Name 3'))

if __name__ == '__main__':
    unittest.main()