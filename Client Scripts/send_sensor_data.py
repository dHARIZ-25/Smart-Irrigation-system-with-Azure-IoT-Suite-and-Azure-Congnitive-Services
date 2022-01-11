import asyncio
import time
import board
import RPi.GPIO as GPIO
import dht11
from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient

CONNECTION_STRING = "HostName=smart-irrigation.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=8F/a9x7VH4XtFPVRgmM8bshWDI2EieINKvUUG2rhOa8="

DELAY = 5
TEMPERATURE = 20.0
HUMIDITY = 60
PAYLOAD = '{{"temperature": {temperature}, "humidity": {humidity}}}'

async def main():

    try:
        # Create instance of the device client
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        # Initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        # Read data using pin GPIO17
        dhtDevice = dht11.DHT11(pin=17)

        print("Simulated device started. Press Ctrl-C to exit")
        while True:

            try:
                result = dhtDevice.read()
                if result.is_valid():
                    temperature = result.temperature
                    humidity = result.humidity

                    data = PAYLOAD.format(temperature=temperature, humidity=humidity)
                    message = Message(data)

                    # Send a message to the IoT hub
                    print(f"Sending message: {message}")
                    await client.send_message(message)
                    print("Message successfully sent")
                else:
                    # print("Error: %d" % result.error_code)
                    continue

                await asyncio.sleep(DELAY)

            except KeyboardInterrupt:
                print("Simulated device stopped")
                GPIO.cleanup()
                break

    except Exception as error:
        print(error.args[0])

if __name__ == '__main__':
    asyncio.run(main())
