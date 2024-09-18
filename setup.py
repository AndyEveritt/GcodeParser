from setuptools import find_packages, setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="gcodeparser",
    version="0.2.3",
    include_package_data=True,
    packages=find_packages(),

    install_requires=[
    ],

    author="Andy Everitt",
    author_email="andreweveritt@e3d-online.com",
    description="Python gcode parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AndyEveritt/GcodeParser",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
