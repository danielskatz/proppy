import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

class Comparison():

    def __init__(self, kappa_theory, lambda_theory, step_sizes, l_c, r_g, path_data, path_figs):
        self.kappa_theory = kappa_theory
        self.lambda_theory = lambda_theory
        self.step_sizes = step_sizes
        self.l_c = l_c
        self.r_g = r_g
        self.path_data = path_data
        self.path_figs = path_figs
        self.load_sim_data()

    def load_sim_data(self):
        try:
            self.df_rwp_results = pd.read_pickle(self.path_data+'/rwp_sim_data.pkl')
        except:
            print("couldn't loade rpw data")
        try:
            self.df_crp_ck_results = pd.read_pickle(self.path_data+'/crp_sim_data_CK.pkl')
        except:
            print("couldn't loade CK data")
        try:
            self.df_crp_bp_results = pd.read_pickle(self.path_data+'/crp_sim_data_BP.pkl')
        except:
            print("couldn't loade BP data")
        try:
            self.df_crp_sde_results = pd.read_pickle(self.path_data+'/crp_sim_data_SDE.pkl')
        except:
            print("couldn't loade SDE data")

        try:
            self.rwp_times = np.array(self.df_rwp_results['time'].values.tolist())
            self.rwp_step_sizes = self.df_rwp_results['step_size']
            self.rwp_kappas = self.df_rwp_results['kappa']
        except:
            print('no rwp data')
            self.rwp_times = np.array([])
            self.rwp_step_sizes = np.array([])
            self.rwp_kappas = np.array([])
        try:
            self.ck_times = np.array(self.df_crp_ck_results['time'].values.tolist())
            self.ck_step_sizes = self.df_crp_ck_results['step_size']
            self.ck_kappas = self.df_crp_ck_results['kappa']
        except:
            print('no ck data')
            self.ck_times = np.array([])
            self.ck_step_sizes = np.array([])
            self.ck_kappas = np.array([])
        try:
            self.bp_times = np.array(self.df_crp_bp_results['time'].values.tolist())
            self.bp_step_sizes = self.df_crp_bp_results['step_size']
            self.bp_kappas = self.df_crp_bp_results['kappa']
        except:
            print('no bp data')
            self.bp_times = np.array([])
            self.bp_step_sizes = np.array([])
            self.bp_kappas = np.array([])
        try:
            self.sde_times = np.array(self.df_crp_sde_results['time'].values.tolist())
            self.sde_step_sizes = self.df_crp_sde_results['step_size']
            self.sde_kappas = self.df_crp_sde_results['kappa']
        except:
            print('no SDE data')
            self.sde_times = np.array([])
            self.sde_step_sizes = np.array([])
            self.sde_kappas = np.array([])

    def plot_running_diffusion_coefficients(self):
        fig, ax1 = plt.subplots(figsize=(5,3.5))

        plt.plot([1e17, 4e17], [self.kappa_theory*10**4,self.kappa_theory*10**4], color='k', linestyle=(0, (3, 1, 1, 1)), label='theory', zorder=-1)
        plt.axvline(x=self.lambda_theory, color='k', linestyle='--', label='$\lambda_\mathrm{theory}$', zorder=-1)
        steps_rwp = []
        steps_ck = []
        steps_bp = []
        steps_sde = []
        kappas_rwp = []
        kappas_ck = []
        kappas_bp = []
        kappas_sde = []

        for i, step_size in enumerate(self.step_sizes):
            color = plt.cm.viridis(np.linspace(0, 1, len(self.step_sizes))[i])
            n_max = -1
            try:
                rwp_l = np.load(self.path_data+'/sim_result_rwp_'+str(step_size/10**11)+'_l.npy')
                rwp_kappa = np.load(self.path_data+'/sim_result_rwp_'+str(step_size/10**11)+'_kappa.npy')
                ax1.plot(rwp_l[:n_max], np.array(rwp_kappa[:n_max])*10**4, color='red', ls='-', zorder=2, lw=2) 
                steps_rwp.append(step_size)
                kappas_rwp.append(np.mean(rwp_kappa[-10:]))
            except:
                print('no data for RPW')
            
            try:
                crp_l = np.load(self.path_data+'/sim_result_crp_BP_stepsize_'+str(step_size/10**11)+'_l.npy')
                crp_kappa = np.load(self.path_data+'/sim_result_crp_BP_stepsize_'+str(step_size/10**11)+'_kappa.npy')
                ax1.plot(crp_l[:n_max], np.array(crp_kappa[:n_max])*10**4, color=color, ls=(0, (1, 1)), lw=2, zorder=4)
                steps_bp.append(step_size)
                kappas_bp.append(np.mean(crp_kappa[-10:]))
            except:
                print('no data for BP')
            
            try:
                crp_l = np.load(self.path_data+'/sim_result_crp_CK_stepsize_'+str(step_size/10**11)+'_l.npy')
                crp_kappa = np.load(self.path_data+'/sim_result_crp_CK_stepsize_'+str(step_size/10**11)+'_kappa.npy')
                ax1.plot(crp_l[:n_max], np.array(crp_kappa[:n_max])*10**4, color=color, ls='-.', lw=2, zorder=4)
                steps_ck.append(step_size)
                kappas_ck.append(np.mean(crp_kappa[-10:]))
            except:
                print('no data for CK')

            try:
                crp_l = np.load(self.path_data+'/sim_result_crp_SDE_stepsize_'+str(step_size/10**11)+'_l.npy')
                crp_kappa = np.load(self.path_data+'/sim_result_crp_SDE_stepsize_'+str(step_size/10**11)+'_kappa.npy')
                ax1.plot(crp_l[:n_max], np.array(crp_kappa[:n_max])*10**4, color=color, ls='--', lw=2, zorder=4)
                steps_sde.append(step_size)
                kappas_sde.append(np.mean(crp_kappa[-10:]))
            except:
                print('no data for SDE')

        # colorbar
        plt.scatter(np.zeros(len(self.step_sizes)), np.zeros(len(self.step_sizes)), c=self.step_sizes, cmap='viridis', norm=matplotlib.colors.LogNorm())
        plt.colorbar(label='step sizes [m]')

        #legend
        plt.plot([0,0], [0,0], c='grey', ls=':', label='CRPropa (BP)', lw=2)
        plt.plot([0,0], [0,0], c='grey', ls='-.', label='CRPropa (CK)', lw=2)
        plt.plot([0,0], [0,0], c='grey', ls='--', label='CRPropa (SDE)', lw=2)
        plt.plot([0,0], [0,0], c='red', ls='-', label='RWPropa', lw=2)

        plt.xlim([min(self.step_sizes)/3, 4e17])

        ax1.set_xlabel('trajectory length [m]')
        ax1.loglog()
        ax1.set_ylabel('running $\kappa$ [cm$^2$/s]')
        plt.legend()
        plt.savefig(self.path_figs+'/running_kappa.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()

        fig, ax1 = plt.subplots(figsize=(5,3.5))
        plt.scatter(steps_rwp, kappas_rwp, label='RWPropa', marker='s', color='green')
        plt.scatter(steps_ck, kappas_ck, label='CRPropa (CK)', color='r')
        plt.scatter(steps_bp, kappas_bp, label='CRPropa (BP)', marker='d', color='k')
        plt.scatter(steps_sde, kappas_sde, label='CRPropa (SDE)', marker='^', color='blue')
        plt.axvline(x=self.l_c, label='$l_\mathrm{c}$', color='grey', ls=':')
        plt.axvline(x=self.r_g*2*3.14, label='$2\pi\, r_\mathrm{g}$', color='grey', ls='--')
        plt.axvline(x=self.kappa_theory*3/(3*10**8), label='$\lambda_\mathrm{theory}$', color='grey', ls='-.')
        plt.axhline(y=self.kappa_theory, color='grey', linestyle='-', label='theory')
        plt.legend()
        plt.loglog()
        plt.show()


    def plot_kappa_convergence_tests(self):
        fig = plt.figure(figsize=(5,3.5))
        ### try to load data and handle if data is not available
        
        zs = np.concatenate([self.rwp_times, self.ck_times, self.bp_times, self.sde_times], axis=0)
        min_, max_ = zs.min(), zs.max()
        plt.scatter(self.rwp_step_sizes, self.rwp_kappas, c=self.rwp_times, cmap='viridis', norm=matplotlib.colors.LogNorm(), marker='s')
        plt.clim(min_, max_)
        plt.scatter(self.ck_step_sizes, self.ck_kappas, c=self.ck_times, cmap='viridis', norm=matplotlib.colors.LogNorm())
        plt.clim(min_, max_)
        plt.scatter(self.bp_step_sizes, self.bp_kappas, c=self.bp_times, cmap='viridis', norm=matplotlib.colors.LogNorm(), marker='d')
        plt.clim(min_, max_)
        plt.scatter(self.sde_step_sizes, self.sde_kappas, c=self.sde_times, cmap='viridis', norm=matplotlib.colors.LogNorm(), marker='^')
        plt.clim(min_, max_)
        plt.colorbar(label='simulation time [s]')
        plt.loglog()
        plt.axvline(x=self.l_c, label='$l_\mathrm{c}$', color='grey', ls=':')
        plt.axvline(x=self.r_g*2*3.14, label='$2\pi\, r_\mathrm{g}$', color='grey', ls='--')
        plt.axhline(y=self.kappa_theory, color='grey', linestyle='-', label='theory')

        # legend
        plt.scatter([0],[0], label='RWPropa', marker='s', color='grey')
        plt.scatter([0],[0], label='CRPropa (CK)', color='grey')
        plt.scatter([0],[0], label='CRPropa (BP)', marker='d', color='grey')
        plt.scatter([0],[0], label='CRPropa (SDE)', marker='^', color='grey')

        plt.xlabel('step size [m]')
        plt.ylabel('$\kappa$ [m$^2$/s]')
        plt.legend()
        plt.savefig(self.path_figs+'/kappa_vs_stepsize.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()


    def plot_kappa_vs_time_steps(self):
        fig = plt.figure(figsize=(5,3.5))
        zs = np.concatenate([self.rwp_step_sizes, self.ck_step_sizes, self.bp_step_sizes, self.sde_step_sizes], axis=0)
        min_, max_ = zs.min(), zs.max()
        plt.scatter(self.rwp_times, self.rwp_kappas, c=self.rwp_step_sizes, cmap='viridis', norm=matplotlib.colors.LogNorm(), marker='s')
        plt.clim(min_, max_)
        plt.scatter(self.ck_times, self.ck_kappas, c=self.ck_step_sizes, cmap='viridis', norm=matplotlib.colors.LogNorm())
        plt.clim(min_, max_)
        plt.scatter(self.bp_times, self.bp_kappas, c=self.bp_step_sizes, cmap='viridis', norm=matplotlib.colors.LogNorm(), marker='d')
        plt.clim(min_, max_)
        plt.scatter(self.sde_times, self.sde_kappas, c=self.sde_step_sizes, cmap='viridis', norm=matplotlib.colors.LogNorm(), marker='^')
        plt.clim(min_, max_)
        plt.colorbar(label='step size [s]')
        plt.loglog()
        plt.axhline(y=self.kappa_theory, color='grey', linestyle='-', label='theory')

        # legend
        plt.scatter([0],[0], label='RWPropa', marker='s', color='grey')
        plt.scatter([0],[0], label='CRPropa (CK)', color='grey')
        plt.scatter([0],[0], label='CRPropa (BP)', marker='d', color='grey')
        plt.scatter([0],[0], label='CRPropa (SDE)', marker='^', color='grey')

        plt.xlabel('simulation time [s]')
        plt.ylabel('$\kappa$ [m$^2$/s]')
        plt.legend(loc = 'center left')
        plt.savefig(self.path_figs+'/kappa_vs_time_steps.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()


    def plot_kappa_vs_time_deviation(self):
        fig = plt.figure(figsize=(5,3.5))
        err_rwp = np.abs(np.log10(self.rwp_kappas)-np.log10(self.kappa_theory))
        err_crp_ck = np.abs(np.log10(self.ck_kappas)-np.log10(self.kappa_theory))
        err_crp_bp = np.abs(np.log10(self.bp_kappas)-np.log10(self.kappa_theory))
        err_crp_sde = np.abs(np.log10(self.sde_kappas)-np.log10(self.kappa_theory))
        zs = np.concatenate([err_rwp, err_crp_ck, err_crp_bp, err_crp_sde], axis=0)
        min_, max_ = zs.min(), zs.max()
        plt.scatter(self.rwp_times, self.rwp_kappas, c=err_rwp, cmap='viridis', marker='s')
        plt.clim(min_, max_)
        plt.scatter(self.ck_times, self.ck_kappas, c=err_crp_ck, cmap='viridis')
        plt.clim(min_, max_)
        plt.scatter(self.bp_times, self.bp_kappas, c=err_crp_bp, cmap='viridis', marker='d')
        plt.clim(min_, max_)
        plt.scatter(self.sde_times, self.sde_kappas, c=err_crp_sde, cmap='viridis', marker='^')
        plt.clim(min_, max_)
        plt.colorbar(label='deviation = |log($\kappa_\mathrm{sim}$) / log($\kappa_\mathrm{theory}$)|')
        plt.loglog()
        plt.axhline(y=self.kappa_theory, color='k', linestyle='-', label='theory')

        # legend
        plt.scatter([0],[0], label='RWPropa', marker='s', color='grey')
        plt.scatter([0],[0], label='CRPropa (CK)', color='grey')
        plt.scatter([0],[0], label='CRPropa (BP)', marker='d', color='grey')
        plt.scatter([0],[0], label='CRPropa (SDE)', marker='^', color='grey')

        plt.xlabel('simulation time [s]')
        plt.ylabel('$\kappa$ [m$^2$/s]')
        plt.legend(loc='center left')
        plt.savefig(self.path_figs+'/kappa_vs_time_deviation.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()


    def plot_deviation_vs_time_steps(self):
        fig = plt.figure(figsize=(5,3.5))
        plt.axhline(y=0, color='k', linestyle='-', zorder=-1, label='theory')
        plt.axvline(x=1, color='grey', linestyle=(0, (5, 0.4)), zorder=-1, label='1 sec')
        plt.axvline(x=60, color='grey', linestyle=(0, (5, 2.5)), zorder=-1, label='1 min')
        plt.axvline(x=60*60, color='grey', linestyle=(0, (5, 7)), zorder=-1, label='1 hour')
        plt.axvline(x=60*60*24, color='grey', linestyle=(0, (5, 13)), zorder=-1, label='1 day')
    
        err_rwp = np.abs(np.log10(self.rwp_kappas)-np.log10(self.kappa_theory))
        err_crp_ck = np.abs(np.log10(self.ck_kappas)-np.log10(self.kappa_theory))
        err_crp_bp = np.abs(np.log10(self.bp_kappas)-np.log10(self.kappa_theory))
        err_crp_sde = np.abs(np.log10(self.sde_kappas)-np.log10(self.kappa_theory)) 
        zs = np.concatenate([self.rwp_step_sizes, self.ck_step_sizes, self.bp_step_sizes, self.sde_step_sizes], axis=0)
        min_, max_ = zs.min(), zs.max()
        plt.scatter(self.rwp_times, err_rwp, c=self.rwp_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis', marker='s')
        plt.clim(min_, max_)
        plt.scatter(self.ck_times, err_crp_ck, c=self.ck_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis')
        plt.clim(min_, max_)
        plt.scatter(self.bp_times, err_crp_bp, c=self.bp_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis', marker='d')
        plt.clim(min_, max_)
        plt.scatter(self.sde_times, err_crp_sde, c=self.sde_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis', marker='^')
        plt.clim(min_, max_)
        plt.colorbar(label='step size [m]')
        plt.xscale('log')

        # legend
        plt.scatter([0],[0], label='RWPropa', marker='s', color='grey')
        plt.scatter([0],[0], label='CRPropa (CK)', color='grey')
        plt.scatter([0],[0], label='CRPropa (BP)', marker='d', color='grey')
        plt.scatter([0],[0], label='CRPropa (SDE)', marker='^', color='grey')

        plt.xlabel('simulation time [s]')
        plt.ylabel('deviation = |log($\kappa_\mathrm{sim}$) / log($\kappa_\mathrm{theory}$)|')
        plt.legend(loc='upper right')
        plt.savefig(self.path_figs+'/deviation_vs_time_steps.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()

    
    def plot_time_vs_deviation_steps(self):
        fig = plt.figure(figsize=(5,3.5))

        plt.axvline(x=0, color='k', linestyle='-', zorder=-1, label='theory')
        plt.axhline(y=1, color='grey', linestyle=(0, (5, 0.4)), zorder=-1, label='1 sec')
        plt.axhline(y=60, color='grey', linestyle=(0, (5, 2.5)), zorder=-1, label='1 min')
        plt.axhline(y=60*60, color='grey', linestyle=(0, (5, 7)), zorder=-1, label='1 hour')
        plt.axhline(y=60*60*24, color='grey', linestyle=(0, (5, 13)), zorder=-1, label='1 day')

        err_rwp = np.abs(np.log10(self.rwp_kappas)-np.log10(self.kappa_theory))
        err_crp_ck = np.abs(np.log10(self.ck_kappas)-np.log10(self.kappa_theory))
        err_crp_bp = np.abs(np.log10(self.bp_kappas)-np.log10(self.kappa_theory))
        err_crp_sde = np.abs(np.log10(self.sde_kappas)-np.log10(self.kappa_theory)) 
        zs = np.concatenate([self.rwp_step_sizes, self.ck_step_sizes, self.bp_step_sizes, self.sde_step_sizes], axis=0)
        min_, max_ = zs.min(), zs.max()
        plt.scatter(err_rwp, self.rwp_times, c=self.rwp_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis', marker='s')
        plt.clim(min_, max_)
        plt.scatter(err_crp_ck, self.ck_times, c=self.ck_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis')
        plt.clim(min_, max_)
        plt.scatter(err_crp_bp, self.bp_times, c=self.bp_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis', marker='d')
        plt.clim(min_, max_)
        plt.scatter(err_crp_sde, self.sde_times, c=self.sde_step_sizes, norm=matplotlib.colors.LogNorm(), cmap='viridis', marker='^')
        plt.clim(min_, max_)
        plt.colorbar(label='step size [m]')
        plt.yscale('log')

        # legend
        plt.scatter([0],[0], label='RWPropa', marker='s', color='grey')
        plt.scatter([0],[0], label='CRPropa (CK)', color='grey')
        plt.scatter([0],[0], label='CRPropa (BP)', marker='d', color='grey')

        plt.ylabel('simulation time [s]')
        plt.xlabel('deviation = |log($\kappa_\mathrm{sim}$) / log($\kappa_\mathrm{theory}$)|')
        plt.legend(loc='upper right', ncol=2)
        plt.savefig(self.path_figs+'/time_vs_deviation_steps.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()