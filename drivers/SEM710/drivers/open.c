/* File: open.c */

#include <ftdi.h>
#include <libusb-1.0/libusb.h>
#include <stdio.h>

#include "open.h"

/* #define USB_DEVICE_MISSING -100 */
/* #define USB_DETACH_DEVICE_FAILED -101 */
/* #define CONTEXT_INIT_FAILED -102 */
/* #define USB_OPEN_FAILED -103 */
/* #define USB_PURGE_RX_FAILED -104 */
/* #define USB_PURGE_TX_FAILED -105 */
/* #define USB_SET_BAUDRATE_FAILED -106 */
/* #define USB_SET_LINE_PROP_FAILED -107 */
/* #define USB_SET_FLOW_CTRL_FAILED -108 */
/* #define USB_SET_LATENCY_TIMER_FAILED -109 */

#define vID 0x0403
#define pID 0xBAB2

int detach_device_kernel(int vendor_id, int product_id)
{
  int failed;
  libusb_context *ctx;
  libusb_device_handle *handle;

  ctx = NULL;
  handle = NULL;

  libusb_init(&ctx);
  libusb_set_debug(ctx, 3);

  handle = libusb_open_device_with_vid_pid(ctx, 
					   vendor_id,
					   product_id);
  if (handle == NULL) {
    return USB_DEVICE_MISSING;
  }

  if (libusb_kernel_driver_active(handle, 0)) {
    failed = libusb_detach_kernel_driver(handle, 0);
    if (failed) {
      return USB_DETACH_DEVICE_FAILED;
    }
  }
  libusb_release_interface(handle, 0);
  libusb_close(handle);
  libusb_exit(ctx);

  return 0;
}

int init_device(int vendor_id, int product_id, struct ftdi_context *ctx) {
  int failed;

  failed = ftdi_init(ctx);
  if (failed) {
    return CONTEXT_INIT_FAILED;
  }

  failed = ftdi_usb_open(ctx, vendor_id, product_id);
  if (failed) {
    return USB_OPEN_FAILED;
  }

  return 0;
}

int prepare_device(struct ftdi_context *ctx) {
  int failed;
  
  failed = ftdi_usb_purge_rx_buffer(ctx);
  if (failed) {
    return USB_PURGE_RX_FAILED;
  }

  failed = ftdi_usb_purge_tx_buffer(ctx);
  if (failed) {
    return USB_PURGE_TX_FAILED;
  }
  
  failed = ftdi_set_baudrate(ctx, 19200);
  if (failed) {
    return USB_SET_BAUDRATE_FAILED;
  }

  failed = ftdi_set_line_property(ctx, 
				  BITS_8, 
				  STOP_BIT_1, 
				  NONE);
  if (failed) {
    return USB_SET_LINE_PROP_FAILED;
  }

  failed = ftdi_setflowctrl(ctx, SIO_DISABLE_FLOW_CTRL);
  if (failed) {
    return USB_SET_FLOW_CTRL_FAILED;
  }

  failed = ftdi_set_latency_timer(ctx, 3);
  if (failed) {
    return USB_SET_LATENCY_TIMER_FAILED;
  }

  return 0;
}

struct ftdi_context *open_device() {
  int detach_error;
  int init_error;
  int prep_error;

  struct ftdi_context *ctx = NULL;
  ctx = ftdi_new();

  detach_error = detach_device_kernel(vID, pID);
  if (detach_error) {
    return NULL;
  }

  init_error = init_device(vID, pID, ctx);
  if (init_error) {
    return NULL;
  }

  prep_error = prepare_device(ctx);
  if (prep_error) {
    return NULL;
  }
  
  return ctx;
}
