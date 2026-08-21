from types import SimpleNamespace
from Worker import Workerclass
import numpy as np
from scipy.optimize import minimize

class Governmentclass(Workerclass):

    def __init__(self,par=None):

        self.par = SimpleNamespace()
        self.sol = SimpleNamespace()
        
        # a. default setup
        self.setup_worker()
        self.setup_government()

        # b. update parameters
        if not par is None: 
            for k,v in par.items():
                self.par.__dict__[k] = v

        # c. random number generator
        self.rng = np.random.default_rng(12345)#our model depends on random productivity draws.by setting a seed (12345), we ensure the same productivities appear every run.

    def setup_government(self):

        par = self.par

        # a. workers
        par.N = 100  # number of workers
        par.sigma_p = 0.3  # std dev of productivity
        par.sigma_nu = 0.5  # std dev of preference
        # b. pulic good
        par.chi = 50.0 # weight on public good in SWF
        par.eta = 0.1 # curvature of public good in SWF

    def draw_productivities(self):

        par = self.par
        sol = self.sol

   # Draw log-normal productivity shocks from equation 6
        par = self.par
        mu = -0.5*par.sigma_p**2
        self.sol.p = self.rng.lognormal(mean=mu, sigma=par.sigma_p, size=par.N)

    def draw_preferences(self):

        par = self.par
        sol = self.sol
        mu_p = -0.5*par.sigma_p**2
        sol.p = self.rng.lognormal(mean=mu_p, sigma=par.sigma_p, size=par.N)
        mu_nu = np.log(par.nu) - 0.5*par.sigma_nu**2
        sol.nu = self.rng.lognormal(mean=mu_nu, sigma=par.sigma_nu, size=par.N)

    def solve_workers(self):
        par = self.par
        sol = self.sol

        if not hasattr(sol,'p'):
            self.draw_productivities()

        N = par.N
        ps = sol.p

        sol.ell = np.zeros(N)
        sol.c   = np.zeros(N)
        sol.U   = np.zeros(N)

        for i in range(N):
            p_i = ps[i]
            opt_i = self.optimal_choice(p_i)
            sol.ell[i] = opt_i.ell
            sol.c[i]   = opt_i.c
            sol.U[i]   = opt_i.U
   
    def solve_workers_preference(self):
        par = self.par
        sol = self.sol

        if not hasattr(sol,'p') or not hasattr(sol,'nu'):
            self.draw_preferences()   # draw both p and nu

        N  = par.N
        ps = sol.p
        nus = sol.nu

        sol.ell = np.zeros(N)
        sol.c   = np.zeros(N)
        sol.U   = np.zeros(N)

        for i in range(N):
            p_i  = ps[i]
            nu_i = nus[i]

            # temporarily set individual nu
            old_nu   = par.nu
            par.nu   = nu_i

            opt_i = self.optimal_choice(p_i)  # use the original individual problem solver

            # revert to the original average nu to avoid affecting other parts
            par.nu   = old_nu

            sol.ell[i] = opt_i.ell
            sol.c[i]   = opt_i.c
            sol.U[i]   = opt_i.U

    def tax_revenue(self):
        par = self.par
        sol = self.sol

        if not hasattr(sol,'ell'):
            self.solve_workers()

        # sum individual taxes (equivalent to N*zeta + tau*sum(w p ell))
        T = 0.0
        for i in range(par.N):
            y_i = self.income(sol.p[i], sol.ell[i])
            T += self.tax(y_i)
        return T
    
    def SWF(self):

        par = self.par
        sol = self.sol

        G =  self.tax_revenue()
        if G < 0:
            return np.nan
        SWF = np.sum(sol.U) + par.chi*(G**par.eta)
        return SWF

    
    def optimal_taxes(self, tau0=None, zeta0=None):

        par = self.par
        sol = self.sol

    # initialize tax parameters from provided guesses
        if not hasattr(sol, 'p'):
            self.draw_productivities()

        p_fixed = sol.p.copy()
        p_min   = p_fixed.min()
        
        if tau0 is None:
            tau0 = par.tau
        if zeta0 is None:
            zeta0 = par.zeta
    # initial guess
        x0 = np.array([tau0, zeta0])

    # a. objective function
        def obj(x):
            tau, zeta = x
            
            if tau < 0.0 or tau >= 0.999:
                return 1e12  # heavy penalty for invalid tau
            
            # avoid overflow
            zeta_max = (1 - tau) * par.w * p_min * par.ell_max
            if zeta >= zeta_max:
                return 1e12 
            
            # update parameters
            par.tau = tau
            par.zeta = zeta
            sol.p = p_fixed  
            
            
            # Workers respond to taxes and consumption changes.
            self.solve_workers()

            # compute social welfare
            SWF = self.SWF()
            
            if not np.isfinite(SWF):
                return 1e12  
            
            return -SWF  # scipy.minimize can only MINIMIZE, so we minimize the NEGATIVE welfare so the optimizer maximizes SWF.
    
    # b. optimization               
        # tau ∈ [0,1),  zeta free but limited to avoid overflow
        bounds = [(0.0, 0.999), (-1e6, 1e6)]

        # run optimizer
        res = minimize(obj, x0, bounds=bounds, method='L-BFGS-B')# limited-memory BFGS with box constraints standard algorithm for smooth, bounded optimization.

    # c. results: 
        par.tau  = float(res.x[0])
        par.zeta = float(res.x[1])

    
        return res        #res.x        # optimal (tau*, zeta*)
                      #res.fun      # minimum value of -SWF
                      #res.success  # True if optimizer succeeded
                      #res.message  # explanation