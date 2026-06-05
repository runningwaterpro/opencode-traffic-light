[English](README.en.md) | [中文](README.md)

# opencode Traffic Light Tray Plugin

A system tray plugin for opencode that shows a traffic light icon reflecting the current status in real time.

## Features

- 🟢 Green steady: opencode is idle
- 🔴 Red steady: opencode is thinking/processing
- 🟡 Yellow blinking (500ms yellow/gray): waiting for user input (permission or question)
- Different tooltips on hover per state (Idle / Processing... / Awaiting input)
- Windows notification popup on state changes (e.g., "Processing complete", "Permission required")

## Requirements

- Python 3 with [pystray](https://pypi.org/project/pystray/) and [Pillow](https://pypi.org/project/Pillow/):
  ```bash
  pip install pystray Pillow
  ```

## Installation

Copy the `plugin/` folder to the opencode plugins directory and rename it to `traffic-light/`:

```bash
# Windows
xcopy /E plugin %USERPROFILE%\.config\opencode\plugins\traffic-light\

# macOS/Linux
cp -r plugin ~/.config/opencode/plugins/traffic-light/
```

Then edit `opencode.json` (in `~/.config/opencode/`) and add the path to the `plugin` array:

```json
{
  "plugin": [
    "file:///C:/Users/yourname/.config/opencode/plugins/traffic-light/index.ts"
  ]
}
```

> Each plugin should use its own subdirectory. opencode's auto-discovery only scans the root of `plugins/`, so you need to reference the subdirectory with a `file:///` URI.

## Usage

After launching opencode, a traffic light icon appears in the system tray:

- Icon color and tooltip reflect the current status
- Yellow blinking indicates pending permission requests or questions
- Right-click "Exit" to quit

## OpenCode Web

Especially useful with [OpenCode Web](https://github.com/open-code-ai/opencode) — when accessing from a mobile browser, the page may not auto-refresh and can appear stuck on "thinking". Just glance at the tray icon: green means the agent is done, refresh the page and see the result.

## Project Structure

```
opencode-traffic-light/
├── plugin/          # ← copy this folder to plugins/traffic-light/
│   ├── index.ts
│   ├── tray.py
│   └── icons/
├── README.md
└── requirements.txt
```

## License

MIT
