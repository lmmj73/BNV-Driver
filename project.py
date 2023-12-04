import serial
from ssp import ssp, ser
from ssp_device import ssp_device
import rest_api


ssp_device.sync(ssp_device)

ssp_device.enable(ssp_device)

ssp_device.set_inhibits(ssp_device)

ssp_device.channels(ssp_device)

ssp_device.dataset(ssp_device)

print("")

ssp_device.firmware(ssp_device)

print("")

while True:

    ssp_device.poll(ssp_device)

    rest_api.rest_api().post()

