from __future__ import division
from numpy import mean, zeros
from priors import include_prior, exclude_prior, \
                   def_priors, all_priors, inc_priors, exc_priors, acc_objpriors, acc_enspriors
from log import log as Log
from environment import env, Object, command

import glcmds
import funcs
import priors
from funcs import default_post_process

if 0:
    from solvers.lpsolve.samplex import Samplex
    import solvers.lpsolve.glcmds 
elif 0:
    from solvers.samplex.samplex import Samplex
    import solvers.samplex.glcmds 
else:
    from solvers.samplexsimple.samplex import Samplex
    import solvers.samplexsimple.glcmds 

if env().withgfx:
    import plots

def _expand_array(nvars, offs, f):
    """Returns a function that will properly prepare a constraint equation
       for the solver. The solver expects all equations to be of the same
       length and span the entire range of variables over all objects. We
       stack the input equations such that the first column of the input
       always goes in the first column for the solver but the rest is
       shifted to the right by offs, which places the input into a region
       of the solver matrix that is just for the same object."""
    def work(eq):
        new_eq = zeros(nvars+1, order='Fortran')
        new_eq[0] = eq[0]
        new_eq[offs+1:offs+len(eq)] = eq[1:]
        f(new_eq)

    return work

def init_model_generator(nmodels, regenerate=False):
    """Construct the linear constraint equations by applying all the
       enabled priors."""

    objs = env().objects

    # ------------- 

    nvars = reduce(lambda s,o: s+o.basis.nvar, objs, 0)
    Log( "Number of variables (nvars) = %i" % nvars )


    offs = 0
    for o in objs:
        o.basis.array_offset = 1+offs
        offs += o.basis.nvar 

    # ------------- 

    Log( '=' * 80 )
    Log( 'PIXEL BASIS MODEL GENERATOR' )
    Log( '=' * 80 )
    if nmodels == 0:
        Log( "No models requested." )
        return

    #---------------------------------------------------------------------------
    # Decide which priors to use. The initial list is the list of default
    # priors. The user can then modify this list be selecting which priors
    # should be included from the entire list, or which ones should be excluded.
    #
    #---------------------------------------------------------------------------
    priors = def_priors

    if exc_priors:
        priors = filter(lambda x: x not in exc_priors, priors)

    if inc_priors:
        priors += filter(lambda x: x not in priors, inc_priors)


    Log( 'Priors:' )
    for p in all_priors:
        Log( '    %s %s' % (p.f.__name__, '[EXCLUDED]' if p not in priors else '') )

    lp = filter(lambda x: x.where == 'object_prior',   priors)
    gp = filter(lambda x: x.where == 'ensemble_prior', priors)

    #---------------------------------------------------------------------------
    # Initialize our model generator, the simplex.
    #---------------------------------------------------------------------------
    opts = env().model_gen_options
    opts['ncols'] = nvars
    if not opts.has_key('nthreads'): opts['nthreads'] = env().ncpus

    #mg = env().model_gen = env().model_gen_factory(env().model_gen_options)
    mg = env().model_gen = Samplex(**env().model_gen_options)

    #---------------------------------------------------------------------------
    # Apply the object priors
    #---------------------------------------------------------------------------
    Log( 'Applying Priors:' )
    for o in objs:
        offs = o.basis.array_offset - 1
        Log( 'array offset %i' % offs )
        for p in lp:
            leq = _expand_array(nvars, offs, mg.leq)
            eq  = _expand_array(nvars, offs, mg.eq)
            geq = _expand_array(nvars, offs, mg.geq)
            p.f(o, leq, eq, geq)

    #---------------------------------------------------------------------------
    # Apply the ensemble priors
    #---------------------------------------------------------------------------
    for p in gp:
        p.f(objs, nvars, mg.leq, mg.eq, mg.geq)


    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------

    global acc_objpriors
    global acc_enspriors
    del acc_objpriors[:]
    del acc_enspriors[:]

    acc_objpriors += lp
    acc_enspriors += gp

def solution_to_dict(obj, sol):
    return obj.basis.solution_to_dict(sol)

def _model_dict(objs, sol):
    if isinstance(objs, Object):
        objs = [objs]

    print objs
    print sol
    return {'sol':      sol,
            'obj,data': zip(objs, map(lambda x: solution_to_dict(x, sol), objs)),
            'tagged':   False}


@command
def generate_models(objs, n, *args, **kwargs):

    if n <= 0: return

    mode = kwargs.get('mode', 'default')

    if mode == 'particles':
        assert n==1, 'Can only generate a single model in particles mode.'
        assert len(objs) == 1, 'Can only model a single object from particles.'
        data = kwargs.get('data', None)
        assert data is not None, 'data keyword must be given with model parameters.'
        objs[0].basis.array_offset = 1
        yield _projected_model(objs[0], *data)
    elif mode != 'default':
        assert False, 'Unsupported model mode "%s"' % mode
    else:

        init_model_generator(n)

        mg = env().model_gen
        
        mg.start()
        for sol in mg.next(n):
            for o in objs:
                for p in acc_objpriors:
                    if p.check: p.check(o, sol)
            for p in acc_enspriors:
                if p.check: p.check(objs, sol)

            yield {'sol':  sol,
                   'obj,data': zip(objs, map(lambda x: solution_to_dict(x, sol), objs)),
                   'tagged':  False}

    for o in objs:
        o.post_process_funcs.append([default_post_process, [], {}])

def regenerate_models(objs):

    assert env().solutions is not None

    init_model_generator(len(env().solutions))

    for sol in env().solutions:
        yield {'sol':  sol,
               'obj,data': zip(objs, map(lambda x: solution_to_dict(x, sol), objs)),
               'tagged':  False}

@command
def make_ensemble_average():
#   Log( "s*********" )
#   for m in env().models:
#       Log( m['sol'] )
#   Log( "s*********" )


    sol = mean([m['sol'] for m in env().models], axis=0)
    objs = env().objects
    env().ensemble_average = \
        {'sol'      : sol,
         'obj,data' : zip(objs, map(lambda x: solution_to_dict(x, sol), objs)),
         'tagged'   : False}

def _projected_model(obj, X,Y,M, src, H0inv):

    grid_mass = obj.basis.grid_mass(X,Y,M, H0inv)
    ps = obj.basis.solution_from_grid(grid_mass, src=src, H0inv=H0inv)
    return {'sol':      ps,
            'obj,data': [[obj,ps]],
            'tagged':   False}

