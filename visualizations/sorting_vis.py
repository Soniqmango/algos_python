import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from algorithms.sorting import insertion_sort_steps, merge_sort_steps, quick_sort_steps


def _style_colors(n, state):
    colors = ["#9ebcda"] * n
    action = state.get("action")
    indices = state.get("indices", [])
    pivot = state.get("pivot")

    if action == "compare":
        for idx in indices:
            colors[idx] = "#fdae61"
    elif action == "swap":
        for idx in indices:
            colors[idx] = "#d7191c"
    elif action == "shift" or action == "insert":
        for idx in indices:
            colors[idx] = "#2b83ba"
    elif action == "write":
        for idx in indices:
            colors[idx] = "#1a9641"
    elif action == "pivot":
        if pivot is not None:
            colors[pivot] = "#8e44ad"
    elif action == "select":
        for idx in indices:
            colors[idx] = "#f46d43"

    if pivot is not None and action not in {"pivot", "compare", "swap"}:
        colors[pivot] = "#8e44ad"

    return colors


def _build_animation(frames, title, interval):
    if not frames:
        raise ValueError("No frames to animate.")

    array, state = frames[0]
    n = len(array)
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.22)
    bars = ax.bar(range(n), array, color=_style_colors(n, state), edgecolor="black")
    ax.set_title(title)
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max(array) * 1.1 if array else 1)
    ax.set_ylabel("Value")
    ax.set_xlabel("Index")

    fig.subplots_adjust(bottom=0.30)
    annotation = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10, va="top")

    current_frame = {"index": 0}
    paused = {"value": False}
    timer_running = {"value": False}

    def draw_frame(frame_index):
        current_frame["index"] = frame_index
        array, state = frames[frame_index]

        for bar, height in zip(bars, array):
            bar.set_height(height)

        colors = _style_colors(n, state)
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        action = state.get("action", "")
        low = state.get("low")
        high = state.get("high")
        annotation.set_text(
            f"Action: {action}\nIndices: {state.get('indices', [])}\nRange: [{low}, {high}]"
        )
        fig.canvas.draw_idle()

    def step_frame():
        next_index = current_frame["index"] + 1
        if next_index < len(frames):
            draw_frame(next_index)
        else:
            timer.stop()
            timer_running["value"] = False
            paused["value"] = True
            pause_button.label.set_text("Play")

    def on_pause(event):
        if paused["value"]:
            timer.start()
            timer_running["value"] = True
            paused["value"] = False
            pause_button.label.set_text("Pause")
        else:
            timer.stop()
            timer_running["value"] = False
            paused["value"] = True
            pause_button.label.set_text("Play")

    def on_step_forward(event):
        if timer_running["value"]:
            timer.stop()
            timer_running["value"] = False
            paused["value"] = True
            pause_button.label.set_text("Play")

        step_frame()

    def on_step_back(event):
        if timer_running["value"]:
            timer.stop()
            timer_running["value"] = False
            paused["value"] = True
            pause_button.label.set_text("Play")

        prev_index = max(0, current_frame["index"] - 1)
        draw_frame(prev_index)

    button_width = 0.16
    button_height = 0.06
    button_y = 0.08

    pause_ax = fig.add_axes([0.28, button_y, button_width, button_height])
    back_ax = fig.add_axes([0.10, button_y, button_width, button_height])
    forward_ax = fig.add_axes([0.46, button_y, button_width, button_height])
    speed_ax = fig.add_axes([0.65, button_y, 0.28, button_height])

    pause_button = Button(pause_ax, "Pause")
    back_button = Button(back_ax, "Back")
    forward_button = Button(forward_ax, "Next")

    timer = fig.canvas.new_timer(interval=interval)
    timer.add_callback(step_frame)

    from matplotlib.widgets import Slider
    speed_slider = Slider(
        speed_ax,
        "Speed",
        valmin=20,
        valmax=500,
        valinit=interval,
        valfmt="%0.0f ms",
    )

    def on_speed_change(value):
        timer.interval = int(value)
        if not paused["value"]:
            timer.stop()
            timer.start()

    speed_slider.on_changed(on_speed_change)

    pause_button.on_clicked(on_pause)
    back_button.on_clicked(on_step_back)
    forward_button.on_clicked(on_step_forward)

    # Keep strong references to all widgets to prevent garbage collection
    fig._widgets = [pause_button, back_button, forward_button, speed_slider]

    draw_frame(0)
    timer.start()
    timer_running["value"] = True

    return timer


def visualize_sort(steps, title="Sorting Visualization", interval=100, show=True):
    """Animate a generator of sort states."""
    frames = list(steps)
    anim = _build_animation(frames, title, interval)
    if show:
        plt.show()
    return anim


def animate_insertion_sort(arr, interval=100, show=True):
    return visualize_sort(insertion_sort_steps(arr), title="Insertion Sort", interval=interval, show=show)


def animate_merge_sort(arr, interval=100, show=True):
    return visualize_sort(merge_sort_steps(arr), title="Merge Sort", interval=interval, show=show)


def animate_quick_sort(arr, interval=100, show=True):
    return visualize_sort(quick_sort_steps(arr), title="Quick Sort", interval=interval, show=show)


if __name__ == "__main__":
    import random

    example = random.sample(range(1, 31), 30)
    print("Running insertion sort animation...")
    animate_insertion_sort(example, interval=75)
    print("Running merge sort animation...")
    animate_merge_sort(example, interval=75)
    print("Running quick sort animation...")
    animate_quick_sort(example, interval=75)