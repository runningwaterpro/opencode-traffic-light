import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

import json, threading, pystray
from PIL import Image
from pathlib import Path

NOTIFICATION_TITLE = "OpenCode"

NOTIFICATION_BODIES = {
    "permission": "需要批准权限",
    "question": "需要回答问题",
    "mixed": "需要您的输入",
    "done": "处理完成",
}


class TrafficLightTray:
    def __init__(self):
        self.icon = None
        self.icons: dict[str, Image.Image] = {}
        self.current_color = "green"
        self.blinking = False
        self.blink_state = False
        self.blink_timer = None
        self._load_icons()

    def _load_icons(self):
        d = Path(__file__).parent / "icons"
        for name in ("red", "green", "yellow", "gray"):
            p = d / f"{name}.png"
            if p.exists():
                self.icons[name] = Image.open(p)

    def send(self, msg):
        print(json.dumps(msg, ensure_ascii=False), flush=True)

    def _read_stdin(self):
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            try:
                self._handle(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass

    def _handle(self, msg):
        t = msg.get("type")
        if t == "state-update":
            self._update(
                color=msg.get("overall", "green"),
                tooltip=msg.get("tooltip", ""),
                yellow_subtype=msg.get("yellowSubtype"),
            )
        elif t == "exit" and self.icon:
            self.icon.stop()

    def _update(self, color, tooltip="", yellow_subtype=None):
        old = self.current_color
        self.current_color = color
        self._stop_blink()

        if tooltip and self.icon:
            self.icon.title = tooltip

        if color == "yellow":
            self._start_blink()
            body = NOTIFICATION_BODIES.get(yellow_subtype, NOTIFICATION_BODIES["mixed"])
            self._notify(body)
        elif self.icon and color in self.icons:
            self.icon.icon = self.icons[color]
            if old == "red" and color == "green":
                self._notify(NOTIFICATION_BODIES["done"])

    def _notify(self, message):
        try:
            if self.icon:
                self.icon.notify(message, NOTIFICATION_TITLE)
        except Exception:
            pass

    def _start_blink(self):
        if self.blinking:
            return
        self.blinking = True
        self.blink_state = True
        self._blink_tick()

    def _stop_blink(self):
        self.blinking = False
        if self.blink_timer:
            self.blink_timer.cancel()
            self.blink_timer = None

    def _blink_tick(self):
        if not self.blinking or not self.icon:
            return
        self.icon.icon = self.icons.get("yellow" if self.blink_state else "gray")
        self.blink_state = not self.blink_state
        t = threading.Timer(0.5, self._blink_tick)
        t.daemon = True
        self.blink_timer = t
        t.start()

    def run(self):
        self.icon = pystray.Icon(
            "opencode",
            self.icons.get("green"),
            "OpenCode 空闲",
            menu=pystray.Menu(pystray.MenuItem("退出", self._on_exit)),
        )
        stdin_thread = threading.Thread(target=self._read_stdin, daemon=True)
        stdin_thread.start()
        self.send({"type": "tray-ready"})
        self.icon.run()

    def _on_exit(self, icon, item):
        self.send({"type": "tray-exit"})
        icon.stop()


if __name__ == "__main__":
    TrafficLightTray().run()
