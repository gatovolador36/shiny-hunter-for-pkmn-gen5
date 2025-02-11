# this program will play a sound when encountering a shiny in a pokemon game (specifically gen 5)

import mss
import numpy as np
import time
import playsound
import pygetwindow as gw
import sys


def is_in_battle(pixel_data: np.ndarray) -> bool:
    """
    Checks if a battle is active by looking for the white HP bars.
    """
    # --- Your Precise Measurements (Relative to Game Screen) ---
    hp_bar_check_region = {
        "top": 1,     # Your Y value (game screen relative)
        "left": 26,    # Your X value (game screen relative)
        "width": 1,   # Your specified width
        "height": 1,  # Your specified height
    }

    print(f"pixel_data shape: {pixel_data.shape}")  # Debug
    hp_bar_region = pixel_data[
        hp_bar_check_region["top"] : hp_bar_check_region["top"] + hp_bar_check_region["height"],
        hp_bar_check_region["left"] : hp_bar_check_region["left"] + hp_bar_check_region["width"],
    ]
    print(f"hp_bar_region shape: {hp_bar_region.shape}")  # Debug
    print(f"hp_bar_region:\n{hp_bar_region}")  # Debug

    # --- SAVE HP BAR REGION (Uncomment for debugging) ---
    # mss.tools.to_png(hp_bar_region.tobytes(), (hp_bar_check_region["width"], hp_bar_check_region["height"]), output="hp_bar_region.png")

    white_threshold = 240  # Adjust if needed
    min_white_pixels = 4    # Adjust if needed

    greater_than_threshold = hp_bar_region >= white_threshold
    print(f"hp_bar_region >= white_threshold:\n{greater_than_threshold}")

    white_pixels = np.all(greater_than_threshold, axis=2)
    print(f"np.all(..., axis=2):\n{white_pixels}")

    num_white_pixels = np.count_nonzero(white_pixels)
    print(f"np.count_nonzero(white_pixels): {num_white_pixels}")


    is_battle_result = num_white_pixels >= min_white_pixels
    print(f"is_in_battle: white pixels={num_white_pixels}, is_battle={is_battle_result}")  # Debug print

    return is_battle_result

def play_shiny_sound() -> None:
    pass #Removed for now.

def main() -> None:
    """Main function for the shiny hunter."""
    print("Shiny Hunter starting...")

    # --- Configuration ---
    monitor_number: int = 1
    capture_width: int = 256       # Native width (1x)
    capture_height: int = 192      # Native height (1x)
    capture_delay: float = 2.0  #  SLOWED WAY DOWN for initial testing
    emulator_title: str = "DeSmuME 0.9.13 x64 SSE2"

    # --- Initialization ---
    try:
        with mss.mss() as sct:
            # --- CORRECTED CAPTURE REGION (Based on your full-screen coordinates) ---
            capture_region = {
                "top": 192,  # Your *screen* Y
                "left": 256, # Your *screen* X
                "width": 256,
                "height": 192,
                "mon": 1,  # Primary monitor
            }
            print(f"Capture region: {capture_region}")

            in_battle = False

            # --- Main Loop ---
            print("Shiny Hunter running...")
            while True:
                try:
                    window = gw.getWindowsWithTitle(emulator_title)[0]
                    window.activate()
                except IndexError:
                    print(f"Error: Could not find window with title '{emulator_title}'. Exiting.")
                    sys.exit(2)  # Exit with error code 2
                    return

                sct_img = sct.grab(capture_region)
                img_array = np.array(sct_img)

                # --- SAVE FULL FRAME (Uncomment for debugging) ---
                # mss.tools.to_png(sct_img.rgb, sct_img.size, output="full_frame.png")

                if is_in_battle(img_array):
                    if not in_battle:
                        print("Battle started!")
                        in_battle = True
                    # Don't do anything else in battle, just keep checking
                else:
                    if in_battle:
                        print("Battle ended! Exiting...")
                        sys.exit(1)  # Exit with code 1 (non-shiny battle)
                    print("Not in battle.")  # Clear indication
                    in_battle = False  # Ensure flag is reset

                time.sleep(capture_delay)  # Use regular time.sleep (not asyncio)

    except KeyboardInterrupt:
        print("Shiny Hunter stopped.")
        sys.exit(2)
    except Exception as e:
        print(f"An error occurred in Shiny Hunter: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()