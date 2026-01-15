import mpmath
import matplotlib.pyplot as plt
import numpy as np

# Set precision to ensure we don't miss anything
mpmath.mp.dps = 50 

print("=== CALCULATING ZETA TOPOLOGY FOR SINGULARITY TRIAD ===")
print("Scanning Critical Line t = [30028, 30033]...")

# 1. Define the Range of the Singularity Triad
t_start = 30028
t_end = 30033
step = 0.05 # Fine resolution scan

# 2. Scan for Zero Crossings (Sign Changes) on the Critical Line (0.5 + it)
# We look for where the Riemann-Siegel Z function crosses 0.
# Z(t) is a real function that has zeros at the same t as Zeta(s).
zeros_found = []
t_val = t_start

prev_Z = mpmath.siegelz(t_val)

while t_val < t_end:
    next_t = t_val + step
    curr_Z = mpmath.siegelz(next_t)
    
    # If signs are different, we crossed a zero
    if mpmath.sign(prev_Z) != mpmath.sign(curr_Z):
        # Use a root finder to get the EXACT zero location
        exact_zero = mpmath.findroot(mpmath.siegelz, (t_val, next_t), solver='anderson')
        zeros_found.append(float(exact_zero))
        print(f"  -> ZERO DETECTED at t = {exact_zero}")
    
    prev_Z = curr_Z
    t_val = next_t

print(f"\nTotal Zeros found in Singularity Sector: {len(zeros_found)}")

# 3. Analyze Proximity to integers 30029, 30030, 30031
targets = [30029, 30030, 30031]
print("\n=== PROXIMITY REPORT ===")
for target in targets:
    # Find nearest zero
    nearest = min(zeros_found, key=lambda x: abs(x - target))
    distance = abs(nearest - target)
    
    status = "MISS"
    if distance < 0.25: status = "NEAR MISS"
    if distance < 0.01: status = "DIRECT HIT"
    
    print(f"Integer {target}: Nearest Zero is at t={nearest:.4f} (Dist: {distance:.4f}) [{status}]")

# 4. Check the Index (Is 30031 the 'n-th' zero?)
# We use the Riemann-von Mangoldt formula to estimate N(T)
# N(T) = (T/2pi) * log(T/2pi) - (T/2pi) + 7/8
def approximate_index(T):
    term1 = (T / (2 * mpmath.pi)) * mpmath.log(T / (2 * mpmath.pi))
    term2 = (T / (2 * mpmath.pi))
    return float(term1 - term2 + 0.875)

print("\n=== INDEX REPORT ===")
index_at_singularity = approximate_index(30030)
print(f"At height t=30030, we are approximately at Zero #{int(index_at_singularity)}")

# 5. Visualize the Critical Strip
t_plot = np.linspace(t_start, t_end, 1000)
z_plot = [float(mpmath.siegelz(t)) for t in t_plot]

plt.figure(figsize=(10, 5))
plt.plot(t_plot, z_plot, label="Riemann-Siegel Z(t)", color='blue')
plt.axhline(0, color='black', linewidth=1)

# Highlight the Triad
colors = {30029: 'red', 30030: 'gold', 30031: 'red'}
for target in targets:
    plt.axvline(target, color=colors[target], linestyle='--', alpha=0.5, label=f"Integer {target}")

plt.title("Zeta Function Behavior at the Singularity Triad")
plt.xlabel("Imaginary Part (t)")
plt.ylabel("Z(t)")
plt.legend()
plt.grid(True)
plt.savefig("Zeta_Singularity_Map.png")
print("Map saved to Zeta_Singularity_Map.png")
