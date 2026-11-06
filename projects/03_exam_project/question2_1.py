import numpy as np
import matplotlib.pyplot as plt
from ExchangeEconomyModel import ExchangeEconomyModelClass

model = ExchangeEconomyModelClass()

p1_grid = np.linspace(0.25, 5, 100)

x1A = np.empty_like(p1_grid)
x1B = np.empty_like(p1_grid)
eps1 = np.empty_like(p1_grid)

for i, p1 in enumerate(p1_grid):
    x1A[i], _ = model.demand_A(p1)
    x1B[i], _ = model.demand_B(p1)
    eps1[i] = x1A[i] + x1B[i] - 1.0  # epsilon_1(p1)

# ---- plots ----
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

axes[0].plot(p1_grid, x1A, label=r"$x^{A*}_1(p_1,m^A)$")
axes[0].plot(p1_grid, x1B, label=r"$x^{B*}_1(p_1,m^B)$")
axes[0].set_ylabel("Demand for good 1")
axes[0].grid(True, alpha=0.3)
axes[0].legend()

axes[1].plot(p1_grid, eps1, label=r"$\epsilon_1(p_1)$")
axes[1].axhline(0.0, linewidth=1)
axes[1].set_xlabel(r"Price $p_1$ (with $p_2=1$)")
axes[1].set_ylabel("Excess demand")
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.show()


# intervals where eps1 changes sign (indicates a root between grid points)
sign_change = np.where(np.sign(eps1[:-1]) * np.sign(eps1[1:]) < 0)[0]
print("\nSign-change intervals [pL, pR]:")
for j in sign_change:
    print([p1_grid[j], p1_grid[j+1]])
print("There are {} equilibria.".format(len(sign_change)))