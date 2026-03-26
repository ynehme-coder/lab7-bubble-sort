from os import system
from colorama import Fore, Back, Style
from time import sleep
from typing import Callable


numbers = [2, 16, 20, 4, 7, 12, 14, 5, 18]


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

    return arr


def get_visualizer_settings() -> dict[str, object]:
    """Return starter settings for the terminal visualizer.

    TODO:
    1) Ask the user if they want step-by-step mode or auto-play mode.
    2) Ask if color should be enabled.
    3) Ask if bars should be auto-scaled to terminal width.
    4) Validate user input and handle unexpected values.
    """

    mode = input("Mode: Step-by-step or auto? (s/a)").lower()
    return {
        "mode": f"{mode}",  # TODO: replace with user-selected mode.
        "use_color": True,  # TODO: replace with user-selected value.
        "auto_scale": True,  # TODO: replace with user-selected value.
        "delay_seconds": 0.25,  # TODO: use only in auto-play mode.
    }



def clear_screen() -> None:
    """Clear the terminal before drawing the next animation frame.

    TODO:
    - Use an OS-aware clear strategy (Windows and Unix).
    - Keep this function small and reusable.
    """
    system("clear||cls")


def render_bars(values: list[int], active_indices: tuple[int, int] | None = None) -> None:
    """Render the list as horizontal bars.

    TODO:
    - Scale bars based on value size (especially if auto-scale is enabled).
    - Highlight active comparison indices in a different color/symbol.
    - Optionally show pass number or swap count for learning feedback.
    """
    for i in range(len(values)):
        x = values[i]
        color = Fore.WHITE
        if active_indices is not None and i in active_indices:
            color = Fore.RED

        bar = ""
        while x > 0:
            bar += "#"
            x -= 1
        print(color + bar)
            


def pause_for_user(mode: str, delay_seconds: float) -> None:
    """Control pacing for each visualization step.

    TODO:
    - In step mode: wait for Enter key.
    - In auto mode: sleep for delay_seconds.
    - Handle invalid mode values gracefully.
    """
    if mode == "step":
        input("Press Enter for next comparison...")
    else:
        sleep(delay_seconds)



def visualize_bubble_sort_learning(values: list[int]) -> list[int]:
    """Learning scaffold for visualizing bubble sort in the terminal.

    This function is intentionally incomplete: follow the TODOs to finish it.
    """
    settings = get_visualizer_settings()
    raw_mode = str(settings["mode"]).strip().lower()
    mode = "step" if raw_mode in ("s", "step", "step-by-step") else "auto"

    def on_step(state: list[int], pass_index: int, j: int, did_swap: bool) -> None:
        clear_screen()
        render_bars(state, active_indices=(j, j + 1))

        action = "swapped" if did_swap else "comparing"
        print(f"\nPass {pass_index + 1}, {action} positions {j} and {j + 1}")

        pause_for_user(
            mode=mode,
            delay_seconds=float(settings["delay_seconds"]),
        )

    return bubble_sort(values, on_step=on_step)


def run_learning_visual_demo() -> None:
    final_state = visualize_bubble_sort_learning(numbers)
    print("\nFinal state:", final_state)


if __name__ == "__main__":
    run_learning_visual_demo()