#!/usr/bin/env python3

from distutils.core import setup, Extension

PACKAGE = "edcra"
NAME = "edcra-client"
DESCRIPTION = """Client-side of software for reading and recording output given by a variety of atmospheric condition-monitoring devices that provide a USB interface."""
AUTHOR = "Connor Peck"
AUTHOR_EMAIL = "cpeck1@ualberta.ca"
URL = "http://github.com/cpeck1/tempmonPython"
VERSION = '0.1'

SEM710_dir = "drivers/SEM710/drivers/"
SEM710_module = Extension(
    "_SEM710",
    libraries=["ftdi1", "usb-1.0"],
    library_dirs=["/usr/local/lib", "/usr/local/lib/libusb-1.0"],
    sources=[SEM710_dir+"SEM710.c", SEM710_dir+"SEM710_wrap.c"]
)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION, 
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    classifiers=[
        "Development Status :: 0 - Alpha",
        "Environment :: Desktop Environment",
        "Intended Audience :: Anyone",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    ext_modules=[
        SEM710_module
    ]
)
