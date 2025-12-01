import numpy as np
from isca import Experiment, DryCodeBase, GFDL_BASE, DiagTable, Namelist
from isca.util import exp_progress

NCORES = 32
RESOLUTION = 'T42', 25  # T42 horizontal resolution, 25 levels in pressure

# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = DryCodeBase.from_directory(GFDL_BASE)

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

    # configure the relaxation profile (PK setup built on HS troposphere)
    'hs_forcing_nml': {
        'equilibrium_t_option': 'Polvani_Kushner',
        'p_trop': 1.0e4,                  # 100 hPa tropopause
        'pk_gamma': 4.0e-3,               # 4 K/km in K/m
        'pk_theta0': np.deg2rad(50.),     # transition latitude
        'pk_dtheta': np.deg2rad(10.),     # transition width
        'pk_hfac': 1.0,                   # +1 NH winter, -1 SH winter
        't_zero': 315.,
        't_strat': 200.,
        'delh': 60.,
        'delv': 10.,
        'eps': 0.,
        'sigma_b': 0.7,
        'ka':   -40.,
        'ks':   -4.,
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


if __name__ == "__main__":
    earth_omega = 7.292e-5

    exp_name = 'polvani_kushner_default'
    omega = earth_omega 

    exp = Experiment(exp_name, codebase=cb)
    exp.set_resolution(*RESOLUTION)

    exp.namelist = namelist
    exp.diag_table = diag
    exp.update_namelist({"constants_nml": {"omega": omega}})


    # Month 1 (fresh start for each experiment)
    with exp_progress(exp):
        exp.run(1, use_restart=False, num_cores=NCORES)

    # Months 2–10
    for n in range(2, 13):
        with exp_progress(exp, description=f"month {n}"):
            exp.run(n, num_cores=NCORES) # use the restart i-1 by default
            exp.delete_restart(n - 1)  # keep space usage sane


