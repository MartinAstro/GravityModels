import numpy as np
from GravityModels.CelestialBodies.Asteroids import *
from GravityModels.CelestialBodies.Planets import * 
from GravityModels.Models import Polyhedral, PointMass, SphericalHarmonics

def test_import_planets():
    earth = Earth()
    moon = Moon()

def test_import_asteroids():
    eros = Eros()
    bennu = Bennu()

def test_polyhedral():
    asteroid = Eros()
    poly_model = Polyhedral(asteroid, asteroid.obj_8k)
    position = np.ones((1, 3)) * 1e4  # Must be in meters
    poly_model.compute_acceleration(position)

def test_point_mass():
    eros = Eros()
    earth = Earth()
    eros_point_mass = PointMass(eros)
    earth_point_mass = PointMass(earth)

    position = np.ones((1, 3)) * 1e4  # Must be in meters
    eros_point_mass.compute_acceleration(position)
    earth_point_mass.compute_acceleration(position)

def test_spherical_harmonics():
    eros = Eros()
    earth = Earth()
    eros_sph_harm = SphericalHarmonics(eros.sh_file, 3)
    earth_sph_harm = SphericalHarmonics(earth.sh_file, 3)

    position = np.ones((1, 3)) * 1e4  # Must be in meters
    eros_sph_harm.compute_acceleration(position)
    earth_sph_harm.compute_acceleration(position)


# def test_energy_conservation():
#     from scipy.integrate import solve_ivp
#     from GravityModels.utils.transformations import cart2sph, invert_projection
#     asteroid = Eros()
#     poly_model = Polyhedral(asteroid, asteroid.obj_8k)
#     def fun(x,y,IC=None):
#         "Return the first-order system"
#         # print(x)
#         R, V = y[0:3], y[3:6]
#         r = np.linalg.norm(R)
#         a = poly_model.compute_acceleration(R.reshape((1,3)), pbar=False)
#         dxdt = np.hstack((V, a.reshape((3,))))
#         return dxdt.reshape((6,))
    
#     T = 1000
#     state = np.array([-6.36256532e+02, -4.58656092e+04,  1.31640352e+04,  3.17126984e-01, -1.12030801e+00, -3.38751010e+00])

#     sol = solve_ivp(fun, [0, T], state.reshape((-1,)), t_eval=None, events=None, atol=1e-12, rtol=1e-12)

    
#     # sol = solve_ivp(fun, [0, T], state.reshape((-1,)), t_eval=None, events=None, atol=1e-14, rtol=1e-14)
#     rVec = sol.y[0:3, :]
#     vVec = sol.y[3:6, :]
#     hVec = np.cross(rVec.T, vVec.T)
#     h_norm = np.linalg.norm(hVec, axis=1)

#     KE = 1./2.*1*np.linalg.norm(vVec, axis=0)**2
#     U = poly_model.compute_potential(rVec.T)

#     energy = KE + U


#     plt.figure()
#     plt.subplot(2,1,1)
#     plt.plot(np.linspace(0, T, len(h_norm)), h_norm, label='orbit')
#     plt.subplot(2,1,2)
#     plt.plot(np.linspace(0, T, len(h_norm)), energy, label='orbit')
#     plt.show()


    


def main():
    test_import_planets()
    test_import_asteroids()
    test_point_mass()
    test_polyhedral()
    test_spherical_harmonics()



if __name__ == "__main__":
    main()