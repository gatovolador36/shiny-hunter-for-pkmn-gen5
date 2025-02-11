# This program will automate walking in a 2x2 grid in a pokemon game(specifically for gen 5)

import pydirectinput
import time
import asyncio

async def walk_square(steps: int = 2) -> None:
    """Walks in a 2x2 square using WASD."""
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

async def test_inputs() -> None:
    """Tests individual key presses for debugging."""
    print("Testing inputs. Make sure DeSmuME has focus.")
    await asyncio.sleep(3)

    print("Pressing 'w' (up)...")
    pydirectinput.press('w')
    await asyncio.sleep(1)

    print("Pressing 's' (down)...")
    pydirectinput.press('s')
    await asyncio.sleep(1)

    print("Pressing 'a' (left)...")
    pydirectinput.press('a')
    await asyncio.sleep(1)

    print("Pressing 'd' (right)...")
    pydirectinput.press('d')
    await asyncio.sleep(1)

    print("Pressing 'enter' (A)...")
    pydirectinput.press('enter')
    await asyncio.sleep(1)

    print("Running from battle...")
    await run_from_battle()
    await asyncio.sleep(1)
    print("Walking in Square")
    await walk_square()

async def main() -> None:
    """Main function for the auto-walker."""
    print("Auto-walker starting...")

    # --- For testing, you can comment/uncomment these: ---
    await test_inputs()  # Uncomment to test individual keys and run_from_battle()
    # await walk_square()     # Uncomment to test just walking
    print("Auto-walker finished.")


if __name__ == "__main__":
    asyncio.run(main())  # *** THIS WAS MISSING ***