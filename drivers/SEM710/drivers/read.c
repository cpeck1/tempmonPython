/* File: read.c */

#include <ftdi.h>
#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <math.h>

#include "read.h"
#include "open.h"

#define B_ENDIAN (get_endianness() == 1)

#define READ_PROCESS 0x2;
#define READ_CONF_BYTE 34;

/* #define MESSAGE_GENERATION_FAILED -200 */
/* #define BAD_RESPONSE -201 */

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

float read_device(struct ftdi_context *ctx)
{
  /*
     sends a read command to the device, and returns the length of the received
     byte array
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
	return written;
      }

      usleep(700000); /* give device some time to transmit process readings */

      received = ftdi_read_data(ctx, incoming_bytes, 280);
      if (received < 0) {
	return received;
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

