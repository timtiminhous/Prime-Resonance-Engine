FROM archlinux:latest

# 1. Install Physics Engine + Analysis Tools (Numpy, Matplotlib, Mpmath)
RUN pacman -Syu --noconfirm && pacman -S --noconfirm \
    base-devel gcc-fortran git perl \
    openmpi hdf5-openmpi gsl openblas hwloc \
    python python-numpy python-matplotlib python-mpmath

# 2. Setup the Physics Lab
COPY Cactus /einstein/Cactus
WORKDIR /einstein/Cactus

# 3. Add Your Discovery Scripts
# (This assumes these scripts are sitting in your main folder. 
# If they are inside Cactus/, change the source path below to Cactus/script_name.py)
COPY Cactus/verify_30030.py /einstein/verify_30030.py
COPY Cactus/check_zeta_singularity.py /einstein/check_zeta_singularity.py
COPY Cactus/singularity_sweep.py /einstein/singularity_sweep.py

# 4. Set Environment Variables
ENV HDF5_DIR=/usr
ENV OPENBLAS_DIR=/usr

# 5. Default Command
ENTRYPOINT ["/bin/bash"]
