from __future__ import division
import math
from numpy import arctan2
from environment import env, Image, System
from shear import Shear
import cosmo
from handythread import parallel_map

def ptmass(xc, yc, mmin, mmax): assert False, "ptmass not implemented"
def redshifts(*args):           assert False, "redshifts not implemented"
def double(*args):              assert False, "double() not supported. Use source()."
def quad(*args):                assert False, "quad() not supported. Use source()."
def multi(*args):               assert False, "multi() not supported. Use source()."
def minsteep(a):                assert False, "minsteep not supported. Use steepness()."
def maxsteep(a):                assert False, "maxsteep not supported. Use steepness()."


def globject(name):
    return env.new_object(name)

def shear(phi):
    env.current_object().shear = Shear(phi)

def zlens(z):
    o = env.current_object()
    o.zlens = z
    o.scales = cosmo.scales(o.zlens, 0)

def cosm(om, ol):
    cosmo.omega_matter = om
    cosmo.omega_lambda = ol

#def lens(zsrc, img0, img0parity, *imgs):
#    print 'lens() is now deprecated. Use source() instead.'
#    source(zsrc, img0, img0parity, imgs)

def source(zsrc, img0=None, img0parity=None, *imgs):

    o = env.current_object()

    assert o.zlens is not None, "zlens() must first be specified."
    assert zsrc >= o.zlens, "Source is not behind lens."

    # XXX: this changes the scales for each lens with a different zsrc!!!
    #o.zlens, o.tscale, o.tscalebg, o.dlscale, o.cdscale = cosmo.scales(o.zlens,zsrc)
    sys = System(zsrc, o.zlens)

    if img0 is not None and img0parity is not None:
        image0 = Image(img0, img0parity)
        sys.add_image(image0)

        prev = image0
        for i in xrange(0, len(imgs), 3):
            img,parity,time_delay = imgs[i:i+3]
            if prev.parity_name == 'sad' and parity == 'max':
                prev.angle = arctan2(prev.pos.imag-img[1], 
                                     prev.pos.real-img[0]) * 180/math.pi
            image = Image(img, parity)
            sys.add_image(image)
            sys.add_time_delay(prev,image, time_delay)
            prev = image

    o.add_system(sys)
    return sys

def delay(A,B, delay):
    """ Add a time delay between images A and B such that B arrive delay days after A. """
    sys = env.current_object().current_system()
    a = sys.images[sys.images.index(A)]
    b = sys.images[sys.images.index(B)]
    sys.add_time_delay(a,b,delay)

def symm(v=False):
    """Turn lens symmetry on or off. Default is off."""
    assert False, "Symmetry not yet supported."
    env.current_object().symm = v

def dgcone(theta):
    assert (0 < theta <= 90), "dgcone: need 0 < theta <= 90"
    env.current_object().cen_ang = (90-theta) * math.pi/180

def steep(lb, ub):
    env.current_object().minsteep = lb
    env.current_object().maxsteep = ub

def g(h):
    env.h_spec = 1.0/h

def kann(theta):
    env.current_object().kann_spec = theta

def maprad(r):
    env.current_object().maprad = r

def clear():
    env.clear()

def postfilter(*fs):
    models = env.models
    if fs:
        for m in models: m['tagged'] = True
        for f in fs:     models = filter(f, models)
        #for f in fs:     models = filter(parallel_map(f, models, threads=env.ncpus))
        for m in models: m['tagged'] = False

    env.accepted_models = models

