import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button, Slider

from algorithms.graph import bfs_steps, dfs_steps, bidirectional_bfs_steps

COLOR_LIST = [
    "#ffffff",  # open
    "#000000",  # wall
    "#a6cee3",  # visited
    "#1f78b4",  # frontier
    "#e31a1c",  # current
    "#33a02c",  # path
    "#ffff33",  # start
    "#ff7f00",  # end
    "#b15928",  # meeting
]

CMAP = ListedColormap(COLOR_LIST)


def _grid_frame(grid, state):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    display = [[1 if grid[r][c] == 1 else 0 for c in range(cols)] for r in range(rows)]

    visited = state.get("visited", set())
    start_visited = state.get("start_visited", set())
    end_visited = state.get("end_visited", set())
    frontier = state.get("frontier", [])
    start_frontier = state.get("start_frontier", [])
    end_frontier = state.get("end_frontier", [])
    path = state.get("path", [])
    current = state.get("current")
    meeting_node = state.get("meeting_node")
    start = state.get("start")
    end = state.get("end")

    for r, c in visited:
        if display[r][c] == 0:
            display[r][c] = 2
    for r, c in start_visited:
        if display[r][c] == 0:
            display[r][c] = 2
    for r, c in end_visited:
        if display[r][c] == 0:
            display[r][c] = 2
    for r, c in frontier:
        if display[r][c] in {0, 2}:
            display[r][c] = 3
    for r, c in start_frontier:
        if display[r][c] in {0, 2}:
            display[r][c] = 3
    for r, c in end_frontier:
        if display[r][c] in {0, 2}:
            display[r][c] = 3
    if current is not None:
        r, c = current
        display[r][c] = 4
    if meeting_node is not None:
        r, c = meeting_node
        display[r][c] = 8
    for r, c in path:
        display[r][c] = 5
    if start is not None:
        r, c = start
        display[r][c] = 6
    if end is not None:
        r, c = end
        display[r][c] = 7

    return display


def _build_grid_animation(frames, grid, title, interval):
    if not frames:
        raise ValueError("No frames to animate.")

    state = frames[0]
    display = _grid_frame(grid, state)
    rows = len(display)
    cols = len(display[0]) if rows else 0

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.30)
    img = ax.imshow(display, cmap=CMAP, vmin=0, vmax=len(COLOR_LIST) - 1, interpolation="nearest")
    ax.set_title(title)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([x - 0.5 for x in range(1, cols)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, rows)], minor=True)
    ax.grid(which="minor", color="#cccccc", linestyle="-", linewidth=0.5)

    annotation = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=9, va="top")

    state_text = {
        "visit": "Visiting",
        "discover": "Discovered",
        "enqueue": "Enqueued",
        "push": "Pushed",
        "path": "Path Found",
        "meet": "Meeting",
        "start": "Start",
    }

    current_frame = {"index": 0}
    paused = {"value": False}
    timer_running = {"value": False}

    def draw_frame(frame_index):
        current_frame["index"] = frame_index
        state = frames[frame_index]
        display = _grid_frame(grid, state)
        img.set_data(display)

        action = state.get("action", "")
        description = state_text.get(action, action.capitalize())
        annotation.set_text(
            f"Action: {description}\nFrame: {frame_index + 1}/{len(frames)}\nVisited: {len(state.get('visited', state.get('start_visited', set())))}"
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
    speed_slider = Slider(speed_ax, "Speed", 20, 500, valinit=interval, valfmt="%0.0f ms")

    timer = fig.canvas.new_timer(interval=interval)
    timer.add_callback(step_frame)

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


def visualize_graph(steps, grid, title="Graph Search Visualization", interval=100, show=True):
    frames = list(steps)
    anim = _build_grid_animation(frames, grid, title, interval)
    if show:
        plt.show()
    return anim


def animate_bfs(grid, start, end, interval=100, show=True):
    return visualize_graph(bfs_steps(grid, start, end), grid, title="BFS", interval=interval, show=show)


def animate_dfs(grid, start, end, interval=100, show=True):
    return visualize_graph(dfs_steps(grid, start, end), grid, title="DFS", interval=interval, show=show)


def animate_bidirectional_bfs(grid, start, end, interval=100, show=True):
    return visualize_graph(bidirectional_bfs_steps(grid, start, end), grid, title="Bidirectional BFS", interval=interval, show=show)


if __name__ == "__main__":
    import random

    grid = [[0 if random.random() > 0.25 else 1 for _ in range(20)] for _ in range(12)]
    start = (0, 0)
    end = (11, 19)
    grid[start[0]][start[1]] = 0
    grid[end[0]][end[1]] = 0

    animate_bfs(grid, start, end, interval=100)
    animate_dfs(grid, start, end, interval=100)
    animate_bidirectional_bfs(grid, start, end, interval=100)