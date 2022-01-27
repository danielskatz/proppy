# First, activate CRPropa environment and then run this current script

from crpropa_sim import *
import numpy as np
import time
from pathlib import Path


path_figs = 'uhecrs_4e27m/figures'
path_data = 'uhecrs_4e27m/data'
path_data_raw = 'uhecrs_4e27m/data/raw_data'
Path(path_figs).mkdir(parents=True, exist_ok=True)
Path(path_data).mkdir(parents=True, exist_ok=True)
Path(path_data_raw).mkdir(parents=True, exist_ok=True)
# save simulation result
path = 'uhecrs_4e27m/'

step_sizes = (np.logspace(20, 26, 19)[::-1])
df_sim_data = pd.DataFrame(columns=('step_size', 'time', 'kappa', 'kappa_err'))

kappa_theory = 1.08*10**33 # [m^2/s]
traj_max = 4e27 # [m]

simulation_setups = [
    {
        'prop_module': 'SDE',
        'turbulence_method': '',
        'nr_grid_points': 0,
        'nr_modes': 0
    },
    {
        'prop_module': 'BP',
        'turbulence_method': 'PW',
        'nr_grid_points': 0,
        'nr_modes': 1000
    },
    {
        'prop_module': 'CK',
        'turbulence_method': 'PW',
        'nr_grid_points': 0,
        'nr_modes': 1000
    },
    {
        'prop_module': 'BP',
        'turbulence_method': 'grid',
        'nr_grid_points': 1024,
        'nr_modes': 0,
    },
]

def simulate(simulation_setup):
    file_name_results = path + 'data/crp_sim_data_'+simulation_setup['prop_module']+'_'+simulation_setup['turbulence_method']+'.pkl'
    for i, step_size in enumerate(step_sizes):
        crp = CRPropa(step_size = step_size, traj_max = traj_max, nr_grid_points = simulation_setup['nr_grid_points'], n_wavemodes = simulation_setup['nr_modes'], l_min = 5*3*10**20, l_max = 5*3e22, energy=1e19, brms=10**(-9), path = path, prop_module = simulation_setup['prop_module'], kappa = kappa_theory, turbulence_method = simulation_setup['turbulence_method'])
        start_time = time.process_time()
        crp.sim()
        time_needed = time.process_time() - start_time
        
        kappa, kappa_err = crp.analyze(step_size)

        df_sim_data.loc[i] = [step_size, time_needed, kappa, kappa_err]
        df_sim_data.to_pickle(file_name_results) # save intermediate results
    
    print(df_sim_data)
 
for simulation_setup in simulation_setups:
    simulate(simulation_setup)