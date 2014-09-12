/* File: decode_error.i */
%module SEM710_decode_error
%include "typemaps.i"

%{
#define SWIG_FILE_WITH_INIT
#include "decode_error.h"
%}

const char *decode_error(int error_code);
