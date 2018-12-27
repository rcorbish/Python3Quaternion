'''
Created on Feb 22, 2015

@author: richard
'''
import unittest
from Quaternion import Quaternion


class Test(unittest.TestCase):

    def setUp(self):
        self.unitQuaternion = Quaternion(0.5,0.5,0.5,0.5) 
        self.up = Quaternion( 0, 0, 1, 0 )


    def tearDown(self):
        pass


    def testNormal(self) :
        normal = Quaternion( 0, -1, 1, 1 ).normalize()
        r1 = Quaternion.FromNormal( self.up.x, self.up.y, self.up.z, normal.x, normal.y, normal.z )
        n_hat = r1.rotate( self.up ).normalize()
        self.assertAlmostEqual( normal.w, n_hat.w, msg="Rotation 1 from normal vector failed - w" )
        self.assertAlmostEqual( normal.x, n_hat.x, msg="Rotation 1 from normal vector failed - x" )
        self.assertAlmostEqual( normal.y, n_hat.y, msg="Rotation 1 from normal vector failed - y" )
        self.assertAlmostEqual( normal.z, n_hat.z, msg="Rotation 1 from normal vector failed - z" )
        
        normal = Quaternion( 0, .707, -4.707, .707 ).normalize()
        r1 = Quaternion.FromNormal( self.up.x, self.up.y, self.up.z, normal.x, normal.y, normal.z )
        n_hat = r1.rotate( self.up ).normalize()
        self.assertAlmostEqual( normal.w, n_hat.w, msg="Rotation 2 from normal vector failed - w" )
        self.assertAlmostEqual( normal.x, n_hat.x, msg="Rotation 2 from normal vector failed - x" )
        self.assertAlmostEqual( normal.y, n_hat.y, msg="Rotation 2 from normal vector failed - y" )
        self.assertAlmostEqual( normal.z, n_hat.z, msg="Rotation 2 from normal vector failed - z" )

        normal = Quaternion( 0, .56, -.01, -1.5 ).normalize()
        r1 = Quaternion.FromNormal( self.up.x, self.up.y, self.up.z, normal.x, normal.y, normal.z )
        n_hat = r1.rotate( self.up ).normalize()
        self.assertAlmostEqual( normal.w, n_hat.w, msg="Rotation 3 from normal vector failed - w" )
        self.assertAlmostEqual( normal.x, n_hat.x, msg="Rotation 3 from normal vector failed - x" )
        self.assertAlmostEqual( normal.y, n_hat.y, msg="Rotation 3 from normal vector failed - y" )
        self.assertAlmostEqual( normal.z, n_hat.z, msg="Rotation 3 from normal vector failed - z" )
        


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

    
    def testFromEuler(self):
        q1 = Quaternion.FromEuler( -90, 0, 90 )
        e = q1.toEuler()
        self.assertTupleAlmostEqual( ( -90, 0, 90 ), e, "Euler conversion failed", 0.001 )

        q1 = Quaternion.FromEuler( 36, 22.5, 36 )
        e = q1.toEuler()
        self.assertTupleAlmostEqual( ( 36, 22.5, 36 ), e, "Euler conversion failed", 0.001 )

        q1 = Quaternion.FromEuler( 17, 87, 63 )
        e = q1.toEuler()
        self.assertTupleAlmostEqual( ( 17, 87, 63 ), e, "Euler conversion failed", 0.001 )
    

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
        
        r = q.rotate( Quaternion( 0, 1, 0, 0 ) )
        self.assertEqual( Quaternion( 0,0,0,-1 ), r, "Rotation failed" )
        
        
        
    def assertTupleAlmostEqual( self, t1, t2, msg, tolerance = 0.0001 ) :
        for i in range(min(len(t1), len(t2) ) ):
            self.assertAlmostEqual( t1[i], t2[i], msg=msg, delta=tolerance )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
