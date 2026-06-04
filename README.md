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

### 方式一：直接复制（推荐）

1. 将整个项目复制为 opencode 插件目录下的 `traffic-light/` 子目录：

   ```bash
   # Windows
   xcopy /E opencode-traffic-light %USERPROFILE%\.config\opencode\plugins\traffic-light\

   # macOS/Linux
   cp -r opencode-traffic-light ~/.config/opencode/plugins/traffic-light/
   ```

2. 编辑 `opencode.json`（位于 `~/.config/opencode/`），在 `plugin` 数组中添加：

   ```json
   {
     "plugin": [
       "file:///C:/Users/yourname/.config/opencode/plugins/traffic-light/index.ts"
     ]
   }
   ```

### 方式二：从 GitHub 克隆

```bash
git clone https://github.com/runningwaterpro/opencode-traffic-light.git
cd opencode-traffic-light
npm install          # 安装 TypeScript 类型定义（可选）
```

然后按方式一的步骤复制到插件目录并配置 `opencode.json`。

> 每个插件使用独立子目录，文件命名无需修改，直接复制即可。opencode 的自动发现只扫描 `plugins/` 根目录，因此需要在 `opencode.json` 中用 `file:///` URI 显式引用子目录中的插件。

## 使用

启动 opencode 后，系统托盘会出现交通灯图标：

- 图标颜色和悬停提示反映当前状态
- 黄色闪烁时表示有权限请求或提问等待处理

## 项目结构

```
opencode-traffic-light/
├── index.ts      # 插件主逻辑（TypeScript）
├── tray.py       # Python 托盘脚本（pystray）
├── icons/        # 红绿黄灰四个圆形图标
├── package.json  # npm 依赖（本地开发用）
├── requirements.txt
└── README.md
```

所有文件已按最终安装时的结构命名，复制后无需改名。

## 开发

```bash
npm install
pip install -r requirements.txt
```

## 许可证

MIT
