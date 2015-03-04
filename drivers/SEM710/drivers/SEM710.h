/* File: SEM710.h */
#ifndef __INC_SEM710
#define __INC_SEM710

#include <ftdi.h>

#define MESSAGE_GENERATION_FAILED -10000
#define BAD_RESPONSE -10001
#define USB_DEVICE_MISSING -20001
#define USB_DETACH_DEVICE_FAILED -20002
#define CONTEXT_INIT_FAILED -20003
#define USB_OPEN_FAILED -20004
#define USB_PURGE_RX_FAILED -20005
#define USB_PURGE_TX_FAILED -20006
#define USB_SET_BAUDRATE_FAILED -20007
#define USB_SET_LINE_PROP_FAILED -20008
#define USB_SET_FLOW_CTRL_FAILED -20009
#define USB_SET_LATENCY_TIMER_FAILED -20010
#define HANDLE_DEINIT_FAILED -300
#define HANDLE_FREE_FAILED -301

struct ftdi_context *open();
float read_channel(struct ftdi_context *ctx, int channel_number);
int close(struct ftdi_context *ctx);

#endif /* __INC_SEM_710_READ_H */
