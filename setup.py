#!/usr/bin/env python3

from distutils.core import setup, Extension

SEM710_dir = "drivers/SEM710/drivers/"
SEM710_open_module = Extension("_SEM710_open",
                               libraries = ["ftdi", "usb-1.0"],
                               library_dirs = ["/usr/local/lib", 
                                               "/usr/local/lib/libusb-1.0"],
                               sources = [SEM710_dir+"open.c", 
                                          SEM710_dir+"open_wrap.c"])

SEM710_close_module = Extension("_SEM710_close",
                                libraries = ["ftdi", "usb-1.0"],
                                library_dirs = ["/usr/local/lib", 
                                                "/usr/local/lib/libusb-1.0"],
                                sources = [SEM710_dir+"close.c",
                                           SEM710_dir+"close_wrap.c"])

SEM710_read_module = Extension("_SEM710_read",
                               libraries = ["ftdi", "usb-1.0"],
                               library_dirs = ["/usr/local/lib", 
                                               "/usr/local/lib/libusb-1.0"],
                               sources = [SEM710_dir+"read.c", 
                                          SEM710_dir+"read_wrap.c"])

SEM710_decode_error_module = Extension("_SEM710_decode_error",
                                       libraries = ["ftdi", "usb-1.0"],
                                       library_dirs = ["/usr/local/lib", 
                                                   "/usr/local/lib/libusb-1.0"],
                                       sources = [SEM710_dir+"decode_error.c",
                                              SEM710_dir+"decode_error_wrap.c"])

setup(name="tempmon",
      version="1.0",
      description="""Program for reading and recording output given by a variety of temperature monitoring devices that provide a USB interface.""",
      author="Connor Peck",
      author_email="cpeck1@ualberta.ca",
      ext_modules=[SEM710_open_module, 
                   SEM710_close_module, 
                   SEM710_read_module,
                   SEM710_decode_error_module])
