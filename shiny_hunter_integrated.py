# this program will play a sound when encountering a shiny in a pokemon game (specifically gen 5)

import mss
import numpy as np
import time
import playsound
import pygetwindow as gw
import sys
import asyncio

def is_shiny_sparkle(pixel_data: np.ndarray, threshold: int = 230, min_sparkle_pixels: int = 8) -> bool:
    """Checks for a shiny sparkle."""
    return np.count_nonzero(np.all(pixel_data >= threshold, axis=2)) >= min_sparkle_pixels

def is_in_battle(pixel_data: np.ndarray) -> bool:
    """
    Checks if a battle is active by looking for the white HP bars.
    """
    # --- USE YOUR PRECISE MEASUREMENTS (relative to game screen) ---
    hp_bar_check_region = {
        "top": 1,     # Your measured Y value RELATIVE TO GAME SCREEN
        "left": 26,    # Your measured X value RELATIVE TO GAME SCREEN
        "width": 5,   # Your specified width
        "height": 5,  # Your specified height
    }

    print(f"pixel_data shape: {pixel_data.shape}")
    hp_bar_region = pixel_data[
        hp_bar_check_region["top"] : hp_bar_check_region["top"] + hp_bar_check_region["height"],
        hp_bar_check_region["left"] : hp_bar_check_region["left"] + hp_bar_check_region["width"],
    ]
    print(f"hp_bar_region shape: {hp_bar_region.shape}")
    print(f"hp_bar_region:\n{hp_bar_region}")

    white_threshold = 240  # Start with a reasonable value
    min_white_pixels = 4    # Start with your specified value

    greater_than_threshold = hp_bar_region >= white_threshold
    print(f"hp_bar_region >= white_threshold:\n{greater_than_threshold}")

    white_pixels = np.all(greater_than_threshold, axis=2)
    print(f"np.all(..., axis=2):\n{white_pixels}")

    num_white_pixels = np.count_nonzero(white_pixels)
    print(f"np.count_nonzero(white_pixels): {num_white_pixels}")

    is_battle_result = num_white_pixels >= min_white_pixels
    print(f"is_in_battle: white pixels={num_white_pixels}, is_battle={is_battle_result}")

    return is_battle_result

def play_shiny_sound() -> None:
    """Plays the notification sound."""
    try:
        playsound.playsound('shiny_sound.wav', block=False)
    except Exception as e:
        print(f"Error playing sound: {e}")

async def main() -> None:
    """Main function for the integrated shiny hunter."""
    print("Shiny Hunter starting...")

    # --- Configuration ---
    monitor_number: int = 1
    capture_width: int = 256       # Native width (1x)
    capture_height: int = 192      # Native height (1x)
    sparkle_top: int = 38          # Recommended starting point (1x)
    sparkle_left: int = 51         # Recommended starting point (1x)
    sparkle_width: int = 154       # Recommended starting point (1x)
    sparkle_height: int = 77       # Recommended starting point (1x)
    capture_delay: float = 0.08
    emulator_title: str = "DeSmuME 0.9.13 x64 SSE2"

    # --- Initialization ---
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_number]
            # --- CORRECTED CAPTURE REGION CALCULATION ---
            capture_region = {
                "top": 192,  #  y
                "left": 256, #  x
                "width": capture_width,
                "height": capture_height,
                "mon": 1,  # Assuming primary monitor
            }
            print(f"Capture region: {capture_region}")

            sparkle_row_start = sparkle_top
            sparkle_row_end = sparkle_top + sparkle_height
            sparkle_col_start = sparkle_left
            sparkle_col_end = sparkle_left + sparkle_width

            in_battle = False

            # --- Main Loop ---
            print("Shiny Hunter (Integrated) running...")
            while True:
                try:
                    window = gw.getWindowsWithTitle(emulator_title)[0]
                    window.activate()
                except IndexError:
                    print(f"Error: Could not find window with title '{emulator_title}'.")
                    return

                sct_img = sct.grab(capture_region)
                img_array = np.array(sct_img)

                new_battle_status = is_in_battle(img_array)
                print(f"Current Frame: in_battle (before)={in_battle}, new_battle_status={new_battle_status}")

                if new_battle_status != in_battle:
                    if new_battle_status:
                        print("Battle started!")
                    else:
                        print("Battle ended!")
                    in_battle = new_battle_status

                if in_battle:
                    sparkle_region = img_array[sparkle_row_start:sparkle_row_end, sparkle_col_start:sparkle_col_end]
                    if is_shiny_sparkle(sparkle_region):
                        print("Shiny detected! Exiting...")
                        play_shiny_sound()
                        await asyncio.sleep(5)
                        sys.exit(0)
                else:
                    print("  Not in battle, skipping sparkle check.")

                await asyncio.sleep(capture_delay)

    except KeyboardInterrupt:
        print("Shiny Hunter stopped.")
    except Exception as e:
        print(f"An error occurred in Shiny Hunter: {e}")

if __name__ == "__main__":
    asyncio.run(main())
