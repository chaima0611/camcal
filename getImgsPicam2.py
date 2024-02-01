import time
import picamera2
import keyboard

class CameraCapture:
    def __init__(self):
        self.camera = picamera.PiCamera()

    def start_preview(self, preview_size=(640, 480)):
        self.camera.resolution = preview_size
        self.camera.start_preview()

    def stop_preview(self):
        self.camera.stop_preview()

    def capture_image(self, index):
        filename = f"output_{index}.jpg"
        self.camera.capture(filename)
        print(f"Image captured: {filename}")
        return index + 1  # Increment the counter

if __name__ == "__main__":
    camera_capture = CameraCapture()
    camera_capture.start_preview()
    print("Press 's' to capture an image. Press 'q' to quit.")

    capture_index = 1  # Initialize the counter

    try:
        while True:
            if keyboard.is_pressed("s"):
                camera_capture.stop_preview()  # Stop the previous preview
                capture_index = camera_capture.capture_image(capture_index)
                camera_capture.start_preview()  # Start a new preview
            elif keyboard.is_pressed("q"):
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        camera_capture.stop_preview()  # Stop the preview when the program exits
        camera_capture.camera.close()  # Close the camera instance
