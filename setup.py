import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="gcodeparser",
    version="0.3.0",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    author="Andy Everitt",
    author_email="andreweveritt@e3d-online.com",
    description="Python gcode parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AndyEveritt/GcodeParser",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
)
