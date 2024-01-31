import numpy as np
import scipy as sp
from scipy.stats import multivariate_normal, poisson


class ParticleField:
    """Simple particle field model with extent in xyz and concentration, samples are drawn from Poisson process
    
    Centroid and Extent are in units of km
    concentration is in units of #/ml/mm
    """
    def __init__(self, centroid, extent, concentration, nominal_size, spectral_slope):
        self.extent = np.array(extent)
        self.centroid = np.array(centroid)
        self.concentration = concentration
        self.nominal_szie = nominal_size
        self.spectral_slope = spectral_slope
        self.rv = multivariate_normal(mean=self.centroid, cov=self.extent**2)
        self.norm = 1/self.rv.pdf(self.centroid)
        self.latest_concentration = 0.0 # assumption we start far from patch
        
    def sample(self, location, imaged_volume, particle_size, spectral_slope):
        
        # Compute concentration at location
        self.latest_concentration = self.norm * self.rv.pdf(location)
        
        # map concentration at nominal size to concentration at actual size
        effective_concentration = self.latest_concentration * particle_size ** spectral_slope * imaged_volume
        
        #if effective_concentration < 1:
        #    logger.warning('Effective concentration in imaged volume is less than 1')
        
        particle_counts =  poisson.rvs(effective_concentration)
        
        return particle_counts
        