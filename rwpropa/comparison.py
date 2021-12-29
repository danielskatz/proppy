import numpy as np
import matplotlib.pyplot as plt
import matplotlib

class Comparison():

    def __init__(self, kappa_theory, lambda_theory, step_sizes, path_data, path_figs):
        self.kappa_theory = kappa_theory
        self.lambda_theory = lambda_theory
        self.step_sizes = step_sizes
        self.path_data = path_data
        self.path_figs = path_figs

    def running_diffusion_coefficients(self):
        fig, ax1 = plt.subplots(figsize=(5,3.5))

        plt.plot([1e17, 4e17], [self.kappa_theory*10**4,self.kappa_theory*10**4], color='k', linestyle=(0, (3, 1, 1, 1)), label='theory', zorder=-1)
        plt.axvline(x=self.lambda_theory, color='k', linestyle='--', label='$\lambda_\mathrm{theory}$', zorder=-1)

        for i, step_size in enumerate(self.step_sizes):
            color = plt.cm.viridis(np.linspace(0, 1, len(self.step_sizes))[i])
            n_max = -1
            try:
                rwp_l = np.load(self.path_data+'/sim_result_rwp_'+str(step_size/10**11)+'_l.npy')
                rwp_kappa = np.load(self.path_data+'/sim_result_rwp_'+str(step_size/10**11)+'_kappa.npy')
                ax1.plot(rwp_l[:n_max], np.array(rwp_kappa[:n_max])*10**4, color='red', ls='-', zorder=2, lw=2) 
            except:
                print('no data')
            
            try:
                crp_l = np.load(self.path_data+'/sim_result_crp_'+str(step_size/10**11)+'_l.npy')
                crp_kappa = np.load(self.path_data+'/sim_result_crp_'+str(step_size/10**11)+'_kappa.npy')
                ax1.plot(crp_l[:n_max], np.array(crp_kappa[:n_max])*10**4, color=color, ls=(0, (1, 1)), lw=2, zorder=4)
            except:
                print('no data')

        # colorbar
        plt.scatter(np.zeros(len(self.step_sizes)), np.zeros(len(self.step_sizes)), c=self.step_sizes, cmap='viridis', norm=matplotlib.colors.LogNorm())
        plt.colorbar(label='step sizes [m]')

        #legend
        plt.plot([0,0], [0,0], c='grey', ls=':', label='CRPropa (cc)', lw=2)
        plt.plot([0,0], [0,0], c='red', ls='-', label='RWPropa', lw=2)

        plt.xlim([min(self.step_sizes)/3, 4e17])

        ax1.set_xlabel('trajectory length [m]')
        ax1.loglog()
        ax1.set_ylabel('running $\kappa$ [cm$^2$/s]')
        plt.legend()
        plt.savefig(self.path_figs+'/running_kappa.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.show()