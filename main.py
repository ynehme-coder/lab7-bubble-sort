from os import system
from colorama import Fore, Style, init
from time import sleep
from typing import Callable


numbers = [2, 16, 20, 4, 7, 12, 14, 5, 18]

init(autoreset=True)


def bubble_sort(
    values: list[int],
    on_step: Callable[[list[int], int, int, bool], None] | None = None,
) -> list[int]:
    arr = values.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - 1 - i):
            if on_step is not None:
                on_step(arr, i, j, False)

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

                if on_step is not None:
                    on_step(arr, i, j, True)

        if not swapped:
            break
    render_bars(arr,active_indices=None,sorted_suffix_start=0)
    return arr


def get_visualizer_settings() -> dict[str, object]:
    """Return starter settings for the terminal visualizer.

    TODO:
    1) Ask the user if they want step-by-step mode or auto-play mode.
    2) Ask if color should be enabled.
    3) Ask if bars should be auto-scaled to terminal width.
    4) Validate user input and handle unexpected values.
    """

    mode = ""
    while mode not in ("step", "auto"):
        mode_input = input("Mode: Step-by-step or auto? (s/a): ").strip().lower()
        if mode_input in ("s", "step", "step-by-step"):
            mode = "step"
        elif mode_input in ("a", "auto"):
            mode = "auto"
        else:
            print("Please enter 's' for step mode or 'a' for auto mode.")

    delay_seconds = 0.25
    if mode == "auto":
        raw_delay = input("Delay between steps in seconds (default 0.25): ").strip()
        if raw_delay:
            try:
                parsed_delay = float(raw_delay)
                if parsed_delay > 0:
                    delay_seconds = parsed_delay
            except ValueError:
                print("Invalid delay. Using default 0.25 seconds.")

    return {
        "mode": mode,  # TODO: add stricter validation and retry loop.
        "use_color": True,  # TODO: replace with user-selected value.
        "auto_scale": True,  # TODO: replace with user-selected value.
        "delay_seconds": delay_seconds,
    }


def clear_screen() -> None:
    """Clear the terminal before drawing the next animation frame.

    TODO:
    - Use an OS-aware clear strategy (Windows and Unix).
    - Keep this function small and reusable.
    """
    system("cls" if __import__("os").name == "nt" else "clear")


def render_bars(
    values: list[int],
    active_indices: tuple[int, int] | None = None,
    sorted_suffix_start: int | None = None,
) -> None:
    """Render the list as horizontal bars.

    TODO:
    - Scale bars based on value size (especially if auto-scale is enabled).
    - Highlight active comparison indices in a different color/symbol.
    - Optionally show pass number or swap count for learning feedback.
    """
    for i, x in enumerate(values):
        color = Fore.WHITE

        if active_indices is not None and i in active_indices:
            color = Fore.RED
        elif sorted_suffix_start is not None and i >= sorted_suffix_start:
            color = Fore.GREEN

        bar = ""
        while x > 0:
            bar += "#"
            x -= 1
        print(color + bar + Style.RESET_ALL)


def pause_for_user(mode: str, delay_seconds: float) -> None:
    """Control pacing for each visualization step.

    TODO:
    - In step mode: wait for Enter key.
    - In auto mode: sleep for delay_seconds.
    - Handle invalid mode values gracefully.
    """
    if mode == "step":
        user_input = (
            input("Press Enter for next comparison (or 'q' then Enter to quit): ")
            .strip()
            .lower()
        )
        if user_input == "q":
            raise KeyboardInterrupt
    elif mode == "auto":
        sleep(delay_seconds)
    else:
        input("Unknown mode. Press Enter to continue...")


def visualize_bubble_sort_learning(values: list[int]) -> list[int]:
    """Learning scaffold for visualizing bubble sort in the terminal.

    This function is intentionally incomplete: follow the TODOs to finish it.
    """
    settings = get_visualizer_settings()
    mode = str(settings["mode"])

    def on_step(state: list[int], pass_index: int, j: int, did_swap: bool) -> None:
        clear_screen()
        sorted_suffix_start = len(state) - pass_index
        render_bars(
            state,
            active_indices=(j, j + 1),
            sorted_suffix_start=sorted_suffix_start,
        )

        action = "swapped" if did_swap else "comparing"
        print(f"\nPass {pass_index + 1}, {action} positions {j} and {j + 1}")

        pause_for_user(
            mode=mode,
            delay_seconds=float(settings["delay_seconds"]),
        )

    return bubble_sort(values, on_step=on_step)


def run_learning_visual_demo() -> None:
    try:
        final_state = visualize_bubble_sort_learning(numbers)
        print("\nFinal state:", final_state)
    except KeyboardInterrupt:
        print("\nVisualization stopped by user.")


if __name__ == "__main__":
    run_learning_visual_demo()
