import numpy as numpy

from . import Tools
from .Formatter import formatter as fmt
from .Dynamic import Dynamic
from .Engine import Engine

__author__ = "Do Kester"
__year__ = 2018
__license__ = "GPL"
__version__ = "1.0"
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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2018        Do Kester


class DeathEngine( Engine ):
    """
    The DeathEngine deletes a component from the model.

    Only for Models that are Dynamic.
    The death rate is governed by the growth-prior in the dynamic model.

    The member is kept when the logLikelihood > lowLhood.

    Author       Do Kester.

    """
#    _deathrate = 1.0

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=23455, verbose=0 ):
        """
        Constructor.

        Parameters
        ----------
        walkers : WalkerList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : GalileanEngine
            to be copied
        seed : int
            for random number generator
        """
        super( DeathEngine, self ).__init__( walkers, errdis, copy=copy,
                    seed=seed, verbose=verbose )

    def copy( self ):
        """ Return copy of this.  """
        return DeathEngine( self.walkers, self.errdis, copy=self )

    def __str__( self ):
        return str( "DeathEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood ):
        """
        Execute the engine by removins a component.

        Parameters
        ----------
        walker : Walker
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood

        Returns
        -------
        int : the number of successfull moves

        """
        self.reportCall()

        cwalker = walker.copy()          ## work on local copy
        problem = cwalker.problem
        model = problem.model
        allp = cwalker.allpars
        ptry = allp
        ftry = cwalker.fitIndex

#        print( "DEAT0  ", fmt( ptry ), fmt( walker.problem.model.parameters ), fmt( ftry ) )

        off = 0
        while model is not None and not isinstance( model, Dynamic ) :
            off += model.npbase
            model = model._next

        nc = model.ncomp
        np = model.npbase

        if self.verbose > 4 :
            print( "DEN1  ", cwalker.id, nc, np, len( ptry ), len( ftry ) )

        # shuffle the parameters (if needed) before throwing the last one out.
        ptry = model.shuffle( ptry, off, np, self.rng )

        if not ( nc > model.growPrior.unit2Domain( self.rng.rand() ) and
                model.shrink( offset=off, rng=self.rng ) ) :
            self.reportFailed()
            return 0

        dnp = model.npbase - np         # parameter decrease

        ftry = model.alterFitindex( ftry, np, dnp, off )
        ptry = problem.model.parameters
        if self.errdis.nphypar > 0 :
            ptry = numpy.append( ptry, allp[-self.errdis.nphypar:] )

        Ltry = self.errdis.logLikelihood( problem, ptry )

        if Ltry >= lowLhood:
            self.reportSuccess()
            self.setWalker( cwalker, problem, ptry, Ltry, fitIndex=ftry )
            wlkr = self.walkers[walker.id]
            wlkr.check( nhyp=self.errdis.nphypar )
            return abs( dnp )

        self.reportReject( )

        return 0


