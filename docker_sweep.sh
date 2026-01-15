#!/bin/bash

# 1. Create a folder on your Host (Ubuntu) to catch the data
mkdir -p sweep_data

# 2. Loop through the amplitudes
for A in {5..23}; do
    echo "=== Running Simulation for Amplitude A=$A ==="
    
    # Create a temporary par file for this specific run
    # We use 'prime_resonance_test19.par' because we know it works!
    sed "s/initial_amplitude.*=.*/initial_amplitude = ${A}.0/" prime_resonance_test19.par > sweep_data/run_A${A}.par
    
    # 3. Launch the Docker Container
    # -v $(pwd)/sweep_data:/data  -> Maps your Ubuntu folder to /data inside the container
    # IO::out_dir                 -> Tells Cactus to force output to that mapped folder
    docker run --rm \
        -v $(pwd)/sweep_data:/data \
        primeresonance-et:v1 \
        /data/run_A${A}.par \
        IO::out_dir=/data/output_A${A}
        
    echo "Finished A=$A. Data saved to ./sweep_data/output_A${A}"
done
