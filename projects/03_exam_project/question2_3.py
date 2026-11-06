import numpy as np
import matplotlib.pyplot as plt
from ExchangeEconomyModel import ExchangeEconomyModelClass 

model = ExchangeEconomyModelClass()

p0_grid = np.linspace(0.25, 5, 50)
pstar = np.empty_like(p0_grid)

for i, p0 in enumerate(p0_grid):
    p_star, _, _ = model.solve_walras(p_guess=p0, print_output=False, method="tatonnement")
    pstar[i] = p_star

plt.figure(figsize=(7,4.5))
plt.plot(p0_grid, pstar, marker="o", lw=1)
plt.xlabel(r"Initial guess $p_1^0$")
plt.ylabel(r"Resulting equilibrium $p_1^*$")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# count how many distinct equilibria you found (within tolerance)
tol = 1e-4
uniq = []
for x in pstar:
    if not any(abs(x-u) < tol for u in uniq):
        uniq.append(x)
print("Distinct p1* (approx):", sorted(uniq))
