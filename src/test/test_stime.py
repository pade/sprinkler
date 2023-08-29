import unittest
from schedule.stime import STime

class TestSTime(unittest.TestCase):
    
    def test_valueInRange(self):
        """ Set value in the correct range """
        stime = STime(13, 4, 50)
        self.assertEqual((stime.hours, stime.minutes, stime.duration), (13, 4, 50))
        
    def test_HoursOutOfRange(self):
        """ Hours are out of range """
        stime = STime(-10, 12, 20)
        self.assertEqual((stime.hours, stime.minutes, stime.duration), (0, 12, 20))
        stime = STime(50, 3, 2)
        self.assertEqual((stime.hours, stime.minutes, stime.duration), (23, 3, 2))

    def test_MinutesOutOfRange(self):
        """ Minutes are out of range """
        stime = STime(10, -12, 20)
        self.assertEqual((stime.hours, stime.minutes, stime.duration), (10, 0, 20))
        stime = STime(0, 70, 2)
        self.assertEqual((stime.hours, stime.minutes, stime.duration), (0, 59, 2))
            
    def test_DurationOutOfRange(self):
        """ Duration is out of range """
        stime = STime(10, 12, -20)
        self.assertEqual((stime.hours, stime.minutes, stime.duration), (10, 12, 0))
