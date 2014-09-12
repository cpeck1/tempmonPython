/* File: closeModule.c */
#include <ftdi.h>
#include <stdio.h>

#include "close.h"

/* #define HANDLE_DEINIT_FAILED -300 */
/* #define HANDLE_FREE_FAILED -301 */

int close_device(struct ftdi_context *ctx) {
  ftdi_deinit(ctx);
  ftdi_free(ctx);
  
  return 0;
}
