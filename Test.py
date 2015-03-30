'''
Created on Feb 22, 2015

@author: richard
'''
import unittest
from Quaternion.Quaternion import Quaternion


class Test(unittest.TestCase):

    def setUp(self):
        self.unitQuaternion = Quaternion(0.5,0.5,0.5,0.5) 


    def tearDown(self):
        pass


    def testNormalize(self):
        q1 = Quaternion(1,1,1,1) 
        q1.normalize()
        self.assertEqual( q1, self.unitQuaternion, "Normalizing a unit quaternion has no effect" )

        q1 = Quaternion(2,2,2,2) 
        q1.normalize()
        self.assertEqual( q1, self.unitQuaternion, "Normalized quaternion should be length 1" )

        q1 = Quaternion(-2,2,2,2) 
        q1.normalize()
        self.assertNotEqual( q1, self.unitQuaternion, "Normalized quaternion should preserve direction" )

    '''
    def testFromEuler(self):
        q1 = Quaternion.FromEuler( -90, 0, 90 )
        e = q1.toEuler()
        self.assertTupleAlmostEqual( ( -90, 0, 90 ), e, "Euler conversion failed" )

        q1 = Quaternion.FromEuler( 36, 22.5, 36 )
        e = q1.toEuler()
        self.assertTupleAlmostEqual( ( 36, 22.5, 36 ), e, "Euler conversion failed" )

        q1 = Quaternion.FromEuler( 17, 87, 63 )
        e = q1.toEuler()
        self.assertTupleAlmostEqual( ( 17, 87, 63 ), e, "Euler conversion failed" )
    '''

    def testSum(self) :
        pass
    

    def testMul(self) :
        q1 = Quaternion(1,0,1,0)
        q2 = Quaternion(1,1,0,0)
        self.assertEqual( q1*q2, Quaternion(1,1,1,-1), "Multiply results incorrect" )

        q1 = Quaternion(1,1,1,1)
        self.assertEqual( q1*q1, Quaternion(-2,2,2,2), "Multiply results incorrect" )
    
        q1 = Quaternion(1,2,3,4)
        q2 = Quaternion(4,3,2,1)
        q3 = q1*q2
        self.assertEqual( q3, Quaternion(-12,6,24,12), "Multiply results incorrect" )
        
        q4=~q2
        self.assertEqual( q3*q4, q1, "Multiply via inverse results incorrect" )
    

    def testRotate(self) :
        q = Quaternion( 0.7071203316249954, 0.0, 0.7071203316249954, 0.0 )
        q.normalize()
        
        self.assertAlmostEqual( 1.0, q.norm(), msg="Normalized quaternion is not unit length", delta=0.000000001 )
        
        r = q.rotate( 1, 0, 0 )
        self.assertEqual( Quaternion( 0,0,0,-1 ), r, "Rotation failed" )
        
        
        
    def assertTupleAlmostEqual( self, t1, t2, msg, tolerance = 0.0001 ) :
        for i in range(min(len(t1), len(t2) ) ):
            self.assertAlmostEqual( t1[i], t2[i], msg=msg, delta=tolerance )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()