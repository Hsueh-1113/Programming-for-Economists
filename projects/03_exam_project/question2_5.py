import numpy as np
import matplotlib.pyplot as plt
from ExchangeEconomyModel import ExchangeEconomyModelClass 

model = ExchangeEconomyModelClass()
par = model.par

# 1) find all equilibria (unique p1*) using Newton over many initial guesses
p0_grid = np.linspace(0.25, 5, 50)
pstar_raw = []

for p0 in p0_grid:
    p_star, _, _ = model.solve_walras(p_guess=p0, method="newton", print_output=False)
    pstar_raw.append(p_star)

# keep unique equilibria
tol = 1e-4
pstars = []
for p in sorted(pstar_raw):
    if not any(abs(p - q) < tol for q in pstars):
        pstars.append(p)

print("Equilibria p1* found:", pstars)

# 2) Edgeworth box
fig, ax_A, ax_B = model.create_edgeworthbox(figsize=(7,7))

# plot initial endowment
ax_A.scatter([par.w1A], [par.w2A], marker="x", s=80, color="black", label="Endowment")

# 3) plot each equilibrium allocation + indifference curves
for i, p1 in enumerate(pstars, start=1):

    # allocations at this equilibrium price
    x1A, x2A = model.demand_A(p1)
    x1B, x2B = model.demand_B(p1)

    # equilibrium point (label only once per equilibrium to keep legend clean)
    ax_A.scatter([x1A], [x2A], s=50, label=fr"Eq {i}: $p_1^*={p1:.3f}$")
    ax_B.scatter([x1B], [x2B], s=50)

    # indifference curves through the equilibrium allocation
    model.indifference_curve_A(ax_A, x1A, x2A, lw=1.5)          # A: solid
    model.indifference_curve_B(ax_B, x1B, x2B, lw=1.5, ls="--") # B: dashed

# legend
model.add_legend(ax_A, ax_B, bbox_to_anchor=(0.05, 0.55))

ax_A.set_title("Edgeworth box: all equilibria with indifference curves")
plt.tight_layout()
plt.show()
