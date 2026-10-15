import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="mausam-mesh",
    version="1.0.0",
    packages=["mausam_mesh"],
    package_dir={"mausam_mesh": "."},
    author="Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)",
    author_email="mohitdonawat24@gmail.com",
    description="Sovereign Edge Meteorological Compression, Spatial Slicing & Disaster Early-Warning Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mohitdonawat.wildus.app/",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Hydrology",
    ],
    keywords="meteorology weather grib2 gis edge-computing quantization early-warning siren bhashini",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mausam-mesh=mausam_mesh.cli:main",
        ],
    },
)
