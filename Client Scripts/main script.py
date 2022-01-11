import time
from azure.iot.device import IoTHubDeviceClient, MethodResponse

CONNECTION_STRING = "HostName=smart-irrigation.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=xxxxxxxxxxxxxxxxxxxxxxx="
def create_client():
    # Instantiate the client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Define behavior for responding to the SetPumpState direct method
    def method_request_handler(method_request):
        if method_request.name == "SetPumpState":
            print("Pump is on")
            resp_status = 200
            resp_payload = {"Response": "SetPumpState called successfully"}
            method_response = MethodResponse.create_from_method_request(
                method_request=method_request,
                status=resp_status,
                payload=resp_payload
            )
            client.send_method_response(method_response)

    # Define behavior for receiving a twin patch
    def twin_patch_handler(twin_patch):
        print("")
        print("Twin desired properties patch received:")
        print(twin_patch)

    # Set the handlers on the client
    try:
        print("Beginning to listen for 'SetPumpState' direct method invocations...")
        client.on_method_request_received = method_request_handler
        print("Beginning to listen for updates to the Twin desired properties...")
        client.on_twin_desired_properties_patch_received = twin_patch_handler
    except:
        # If something goes wrong while setting the handlers, clean up the client
        client.shutdown()
        raise
    
def main():
    print ("Starting the IoT Hub Python jobs sample...")
    client = create_client()

    print ("IoTHubDeviceClient waiting for commands, press Ctrl-C to exit")
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print("IoTHubDeviceClient sample stopped!")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()


if __name__ == "__main__":
    main()
