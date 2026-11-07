import numpy as np
import matplotlib.pyplot as plt
from ASADModel import ASADModelClass

model = ASADModelClass()
p = model.par

T = 5
v_path = np.zeros(T)
v_path[0] = 0.1  # temporary demand shock: v0=0.1, vt=0 for t>0

pi_e = np.zeros(T)
y_star = np.zeros(T)
pi_star = np.zeros(T)

# initial expectation
pi_e[0] = p["pi_star"]

# a fixed y-grid and axis limits make figures comparable across t
y_grid = np.linspace(0.97, 1.04, 400)
pi_min, pi_max = -0.4, 0.4

for t in range(T):

    if t > 0:
        pi_e[t] = p["phi"] * pi_e[t-1] + (1 - p["phi"]) * pi_star[t-1]

    # equilibrium (y*_t, pi*_t) given pi_e[t] and v_t
    y_star[t], pi_star[t] = model.equilibrium(pi_e=pi_e[t], v=v_path[t])

    # curves
    pi_AD = model.AD_curve(y_grid, v=v_path[t])
    pi_SRAS = model.SRAS_curve(y_grid, pi_e=pi_e[t])

    # plot (one figure per period)
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(y_grid, pi_AD, label=f"AD (v={v_path[t]:.2f})")
    ax.plot(y_grid, pi_SRAS, label=fr"SRAS ($\pi^e={pi_e[t]:.3f}$)")

    # equilibrium points (no annotate, just legend)
    ax.scatter([y_star[t]], [pi_star[t]],
               c="red", zorder=5,
               label=fr"Equilibrium ($y^*={y_star[t]:.3f}, \pi^*={pi_star[t]:.3f}$)")

    ax.set_title(f"Period t={t}")
    ax.set_xlabel("Output, y")
    ax.set_ylabel("Inflation, $\\pi$")
    ax.set_xlim(y_grid.min(), y_grid.max())
    ax.set_ylim(pi_min, pi_max)
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()