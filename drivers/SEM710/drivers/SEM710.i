/* File: SEM710.i */
%module SEM710

%{
#define SWIG_FILE_WITH_INIT
#include "SEM710.h"
#include <libftdi1/ftdi.h>
#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <math.h>

%}

struct ftdi_context *open_method(int bus, int address);
float read_channel_method(struct ftdi_context *ctx, int channel_number);
int close_method(struct ftdi_context *ctx);
