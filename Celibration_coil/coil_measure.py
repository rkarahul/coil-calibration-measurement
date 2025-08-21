# import cv2
# import threading
# import customtkinter as ctk
# from queue import Queue
# from PIL import Image, ImageTk
# from Cam_infer_1 import generate_frames_1, stop_grabbing_1
# import time
# import os
# from datetime import datetime

# def run_generate_frames(camera_active, output_queue_1, output_queue_2):
#     frame_generator_1 = generate_frames_1(camera_active)
#     while camera_active[0]:
#         frame_1, roi_flags_1 = next(frame_generator_1, (None, None))
#         if frame_1 is not None:
#             output_queue_1.put((frame_1, roi_flags_1, time.time()))
#         cv2.waitKey(1)

# def start_camera(camera_active, output_queue_1, output_queue_2):
#     if not camera_active[0]:
#         camera_active[0] = True
#         frame_thread_1 = threading.Thread(target=run_generate_frames, args=(camera_active, output_queue_1, output_queue_2))
#         frame_thread_1.daemon = True
#         frame_thread_1.start()

# def stop_camera(camera_active, output_queue_1, output_queue_2):
#     if camera_active[0]:
#         camera_active[0] = False
#         stop_grabbing_1()

# class CameraApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("YKK Zipper Inspection")
#         self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
#         self.minsize(1000, 600)

#         self.camera_active = [False]
#         self.output_queue_1 = Queue()
#         self.output_queue_2 = Queue()
#         self.last_frame_time = None
#         self.last_image = None

#         ctk.set_appearance_mode("dark")
#         self.configure(fg_color="#1F2A40")  # Background

#         # Layout
#         self.grid_rowconfigure(1, weight=1)
#         self.grid_columnconfigure(0, weight=3)
#         self.grid_columnconfigure(1, weight=1)

#         # === Header ===
#         self.header = ctk.CTkLabel(
#             self,
#             text="YKK Zipper Inspection",
#             font=("Arial", 30, "bold"),
#             text_color="white"
#         )
#         self.header.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

#         # === Left: Image Frame ===
#         self.image_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2C3E50")
#         self.image_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
#         self.image_frame.grid_rowconfigure(0, weight=1)
#         self.image_frame.grid_columnconfigure(0, weight=1)

#         # === Border Frame for image ===
#         self.image_border_frame = ctk.CTkFrame(self.image_frame, corner_radius=10, fg_color="#FFFFFF")
#         self.image_border_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
#         self.image_border_frame.grid_rowconfigure(0, weight=1)
#         self.image_border_frame.grid_columnconfigure(0, weight=1)

#         self.camera_feed_label = ctk.CTkLabel(self.image_border_frame, text="", anchor="center")
#         self.camera_feed_label.grid(row=0, column=0, sticky="nsew")

#         # === Right: Control Panel ===
#         self.control_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#273746")
#         self.control_frame.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
#         for i in range(6):
#             self.control_frame.grid_rowconfigure(i, weight=1, minsize=40)
#         self.control_frame.grid_columnconfigure(0, weight=1)

#         btn_pad_y = 3

#         self.start_button = ctk.CTkButton(
#             self.control_frame, text="Start Camera",
#             command=self.start_camera, fg_color="#2ECC71", hover_color="#27AE60"
#         )
#         self.start_button.grid(row=0, column=0, padx=15, pady=btn_pad_y, sticky="ew")

#         self.stop_button = ctk.CTkButton(
#             self.control_frame, text="Stop Camera",
#             command=self.stop_camera, fg_color="#E74C3C", hover_color="#C0392B"
#         )
#         self.stop_button.grid(row=1, column=0, padx=15, pady=btn_pad_y, sticky="ew")

#         self.status_label = ctk.CTkLabel(
#             self.control_frame, text="Camera Status: NG",
#             font=("Arial", 14), fg_color="#E74C3C", corner_radius=10
#         )
#         self.status_label.grid(row=2, column=0, padx=15, pady=btn_pad_y, sticky="ew")

#         # FPS Label (hidden)
#         self.fps_label = ctk.CTkLabel(
#             self.control_frame, text="",  # Keep blank to hide
#             font=("Arial", 14), fg_color="#5D6D7E", corner_radius=10
#         )
#         self.fps_label.grid(row=3, column=0, padx=15, pady=btn_pad_y, sticky="ew")

#         self.save_button = ctk.CTkButton(
#             self.control_frame, text="Save Image", command=self.save_current_image,
#             fg_color="#3498DB", hover_color="#2980B9"
#         )
#         self.save_button.grid(row=4, column=0, padx=15, pady=btn_pad_y, sticky="ew")

#         self.Result_button = ctk.CTkButton(
#             self.control_frame,
#             text="Detection Result",
#             state="disabled",
#             font=("Arial", 24, "bold"),
#             height=100,
#             fg_color="#7F8C8D",
#             hover_color="#7F8C8D"
#         )
#         self.Result_button.grid(row=5, column=0, padx=15, pady=15, sticky="ew")

#         self.update_frame()

#     def start_camera(self):
#         start_camera(self.camera_active, self.output_queue_1, self.output_queue_2)
#         self.status_label.configure(text="Camera Status: OK", fg_color="#2ECC71")
#         self.Result_button.configure(state="normal")

#     def stop_camera(self):
#         stop_camera(self.camera_active, self.output_queue_1, self.output_queue_2)
#         self.status_label.configure(text="Camera Status: NG", fg_color="#E74C3C")
#         self.Result_button.configure(state="disabled")

#     def save_current_image(self):
#         if self.last_image:
#             os.makedirs("saved_images", exist_ok=True)
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             path = f"saved_images/frame_{timestamp}.jpg"
#             self.last_image.save(path)
#             print(f"Image saved to {path}")

#     def update_frame(self):
#         if not self.output_queue_1.empty():
#             frame, roi_flags, timestamp = self.output_queue_1.get()
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             pil_img = Image.fromarray(rgb)
#             self.last_image = pil_img
#             tk_img = ImageTk.PhotoImage(pil_img)
#             self.camera_feed_label.configure(image=tk_img)
#             self.camera_feed_label.image = tk_img

#             # Optional FPS update (currently hidden)
#             self.last_frame_time = timestamp

#             self.update_detection_status(roi_flags)

#         self.after(50, self.update_frame)

#     def update_detection_status(self, flags):
#         defect_detected = any(flags)
#         if defect_detected:
#             self.Result_button.configure(
#                 text="⚠️ DEFECT DETECTED",
#                 fg_color="#E74C3C",
#                 hover_color="#C0392B",
#                 text_color="white"
#             )
#         else:
#             self.Result_button.configure(
#                 text="✔️ NO DEFECT",
#                 fg_color="#2ECC71",
#                 hover_color="#27AE60",
#                 text_color="black"
#             )

# if __name__ == "__main__":
#     app = CameraApp()
#     app.mainloop()



#################################Version 2###### with FPS#####################################

import cv2
import threading
import customtkinter as ctk
from queue import Queue
from PIL import Image, ImageTk
from Cam_infer_1 import generate_frames_1, stop_grabbing_1
import time
import os
from datetime import datetime

def run_generate_frames(camera_active, output_queue_1, output_queue_2):
    frame_generator_1 = generate_frames_1(camera_active)
    while camera_active[0]:
        frame_1, roi_flags_1 = next(frame_generator_1, (None, None))
        if frame_1 is not None:
            output_queue_1.put((frame_1, roi_flags_1, time.time()))
        cv2.waitKey(0)

def start_camera(camera_active, output_queue_1, output_queue_2):
    if not camera_active[0]:
        camera_active[0] = True
        frame_thread_1 = threading.Thread(target=run_generate_frames, args=(camera_active, output_queue_1, output_queue_2))
        frame_thread_1.daemon = True
        frame_thread_1.start()

def stop_camera(camera_active, output_queue_1, output_queue_2):
    if camera_active[0]:
        camera_active[0] = False
        stop_grabbing_1()

class CameraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Measurements")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.minsize(1000, 600)

        self.camera_active = [False]
        self.output_queue_1 = Queue()
        self.output_queue_2 = Queue()
        self.last_frame_time = None
        self.last_image = None

        # Theme and colors
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#1F2A40")  # Background

        # === Layout Config ===
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        # === Top Header ===
        self.header = ctk.CTkLabel(
            self, text="Measurements Check",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        self.header.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        # === Left: Image Frame ===
        self.image_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2C3E50")
        self.image_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        # === Border Frame for image ===
        self.image_border_frame = ctk.CTkFrame(self.image_frame, corner_radius=10, fg_color="#FFFFFF")
        self.image_border_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.image_border_frame.grid_rowconfigure(0, weight=1)
        self.image_border_frame.grid_columnconfigure(0, weight=1)

        #########
        self.camera_feed_label = ctk.CTkLabel(self.image_frame, text="", anchor="center")
        self.camera_feed_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # === Right: Control Panel ===
        self.control_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#273746")
        self.control_frame.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        for i in range(7):
            self.control_frame.grid_rowconfigure(i, weight=1, minsize=50)
        self.control_frame.grid_columnconfigure(0, weight=1)

        btn_pad_y = 5

        self.start_button = ctk.CTkButton(
            self.control_frame, text="Start Camera",
            command=self.start_camera, fg_color="#2ECC71", hover_color="#27AE60"
        )
        self.start_button.grid(row=0, column=0, padx=15, pady=btn_pad_y, sticky="ew")

        self.stop_button = ctk.CTkButton(
            self.control_frame, text="Stop Camera",
            command=self.stop_camera, fg_color="#E74C3C", hover_color="#C0392B"
        )
        self.stop_button.grid(row=1, column=0, padx=15, pady=btn_pad_y, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.control_frame, text="Camera Status: NG",
            font=("Arial", 14), fg_color="#E74C3C", corner_radius=10
        )
        self.status_label.grid(row=2, column=0, padx=15, pady=btn_pad_y, sticky="ew")

        self.fps_label = ctk.CTkLabel(
            self.control_frame, text="FPS: --",
            font=("Arial", 14), fg_color="#5D6D7E", corner_radius=10
        )
        self.fps_label.grid(row=3, column=0, padx=15, pady=btn_pad_y, sticky="ew")

        self.save_button = ctk.CTkButton(
            self.control_frame, text="Save Image", command=self.save_current_image,
            fg_color="#3498DB", hover_color="#2980B9"
        )
        self.save_button.grid(row=4, column=0, padx=15, pady=btn_pad_y, sticky="ew")

        self.Result_button = ctk.CTkButton(
            self.control_frame,
            text="Detection Result",
            state="disabled",
            font=("Arial", 20, "bold"),
            height=100,
            fg_color="#7F8C8D",
            hover_color="#7F8C8D"
        )
        self.Result_button.grid(row=5, column=0, padx=15, pady=15, sticky="ew")

        self.update_frame()

    def start_camera(self):
        start_camera(self.camera_active, self.output_queue_1, self.output_queue_2)
        self.status_label.configure(text="Camera Status: OK", fg_color="#2ECC71")
        self.Result_button.configure(state="normal")

    def stop_camera(self):
        stop_camera(self.camera_active, self.output_queue_1, self.output_queue_2)
        self.status_label.configure(text="Camera Status: NG", fg_color="#E74C3C")
        self.Result_button.configure(state="disabled")

    def save_current_image(self):
        if self.last_image:
            os.makedirs("saved_images", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"saved_images/frame_{timestamp}.jpg"
            self.last_image.save(path)
            print(f"Image saved to {path}")

    def update_frame(self):
        if not self.output_queue_1.empty():
            frame, roi_flags, timestamp = self.output_queue_1.get()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)
            self.last_image = pil_img
            tk_img = ImageTk.PhotoImage(pil_img)
            self.camera_feed_label.configure(image=tk_img)
            self.camera_feed_label.image = tk_img

            # FPS update
            if self.last_frame_time:
                delta = timestamp - self.last_frame_time
                fps = 1 / delta if delta > 0 else 0
                self.fps_label.configure(text=f"FPS: {fps:.2f}")
            self.last_frame_time = timestamp

            self.update_detection_status(roi_flags)

        self.after(50, self.update_frame)

    def update_detection_status(self, flags):
        defect_detected = any(flags)
        if defect_detected:
            self.Result_button.configure(
                text="⚠️ DEFECTED",
                fg_color="#E74C3C",
                hover_color="#C0392B",
                text_color="white"
            )
        else:
            self.Result_button.configure(
                text="✔️NO DEFECT",
                fg_color="#2ECC71",
                hover_color="#27AE60",
                text_color="black"
            )

if __name__ == "__main__":
    app = CameraApp()
    app.mainloop()


###########################################Version 1###############################################
# import cv2
# import threading
# import customtkinter as ctk
# import tkinter as tk
# from queue import Queue
# from PIL import Image, ImageTk
# from Cam_infer_1 import generate_frames_1, stop_grabbing_1
# import ctypes

# # Define the function to run the frame generation from the camera in parallel
# def run_generate_frames(camera_active, output_queue_1, output_queue_2):
#     frame_generator_1 = generate_frames_1(camera_active)
    
#     while camera_active[0]:
#         frame_1, roi_flags_1 = next(frame_generator_1, (None, None))
#         if frame_1 is not None:
#             output_queue_1.put((frame_1, roi_flags_1))
#         cv2.waitKey(1)  # Sleep to allow the other thread to run smoothly

# # Function to start camera feed
# def start_camera(camera_active, output_queue_1, output_queue_2):
#     if not camera_active[0]:
#         camera_active[0] = True
#         frame_thread_1 = threading.Thread(target=run_generate_frames, args=(camera_active, output_queue_1, output_queue_2))
#         frame_thread_1.daemon = True
#         frame_thread_1.start()

# # Function to stop camera feed
# def stop_camera(camera_active, output_queue_1, output_queue_2):
#     if camera_active[0]:
#         camera_active[0] = False
#         stop_grabbing_1()

# # GUI Class to handle layout and update frames
# class CameraApp(ctk.CTk):

#     def __init__(self):
#         super().__init__()

#         self.title("Camera Feed Application")
        
#         # Get screen width and height
#         user32 = ctypes.windll.user32
#         screen_width = user32.GetSystemMetrics(0)
#         screen_height = user32.GetSystemMetrics(1)
#         self.geometry(f"{screen_width}x{screen_height}")
        
#         self.camera_active = [False]
#         self.output_queue_1 = Queue()
#         self.output_queue_2 = Queue()
        
#         # Title label (at the top)
#         self.title_label = ctk.CTkLabel(self, text="YKK Zipper Inspection", 
#                                         font=("Arial", 30, "bold"), width=1000, height=60, 
#                                         fg_color = "#008000")
#         self.title_label.grid(row=0, column=0, columnspan=3, padx=50, pady=20, sticky="n")

#         # Create a frame to hold the camera feed and center it
#         self.camera_feed_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#2C3E50")
#         self.camera_feed_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

#         # Camera feed label (only one label now)
#         self.camera_feed_label = ctk.CTkLabel(self.camera_feed_frame, text="", 
#                                               width=800, height=450, corner_radius=20, 
#                                               fg_color="#FFFFFF", bg_color="#e74c3c",
#                                               font=("Arial", 16, "bold"))
#         self.camera_feed_label.grid(row=0, column=0, padx=10, pady=10)

#         # Configure grid row and column weights for responsiveness
#         self.grid_rowconfigure(1, weight=1, minsize=400)
#         self.grid_columnconfigure(1, weight=1, minsize=800)

#         # Control buttons frame (below the camera feed)
#         self.control_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#34495E")
#         self.control_frame.grid(row=2, column=0, columnspan=3, padx=50, pady=10, sticky="nsew")

#         # Start and stop buttons
#         self.start_button = ctk.CTkButton(self.control_frame, text="Start Camera", corner_radius=10, command=self.start_camera, fg_color="#28a745", hover_color="#218838")
#         self.start_button.grid(row=0, column=0, padx=10, pady=10)

#         self.stop_button = ctk.CTkButton(self.control_frame, text="Stop Camera", corner_radius=10, command=self.stop_camera, fg_color="#dc3545", hover_color="#c82333")
#         self.stop_button.grid(row=1, column=0, padx=10, pady=10)

#         # Step buttons (Step 1 to Step 5)
#         self.Result_button = ctk.CTkButton(self.control_frame, text="Detection Result", state="disabled", corner_radius=10, fg_color="#28a745", hover_color="#218838")
#         self.Result_button.grid(row=0, column=1, padx=10, pady=3)

#         # Status label (on the right of the camera feed)
#         self.status_label = ctk.CTkLabel(self, text="Camera Status: NG", font=("Arial", 12), fg_color="red", corner_radius=10)
#         self.status_label.grid(row=2, column=2, padx=10, pady=10)

#         # Ensure the layout expands responsively
#         self.grid_rowconfigure(2, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(2, weight=1)

#         self.update_frame()

#     def start_camera(self):
#         start_camera(self.camera_active, self.output_queue_1, self.output_queue_2)
#         self.status_label.configure(text="Camera Status: OK", fg_color="green")
#         self.Result_button.configure(state="normal")

#     def stop_camera(self):
#         stop_camera(self.camera_active, self.output_queue_1, self.output_queue_2)
#         self.status_label.configure(text="Camera Status: NG", fg_color="red")
#         self.Result_button.configure(state="disabled")

#     def update_frame(self):
#         if not self.output_queue_1.empty():
#             frame_1, roi_flags_1 = self.output_queue_1.get()

#             # Convert frames to Tkinter compatible format
#             img_rgb_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
#             pil_img_1 = Image.fromarray(img_rgb_1)
#             img_1 = ImageTk.PhotoImage(pil_img_1)
#             # Update image
#             self.camera_feed_label.configure(image=img_1)
#             self.camera_feed_label.image = img_1

#             # Update Step buttons based on flags
#             self.update_step_buttons(roi_flags_1)

#         self.after(50, self.update_frame)

#     def update_step_buttons(self, step_flags):
#         """ Update each step button's text and color based on the step flags """
#         for flag in step_flags:
#             if flag:
#                     button = getattr(self, f"Result_button")
#                     button.configure(fg_color="red", text=f"Defected - {flag}")
#             else:
#                 button = getattr(self, f"Result_button")
#                 button.configure(fg_color="green", text=f"No - Defect")

# # Run the application
# if __name__ == "__main__":
#     app = CameraApp()
#     app.mainloop()
