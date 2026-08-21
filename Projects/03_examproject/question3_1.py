import numpy as np
import matplotlib.pyplot as plt
from ASADModel import ASADModelClass

model = ASADModelClass()
p = model.par
y = np.linspace(0.85, 1.15, 400)


v0 = 0.0

# Curves
pi_AD = model.AD_curve(y, v=v0)
pi_SRAS_lr = model.SRAS_curve(y, pi_e=p['pi_star'])  # pi_e = pi_star (long-run SRAS)
pi_SRAS_shift = model.SRAS_curve(y, pi_e=0.08)       # pi_e jumps to 0.08

# Equilibria
y_lr, pi_lr = p['ybar'], p['pi_star']
y_new, pi_new = model.equilibrium(pi_e=0.08, v=v0)

# Print results
print(f"Long-run eq: y={y_lr:.6f}, pi={pi_lr:.6f}")
print(f"New eq (pi_e=0.08, v=0): y*={y_new:.6f}, pi*={pi_new:.6f}")

# Plotting
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(y, pi_AD, label="AD")
ax.plot(y, pi_SRAS_lr, label="SRAS ($\\pi_t^e$ = $\\pi^*$)")
ax.plot(y, pi_SRAS_shift, linestyle="--", label="SRAS ($\\pi_t^e$ = 0.08)")

ax.scatter([y_lr], [pi_lr],
           c="black", zorder=5,
           label=r"Long-run eq ($\bar{y}, \pi^*$)")

ax.scatter([y_new], [pi_new],
           c="red", zorder=5,
           label=fr"New eq ($y^*={y_new:.3f}, \pi^*={pi_new:.3f}$)")


ax.set_xlabel("Output, $y_t$")
ax.set_ylabel("Inflation, $\\pi_t$")
ax.set_title("AS-AD: AD, SRAS, and SRAS shift when $\\pi_t^e$ jumps")
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()
