import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

previous_cursor = None

def init_graph(frame):
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas_graph = FigureCanvasTkAgg(fig, master=frame)
    canvas_graph.get_tk_widget().pack()
    return fig, ax

def update_graph(ax, fig, ping_times):
    global previous_cursor
    ax.clear()
    
    x_positions = range(50)
    colors = [
        "#FF9999" if ping < 0 else
        "#99FF99" if ping < 60 else
        "#FFFF99" if ping < 100 else
        "#FFCC99" if ping >= 100 else "#FF0000"
        for ping in ping_times
    ]
    bars = ax.bar(x_positions, ping_times + [0] * (50 - len(ping_times)), color=colors)
    
    
    
    if previous_cursor:
        previous_cursor.remove()
    
    cursor = mplcursors.cursor(bars, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        if sel.target[1] == -1:
            sel.annotation.set_text("Offline")
        else:
            sel.annotation.set_text(f"{sel.target[1]:.0f} ms")
        sel.annotation.get_bbox_patch().set(fc="orange", alpha=0.8)

    previous_cursor = cursor

    ax.set_title("Ping in time", fontsize=14, fontweight='bold')
    ax.set_xlabel("Tests", fontsize=12)
    ax.set_ylabel("Ping (ms)", fontsize=12)
    ax.set_xlim(-1, 50)
    ax.set_ylim(-1, 200)

    fig.canvas.draw()
