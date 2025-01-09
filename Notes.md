# Camera Installation on Raspberry Pi 4

We now have WebRTC with a good frame rate, providing an all-in-one solution for the camera. You can control the camera at:
http://fablab38.local/webcam/control

## Problems

1. The second camera wasn't available.
    - Checked the forums of Octoprint and found out this issue can be caused by these two tags:
      > FORMAT=YUYU
      > Camera resolution --> WIDTH & HEIGHT
    - Reduced the resolution to SD for the second camera.
    - Changed format to MJPEG.
2. The port for `libcamera` should not be less than the other cameras.

References to fix the issues:
- https://community.octoprint.org/t/usb-webcams-known-to-work-with-mjpg-streamer/21149
- https://community.octoprint.org/t/camera-streamer-configuration-on-the-new-camera-stack-for-octopi/49950
- https://community.octoprint.org/t/tutorial-adding-multiple-usb-webcams-to-octoprint-using-new-webcam-stack/60324

# Camera Setup

Following Obico's manual: https://www.obico.io/docs/user-guides/multiple-cameras-octoprint/

## First Camera Setup: Creative

```console
No port provided, automatically selected port 8081

Please make sure your USB camera is plugged in and select it below:

1) /dev/v4l/by-id/usb-Creative_Technology_Ltd._VF0700_Live__Cam_Chat_HD_2C175066-video-index0
2) /dev/v4l/by-id/usb-Mintion_NZC_Mintion_NZC_SN0001-video-index0
? 1

Adding path unit for autolaunch of camera-streamer-usb@Creative
Running restart for camera-streamer-usb-Creative.path...
... done.
USB camera Creative added

Port:               8081
Device:             /dev/v4l/by-id/usb-Creative_Technology_Ltd._VF0700_Live__Cam_Chat_HD_2C175066-video-index0
Configuration file: /etc/camera-streamer.conf.d/usb-Creative.conf

```

## Nozzle Camera Setup

| Camera Model                        | ID        | Resolution & Frame Rate Options | Notes                                      |
|-------------------------------------|-----------|---------------------------------|--------------------------------------------|
| Creative Live! Cam Sync HD (VF0770) | 041e:4095 | -r HD -f 5, -r HD -f 10, -r HD -f 30 | Tested on Nexx WT3020 running OpenWRT - sanchosk 10, Tested on Raspberry Pi 3 Model B - eridem |

From here:
>'https://community.octoprint.org/t/usb-webcams-known-to-work-with-mjpg-streamer/21149'

Extra option:
> --http-listen=0.0.0.0

# Second Camera - Nozzle Camera

```console
No port provided, automatically selected port 8082

Please make sure your USB camera is plugged in and select it below:

1) /dev/v4l/by-id/usb-Creative_Technology_Ltd._VF0700_Live__Cam_Chat_HD_2C175066-video-index0
2) /dev/v4l/by-id/usb-Mintion_NZC_Mintion_NZC_SN0001-video-index0
? 2

Adding path unit for autolaunch of camera-streamer-usb@NozzleCam_Mintion
Running restart for camera-streamer-usb-NozzleCam_Mintion.path...
... done.
USB camera NozzleCam_Mintion added

Port:               8082
Device:             /dev/v4l/by-id/usb-Mintion_NZC_Mintion_NZC_SN0001-video-index0
Configuration file: /etc/camera-streamer.conf.d/usb-NozzleCam_Mintion.conf

```
Extra option:
> --http-listen=0.0.0.0

Current Pi Temperature:
>vcgencmd measure_temp | 
temp=57.9'C