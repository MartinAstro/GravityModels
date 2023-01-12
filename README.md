![Tests](https://img.shields.io/github/actions/workflow/status/joma5012/GravityModels/python-package.yml)
![License](https://img.shields.io/github/license/joma5012/GravityModels)

# Welcome to GravityModels!

This package is intended to be a one stop shop for various gravity model implementations in Python.

Currently the package supports the following models:
- Spherical Harmonics
- Polyhedral 
- Point Mass

In addition, this repository hosts the following gravity information for the following celestial objects:
- Earth (EGM 2008, EGM 96)
- Moon (GRGM)
- Eros (Multiple shape models, and 16th degree spherical harmonic model)
- Bennu (Multiple shape models, and 16th degree spherical harmonic model)

# Usage

Initialize a celestial object of interest. Note, depending on the planet, this may take a minute as there is a one time operation which pulls the relevant gravity file from the internet. Some of these models can be rather large, but once pulled, the files are stashed locally and this operation will not occur again. 

Once the object is loaded, initialize your gravity model of choice and compute accelerations or potentials as necessary!

    from GravityModels.CelestialBodies.Planets import Earth
    from GravityModels.Models import SphericalHarmonics
    earth = Earth()
    earth_sph_harm = SphericalHarmonics(earth.sh_file, 3)
    position = np.ones((1, 3)) * 1e4  # Must be in meters
    accelerations = earth_sph_harm.compute_acceleration(position)

# Future Work

This will repository will include the [PINN Gravity Model](https://github.com/joma5012/GravNN) in the near future!