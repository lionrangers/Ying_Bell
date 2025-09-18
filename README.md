# Ying_Bell
## Overview
This project aims to design an open-source, visual doorbell system that is user-friendly and practical. The primary functions include:
## Features
+ Doorbell: A button that triggers an indoor chime.
+ Video Capture upon Doorbell Press: When the doorbell button is pressed, the camera activates to transmit live footage of the doorstep to an indoor monitor.
## Additional Features
+ Motion Detection: An infrared sensor captures the presence of a person or animal within a certain range, activating the camera to record video.
+ Remote Control via Mobile App: Allows remote monitoring and control through a smartphone application.
+ Video and Photo Storage: Recorded videos and photos are uploaded to a home server for secure storage.
+ Expandable Camera Network: A scalable system capable of supporting multiple cameras, offering comprehensive security monitoring.
## Hardware
| Component        | Description               |
|-------------------|------------------------------|
| Raspberry Pi 4B  | Controller   |
| Pi Camera   | Camera   |
| PIR sensor   | Montion Monitor   |
| Button    |    |
| 7 inch touch screen   | Monitor and input   |



## Connections:
+ Button - LED power GPIO27;
+ Button - LED ground - ground;
+ Button - ON enable - GPIO4;
+ Button - ON button - GPIO17;
+ Relay - VCC - 3V3 (#17)
+ Relay - IN - GPIO24 (#18)
+ Relay - GND - Ground (#20)
+ PIR - VCC - GPIO22 (15)
+ PIR - PIN - GPIO23
