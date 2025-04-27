import usb.core
import usb.util

# Replace with your device's vendor and product ID
VENDOR_ID = 0x0403
PRODUCT_ID = 0x6001

# Find the device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("Device not found")

# Detach kernel driver if necessary
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set configuration
dev.set_configuration()

# Get active configuration and interface
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

# Find the OUT endpoint (write endpoint)
ep_out = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

if ep_out is None:
    raise ValueError("No OUT endpoint found")

# Data to send (must be bytes)
data = b'Hello USB'

# Write data to the endpoint
ep_out.write(data)

print("Data sent successfully!")

# Find the IN endpoint (read endpoint)
ep_in = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

if ep_in is None:
    raise ValueError("No IN endpoint found")

# Read data from the endpoint
try:
    data = ep_in.read(64, timeout=1000)  # Read 64 bytes with 1s timeout
    print("Data received:", data.tobytes())
except usb.core.USBError as e:
    print("USB Error:", e)