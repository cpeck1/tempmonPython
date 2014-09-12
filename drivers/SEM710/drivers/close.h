/* File: closeModule.h */

#ifndef __INC_SEM710_CLOSE_H
#define __INC_SEM710_CLOSE_H

#include <ftdi.h>

#define HANDLE_DEINIT_FAILED -300
#define HANDLE_FREE_FAILED -301

int close_device(struct ftdi_context *ctx);

#endif /* __INC_SEM_710_CLOSE_H */
