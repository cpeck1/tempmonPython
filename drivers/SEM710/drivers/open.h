/* File: open.h */
#ifndef __INC_SEM710_OPEN_H
#define __INC_SEM710_OPEN_H

#include <ftdi.h>

#define USB_DEVICE_MISSING -100
#define USB_DETACH_DEVICE_FAILED -101
#define CONTEXT_INIT_FAILED -102
#define USB_OPEN_FAILED -103
#define USB_PURGE_RX_FAILED -104
#define USB_PURGE_TX_FAILED -105
#define USB_SET_BAUDRATE_FAILED -106
#define USB_SET_LINE_PROP_FAILED -107
#define USB_SET_FLOW_CTRL_FAILED -108
#define USB_SET_LATENCY_TIMER_FAILED -109

struct ftdi_context *open_device(int vendor_id, int product_id);

#endif /* __INC_SEM_710_OPEN_H */
