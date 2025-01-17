# run with : python3 -m unittest TestAmoebaFitter

import unittest
import numpy as numpy
from numpy.testing import assert_array_almost_equal as assertAAE
from astropy import units
import math

import matplotlib.pyplot as plt


from BayesicFitting import *


__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

#  *
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
#  *  2004 - 2014 Do Kester, SRON (Java code)
#  *    2016 - 2017 Do Kester

class TestAmoebaFitter( unittest.TestCase ):
    """
    Test harness for Fitter class.

    Author:      Do Kester

    """
    aa = 5              #  average offset
    bb = 2              #  slope
    ss = 0.3            #  noise Normal distr.

    x = numpy.asarray( [ -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0] )
    noise = numpy.asarray( [-0.000996, -0.046035,  0.013656,  0.418449,  0.0295155,  0.273705,
      -0.204794,  0.275843, -0.415945, -0.373516, -0.158084] )

    def eq( self, a, b, eps=1e-10 ) :
        if ( a + b ) != 0 :
            return abs( a - b ) / abs( a + b ) < eps
        else :
            return abs( a - b ) < eps


################################################################################
    def plotAmoebaFitter( self ):
        self.testAmoebaFitter( plot=True )

    def testAmoebaFitter( self, plot=False ):

        c0 = 3.2
        c1 = -0.1
        c2 = 0.3
        c3 = 1.1
        c4 = 2.1
        y = ( self.x - c1 ) / c2
        y = c0 * numpy.exp( -y * y ) + self.noise

        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        print( "Testing Nonlinear Fitters: Amoeba" )
        print( "++++++++++++++++++++++++++++++++++++++++++++++++++" )
        modl1 = GaussModel( )

        numpy.set_printoptions(  precision=3, suppress=True )
        amfit = AmoebaFitter( self.x, modl1 )

        tr = numpy.asarray( [c0,c1,c2,c3,c4] )
        print( "Truth ", tr )

        par1 = amfit.fit( y )

        print( "x     ", self.x )
        print( "y     ", y )
        print( "par   ", par1 )

        modl2 = GaussModel( )
        modl2.addModel( PolynomialModel(1) )
        z = y + c4 * self.x + c3

        modl2.parameters = numpy.append( par1, [0,0] )
        lmfit = AmoebaFitter( self.x, modl2 )

        par2 = lmfit.fit( z )
        print( "z      ", z )
        print( "par2   ", par2 )


        print( "chisq1 = ", amfit.chisq, "  chisq2 = ", lmfit.chisq )

        assertAAE( par1, par2[:3], 1 )
        assertAAE( par2, tr, 0 )

        if plot :
            xx = numpy.linspace( -1, +1, 1001 )
            plt.plot( self.x, y, 'k+' )
            plt.plot( xx, modl1.result( xx ), 'k-' )
            plt.plot( self.x, z, 'r+' )
            plt.plot( xx, modl2.result( xx ), 'r-' )
            plt.show()



    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestAmoebaFitter.__class__ )


