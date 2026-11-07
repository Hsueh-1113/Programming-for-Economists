import matplotlib.pyplot as plt
from ExchangeEconomyModel import ExchangeEconomyModelClass 

model = ExchangeEconomyModelClass()

fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

for p0 in [0.9, 1.1]:
    p_star, p_path, eps_path = model.solve_walras(p_guess=p0, method="tatonnement", print_output=True)

    axes[0].plot(p_path, label=f"p0={p0}")
    axes[1].plot(eps_path, label=f"p0={p0}")

axes[0].set_ylabel(r"$p_1^k$")
axes[1].set_ylabel(r"$\epsilon_1^k$")
axes[1].set_xlabel("iteration k")

for ax in axes:
    ax.grid(True, alpha=0.3)
    ax.legend()

plt.tight_layout()
plt.show()
