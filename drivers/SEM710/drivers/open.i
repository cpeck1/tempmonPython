/* File: open.i */
%module SEM710_open

%{
#define SWIG_FILE_WITH_INIT
#include "open.h"
%}

struct ftdi_context *open_device();
