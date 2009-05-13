import  numpy 
from numpy import arctan2, pi, linspace, atleast_2d
from potential import poten2d

from solvers.samplex.samplex import Samplex as model_generator

class Object:

    def __init__(self, name):
        self.name = name
        self._current_system = None
        self.systems = []

        self.S          = 0
        self.shear      = None
        self.zlens      = 0
        self.tscale     = 0
        self.tscalebg   = 0
        self.dlscale    = 0
        self.cdscale    = 0
        self.kann_spec  = 0
        self.h_spec     = 0
        self.minsteep   = 0.5
        self.maxsteep   = self.minsteep
        self.cen_ang    = pi/4
        self.symm       = False

        self.maprad     = None

        self.basis = None

    def current_system(self):
        return self._current_system

    def add_system(self, system):
        self._current_system = system
        self.systems.append(system)

    def init(self):
        self.basis.init(self)
        subdivision = 5.

        r = self.maprad
        w = (2*r+1) / subdivision

        gx = linspace(-r,r, (2*r+1) * subdivision)
        gy = atleast_2d(linspace(-r,r, (2*r+1) * subdivision)).T

        self.lnr = poten2d(gx, gy, w)


class Image:
    def __init__(self, r, parity):
        assert parity in ['min', 'sad', 'max']

        self._pos = r;
        self.pos = complex(r[0], r[1])
        self.angle = arctan2(self.pos.imag, self.pos.real) * 180/pi
        #self.angle = numpy.angle(self.pos, deg=True)
        self.elongation = [0.1, 10, 0.9]
        self.parity = ['min', 'sad', 'max'].index(parity)

    def __eq__(self, a):
        return a is self or a is self._pos 
        

class System:
    def __init__(self, size):
        self.zcap = 1.0 # size
        self.images = []
        self.time_delays = []
        print "zcap =", self.zcap

    def add_image(self, A):
        assert A not in self.images
        self.images.append(A)

    def add_time_delay(self, A,B, delay):
        assert A in self.images
        assert B in self.images
        self.time_delays.append((A,B,delay))

class Environment:

    def __init__(self):
        self.objects = []
        self._current_object = None
        self.nmodels = 0
        self.model_gen_class = model_generator
        self.model_gen = None

    def current_object(self):
        return self._current_object

    def new_object(self, name):
        self._current_object = Object(name)
        self.objects.append(self._current_object)
        return self._current_object
        
env = Environment()

