from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Conways_game_of_life',
    ext_modules=cythonize("c_game_of_life.pyx")
)
