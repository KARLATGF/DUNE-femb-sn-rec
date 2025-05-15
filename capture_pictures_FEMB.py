import cv2
from vmbpy import *
import datetime
import numpy as np
import os

def capture_image_pair_loop(batch_id, settings_file=None):
    # Creating the storage directory for this batch:
    batch_dir = f"images/batch_{batch_id}"
    os.makedirs(batch_dir, exist_ok=True)

    picture_id = 1
     

    # Initialize Vimba API
    with VmbSystem.get_instance() as vmb:
        # Get the first available camera
        cams = vmb.get_all_cameras()
        if not cams:
            print("No cameras found! Have you turned the power supply on?")
            return

        with cams[0] as cam:
            #cam.open()  # Open the camera to configure it

            # Load settings file once
            if settings_file:
                try:
                    cam.load_settings(settings_file, PersistType.All)
                    print(f"Feature values have been loaded from '{settings_file}'")
                except Exception as e:
                    print(f"Could not load settings from {settings_file}: {e}")
                    return
            
            # Check the current pixel format after loading settings
            current_pixel_format = cam.get_pixel_format()
            #print(f"Loaded PixelFormat: {current_pixel_format}")

            if current_pixel_format != PixelFormat.Rgb8:
                print(f"Warning: Unexpected PixelFormat '{current_pixel_format}'. Adjusting for OpenCV compatibility.")
            print("------------------------------------------")
            print("Ready to capture images!")
            print("Type 'EXIT' at any time to stop.")
            print("------------------------------------------\n")
            
            number_of_pictures = picture_id

            while True: 

                # Wait for user input to start capturing a new pair
                user_input = input("--> Press ENTER to capture the FRONT image or type 'EXIT' to stop: ").strip().upper()
                if user_input == "EXIT":
                    print("Exiting...")
                    break

                # Capture the FRONT image
                frame_front = cam.get_frame()

    
                try:
                    # Convert frame to numpy array and reorder channels for OpenCV
                    frame_data = frame_front.as_numpy_ndarray()
                    frame_bgr = cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR)

                    # Save the front image
                    
                    # Getting current date and time for timestamps:
                    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') 

                    #file_name_front = f"images/{picture_id}_FRONT_{date_str}.png"
                    file_name_front = os.path.join(batch_dir, f"{picture_id}_FRONT_{date_str}.png")
                    cv2.imwrite(file_name_front, frame_bgr)
                    print(f"Front image saved as {file_name_front}")
                except ValueError as e:
                    print(f"Error processing FRONT image: {e}")
                    break

                # Prompt user for the BACK image or exit
                print("\nDon't forget to flip the board!")
                user_input = input("--> Press Enter to capture BACK image or type 'EXIT' to stop: ").strip().upper()
                
                if user_input == "EXIT":
                    print("Exiting...")
                    break

                # Capture the BACK image
                frame_back = cam.get_frame()
                try:
                    # Getting the sate again:
                    date_str_2 = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') 

                    # Convert frame to numpy array and reorder channels for OpenCV
                    frame_data = frame_back.as_numpy_ndarray()
                    frame_bgr = cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR)

                    # Save the back image
                    #file_name_back = f"images/{picture_id}_BACK_{date_str}.png"
                    file_name_back = os.path.join(batch_dir, f"{picture_id}_BACK_{date_str_2}.png")
                    cv2.imwrite(file_name_front, frame_bgr)
                    cv2.imwrite(file_name_back, frame_bgr)
                    print(f"Back image saved as {file_name_back}")
                    print("********************************************************")
                except ValueError as e:
                    print(f"Error processing BACK image: {e}")
                    break

                picture_id += 1
                

                #print(f"Last picture ID used: {last_picture_id}")

                # Increment the picture ID for the next pair
                number_of_pictures += 1
                number_of_fembs = number_of_pictures -1

            
            print(f"Number of FEMBs in this batch: {number_of_fembs}")


if __name__ == "__main__":
    # Prompt user for starting picture ID and set a fixed path for the settings file
    try:

        batch_id = int(input("--> Enter the Batch ID: ").strip())
        
        # Set the settings file path directly
        settings_file = "/home/coldelec/Documents/camera_settings_08-2024.xml"
        
        capture_image_pair_loop(batch_id, settings_file)
    except ValueError:
        print("Invalid input for picture ID. Please enter a number.")
