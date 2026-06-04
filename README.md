# opencode 交通灯托盘插件

一个 opencode 插件，在系统托盘显示交通灯图标，实时反映 opencode 的状态。

## 功能

- 🟢 绿色常亮：opencode 空闲
- 🔴 红色常亮：opencode 正在思考/处理中
- 🟡 黄色闪烁（500ms 交替黄/灰）：opencode 等待用户输入（权限/提问）
- 不同状态下鼠标悬停提示不同文字（空闲 / 处理中... / 等待您的输入）

## 前置要求

- Python 3，已安装 [pystray](https://pypi.org/project/pystray/) 和 [Pillow](https://pypi.org/project/Pillow/)：
  ```bash
  pip install pystray Pillow
  ```

## 安装

将 `plugin/` 文件夹复制到 opencode 插件目录下，重命名为 `traffic-light/`：

```bash
# Windows
xcopy /E plugin %USERPROFILE%\.config\opencode\plugins\traffic-light\

# macOS/Linux
cp -r plugin ~/.config/opencode/plugins/traffic-light/
```

然后编辑 `opencode.json`（位于 `~/.config/opencode/`），在 `plugin` 数组中添加：

```json
{
  "plugin": [
    "file:///C:/Users/yourname/.config/opencode/plugins/traffic-light/index.ts"
  ]
}
```

> 每个插件使用独立子目录，文件无需改名，复制即可用。opencode 的自动发现只扫描 `plugins/` 根目录，需要在 `opencode.json` 中用 `file:///` URI 显式引用子目录中的插件。

## 使用

启动 opencode 后，系统托盘会出现交通灯图标：

- 图标颜色和悬停提示反映当前状态
- 黄色闪烁时表示有权限请求或提问等待处理

## 项目结构

```
opencode-traffic-light/
├── plugin/          # ← 复制这个文件夹到 plugins/traffic-light/
│   ├── index.ts
│   ├── tray.py
│   └── icons/
├── README.md
└── requirements.txt
```

## 开发

```bash
npm install
pip install -r requirements.txt
```

## 许可证

MIT
