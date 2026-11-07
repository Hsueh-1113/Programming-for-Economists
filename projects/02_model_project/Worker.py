from types import SimpleNamespace
from copy import deepcopy
import numpy as np

from scipy.optimize import minimize_scalar
from scipy.optimize import root_scalar

class Workerclass(): #the class customizes parameters without rewriting code.

    def __init__(self,par=None):#overwrites those defaults with any values you pass in via par (a dict).

        # a. setup
        self.setup_worker()#represents a worker who chooses labor supply ell (hours worked) to maximize utility, given wages and taxes.

        # b. update parameters (k = the name of a parameter you want to change, v = the value you want to change it to)
        if not par is None: 
            for k,v in par.items():
                self.par.__dict__[k] = v

    def setup_worker(self):
#par holds parameters; sol will hold solutions later.
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()
#nu and epsilon shape the disutility from working
        par.nu = 0.015 # weight on labor disutility
        par.epsilon = 1.0 # curvature of labor disutility
        
        # b. productivity and wages
        par.w = 1.0 # wage rate
        par.ps = np.linspace(0.5,3.0,100) # This creates a grid of 100 different productivity values evenly spaced between:
        par.ell_max = 16.0 # max labor supply
        
        # c. taxes
        par.tau = 0.50 # proportional tax rate
        par.zeta = 0.10 # lump-sum tax
        par.kappa = np.nan # income threshold for top tax # np.nan (“Not a Number”) means no threshold is active, because the paper you’re working from does not include a progressive bracket.It’s included only because the code skeleton is meant to be reusable for a more general tax system
        par.omega = 0.20 # top rate rate
          
    def utility(self,c,ell):#defining utility function (equation 2) # U = \log c - \nu \frac{1 + \epsilon \ell}{1 + \epsilon}

        par = self.par

        u = np.log(c) - par.nu * ell**(1+par.epsilon)/(1+par.epsilon)
        
        return u
    
    def income(self,p,ell):#defining income = w*p*ell

        par = self.par

        y = par.w * p * ell

        return y
    
    def tax(self,pre_tax_income):# taking equation 1 and and doing pre tax income - post tax income we get  tau* income + lumpsum tax
        par = self.par
        tax = par.tau * pre_tax_income + par.zeta
        return tax

    def post_tax_income(self,p,ell): # this is simply pre-tax income - tax
        pre_tax_income = self.income(p,ell)
        tax = self.tax(pre_tax_income)
        return pre_tax_income - tax
    
    def max_post_tax_income(self,p):# defining maximum of equation 1

        par = self.par
        return self.post_tax_income(p,par.ell_max)

    def value_of_choice(self,p,ell):

        par = self.par

        c = self.post_tax_income(p,ell)
        U = self.utility(c,ell)

        return U
    
    def get_min_ell(self,p):# ell_bar is the maximum number of hours labour can supply is measured
    
        par = self.par

        min_ell = par.zeta/(par.w*p*(1-par.tau))

        return np.fmax(min_ell,0.0) + 1e-8 #the exponential trick is to avoid the optimizer from sitting in the boundary condition, avoids issues like log(0) in the utility function.np.fmax(min_ell,0.0) ensures it’s not negative
    
    def optimal_choice(self,p):# scipy.minimize can only MINIMIZE, so we minimize the NEGATIVE utility.we use numericall optimizer

        par = self.par
        opt = SimpleNamespace()

        # a. objective function : minimize **negative** utility
        def obj(ell):
            return -self.value_of_choice(p, ell)

        # b. bounds and minimization
        min_ell = self.get_min_ell(p)
        res = minimize_scalar( obj, bounds=(min_ell, par.ell_max), method='bounded')

        # c. results
        opt.ell = res.x
        opt.U = -res.fun
        opt.c = self.post_tax_income(p,opt.ell)

        return opt
    
    def FOC(self,p,ell):# numerically directly from equation 5

        par = self.par

    # compute consumption c = post-tax income
        c = self.post_tax_income(p, ell)

    # first-order condition: (1 - tau) * w * p / c - nu * ell^epsilon
        FOC = (1 - par.tau) * par.w * p / c - par.nu * ell**par.epsilon

        return FOC
    
    def optimal_choice_FOC(self,p):# using root finder

        par = self.par
        opt = SimpleNamespace()

        min_ell = self.get_min_ell(p)# a worker has to work minimum hours to keep his c> or equal to 0
        ell_max = par.ell_max # a worker has max hours to work

    # Workers must pick ℓmin​≤ℓ≤ℓmax​.This becomes the bracket for the root finder.

        try:
            # solve FOC(ℓ) = 0 on [ell_min, ell_max]
            sol = root_scalar(lambda ell: self.FOC(p,ell),
                              bracket=[ min_ell,ell_max],
                              method='brentq')
            ell_star = sol.root
        except:
            # if no interior solution, fall back to boundary
            ell_star =  min_ell

        opt.ell = ell_star
        opt.c = self.post_tax_income(p, opt.ell)
        opt.U = self.utility(opt.c, opt.ell)

        return opt
    
        