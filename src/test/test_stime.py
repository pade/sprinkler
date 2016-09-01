# -*- coding: UTF-8 -*-
'''
Created on 29 août 2016

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

    def test_intoMinutes(self):
        
        t = stime.STime(hour=5,minute=20)
        self.assertTrue(t.intoMinutes() == 320)
        
        
    def test_str(self):
        '''
        Test print STime
        '''
        str_stime = "%s" % stime.STime(hour=12, minute=10)
        self.assertTrue(str_stime == "12:10")
        
        str_stime = "%s" % stime.STime(hour=1, minute=2)
        self.assertTrue(str_stime == "01:02")
        
    def test_add(self):
        '''
        Test add function with STime class
        '''
        t1 = stime.STime(hour=2, minute=10)
        
        t = t1 + 130
        self.assertTrue(t.hour == 4 and t.minute == 20)
        
        t2 = stime.STime(hour=23, minute=10)
        t = t2 + 60
        self.assertTrue(t.hour == 0 and t.minute == 10)
        
        t3 = stime.STime(hour=23, minute=45)
        t = t3 + 150
        self.assertTrue(t.hour == 2 and t.minute == 15, "Expected 02:15, get %s" % t)
        
    def test_set(self):
        '''
        Test set method
        '''
        t = stime.STime()
        t.set("2:3")
        self.assertTrue(t.hour == 2 and t.minute == 3)
        t.set("05:02")
        self.assertTrue(t.hour == 5 and t.minute == 2)

        self.assertRaises(ValueError, t.set, "abc")
        
    def test_toDateTime(self):
        '''
        Test toDateTime method
        '''
        now = datetime.today()
        t = stime.STime(5,20)
        dt = t.toDateTime()
        self.assertTrue(dt.year == now.year and dt.month == now.month and 
                        dt.day == now.day and dt.hour == t.hour and dt.minute == t.minute)
        

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
