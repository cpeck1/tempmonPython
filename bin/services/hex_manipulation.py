def int_base_16(num_string):
    return int(num_string, 16)

def hex_zpadded(number, zeroes):
    """return a hexadecimal string with value equal to number and zeroes
    following the 0x
    """
    hex_val = hex(number)[2:] 
    return "{}{}".format('0x', hex_val.zfill(zeroes))
