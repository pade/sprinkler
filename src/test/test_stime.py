# -*- coding: UTF-8 -*-
'''
Created on 29 ao�t 2016

@author: dassierp
'''
import os
import sys
from datetime import datetime
import unittest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import stime

class TestSTime(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        '''
        Test STime initialisation
        '''
        t = stime.STime(hour=5, minute=10)
        self.assertTrue(t.hour == 5 and t.minute == 10)
        
        t = stime.STime(hour=25, minute=10)
        self.assertTrue(t.hour == 23 and t.minute == 10)
        
        t = stime.STime(hour=-1, minute=10)
        self.assertTrue(t.hour == 0 and t.minute == 10)
        
        t = stime.STime(hour=5, minute=60)
        self.assertTrue(t.hour == 5 and t.minute == 59)
        
        t = stime.STime(hour=5, minute=-1)
        self.assertTrue(t.hour == 5 and t.minute == 0)
        
        t = stime.STime(1, hour=2, minute=10)
        self.assertTrue(t.day == 1 and t.hour == 2 and t.minute == 10)

    def test_intoMinutes(self):
        
        t = stime.STime(hour=5,minute=20)
        self.assertTrue(t.intoMinutes() == 320)
        
        
    def test_str(self):
        '''
        Test print STime
        '''
        str_stime = "%s" % stime.STime(day=1, hour=12, minute=10)
        self.assertTrue(str_stime == "[Mon] 12:10")
        
        str_stime = "%s" % stime.STime(day=5, hour=1, minute=2)
        self.assertTrue(str_stime == "[Fri] 01:02")
        
    def test_add_stime(self):
        '''
        Test add function with STime class
        '''
        t1 = stime.STime(day=1, hour=2, minute=10)
        
        t2 = stime.STime(day=0, hour=0, minute=20)
        t3 = t1 + t2
        self.assertTrue(t3.hour == 2 and t3.minute == 30)
        
        t2 = stime.STime(hour=0, minute=55)
        t3 = t1 + t2
        self.assertTrue(t3.hour == 3 and t3.minute == 5)
        
        t2 = stime.STime(hour=23, minute=10)
        t3 = t1 + t2
        self.assertTrue(t3.day == 2 and t3.hour == 1 and t3.minute == 20)
        
        t2 = stime.STime(hour=23, minute=55)
        t3 = t1 + t2
        self.assertTrue(t3.day == 2 and t3.hour == 2 and t3.minute == 5, "Expected [Tue] 02:05, get %s" % t3)
        
    def test_add_duration(self):
        '''
        Test add function with duration
        '''
        t = stime.STime(2, 10)
        
        t2 = t + 20
        self.assertTrue(t2.hour == 2 and t2.minute == 30)
        
        t2 = t + 90
        self.assertTrue(t2.hour == 3 and t2.minute == 40)
        
        t2 = t + 23 * 60 + 10
        self.assertTrue(t2.hour == 1 and t2.minute == 20)

    def test_now(self):
        '''
        Text 'now()' class method
        '''
        t = stime.STime.now()
        dt = datetime.now()
        self.assertTrue(t.hour == dt.hour and t.minute == dt.minute, "Expected %02d:%02d, get %s" % (dt.hour, dt.minute, t))
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSTime))
    return suite    

        
if __name__ == "__main__":   
    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)