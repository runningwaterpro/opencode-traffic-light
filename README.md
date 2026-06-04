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

### 方式一：直接复制文件（推荐）

1. 在 opencode 插件目录下创建 `traffic-light/` 子目录：

   | 平台 | 插件目录 |
   |------|---------|
   | Windows | `%USERPROFILE%\.config\opencode\plugins\` |
   | macOS/Linux | `~/.config/opencode/plugins/` |

2. 将 `index.ts`、`tray.py`、`icons/` 复制到该子目录。

3. 编辑 `opencode.json`（与 `plugins/` 同目录），在 `plugin` 数组中添加 `file:///` 路径：

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

然后在插件目录下创建 `traffic-light/` 子目录，将 `index.ts`、`tray.py`、`icons/` 复制进去，并配置 `opencode.json` 添加 `file:///` 路径。

> 每个插件使用独立子目录可以避免文件命名冲突，项目结构更清晰。虽然 opencode 的自动发现只扫描 `plugins/` 根目录的 `.ts` 文件，但通过 `opencode.json` 的 `file:///` URI 可以加载子目录中的插件。

## 使用

启动 opencode 后，系统托盘会出现交通灯图标：

- 图标颜色和悬停提示反映当前状态
- 黄色闪烁时表示有权限请求或提问等待处理

## 开发

### 项目结构

```
opencode-traffic-light/
├── traffic-light.ts  # 插件主逻辑（TypeScript，开发入口）
├── tray.py           # Python 托盘脚本（pystray）
├── icons/            # 红绿黄灰四个圆形图标
├── package.json      # npm 依赖（本地开发用）
└── requirements.txt  # Python 依赖
```

注：安装到 `plugins/` 时，需将 `traffic-light.ts` 重命名为 `index.ts` 并放入 `traffic-light/` 子目录。

### 本地开发

```bash
# 安装依赖
npm install
pip install -r requirements.txt
```

## 许可证

MIT
