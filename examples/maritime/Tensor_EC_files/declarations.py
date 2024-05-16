
from src.processEvents import InputEvent, ComplexEvent
from src.processSimpleFluents import SimpleFluent
from src.processSDFluents import InputSDF, ComplexSDF

declarations = {('coord',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGr2_7Lt48_6',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGr48_6',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityLt2_7',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityAngleGr15',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityAngleLe15',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityLt0_005',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGr0_005',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityLt0_2',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGr0_2',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGr1Lt9',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGr9',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityLt1',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGrMinLtMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGrMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityLtMin',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityGeMin',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocityLeMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_anchorage',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_fishing',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_natura',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_nearCoast',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_nearCoast5k',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_nearPorts',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_anchorage',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_fishing',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_natura',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_nearCoast',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_nearCoast5k',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_nearPorts',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('proximity',):

                    {'type': InputSDF, 'index': (5, 6), 'value': 4, 'interval': (2, 3), 'Ndim': 2},

                ('change_in_speed_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('change_in_speed_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('change_in_heading',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('stop_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('stop_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('slow_motion_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('slow_motion_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('gap_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('gap_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('gap', 'nearPort'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('gap', 'farFromPorts'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('stopped', 'nearPort'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('stopped', 'farFromPorts'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('lowSpeed', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'anchorage', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'fishing', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'natura', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'nearCoast', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'nearCoast5k', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'nearPorts', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('underWay', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('adrift', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('anchor', 'nearPort'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('anchor', 'farFromPorts'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('beforeaground', 'nearPort'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('beforeaground', 'farFromPorts'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('trawlSpeed', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('speedLessThanMin', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('speedGrThanMax', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('travelSpeed', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel',), 'Ndim': 1, 'library': 'scipy'},

                ('rendezVous', 'true'):

                    {'type': SimpleFluent, 'Ndim': 2, 'index': ('vesselPair',)},
                }
