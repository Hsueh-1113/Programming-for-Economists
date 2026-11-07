import numpy as np
import matplotlib.pyplot as plt
from ASADModel import ASADModelClass

model = ASADModelClass()
p = model.par

T = 500
sigma_eps = 0.01  # from the exam
np.random.seed(123)
eps = np.random.normal(loc=0.0, scale=sigma_eps, size=T)  # eps_t ~ N(0, sigma_eps)

for rho in [0.8, 0.5]:

    y_star, pi_star, v, pi_e = model.simulate(rho=rho, eps=eps)
    sd_y, sd_pi, corr = model.moments(y_star, pi_star)

    print(f"rho = {rho:.2f}")
    print(f"sd(y*)  = {sd_y:.6f}")
    print(f"sd(pi*) = {sd_pi:.6f}")
    print(f"corr(y*, pi*) = {corr:.6f}")
    print("-"*40)

    # --- Plot time series (one figure with 3 panels) ---
    fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)

    axes[0].plot(y_star)
    axes[0].set_ylabel("$y^*$")
    axes[0].set_title(f"Time series (T={T}) with rho={rho:.2f}")

    axes[1].plot(pi_star)
    axes[1].set_ylabel("$\\pi^*$")
    
    axes[2].plot(v)
    axes[2].set_ylabel("v")
    axes[2].set_xlabel("t")

    for ax in axes:
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
