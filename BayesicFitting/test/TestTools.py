# run with : python3 -m unittest TestTools

import unittest
import numpy as numpy
import math
from datetime import date

from BayesicFitting import *

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *  2006-2015 Do Kester (JAVA CODE)

class ATestClass( object ) :
    def __init__( self, copy=None ) :
        super( ATestClass, self ).__init__( )
        self.setatt( "n1", 4 )
        self.setatt( "n2", 4, type=int )
        self.setatt( "p1", 4.0, type=float, isnone=True )
        self.setatt( "p2", None, type=float, isnone=True )
        self.setatt( "ln", 4, type=int, islist=True )
        self.setatt( "lp", 4, type=float, islist=True )

        try :
            self.setatt( "ep", 4.78, type=int, islist=True )
            assert( False )
        except TypeError :
            assert( True )

    def setatt( self, name, value, type=None, islist=None, isnone=False ) :
        Tools.setAttribute( self, name, value, type=type, islist=islist, isnone=isnone )


class TestTools( unittest.TestCase ) :
    """
    Test harness for Fitter class.

    @author Do Kester

    """
    def testATestClass( self ) :
        atc = ATestClass()

        Tools.printclass( atc )

    def testIsBetween( self ) :
        self.assertTrue( Tools.isBetween( 1, 2, 3 ) )
        self.assertTrue( Tools.isBetween( 3, 2, 1 ) )

        self.assertFalse( Tools.isBetween( 2, 1, 3 ) )
        self.assertFalse( Tools.isBetween( 2, 3, 1 ) )


        self.assertTrue( Tools.isBetween( 2, 2, 3 ) )
        self.assertTrue( Tools.isBetween( 1, 2, 2 ) )
        self.assertTrue( Tools.isBetween( 2, 2, 1 ) )
        self.assertTrue( Tools.isBetween( 3, 2, 2 ) )
        self.assertTrue( Tools.isBetween( 2, 2, 2 ) )




    def testBaseModel( self ) :
        atc = BaseModel( 4 )
        atc.posIndex = [1,2]
        print( atc.posIndex )

#        atc.posIndex = 1.2

        try :
            atc.posIndex = 1.2
            print( atc.posIndex )
            self.assertTrue( False )
        except TypeError :
            self.assertTrue( True )

        try :
            atc.PosIndex = 1
            self.assertTrue( False )
        except AttributeError :
            self.assertTrue( True )

        try :
            atc.posIndex = None
            self.assertTrue( False )
        except TypeError :
            self.assertTrue( True )


    def testtoday( self ):
        print( date.today() )

    def testMakeNext( self ):
        print( "===== makeNext ===========================" )
        x = 2
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( nx == 2 )
        xgen.close()

        x = [2,3,4,5]
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( ( nx == (k+2) and k < 4 ) or nx == 5 )
        xgen.close()

        x = [2,3,4,5,6,7,8,9,10,11]
        xgen = Tools.makeNext( x, 0 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( nx == (k+2) )

        x = [2,3,4,5]
        xgen = Tools.makeNext( x, 2 )
        for k in range( 10 ) :
            nx = next( xgen )
            print( k, nx )
            self.assertTrue( ( nx == (k+4) and k < 6 ) or nx == 5 )
        xgen.close()

    def testLength( self ) :
        print( "===== length ================================" )
        x = 3.0
        self.assertTrue( Tools.length( x ) == 1 )
        x = [2,3,4,5]
        self.assertTrue( Tools.length( x ) == 4 )
        x = numpy.asarray( [2,3,4,5] )
        self.assertTrue( Tools.length( x ) == 4 )
        x.resize( 2, 2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( Tools.length( x ) == 2 )
        x = [2,3,4,5]
        x = numpy.asarray( [x] )
        print( x, x.shape, x.__class__ )
        self.assertTrue( Tools.length( x ) == 1 )

    def testToArray( self ) :
        print( "===== toArray ================================" )
        x = Tools.toArray( 3 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( 3.0 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4,5,6] )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4.5,5,6], ndim=1 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 1 )
        x = Tools.toArray( [3,4.5], ndim=2 )
        print( x, x.shape, x.__class__ )
        self.assertTrue( isinstance( x, numpy.ndarray ) and x.ndim == 2 )

    @classmethod
    def suite( cls ):
        return ConfiguredTestCase.suite( PriorTest.__class__ )

if __name__ == '__main__':
    unittest.main( )


