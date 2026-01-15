import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = "singularity_data"
MANIFEST = f"{DATA_DIR}/sweep_manifest.csv"

def get_energy(output_dir):
    # Path to the ASCII output file
    # Note: Adjust filename pattern if your par file names the output differently
    # Usually it's something like "prime_resonance_test19.par.asc" inside the folder
    # We will look for any .asc or .out file in the folder
    try:
        files = os.listdir(output_dir)
        target_file = None
        for f in files:
            if "phi.asc" in f or "phi" in f: # Look for the scalar field output
                target_file = f
                break
        
        if not target_file: return 0
        
        filepath = os.path.join(output_dir, target_file)
        
        # Load Data (Time, Phi)
        # Skip comments (#)
        data = []
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                parts = line.split()
                if len(parts) > 11: # Standard Cactus output has many columns
                    # Column 9 is usually the scalar value, Column 1 is Time
                    # We might need to adjust based on your specific IOASCII settings
                    # Let's assume standard 1D output format:
                    # iter time x y z data
                    try:
                        val = float(parts[-1]) # Last column is usually the data
                        data.append(val * val) # Energy is proportional to Phi^2
                    except: pass
        
        if len(data) == 0: return 0
        return np.mean(data) # Return Average Energy Density
    except:
        return 0

print("Analyzing Singularity Data...")
df = pd.read_csv(MANIFEST)
energies = []

for index, row in df.iterrows():
    if row['Status'] == 'SUCCESS':
        # path is relative to script, so we fix it
        full_path = os.path.join(DATA_DIR, f"output_A{row['Amplitude']}")
        # In Docker we mapped it differently, so we look for the folder name
        local_path = os.path.join(DATA_DIR, f"output_A{row['Amplitude']}")
        
        e = get_energy(local_path)
        energies.append(e)
    else:
        energies.append(0)

df['Energy'] = energies

# --- THE SINGULARITY PLOT ---
# Filter for the Triad
triad = df[df['Amplitude'].between(30020, 30040)]

plt.figure(figsize=(12, 6))
colors = []
for t in triad['Type']:
    if t == 'PRIME': colors.append('red')
    elif t == 'PRIMORIAL_SINGULARITY': colors.append('gold')
    else: colors.append('blue')

plt.bar(triad['Amplitude'], triad['Energy'], color=colors)
plt.title("Energy Density: The Singularity Triad (30029-30030-30031)")
plt.xlabel("Amplitude (Integer)")
plt.ylabel("Mean Field Energy (φ²)")
plt.xticks(triad['Amplitude'], rotation=45)
plt.grid(axis='y', alpha=0.3)

# Add legend manually
from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color='red', lw=4),
                Line2D([0], [0], color='blue', lw=4),
                Line2D([0], [0], color='gold', lw=4)]
plt.legend(custom_lines, ['Prime', 'Composite', '30030 Singularity'])

plt.tight_layout()
plt.savefig("Singularity_Triad_Analysis.png")
print("Analysis Complete. Check Singularity_Triad_Analysis.png")
