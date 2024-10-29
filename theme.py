import platform
import subprocess
import winreg
import matplotlib.pyplot as plt

def set_light_mode(root, canvas, frame, ax, fig, network_label):
    root.configure(bg='white')
    canvas.config(bg='white')
    frame.config(bg='white')
    network_label.config(bg='white', fg='black') 
    apply_style(ax, fig, "#000000", "#FFFFFF", "#DDDDDD")

def set_dark_mode(root, canvas, frame, ax, fig, network_label):
    root.configure(bg='#2E2E2E')
    canvas.config(bg='#2E2E2E')
    frame.config(bg='#2E2E2E')
    network_label.config(bg='#2E2E2E', fg='white')
    apply_style(ax, fig, "#FFFFFF", "#2E2E2E", "#555555")

def apply_style(ax, fig, text_color, bg_color, bar_color):

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    plt.rcParams['text.color'] = text_color
    plt.rcParams['axes.labelcolor'] = text_color
    plt.rcParams['xtick.color'] = text_color 
    plt.rcParams['ytick.color'] = text_color 
    plt.rcParams['axes.titlecolor'] = text_color 

    ax.spines['bottom'].set_color(text_color)
    ax.spines['top'].set_color(text_color)
    ax.spines['left'].set_color(text_color)
    ax.spines['right'].set_color(text_color)

    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)

    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)

    ax.title.set_color(text_color)

    fig.canvas.draw_idle()

def set_auto_mode(root, canvas, frame, ax, fig, network_label):
    if platform.system() == 'Windows':
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            if value == 0:
                set_dark_mode(root, canvas, frame, ax, fig, network_label)
            else:
                set_light_mode(root, canvas, frame, ax, fig, network_label)
            winreg.CloseKey(key)
        except:
            set_light_mode(root, canvas, frame, ax, fig, network_label)
    elif platform.system() == 'Darwin':
        result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True)
        if 'Dark' in result.stdout:
            set_dark_mode(root, canvas, frame, ax, fig, network_label)
        else:
            set_light_mode(root, canvas, frame, ax, fig, network_label)
    else:
        set_light_mode(root, canvas, frame, ax, fig, network_label)
