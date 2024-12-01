from picamera2 import Picamera2, Preview

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (800, 480)}))


camera.start_preview(Preview.QTGL) 
camera.start()

print("Camera preview running. Press Ctrl+C to stop.")
try:
    while True:
        pass
except KeyboardInterrupt:
    camera.stop()
    print("Camera stopped.")
