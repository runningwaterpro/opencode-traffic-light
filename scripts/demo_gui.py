import sys
import threading
from pathlib import Path
from PIL import Image
import pystray
from winotify import Notification as Toast, audio as toast_audio
import tkinter as tk

ICONS_DIR = Path(__file__).parent.parent / "plugin" / "icons"

# Load tray icons (original size, pystray handles display scaling)
def load_tray_icons():
    icons = {}
    for name in ("red", "green", "yellow", "gray"):
        p = ICONS_DIR / f"{name}.png"
        if p.exists():
            with Image.open(p) as img:
                icons[name] = img.copy()
    return icons

TRAY_ICONS = load_tray_icons()

# Load notification icons (64x64 for toast)
def load_notify_icons():
    icons = {}
    tmp = Path(sys.argv[0]).parent
    for name in ("red", "green", "yellow", "gray"):
        p = ICONS_DIR / f"{name}.png"
        if p.exists():
            with Image.open(p) as img:
                resized = img.resize((64, 64), Image.LANCZOS)
                out = tmp / f"{name}_64.png"
                resized.save(out)
                icons[name] = str(out)
    return icons

NOTIFY_ICONS = load_notify_icons()

# --- Tray icon ---
tray_icon = pystray.Icon(
    "opencode-demo",
    TRAY_ICONS.get("green"),
    "OpenCode Demo",
    menu=pystray.Menu(pystray.MenuItem("退出", lambda icon, item: icon.stop())),
)

def set_tray_color(color):
    if color in TRAY_ICONS:
        tray_icon.icon = TRAY_ICONS[color]

# --- Notification ---
NOTIFY_TITLE = "OpenCode"

def notify(message, color="green"):
    icon_path = NOTIFY_ICONS.get(color, NOTIFY_ICONS.get("green"))
    toast = Toast(
        app_id=NOTIFY_TITLE,
        title="",
        msg=message,
        icon=icon_path,
        duration="short",
    )
    toast.tag = "opencode-status"
    toast.set_audio(toast_audio.Default, loop=False)
    toast.show()

# --- Button handlers (tray + notification) ---
def show_permission():
    set_tray_color("yellow")
    notify("需要批准权限", "yellow")

def show_question():
    set_tray_color("yellow")
    notify("需要回答问题", "yellow")

def show_mixed():
    set_tray_color("yellow")
    notify("需要您的输入", "yellow")

def show_done():
    set_tray_color("green")
    notify("处理完成", "green")

def show_busy():
    set_tray_color("red")

# --- Start tray in background thread ---
tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
tray_thread.start()

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Traffic Light Demo")
root.geometry("340x280")
root.resizable(False, False)

tk.Label(root, text="Traffic Light Demo", font=("Segoe UI", 12, "bold")).pack(pady=(15, 5))
tk.Label(root, text="托盘图标 + 通知 同步变化", font=("Segoe UI", 9), fg="gray").pack(pady=(0, 10))

frame = tk.Frame(root)
frame.pack(expand=True)

tk.Button(frame, text="Red (busy)", bg="#ff4444", fg="white", font=("Segoe UI", 9, "bold"),
          width=14, command=show_busy).grid(row=0, column=0, padx=6, pady=4)

tk.Button(frame, text="需要批准权限", bg="#ffcc00", fg="black", font=("Segoe UI", 9, "bold"),
          width=14, command=show_permission).grid(row=0, column=1, padx=6, pady=4)

tk.Button(frame, text="需要回答问题", bg="#ffcc00", fg="black", font=("Segoe UI", 9, "bold"),
          width=14, command=show_question).grid(row=1, column=0, padx=6, pady=4)

tk.Button(frame, text="需要您的输入", bg="#ffcc00", fg="black", font=("Segoe UI", 9, "bold"),
          width=14, command=show_mixed).grid(row=1, column=1, padx=6, pady=4)

tk.Button(frame, text="处理完成", bg="#44cc44", fg="white", font=("Segoe UI", 9, "bold"),
          width=14, command=show_done).grid(row=2, column=0, columnspan=2, pady=4)

root.mainloop()
