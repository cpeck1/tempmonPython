import _SEM710_open as open
import _SEM710_read as read

dev = open.open_device(0x0403, 0xBAB2)
read.read_device(dev)
