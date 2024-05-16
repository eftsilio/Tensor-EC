from src.processEvents import Event, InputEvent, ComplexEvent
from src.processSimpleFluents import SimpleFluent
from src.processSDFluents import InputSDF, ComplexSDF
from . import declarations

import numpy as np
from scipy import sparse as sp


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% GAP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtGapNP():
    x = InputEvent.__getTimeMatrix__(('gap_start',))
    y = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = x.multiply(y)

    return result


def initiatedAtGapFFP():
    x = InputEvent.__getTimeMatrix__(('gap_start',))
    y = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = x - x.multiply(y)

    return result


def terminatedAtGap():
    return InputEvent.__getTimeMatrix__(('gap_end',))


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% STOPPED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtStoppedNP():
    x = InputEvent.__getTimeMatrix__(('stop_start',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = (x - x.multiply(y)).multiply(z)

    return result


def initiatedAtStoppedFFP():
    x = InputEvent.__getTimeMatrix__(('stop_start',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r1 = x - x.multiply(y)
    result = r1 - r1.multiply(z)

    return result


def terminatedAtStopped():
    x = InputEvent.__getTimeMatrix__(('stop_end',))

    result = x

    return result


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LOWSPEED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtLowSpeed():
    x = InputEvent.__getTimeMatrix__(('slow_motion_start',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    result = x - x.multiply(y)

    return result


def terminatedAtLowSpeed():
    x = InputEvent.__getTimeMatrix__(('slow_motion_end',))

    result = x

    return result


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% WITHIN_AREA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtWithinAreaAnchorage():
    x = InputEvent.__getTimeMatrix__(('entersArea_anchorage',))

    return x


def initiatedAtWithinAreaFishing():
    x = InputEvent.__getTimeMatrix__(('entersArea_fishing',))

    return x


def initiatedAtWithinAreaNatura():
    x = InputEvent.__getTimeMatrix__(('entersArea_natura',))

    return x


def initiatedAtWithinAreaNearCoast():
    x = InputEvent.__getTimeMatrix__(('entersArea_nearCoast',))

    return x


def initiatedAtWithinAreaNearCoast5k():
    x = InputEvent.__getTimeMatrix__(('entersArea_nearCoast5k',))

    return x


def initiatedAtWithinAreaNearPorts():
    x = InputEvent.__getTimeMatrix__(('entersArea_nearPorts',))

    return x


######################################################################################################################
def terminatedAtWithinAreaAnchorage():
    x = InputEvent.__getTimeMatrix__(('leavesArea_anchorage',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y


def terminatedAtWithinAreaFishing():
    x = InputEvent.__getTimeMatrix__(('leavesArea_fishing',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y


def terminatedAtWithinAreaNatura():
    x = InputEvent.__getTimeMatrix__(('leavesArea_natura',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y


def terminatedAtWithinAreaNearCoast():
    x = InputEvent.__getTimeMatrix__(('leavesArea_nearCoast',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y


def terminatedAtWithinAreaNearCoast5k():
    x = InputEvent.__getTimeMatrix__(('leavesArea_nearCoast5k',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y


def terminatedAtWithinAreaNearPorts():
    x = InputEvent.__getTimeMatrix__(('leavesArea_nearPorts',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% UNDER_WAY %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtUnderWay():
    x = InputEvent.__getTimeMatrix__(('velocityGr2_7Lt48_6',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    result = x - x.multiply(y)

    return result


def terminatedAtUnderWay():
    x1 = InputEvent.__getTimeMatrix__(('velocityGr48_6',))
    x2 = InputEvent.__getTimeMatrix__(('velocityLt2_7',))

    return x1 + x2


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ADRIFT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtAdrift():
    x = InputEvent.__getTimeMatrix__(('velocityAngleGr15',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('underWay', 'true'))

    result = (x - x.multiply(y)).multiply(z)

    return result


def terminatedAtAdrift():
    x = InputEvent.__getTimeMatrix__(('velocityAngleLe15',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('underWay', 'true'))

    r1 = (x - x.multiply(y)).multiply(z)

    v = InputEvent.__getTimeMatrix__(('velocity',))
    u = SimpleFluent.__getHoldsAtMatrix__(('underWay', 'true'))

    r3 = v - v.multiply(u)

    return r1 + r3


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BEFOREAGROUND %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtBeforeAgroundNP():
    x = InputEvent.__getTimeMatrix__(('velocityLt0_005',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    return (x - x.multiply(y)).multiply(z)


def initiatedAtBeforeAgroundFFP():
    x = InputEvent.__getTimeMatrix__(('velocityLt0_005',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r1 = x - x.multiply(y)

    return r1 - r1.multiply(z)


def terminatedAtBeforeAground():
    x = InputEvent.__getTimeMatrix__(('velocityGr0_005',))

    return x


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ANCHOR %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtAnchorNP():
    x = InputEvent.__getTimeMatrix__(('velocityLt0_2',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    return (x - x.multiply(y)).multiply(z)


def initiatedAtAnchorFFP():
    x = InputEvent.__getTimeMatrix__(('velocityLt0_2',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r1 = x - x.multiply(y)

    return r1 - r1.multiply(z)


def terminatedAtAnchorNP():
    x = InputEvent.__getTimeMatrix__(('coord',))
    y = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r1 = x - x.multiply(y)
    r2 = InputEvent.__getTimeMatrix__(('velocityGr0_2',))

    return r1 + r2


def terminatedAtAnchorFFP():
    x = InputEvent.__getTimeMatrix__(('coord',))
    y = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r1 = x.multiply(y)
    r2 = InputEvent.__getTimeMatrix__(('velocityGr0_2',))

    return r1 + r2


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRAWLSPEED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtTrawlSpeed():

    x = InputEvent.__getTimeMatrix__(('velocityGr1Lt9',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r1 = x - x.multiply(y)
    return r1 - r1.multiply(z)


def terminatedAtTrawlSpeed():
    x1 = InputEvent.__getTimeMatrix__(('velocityGr9',))
    x2 = InputEvent.__getTimeMatrix__(('velocityLt1',))

    r1 = x1 + x2

    y = InputEvent.__getTimeMatrix__(('coord',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    r2 = y.multiply(z)

    return r1 + r2


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRAVELSPEED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtTravelSpeed():
    x = InputEvent.__getTimeMatrix__(('velocityGrMinLtMax',))
    w = InputEvent.__getTimeMatrix__(('gap_start',))

    return x - x.multiply(w)


def terminatedAtTravelSpeed():
    x1 = InputEvent.__getTimeMatrix__(('velocityGrMax',))
    x2 = InputEvent.__getTimeMatrix__(('velocityLtMin',))

    return x1 + x2


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% speedLessThanMin %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtSpeedLessThanMin():
    x = InputEvent.__getTimeMatrix__(('velocityLtMin',))
    w = InputEvent.__getTimeMatrix__(('gap_start',))

    return x - x.multiply(w)


def terminatedAtSpeedLessThanMin():
    x = InputEvent.__getTimeMatrix__(('velocityGeMin',))

    return x


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% speedGrThanMax %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtSpeedGrThanMax():
    x = InputEvent.__getTimeMatrix__(('velocityGrMax',))
    w = InputEvent.__getTimeMatrix__(('gap_start',))

    return x - x.multiply(w)


def terminatedAtSpeedGrThanMax():
    x = InputEvent.__getTimeMatrix__(('velocityLeMax',))

    return x


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% rendezVous %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtRendezVous():

    x = InputEvent.__getTimeMatrix__(('stop_start',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))
    w = InputSDF.__getTimeMatrix__(('proximity', 'true'), 2)
    dim = declarations[('rendezVous', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    r1 = x - x.multiply(y)
    r1 = r1 - r1.multiply(z)
    r1a = sp.kron(ones, r1, format='csc')
    r1b = sp.kron(r1, ones, format='csc')
    r1 = r1a + r1b
    r1 = r1.multiply(w)

    x = InputEvent.__getTimeMatrix__(('slow_motion_start',))
    x = x - x.multiply(y)
    x1 = sp.kron(ones, x, format='csc')
    x2 = sp.kron(x, ones, format='csc')
    x = x1 + x2
    r2 = x.multiply(w)

    result = r1 + r2

    return result


def terminatedAtRendezVous():

    dim = declarations[('rendezVous', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    x = InputEvent.__getTimeMatrix__(('stop_end',))
    y = InputEvent.__getTimeMatrix__(('slow_motion_end',))

    x1 = sp.kron(ones, x, format='csc')
    x2 = sp.kron(x, ones, format='csc')

    y1 = sp.kron(ones, y, format='csc')
    y2 = sp.kron(y, ones, format='csc')

    result = x1 + x2 + y1 + y2

    return result


definitions = {('gap', 'nearPort'):

                   {'initiatedAt': initiatedAtGapNP, 'terminatedAt': terminatedAtGap},

               ('gap', 'farFromPorts'):

                   {'initiatedAt': initiatedAtGapFFP, 'terminatedAt': terminatedAtGap},

               ('stopped', 'nearPort'):

                   {'initiatedAt': initiatedAtStoppedNP, 'terminatedAt': terminatedAtStopped},

               ('stopped', 'farFromPorts'):

                   {'initiatedAt': initiatedAtStoppedFFP, 'terminatedAt': terminatedAtStopped},

               ('lowSpeed', 'true'):

                   {'initiatedAt': initiatedAtLowSpeed, 'terminatedAt': terminatedAtLowSpeed},

               ('withinArea', 'anchorage', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaAnchorage, 'terminatedAt': terminatedAtWithinAreaAnchorage},

               ('withinArea', 'fishing', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaFishing, 'terminatedAt': terminatedAtWithinAreaFishing},

               ('withinArea', 'natura', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNatura, 'terminatedAt': terminatedAtWithinAreaNatura},

               ('withinArea', 'nearCoast', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNearCoast, 'terminatedAt': terminatedAtWithinAreaNearCoast},

               ('withinArea', 'nearCoast5k', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNearCoast5k, 'terminatedAt': terminatedAtWithinAreaNearCoast5k},

               ('withinArea', 'nearPorts', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNearPorts, 'terminatedAt': terminatedAtWithinAreaNearPorts},

               ('underWay', 'true'):

                   {'initiatedAt': initiatedAtUnderWay, 'terminatedAt': terminatedAtUnderWay},

               ('adrift', 'true'):

                   {'initiatedAt': initiatedAtAdrift, 'terminatedAt': terminatedAtAdrift},

               ('anchor', 'nearPort'):

                   {'initiatedAt': initiatedAtAnchorNP, 'terminatedAt': terminatedAtAnchorNP},

               ('anchor', 'farFromPorts'):

                   {'initiatedAt': initiatedAtAnchorFFP, 'terminatedAt': terminatedAtAnchorFFP},

               ('beforeaground', 'nearPort'):

                   {'initiatedAt': initiatedAtBeforeAgroundNP, 'terminatedAt': terminatedAtBeforeAground},

               ('beforeaground', 'farFromPorts'):

                   {'initiatedAt': initiatedAtBeforeAgroundFFP, 'terminatedAt': terminatedAtBeforeAground},

               ('trawlSpeed', 'true'):

                   {'initiatedAt': initiatedAtTrawlSpeed, 'terminatedAt': terminatedAtTrawlSpeed},

               ('speedLessThanMin', 'true'):

                   {'initiatedAt': initiatedAtSpeedLessThanMin, 'terminatedAt': terminatedAtSpeedLessThanMin},

               ('speedGrThanMax', 'true'):

                   {'initiatedAt': initiatedAtSpeedGrThanMax, 'terminatedAt': terminatedAtSpeedGrThanMax},

               ('travelSpeed', 'true'):

                   {'initiatedAt': initiatedAtTravelSpeed, 'terminatedAt': terminatedAtTravelSpeed},

               ('rendezVous', 'true'):

                   {'initiatedAt': initiatedAtRendezVous, 'terminatedAt': terminatedAtRendezVous},

               }


def readDefinitions(patterns):
    cachingOrder = []
    tensors_dim = [1, 2]

    with open(patterns) as f:
        for line in f:
            if 'cachingOrder' in line:
                line = line.split(', ')[-1]
                ce = line.split('(')[0]
                val = line.split('=')[-1].split(')')[0]
                if (ce, val) in definitions:
                    cachingOrder.append((ce, val))
                elif ce == 'withinArea':
                    for area in ['anchorage', 'fishing', 'natura', 'nearCoast', 'nearCoast5k', 'nearPorts']:
                        cachingOrder.append((ce, area, val))

    return cachingOrder, definitions, tensors_dim
