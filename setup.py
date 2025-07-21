from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import pybind11

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "orca",
        [
            "src/orca.cpp",
            "python/pybind11_wrapper.cpp",
        ],
        include_dirs=[
            pybind11.get_cmake_dir(),
            "src/",
        ],
        cxx_std=11,
        define_macros=[("VERSION_INFO", '"dev"')],
    ),
]

setup(
    name="orca-graphlets",
    version="0.1.0",
    author="Ole Petersen",
    author_email="peteole2707@gmail.com",
    description="Python bindings for ORCA (ORbit Counting Algorithm) - graphlet counting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.15",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords="graph analysis, graphlets, network science, orbits, bioinformatics",
    url="https://github.com/peteole/orca-python",
    project_urls={
        "Original ORCA": "https://github.com/thocevar/orca",
        "Bug Reports": "https://github.com/peteole/orca-python/issues",
        "Source": "https://github.com/peteole/orca-python",
    },
)
