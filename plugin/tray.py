#!/usr/bin/env python3
"""opencode 交通灯托盘图标"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
import json
import threading
import pystray
from PIL import Image, ImageDraw
from pathlib import Path

# 颜色定义
COLORS = {
    "red": (220, 20, 20),
    "green": (20, 180, 20),
    "yellow": (247, 181, 0),
    "gray": (128, 128, 128)
}

class TrafficLightTray:
    def __init__(self):
        self.icon = None
        self.icons = {}
        self.current_color = "green"
        self.blinking = False
        self.blink_state = False
        self.blink_timer = None
        self.load_icons()
    
    def load_icons(self):
        """加载所有图标"""
        icons_dir = Path(__file__).parent / "icons"
        for color_name in COLORS:
            icon_path = icons_dir / f"{color_name}.png"
            if icon_path.exists():
                self.icons[color_name] = Image.open(icon_path)
            else:
                # 如果图标文件不存在，动态生成
                self.icons[color_name] = self.create_icon(color_name)
    
    def create_icon(self, color_name):
        """动态创建圆形图标"""
        color = COLORS.get(color_name, COLORS["gray"])
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 60, 60], fill=color)
        return img
    
    def send_message(self, msg):
        """发送消息到 Node.js"""
        print(json.dumps(msg))
        sys.stdout.flush()
    
    def read_stdin(self):
        """从 stdin 读取 Node.js 发送的消息"""
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            try:
                msg = json.loads(line.strip())
                self.handle_message(msg)
            except json.JSONDecodeError:
                pass
    
    def handle_message(self, msg):
        """处理收到的消息"""
        msg_type = msg.get("type")
        
        if msg_type == "state-update":
            state = msg.get("state", {})
            overall = state.get("overall", "green")
            tooltip = msg.get("tooltip", "")
            self.update_icon(overall, tooltip)
        
        elif msg_type == "exit":
            if self.icon:
                self.icon.stop()
    
    def update_icon(self, color_name, tooltip=""):
        """更新托盘图标颜色和悬停提示"""
        old_color = self.current_color
        self.current_color = color_name
        self.stop_blinking()

        if tooltip and self.icon:
            self.icon.title = tooltip

        if color_name == "yellow":
            self.start_blinking()
            # 黄色：等待输入，弹通知提醒
            self.show_notification("OpenCode 需要您的输入", tooltip or "OpenCode 需要您的输入")
        elif self.icon and color_name in self.icons:
            self.icon.icon = self.icons[color_name]
            # 红→绿：处理完成，弹通知
            if old_color == "red" and color_name == "green":
                self.show_notification("OpenCode 处理完成", tooltip or "OpenCode 空闲")

    def show_notification(self, title, message):
        """弹出 Windows 通知（显示约 5-10 秒后自动消失）"""
        try:
            if self.icon:
                self.icon.notify(message, title)
        except Exception:
            pass

    def start_blinking(self):
        """启动黄色闪烁（500ms 交替黄/灰）"""
        if self.blinking:
            return
        self.blinking = True
        self.blink_state = True
        self._blink_tick()

    def stop_blinking(self):
        """停止闪烁"""
        self.blinking = False
        if self.blink_timer:
            self.blink_timer.cancel()
            self.blink_timer = None

    def _blink_tick(self):
        if not self.blinking or not self.icon:
            return
        self.icon.icon = self.icons.get("yellow" if self.blink_state else "gray")
        self.blink_state = not self.blink_state
        self.blink_timer = threading.Timer(0.5, self._blink_tick)
        self.blink_timer.daemon = True
        self.blink_timer.start()
    
    def run(self):
        """运行托盘图标"""
        # 创建初始图标（绿色）
        self.icon = pystray.Icon(
            "opencode",
            self.icons.get("green", self.create_icon("green")),
            "OpenCode 空闲"
        )
        
        # 设置点击事件
        self.icon.menu = pystray.Menu(
            pystray.MenuItem("退出", self.on_exit)
        )
        
        # 在后台线程中读取 stdin
        stdin_thread = threading.Thread(target=self.read_stdin, daemon=True)
        stdin_thread.start()
        
        # 通知 Node.js 已就绪
        self.send_message({"type": "tray-ready"})
        
        # 运行托盘图标
        self.icon.run()
    
    def on_exit(self, icon, item):
        """退出托盘"""
        self.send_message({"type": "tray-exit"})
        icon.stop()

if __name__ == "__main__":
    tray = TrafficLightTray()
    tray.run()
