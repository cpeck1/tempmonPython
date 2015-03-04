/* File: SEM710.i */
%module SEM710

%{
#define SWIG_FILE_WITH_INIT
#include "SEM710.h"
%}

struct ftdi_context *open();
float read_channel(struct ftdi_context *ctx, int channel_number);
int close(struct ftdi_context *ctx);
