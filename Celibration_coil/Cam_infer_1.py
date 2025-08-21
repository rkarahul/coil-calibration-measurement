import cv2
import numpy as np
import torch
import gc
from threading import Thread
from queue import Queue
from coil_HW_mesure import measure_and_draw_contours
from pypylon import pylon
import traceback

# Global control flags
camera_active = True
processing_complete = True

# Replace with your Basler camera serial number
serial_number = "25109240"

# Initialize camera
tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()

if not devices:
    print("❌ No cameras found!")
    exit()

# Find the camera by serial number
camera = None
for dev in devices:
    if dev.GetSerialNumber() == serial_number:
        camera = pylon.InstantCamera(tl_factory.CreateDevice(dev))
        break

if camera is None:
    print(f"❌ Camera with serial {serial_number} not found.")
    exit()

camera.Open()
camera.AcquisitionMode.SetValue("Continuous")
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Image converter
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Threaded detection
def ykk_result(img, output_queue):
    process_img,width_mm,height_mm = measure_and_draw_contours(img)
    output_queue.put((process_img, [width_mm,height_mm]))

# Stop grabbing
def stop_grabbing():
    global camera_active
    camera_active = False

# Frame grabber generator
def generate_frames():
    global processing_complete
    output_queue = Queue()

    while camera_active and camera.IsGrabbing():
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            img = converter.Convert(grab_result).GetArray()
            grab_result.Release()

            if processing_complete:
                processing_complete = False
                Thread(target=ykk_result, args=(img.copy(), output_queue)).start()

            if not output_queue.empty():
                img_combined, roi_flags = output_queue.get()
                processing_complete = True
                img_combined = cv2.resize(img_combined, (800, 800))
                yield img_combined, roi_flags
        else:
            grab_result.Release()

# Cleanup (call when finished)
def cleanup():
    camera.StopGrabbing()
    camera.Close()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    for frame, flags in generate_frames():
        cv2.imshow("Pylon Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stop_grabbing()
    cleanup()
