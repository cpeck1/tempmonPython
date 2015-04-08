/* File: SEM710.i */
%define DOCSTRING
"The SEM710 module contains the functions needed to open, read and close
a SEM710 temperature transmitter by Status Instruments"
%enddef

%module(docstring=DOCSTRING) SEM710

%{
#define SWIG_FILE_WITH_INIT
#include "SEM710.h"
#include <libftdi1/ftdi.h>
#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <math.h>

%}
%feature("autodoc", "1");
struct ftdi_context *open_method(int bus, int address);
%feature("autodoc", "1");
float read_channel_method(struct ftdi_context *ctx, int channel_number);
%feature("autodoc", "1");
int close_method(struct ftdi_context *ctx);
