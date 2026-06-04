# opencode 交通灯托盘插件

一个 opencode 插件，在系统托盘显示交通灯图标，实时反映 opencode 的状态。

## 功能

- 🟢 绿色常亮：opencode 空闲
- 🔴 红色常亮：opencode 正在思考/处理中
- 🟡 黄色闪烁（500ms 交替黄/灰）：opencode 等待用户输入（权限/提问）
- 不同状态下鼠标悬停提示不同文字（空闲 / 处理中... / 等待您的输入）

## 安装

### 1. 安装 Python 依赖

```bash
pip install pystray Pillow
```

### 2. 放置插件文件

将 `index.ts`、`tray.py`、`icons/`、`package.json` 放入 opencode 插件目录：

```bash
# Windows
%USERPROFILE%\.config\opencode\plugins\

# macOS/Linux
~/.config/opencode/plugins/
```

插件文件放入后会被 opencode 自动加载，无需修改 `opencode.json`。

### 3. 配置 npm 依赖

如需使用外部 npm 包，在 `~/.config/opencode/` 下创建 `package.json`：

```json
{
  "dependencies": {
    "@opencode-ai/plugin": "^1.15.13"
  }
}
```

## 使用

启动 opencode 后，系统托盘会出现交通灯图标：

- 图标颜色和悬停提示反映当前状态
- 黄色闪烁时表示有权限请求或提问等待处理

## 开发

### 项目结构

```
opencode-traffic-light/
├── index.ts          # 插件主逻辑（TypeScript）
├── tray.py           # Python 托盘脚本（pystray）
├── icons/            # 红绿黄灰四个圆形图标
├── package.json
└── requirements.txt
```

### 本地开发

```bash
# 安装依赖
npm install
pip install -r requirements.txt
```

## 许可证

MIT
