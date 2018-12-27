'''
Created on Feb 22, 2015

@author: richard
'''
import math


class Quaternion(object):
    '''
    This implements quaternion algebra. A quaternion is represented by 4 
    components: a real part (w) and 3 imaginary parts (x,y,z)
    
    There is no divide operation - since in this type of algebra we
    multiply by an inverse. 
    
    At present this is not maximally efficient, I'll do that later when
    I know what needs to be done
    
    Some references I referred to:
    
    http://en.wikipedia.org/wiki/Quaternion
    http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19770024290.pdf
    http://introcs.cs.princeton.edu/java/32class/Quaternion.java.html
    http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/index.htm
    
    '''

    def __init__(self, w,x,y,z):
        '''
        Constructor
        '''
        self.q = [ w,x,y,z ]



        
        
        
    def normalize(self,tolerance=0.00001):
        '''
            Make the receiver into a quaternion of unit length
            
            This does change the input quaternion. 
            
            @return: self - can be used for chaining
        '''
        mag2 = sum(n * n for n in self.q)
        if abs(mag2 - 1.0) > tolerance:
            mag = math.sqrt(mag2)
            self.q = list( map( lambda x: x/mag, self.q ) )
        return self
        
        
        
    def norm(self) :
        '''
            Return a value representing the norm of the quaternion
            
            @return the norm of the quaternion ( as a number )
        '''
        return math.sqrt( self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z )


    
    def conj(self):
        '''
            Calculate the conjugate of a quaternion. This returns a new instance
            and leaves the receiver of the call alone
            
            @return: a brand new quaternion
        '''
        return Quaternion( self.w, -self.x, -self.y, -self.z )
        
        
        
    def rotate(self, p ):
        '''
            Rotate a vector using this quaternion. This implements a
            Hamiltonian multiply  Q x P  = Q P Q'
                         
            self is the rotation quaternion
            p is the vector to rotate as a quaternion (0,x,y,z)

            @return:  a quaternion
        '''
        return (self * p) * ~self



    def dot(self,other):
        '''
            A standard dot product - just a 4D extension of the 3D version
        '''
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z 



    def __invert__(self):
        '''
            Calculate the inverse of a quaternion. This returns a new instance
            and leaves the receiver of the call alone
        
            @return: a brand new quaternion
        '''
        n = self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z
        return Quaternion( self.w/n, -self.x/n, -self.y/n, -self.z/n )
        
    
    
    def __add__(self,other):
        '''
            Return the result of adding two quaternions together
            
            @return a new quaternion
        '''
        return Quaternion( self.w+other.w, self.x+other.x, self.y+other.y, self.z+other.z )
    
    
    def __sub__(self,other):
        '''
            Return the result of subtracting one quaternion from another
            
            @return a new quaternion
        '''
        return Quaternion( self.w-other.w, self.x-other.x, self.y-other.y, self.z-other.z )
    
    
    def __mul__(self,other):
        '''
            Return the result of multiplying one quaternion by another
            Note this is not-commutative ( see also __rmul__ )
            
            This is aka Kroenecker product 
            
            @return a new quaternion
        '''
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z;
        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y;
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x;
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w;
        return Quaternion( w,x,y,z ) 
    
    
    def __rmul__(self,other):
        '''
            Return the result of multiplying one quaternion by another. Note
            that quaternion multiplication is not commutative so this switches
            the argument order
            
            @return a new quaternion
        '''
        return other.__mul__(self)
    



        
    def toEuler(self):
        '''
            Convert the quaternion into a tuple of Euler angles
            
            @return:  tuple representing (yaw, pitch,roll)
            
        '''
        sqw = self.w*self.w;
        sqx = self.x*self.x;
        sqy = self.y*self.y;
        sqz = self.z*self.z;
        unit = sqx + sqy + sqz + sqw; # if normalised is one, otherwise is correction factor
        
        test = self.x*self.y + self.z*self.w;
        if (test > 0.4999*unit) : # singularity at north pole
            yaw = 2 * math.atan2(self.x,self.w);
            pitch = math.pi/2;
            roll = 0;
            
        else :
            if (test < -0.4999*unit) : # singularity at south pole
                yaw = -2 * math.atan2(self.x, self.w);
                pitch = -math.pi/2;
                roll = 0;
            else :
                yaw   = math.atan2( 2 * (self.y * self.w  -  self.x * self.z) , sqx - sqy - sqz + sqw )
                pitch = math.asin ( 2 * test / unit )
                roll  = math.atan2( 2 * (self.w * self.x  -  self.y*self.z) , -sqx + sqy - sqz + sqw )
                
        return ( math.degrees( roll ), math.degrees( pitch ), math.degrees( yaw ) )


    @classmethod
    def FromEuler(cls, yaw, pitch, roll ) :
        '''
            Convert the Euler angles (in degrees) into a quaternion
            of unit length
            
            Technically these are Tait-Bryan angles but are frequently
            referred to as Euler. However, these do have the 3 axes used.
            
            Conventions:  <derived from http://www.web3d.org/standards>
                yaw = rotation about y axis
                pitch = rotation about z axis
                roll = rotation about x axis
                
        '''
        y = math.radians( yaw / 2.0 )
        p = math.radians( pitch / 2.0  )
        r = math.radians( roll / 2.0 )
 
        '''
            Note that the observed axes are measured wrt actual co-ordinates
            they are extrinsic angles: so we need to reverse the order of multiplication
            of the matrices.
        '''
        s3 = math.sin(y)
        c3 = math.cos(y)
        s2 = math.sin(p)
        c2 = math.cos(p)
        s1 = math.sin(r)
        c1 = math.cos(r)
 
        c1c2 = c1*c2
        s1s2 = s1*s2
        
        w = c1c2*c3  - s1s2*s3
        x = c1c2*s3  + s1s2*c3
        y = s1*c2*c3 + c1*s2*s3
        z = c1*s2*c3 - s1*c2*s3

        this = cls(w,x,y,z)
        this.normalize()
        return this

    
    @classmethod
    def FromXYZ(cls, x, y, z ) :
        '''
            Convert the Tait-Bryan angles (in degrees) into a quaternion
            of unit length
            
            This is one of 12 possible quaternions that can rotate a vector
            to the given orientation
                
        '''
        x2 = math.radians( x / 2.0 )
        y2 = math.radians( y / 2.0  )
        z2 = math.radians( z / 2.0 )
         
        s1 = math.sin(x2)
        c1 = math.cos(x2)
        s2 = math.sin(y2)
        c2 = math.cos(y2)
        s3 = math.sin(z2)
        c3 = math.cos(z2)
 
        w = -s1*s2*s3 + c1*c2*c3
        x =  s1*c2*c3 + s2*s3*c1
        y = -s1*s3*c2 + s2*c1*c3
        z =  s1*s2*c3 + s3*c1*c2

        this = cls(w,x,y,z)
        this.normalize()
        return this

    
    @classmethod
    def Between( cls, fx, fy, fz, tx, ty, tz ) :
        '''
            Generate a quaternion that would rotate 
            the from vector (fx,fy,fz) into the to vector (tx,ty,tz)
        '''
        # dot product of from & to
        dot = fx*tx + fy*ty + fz*tz

        # cross product of from & to
        x = fy*tz - ty*fz
        y = fz*tx - tz*fx
        z = fx*ty - tx*fy

        w = math.sqrt( (fx*fx + fy*fy + fz*fz) * (tx*tx + ty*ty + tz*tz) ) + dot
        if w < 0.0001 : # vectors are exact opposite
            w = 0 
            x = -nz
            y = ny
            z = nx

        this = cls( w, x, y, z )
        return this



        if dot > 1 :
            return Quaternion( 0,0,0,1 ) 

        if dot <= -1 :
            return Quaternion( 0,1,0,0 ) 

        s = math.sqrt( (1+dot) * (1+dot) )
        
        this = cls( s/2.0, ax/s, ay/s, az/s ) 
        this.normalize()
        return this

    
    
        
    def __getattribute__(self,name):
        '''
            Used to export the individual components as named atts
        '''
        if( name=="w") : return self.q[0]
        if( name=="x") : return self.q[1]
        if( name=="y") : return self.q[2]
        if( name=="z") : return self.q[3]
        return object.__getattribute__(self,name)
    
    
    def __repr__(self) :
        '''
            A unique representation of the quaternion
        '''
        return str( self )
    
    
    def __str__(self) :
        '''
            Return the quaternion as w+xi+yj+zk
        '''
        return "{:.3g} {:+.3g}i {:+.3g}j {:+.3g}k".format( self.q[0] ,self.q[1], self.q[2], self.q[3] )
    
    
    def __eq__(self,other):
        '''
            This compares the individual values. If they're the same
            so are both quaternions
        '''
        return self.q==other.q
    
    def __bool__(self):
        '''
           if all values w,x,y,z are 0 then return false 
        '''
        return not all( v==0 for v in self.q )