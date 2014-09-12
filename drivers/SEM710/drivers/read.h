/* File: read.h */

#ifndef __INC_SEM710_READ_H
#define __INC_SEM710_READ_H

#include <ftdi.h>

#define MESSAGE_GENERATION_FAILED -200
#define BAD_RESPONSE -201

float read_device(struct ftdi_context *ctx);

#endif /* __INC_SEM_710_READ_H */
