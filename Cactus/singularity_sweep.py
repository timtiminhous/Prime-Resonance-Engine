import os
import subprocess
import time
import math

# --- CONFIGURATION ---
DOCKER_IMAGE = "primeresonance-et:v1"
OUTPUT_DIR = "singularity_data"
PAR_TEMPLATE = "prime_resonance_test19.par"

# --- THE TARGET LIST ---
# We build a specific list of amplitudes to test
targets = []

# 1. The Foundation (5 to 50)
targets.extend(range(5, 51))

# 2. The Mid-Range Scouts (Random samples to test the waters)
targets.extend([137, 360, 720, 1000, 2520, 5040])

# 3. The SINGULARITY SECTOR (30,020 to 30,040)
# This captures 30029 (Prime), 30030 (Primorial), 30031 (Prime)
targets.extend(range(30020, 30041))

# Remove duplicates and sort
targets = sorted(list(set(targets)))

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# --- EXECUTION ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"=== INITIALIZING SINGULARITY SWEEP ===")
print(f"Target Count: {len(targets)} simulations")
print(f"Singularity Sector: 30029 (P), 30030 (M), 30031 (P) LOCKED IN.")

results_log = open(f"{OUTPUT_DIR}/sweep_manifest.csv", "w")
results_log.write("Amplitude,Type,Status,OutputFile\n")

for A in targets:
    # Determine Type
    if A == 30030:
        a_type = "PRIMORIAL_SINGULARITY"
    elif is_prime(A):
        a_type = "PRIME"
    else:
        a_type = "COMPOSITE"
    
    print(f"\n[TARGET LOCKED] A={A} ({a_type})")
    
    # 1. Generate Custom Par File
    par_filename = f"run_A{A}.par"
    host_par_path = os.path.join(os.getcwd(), OUTPUT_DIR, par_filename)
    
    # Read template
    with open(PAR_TEMPLATE, "r") as f:
        content = f.read()
    
    # Inject Amplitude (We replace the default 5.0 with our Target)
    # Using regex-like replacement for safety
    new_content = content.replace("initial_amplitude = 5.0", f"initial_amplitude = {A}.0")
    
    # Write new par file to the output directory
    with open(host_par_path, "w") as f:
        f.write(new_content)
        
    # 2. Run Docker Container
    # We map the OUTPUT_DIR to /data inside the container
    container_out_dir = f"/data/output_A{A}"
    
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/{OUTPUT_DIR}:/data",  # Map host folder to container
        DOCKER_IMAGE,
        f"/data/{par_filename}",           # The par file we just made
        f"IO::out_dir={container_out_dir}" # Where to save data
    ]
    
    try:
        # Run simulation (suppress massive output, just show errors)
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"  -> Simulation Complete. Data secure.")
        results_log.write(f"{A},{a_type},SUCCESS,{container_out_dir}\n")
        results_log.flush()
    except subprocess.CalledProcessError as e:
        print(f"  -> FAILURE: {e}")
        results_log.write(f"{A},{a_type},FAILED,N/A\n")

    # Small cool-down to let the SSD write buffer clear
    time.sleep(1)

results_log.close()
print("\n=== SWEEP COMPLETE ===")
print(f"Data stored in: {os.getcwd()}/{OUTPUT_DIR}")
