/* File: read.i */
%module SEM710_read

%{
#define SWIG_FILE_WITH_INIT
#include "read.h" 
%}

float read_device(struct ftdi_context *ctx);
