/* File: decode_error.c */

#include <stdio.h>
#include <string.h>

#include "decode_error.h"

#include "open.h"
#include "read.h"
#include "close.h"

const char *decode_error(int error_code)
{
  switch(error_code) {
  case USB_DEVICE_MISSING:
    return "device missing"; 
  case USB_DETACH_DEVICE_FAILED:
    return "failed to detach device from kernel"; 
  case CONTEXT_INIT_FAILED:
    return "failed to initialize device context"; 
  case USB_OPEN_FAILED:
    return "failed to open USB device"; 
  case USB_PURGE_RX_FAILED:
    return "failed to purge USB device's RX port"; 
  case USB_PURGE_TX_FAILED:
    return "failed to purge USB device's TX port"; 
  case USB_SET_BAUDRATE_FAILED:
    return "failed to set the USB device's baudrate"; 
  case USB_SET_LINE_PROP_FAILED:
    return "failed to set the USB device's line property"; 
  case USB_SET_FLOW_CTRL_FAILED:
    return "failed to set the USB device's flow control"; 
  case USB_SET_LATENCY_TIMER_FAILED:
    return "failed to set the USB device's latency timer"; 
  case MESSAGE_GENERATION_FAILED:
    return "failed to generate message for device"; 
  case BAD_RESPONSE:
    return "received bad response from device"; 
  case HANDLE_DEINIT_FAILED:
    return "failed to deinitialize device handle";
  case HANDLE_FREE_FAILED:
    return "failed to free device handle"; 
  default:
    return "unknown error";
  }
}
