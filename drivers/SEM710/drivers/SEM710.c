/* File: SEM710.c */

#include <ftdi.h>
#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <math.h>

#include "SEM710.h"

#define B_ENDIAN (get_endianness() == 1)

#define READ_PROCESS 0x2;
#define READ_CONF_BYTE 34;

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

struct ftdi_context *open() {
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

uint16_t make_crc(uint8_t *byte_array, int start_position, int end_position)
{
  /*
    make a cyclic redundancy check for the given byte array; this is per the
    rules found in the SEM710 specifications provided by Status Instruments;
    This crc currently causes the device to respond to messages sent, however
    the crc the device returns is incorrect by comparison to the one determined
    here.
  */
  int i;
  uint16_t crc;
  char j;
  char char_in;
  int lsBit;

  /*
    The CRC is based on the following components of this message:

    Start
    Command
    Length
    Data
  */

  crc = 0xFFFF;
  for (i = start_position; i <= end_position; i++) {
    char_in = byte_array[i];
    crc = crc ^ char_in;
    for (j = 1; j <= 8; j++) {
      lsBit = crc & 1;
      crc = crc >> 1;
      if (lsBit == 1) {
	crc = crc ^ 0xA001;
      }
    }
  }
  return crc;
}

int crc_pass(uint8_t *rx_data, int rx_pointer)
{
  /*
    returns whether the received crc is the same as the calculated crc from
    the byte array passed by the USB device; if it is not, then the usb
    transfer was "faulty"
  */
  uint16_t calculated_crc;
  uint16_t rx_crc;
  
  calculated_crc = make_crc(rx_data, 1, rx_pointer - 2);
  rx_crc = (((uint16_t) rx_data[rx_pointer]) << 8) + 
    ((uint16_t) rx_data[rx_pointer - 1]);

  printf("Calculated crc: %d\n", calculated_crc);
  printf("Received crc: %d\n", rx_crc);

  return (calculated_crc == rx_crc);
}


int generate_message(uint8_t* byte_array,
		     int byte_array_upper_index)
{
  /*
    Generate a message to send to the device, based on the given command and
    byte array; returns the size of the message
  */
  uint8_t output[255];
  int i;
  uint8_t x;
  uint16_t crc;
  uint8_t lbyte;
  uint8_t rbyte;

  /* start byte */
  i = 0;
  output[i] = 0x55;

  /* command */
  i++;
  output[i] = 0x2;

  /* length */
  i++;
  output[i] = byte_array_upper_index;

  /* data */
  for (x = 0; x <= byte_array_upper_index; x++) {
    i++;
    output[i] = byte_array[x];
  }

  /* crc */
  crc = make_crc(output, 1, i);
  lbyte = (crc >> 8) & 0xFF;
  rbyte = (crc) & 0xFF;

  /* put CRC on byte_array, little Endian */
  i++;
  output[i] = rbyte;
  i++;
  output[i] = lbyte;

  /* add end byte */
  i++;
  output[i] = 0xAA;

  for (x = 0; x <= i; x++) {
    byte_array[x] = output[x];
  }

  return (i + 1); /* returns the size, NOT the highest index */
}

int get_endianness(void)
{
  /*
    Return 0 if this machine uses little endian byte storage or 1 if it uses
    big endian byte storage
  */
  int a = 0x12345678;
  unsigned char *c = (unsigned char*)(&a);
  if (*c == 0x78) {
    return 0;
  }
  else {
    return 1;
  }
}

float float_from_byte_array(uint8_t *byte_array, int start_index)
{
  /* Gets and returns the float stored in the given byte array. */
  int i;
  float f1;
  int size;
  uint8_t *bytes;

  size = (int) sizeof(float);
  bytes = (uint8_t *) malloc(size);

  if (B_ENDIAN) {
    /* If this machine is big endian, reverse the order of the bytes */
    for (i = 0; i < size; i++) {
      bytes[(size-1) - i] = byte_array[start_index + i];
    }
    f1 = *((float *)(&bytes[0]));
  }
  else {
    f1 = *((float *)(&byte_array[start_index]));
  }

  free(bytes);
  return f1;
}

int extract_temperature_from_buffer(uint8_t *buffer) 
{
  return float_from_byte_array(buffer, 11);
}

float read_channel(struct ftdi_context *ctx, int channel_number)
{
  /*
     sends a read command to the device, and returns the length of the 
     received byte array

     note we do not use channel_number since the SEM710 has only one
     channel, but we include it in the function to conform witho other
     functions
  */
  uint8_t incoming_bytes[255];
  uint8_t outgoing_bytes[255];

  int len;
  int i;

  int written;
  int received;
  int confirmation_byte;

  for (i = 0; i < 255; i++) {
    incoming_bytes[i] = 0;
  }
  confirmation_byte = READ_CONF_BYTE;

  outgoing_bytes[0] = 0;
  len = generate_message(outgoing_bytes, 0);
  if (len <= 0) {
    return MESSAGE_GENERATION_FAILED;
  }

  received = 0;
  for (i = 0; (i < 4 && (incoming_bytes[1] != confirmation_byte)); i++) {
    /*  until positive response received, or 4 no-replies (2.8 seconds) */
    if (ctx) {
      written = ftdi_write_data(ctx, outgoing_bytes, len);
      if (written < 0) {
	return BAD_RESPONSE;
      }

      usleep(700000); /* give device some time to transmit process readings */

      received = ftdi_read_data(ctx, incoming_bytes, 280);
      if (received < 0) {
	return BAD_RESPONSE;
      }
    } else {
      return USB_DEVICE_MISSING;
    }
  }

  if (incoming_bytes[1] != confirmation_byte) {
    return BAD_RESPONSE;
  }

  return (float) extract_temperature_from_buffer(incoming_bytes);
}

int close(struct ftdi_context *ctx) {
  ftdi_deinit(ctx);
  ftdi_free(ctx);
  
  return 0;
}
