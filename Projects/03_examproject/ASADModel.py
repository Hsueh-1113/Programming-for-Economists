import numpy as np
import matplotlib.pyplot as plt

class ASADModelClass:

    def __init__(self, par=None):
    
        par = dict(
            ybar    = 1.0,
            pi_star = 0.02,
            b       = 0.6,
            a1      = 1.5,
            a2      = 0.10,
            gamma   = 4.0,
            phi     = 0.6
        )

        self.par = par.copy()

    def _alpha_z(self, v):

        p = self.par

        alpha = p['b'] * p['a1'] / (1.0 + p['b'] * p['a2'])
        z = v / (1.0 + p['b'] * p['a2'])

        return alpha, z

    def AD_curve(self, y, v):

        p = self.par
        alpha, z = self._alpha_z(v)
        inv_alpha = 1.0 / alpha
        return p['pi_star'] - inv_alpha * ((y - p['ybar']) - z)

    def SRAS_curve(self, y, pi_e):
        
        p = self.par
        return pi_e + p['gamma'] * (y - p['ybar'])

    # analytical equilibrium y_t^*, pi_t^* given pi_e and v
    def equilibrium(self, pi_e, v):

        p = self.par
        alpha, z = self._alpha_z(v)
        inv_alpha = 1.0 / alpha
        y_star = p['ybar'] + (p['pi_star'] - pi_e + inv_alpha * z) / (inv_alpha + p['gamma'])
        pi_star = pi_e + p['gamma'] * (p['pi_star'] - pi_e + inv_alpha * z) / (inv_alpha + p['gamma'])
        return y_star, pi_star
    # simulation
    def simulate(self, rho, eps):
        p = self.par
        T = len(eps)
        
        y_star = np.empty(T)
        pi_star = np.empty(T)
        v = np.empty(T)
        pi_e = np.empty(T)
    
        # initial conditions
        pi_e[0] = p["pi_star"]
        v_lag = 0.0  # v_{-1} = 0

        for t in range(T):

            if t > 0:
                pi_e[t] = p["phi"] * pi_e[t-1] + (1 - p["phi"]) * pi_star[t-1]
            
            v[t] = rho * v_lag + eps[t]
            v_lag = v[t]

            # equilibrium given (pi_e[t], v[t])
            y_star[t], pi_star[t] = self.equilibrium(pi_e=pi_e[t], v=v[t])
        return y_star, pi_star, v, pi_e
    # compute sd(y_gap), sd(pi), corr(y_gap, pi)
    def moments(self, y, pi):
        sd_y = np.std(y)
        sd_pi = np.std(pi)
        corr = np.corrcoef(y, pi)[0, 1]
        return sd_y, sd_pi, corr
