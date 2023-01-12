from setuptools import find_packages, setup

setup(
    name='GravityModels',
    packages=find_packages(),
    version='0.1.0',
    description='A collection of gravity models intended for use by astrodynamicists',
    author='John M',
    license='MIT',
    setup_requires=['numpy == 1.23.0',
                    'numba',                
                    'tqdm',
                    'trimesh == 3.9.31',
                    'rtree',
                    'pooch',
                    'sphinxcontrib-applehelp==1.0.2',
                    'sphinx == 5.3.0',
                    "sphinx_rtd_theme",
                    ],
    install_requires=[
                    'numpy == 1.23.0',
                    'numba',                
                    'tqdm',
                    'trimesh == 3.9.31',
                    'rtree',
                    'pooch',
                    'sphinxcontrib-applehelp==1.0.2',
                    'sphinx == 5.3.0',
                    "sphinx_rtd_theme",
                    ],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)


