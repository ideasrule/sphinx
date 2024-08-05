import numpy as np
import scipy.interpolate
import os

class SphinxInterpolator:
    def __init__(self, output_path='./', input_path='./sphinx_models'):

        assert os.path.exists(input_path) 

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        self.input_path = input_path
        self.output_path = output_path

        self.Teff_grid = np.linspace(2000, 4000, 21)
        self.logg_grid = np.linspace(4, 5.5, 7)
        self.logZ_grid = np.linspace(-1, 1, 9)
        self.CtoO_grid = [0.3, 0.5, 0.7, 0.9]

        self.logg_label_grid = ['4.0', '4.25', '4.5', '4.75', '5.0', '5.25', '5.5']
        self.logZ_label_grid = ['-1.0', '-0.75', '-0.5', '-0.25', '+0.0', '+0.25', '+0.5', '+0.75', '+1.0']  # dumb hack


        self.wav, _ = np.loadtxt(os.path.join(self.input_path, 'SPECTRA/Teff_2000.0_logg_4.0_logZ_+0.0_CtoO_0.3_spectra.txt'), unpack=True,)

        self.flux_grid = np.zeros([len(self.Teff_grid), len(self.logg_grid), len(self.logZ_grid), len(self.CtoO_grid), len(self.wav)])

        for it,t in enumerate(self.Teff_grid):
            for ig,g in enumerate(self.logg_grid):
                for iz,z in enumerate(self.logZ_grid):
                    for ic,c in enumerate(self.CtoO_grid):
                        _, flux = np.loadtxt(os.path.join(self.input_path, 'SPECTRA/Teff_%4.1f_logg_%s_logZ_%s_CtoO_%1.1f_spectra.txt'%(t,self.logg_label_grid[ig],self.logZ_label_grid[iz],c)),
                                             unpack=True,)
                        self.flux_grid[it, ig, iz, ic, :] = flux

    def get_interpolated_flux(self, Teff, logg, logZ, CtoO=0.53, method='linear'):
        flux_interpolated = scipy.interpolate.interpn((self.Teff_grid, self.logg_grid, self.logZ_grid, self.CtoO_grid), self.flux_grid, [Teff, logg, logZ, CtoO], method=method)
        return flux_interpolated[0,:]

    def save_interpolated_flux(self, Teff, logg, logZ, CtoO=0.53, method='linear', filename='star', plot=False):
        print("Saving to", os.path.join(self.output_path, '%s.txt'%filename))
        flux_interpolated = self.get_interpolated_flux(Teff, logg, logZ, CtoO, method)

        if plot:
            import matplotlib.pyplot as plt
            plt.plot(self.wav, flux_interpolated, lw=0.8)
            plt.xlabel('Wavelength')
            plt.ylabel('Flux')
            plt.xscale('log')
            plt.yscale('log')
            plt.show()

        np.savetxt(os.path.join(self.output_path, '%s.txt'%filename),
                    np.array([self.wav, flux_interpolated]).T,       
                    header='# Wavelength (micrometer), Flux (W / m2 / m)')
        return

if __name__=='__main__':

    si = SphinxInterpolator(input_path='sphinx_models/')

    # si.save_interpolated_flux(2566, 5.2396, 0.04, 0.5, filename='trappist1')
    si.save_interpolated_flux(3291, 4.82, -0.15, 0.5, filename='sphinx_spectrum')
    #si.save_interpolated_flux(3340 - 150, 5.0, -0.34, 0.5, filename='ltt1445A_sphinx_cold_spectrum')
    #si.save_interpolated_flux(3522, 4.776, -0.01, 0.5, filename='gj367_sphinx_spectrum')
