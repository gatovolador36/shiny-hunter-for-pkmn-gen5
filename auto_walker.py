# This program will automate walking in a 2x2 grid in a pokemon game(specifically for gen 5)

import pydirectinput
import time
import subprocess
import sys
import signal
import asyncio

async def walk_square(steps: int = 2) -> None:
    """Walks the character in a 2x2 square using WASD."""
    directions = ['w', 'd', 's', 'a']
    sleep_duration = 0.25
    step_pause = 0.25

    for direction in directions:
        for _ in range(steps):
            pydirectinput.press(direction, presses=1, interval=sleep_duration)
            await asyncio.sleep(step_pause)

async def run_from_battle() -> None:
    """Simulates pressing the keys to run from a battle (Gen 5)."""
    pydirectinput.press('s', presses=3, interval=0.1)  # Three 'down' presses
    await asyncio.sleep(0.5)
    pydirectinput.press('enter')
    await asyncio.sleep(1.5)

async def main() -> None:
    """Main function for the auto-walker."""
    print("Auto-walker starting...")
    try:
        hunter_process = subprocess.Popen([sys.executable, "shiny_hunter_integrated.py"])
        print("Shiny hunter process started.")
    except FileNotFoundError:
        print("Error: shiny_hunter_integrated.py not found.")
        return
    except Exception as e:
        print(f"Error starting shiny hunter process: {e}")
        return

    print("Auto-walker running. Press Ctrl+C to stop.")

    try:
        while True:
            await walk_square()
            if hunter_process.poll() is not None:
                print("Shiny hunter process has exited. Stopping auto-walker.")
                break
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping auto-walker and shiny hunter...")
        hunter_process.send_signal(signal.SIGINT)
        try:
            hunter_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Shiny hunter process did not exit gracefully, terminating forcefully.")
            hunter_process.terminate()
        print("Programs stopped.")
    except Exception as e:
        print(f"An unexpected error occurred in auto_walker: {e}")
        hunter_process.terminate()
    finally:
        if hunter_process.poll() is None:
            hunter_process.terminate()

if __name__ == "__main__":
    asyncio.run(main())