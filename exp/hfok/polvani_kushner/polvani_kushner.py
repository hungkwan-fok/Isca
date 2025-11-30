import numpy as np

from isca import DryCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

NCORES = 32
RESOLUTION = 'T42', 25  # T42 horizontal resolution, 25 levels in pressure

# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = DryCodeBase.from_directory(GFDL_BASE)

# or it can point to a specific git repo and commit id.
# This method should ensure future, independent, reproducibility of results.
# cb = DryCodeBase.from_repo(repo='https://github.com/isca/isca', commit='isca1.1')

# compilation depends on computer specific settings.  The $GFDL_ENV
# environment variable is used to determine which `$GFDL_BASE/src/extra/env` file
# is used to load the correct compilers.  The env file is always loaded from
# $GFDL_BASE and not the checked out git repo.

# create an Experiment object to handle the configuration of model parameters
# and output diagnostics

exp_name = 'polvani_kushner'
exp = Experiment(exp_name, codebase=cb)

#Tell model how to write diagnostics
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True)
diag.add_field('dynamics', 'div', time_avg=True)

exp.diag_table = diag

# define namelist values as python dictionary
# wrapped as a namelist object.
namelist = Namelist({
    'main_nml': {
        'dt_atmos': 600, # second
        'days': 30,
        'calendar': 'thirty_day',
        'current_date': [2000,1,1,0,0,0]
    },

    'atmosphere_nml': {
        'idealized_moist_model': False  # False for Newtonian Cooling.  True for Isca/Frierson
    },

    'spectral_dynamics_nml': {
        'damping_order'           : 4,                      # default: 2
        'water_correction_limit'  : 200.e2,                 # default: 0
        'reference_sea_level_press': 1.0e5,                  # default: 101325
        'valid_range_t'           : [100., 800.],           # default: (100, 500)
        'initial_sphum'           : 0.0,                  # default: 0
        'vert_coord_option'       : 'uneven_sigma',         # default: 'even_sigma'
        'scale_heights': 6.0,
        'exponent': 7.5,
        'surf_res': 0.5
    },

    # configure the relaxation profile
    'hs_forcing_nml': {
        'equilibrium_t_option': 'Held_Suarez_PK09',
        'pk_deltaT': 30.,      # K cooling amplitude
        'pk_sigma0': 0.1,      # transition sigma
        'pk_lat_pow': 4.,      # lat sharpness
        'pk_sigma_pow': 2.,    # vertical sharpness

        't_zero': 315.,
        't_strat': 200.,
        'delh': 60.,
        'delv': 10.,
        'eps': 0.,
        'sigma_b': 0.7,
        'ka':   -40.,
        'ks':   -40.,          # lengthen stratospheric damping vs default -4
        'kf':   -1.,
        'do_conserve_energy': True,
    },


    'diag_manager_nml': {
        'mix_snapshot_average_fields': False
    },

    'fms_nml': {
        'domains_stack_size': 600000                        # default: 0
    },

    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    }
})

exp.namelist = namelist
exp.set_resolution(*RESOLUTION)

#Lets do a run!
if __name__ == '__main__':
    
    cb.compile()  # compile the source code to working directory $GFDL_WORK/codebase

    exp.run(1, num_cores=NCORES, use_restart=False)
    for i in range(2, 13):
        exp.run(i, num_cores=NCORES)  # use the restart i-1 by default