/* File: close.i */
%module SEM710_close

%{
#define SWIG_FILE_WITH_INIT
#include "close.h" 
%}

int close_device(struct ftdi_context *ctx);
