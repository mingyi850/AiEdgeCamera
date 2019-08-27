# Copyright (c) 2018, The Linux Foundation. All rights reserved.
# Licensed under the BSD License 2.0 license. See LICENSE file in the project root for
# full license information.

import argparse
import sys
import time
import subprocess
import utility
import os
import iot
from camera import CameraClient
import azureStorage


# Handle SIGTERM signal when docker stops the current VisionSampleModule container
import signal
IsTerminationSignalReceived = False

def main(protocol=None):
    print("\nPython %s\n" % sys.version)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='ip address of the camera', default=utility.getWlanIp())
    parser.add_argument('--username', help='username of the camera', default='admin')
    parser.add_argument('--password', help='password of the camera', default='admin')
    args = parser.parse_args()
    ip_addr = args.ip
    username = args.username
    password = args.password
    ip_addr = '127.0.0.1'
    #ip_addr = '10.104.68.189' #remote
    hub_manager = iot.HubManager()

    with CameraClient.connect(ip_address=ip_addr, username=username, password=password) as camera_client:
        #transferring model files to device
        utility.transferdlc()

        print(camera_client.configure_preview(display_out=1))
        camera_client.toggle_preview(True)

        time.sleep(15)
        rtsp_ip = utility.getWlanIp()
        rtsp_stream_addr = "rtsp://" + rtsp_ip + ":8900/live"
        hub_manager.iothub_client_sample_run(rtsp_stream_addr)

        camera_client.toggle_vam(True)
        print("Completed toggle_vam in main")
        camera_client.configure_overlay("inference")
        print("Completed configure overlay in main")
        camera_client.toggle_overlay(True)
        print("Completed toggle_overlay in main")
        #firstImage = camera_client.captureimage()
        #print("First Image from main connection: ", firstImage)
        try: #uses instance of camera_client, to start reading stream of metadata and parse into data.
            with camera_client.get_inferences() as results:
                print_inferences(hub_manager, camera_client, results)

        except KeyboardInterrupt:
            print("Stopping")
        try:
            print("inside infinite loop now")
            #while(True):
                #time.sleep(2)
        except KeyboardInterrupt:
            print("Stopping")

        camera_client.toggle_overlay(False)

        camera_client.toggle_vam(False)

        camera_client.toggle_preview(False)

def get_model_config():
    # TODO: get the AML model and return an AiModelConfig
    return None



def print_inferences(hub_manager, camera, results=None):
    deviceID = os.environ["IOTEDGE_DEVICEID"]
    global IsTerminationSignalReceived
    print("")
    lastTime = time.time()
    messageDelay = 2
    for result in results:
        if time.time() - lastTime < messageDelay:
            continue
        else:
            lastTime = time.time()
        if result is not None and result.objects is not None and len(result.objects):
            timestamp = lastTime
            #if timestamp:
                #print("timestamp={}".format(timestamp))
            #else:
                #print("timestamp= " + "None")
            for object in result.objects:
                id = object.id
                label = object.label
                confidence = object.confidence
                x = object.position.x
                y = object.position.y
                w = object.position.width
                h = object.position.height
                imageLocation = azureStorage.dummyDict
                helmetAlertFlag = "false"
                objectTransportFlag = "false"

                #Generic info about recognition object                
                print("id={}".format(id))
                print("label={}".format(label))
                print("confidence={}".format(confidence))
                print("Position(x,y,w,h)=({},{},{},{})".format(x, y, w, h))
                
                if object.confidence > 50:

                    #Module only captures image for helmet/nohelmet model
                    normalizedLabel = object.label.lower().replace(" ", "")
                    if normalizedLabel == "nohelmet":
                        helmetAlertFlag = "true"
                        print("NO HELMET!...Taking picture")
                        imageLocation = capture_and_upload_image(camera)
                        print("new image Location: ", imageLocation)
                    
                    imageURL = imageLocation["imageURL"]
                    imagePath = imageLocation["imagePath"]
                    
                    #Case: 2nd object detection model is active
                    if normalizedLabel != "helmet" and normalizedLabel != "nohelmet":
                        objectTransportFlag = "true"

                    MSG_FORMAT = "{{\"id\": {},\"label\": \"{}\", \"confidence\": {}, \"timestamp\": {}, \"noHelmetAlert\": {}, \"device\": \"{}\", \"location\": \"Warehouse 1\", \"imageUrl\": \"{}\", \"imagePath\": \"{}\"}}"
                    formattedMsg = MSG_FORMAT.format(str(id), str(label), str(confidence), str(timestamp), str(helmetAlertFlag), str(deviceID), str(imageURL), str(imagePath))
                    print(formattedMsg)
                    propertiesDict = dict()
                    propertiesDict["helmetAlertFlag"] = helmetAlertFlag
                    propertiesDict["objectTransportFlag"] = objectTransportFlag
                    hub_manager.SendPropertisedMsgToCloud(formattedMsg, propertiesDict)
                    time.sleep(1)
                
        else:
            print("No results for this frame")

        # Handle SIGTERM signal
        if (IsTerminationSignalReceived == True):
            print('!!! SIGTERM signal is received  !!!')
            break

#capture current frame and send frame to AzureBlobStorage
def capture_and_upload_image(camera):
    imageDict = camera.captureimage()
    print("image Dict: ", imageDict)
    fileName = imageDict["fileName"]
    filePath = imageDict["filePath"]
    pathDetails = azureStorage.uploadBlob(filePath,fileName)
    print("pathDetails: ", pathDetails)
    #delete file from local storage
    os.remove(filePath)
    return pathDetails
    
# Handle SIGTERM signal when docker stops the current VisionSampleModule container
def receive_termination_signal(signum, frame):
    global IsTerminationSignalReceived
    IsTerminationSignalReceived = True

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, receive_termination_signal)  # Handle SIGTERM signal
    main()
