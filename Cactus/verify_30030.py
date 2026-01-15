import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = "singularity_data/output_A30030"

def find_phi_file(root_dir):
    print(f"Searching for 'phi' data in: {root_dir}")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Look for .xg files now
            if "phi" in file and file.endswith(".xg"):
                full_path = os.path.join(root, file)
                print(f"FOUND: {full_path}")
                return full_path
    return None

def load_xg_data(filepath):
    """Load xgraph format data"""
    times = []
    values = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line.startswith('"') or not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    x = float(parts[0])  # coordinate or time
                    val = float(parts[1])  # value
                    times.append(x)
                    values.append(val)
                except ValueError:
                    continue
    return np.array(times), np.array(values)

# 1. Find the file - prefer the diagonal for time evolution
target_file = os.path.join(DATA_DIR, "phi_3D_diagonal.xg")
if not os.path.exists(target_file):
    target_file = find_phi_file(DATA_DIR)

if target_file and os.path.exists(target_file):
    print(f"Loading: {target_file}")
    x, phi = load_xg_data(target_file)
    
    if len(x) > 0:
        print(f"Loaded {len(x)} data points.")
        
        energy = phi**2
        mean_energy = np.mean(energy)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, phi, color='gold', linewidth=1.5, label='Field Amplitude')
        plt.title(f"Singularity A=30030: Field Evolution")
        plt.xlabel("Coordinate")
        plt.ylabel("φ (Phi)")
        plt.grid(alpha=0.3)
        plt.legend()
        
        output_img = "Singularity_30030_Diagnostics.png"
        plt.savefig(output_img)
        
        print(f"\n=== SUCCESS ===")
        print(f"Mean Energy Density: {mean_energy:.6e}")
        print(f"Max phi: {np.max(phi):.6e}")
        print(f"Min phi: {np.min(phi):.6e}")
        print(f"Graph saved to: {output_img}")
    else:
        print("File found, but it was empty or unreadable.")
else:
    print("ERROR: Could not find phi data file.")