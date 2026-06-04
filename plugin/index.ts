import type { Plugin } from "@opencode-ai/plugin"
import { spawn, ChildProcess } from "child_process"
import { join, dirname } from "path"
import { fileURLToPath } from "url"

const pluginDir = dirname(fileURLToPath(import.meta.url))

// 状态类型定义
type TrayState = {
  overall: "red" | "yellow" | "green"
  pendingSessions: Array<{
    sessionID: string
    type: "permission" | "question"
    timestamp: number
  }>
}

type SessionStatus = {
  sessionID: string
  status: "idle" | "busy" | "retry"
}

// 插件主逻辑
const trafficLightPlugin: Plugin = async ({ client, project, directory }) => {
  let pythonProcess: ChildProcess | null = null
  let trayState: TrayState = {
    overall: "green",
    pendingSessions: []
  }
  
  // session 状态追踪
  const sessionStatuses = new Map<string, SessionStatus>()

  // 启动 Python 托盘进程
  function startTrayProcess() {
    const scriptPath = join(pluginDir, "tray.py")
    
    pythonProcess = spawn("pythonw", [scriptPath], {
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true
    })

    // 监听 Python 发送的消息
    pythonProcess.stdout?.on("data", (data) => {
      const lines = data.toString().split("\n")
      for (const line of lines) {
        if (line.trim()) {
          try {
            const msg = JSON.parse(line)
            handleTrayMessage(msg)
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    })

    // 监听错误
    pythonProcess.stderr?.on("data", (data) => {
      console.error("Tray process error:", data.toString())
    })

    // 监听进程退出
    pythonProcess.on("exit", () => {
      pythonProcess = null
    })
  }

  // 处理托盘进程消息
  function handleTrayMessage(msg: any) {
    if (msg.type === "tray-ready") {
      // Python 托盘就绪后立即发送初始状态
      updateTrayState()
    }
  }

  // 发送消息给 Python
  function sendToTray(msg: any) {
    if (pythonProcess?.stdin) {
      pythonProcess.stdin.write(JSON.stringify(msg) + "\n")
    }
  }

  const tooltips: Record<string, string> = {
    red: "OpenCode 处理中...",
    yellow: "OpenCode 等待您的输入",
    green: "OpenCode 空闲",
  }

  function updateTrayState() {
    let overall: "red" | "yellow" | "green" = "green"
    
    if (trayState.pendingSessions.length > 0) {
      overall = "yellow"
    } else {
      for (const status of sessionStatuses.values()) {
        if (status.status === "busy" || status.status === "retry") {
          overall = "red"
          break
        }
      }
    }
    
    trayState.overall = overall
    
    sendToTray({
      type: "state-update",
      state: trayState,
      tooltip: tooltips[overall],
    })
  }

  // 启动托盘进程
  startTrayProcess()

  return {
    // 清理函数
    dispose: async () => {
      if (pythonProcess) {
        sendToTray({ type: "exit" })
        pythonProcess.kill()
        pythonProcess = null
      }
    },

    // 事件钩子
    event: async ({ event }) => {
      const eventType = event.type

      // 处理 session 状态变化
      if (eventType === "session.status") {
        const { sessionID, status } = (event as any).properties
        sessionStatuses.set(sessionID, {
          sessionID,
          status: status.type
        })
        updateTrayState()
      }

      // 处理 session 空闲
      if (eventType === "session.idle") {
        const { sessionID } = (event as any).properties
        sessionStatuses.delete(sessionID)
        updateTrayState()
      }

      // 处理权限请求
      if (eventType === "permission.asked") {
        const { sessionID } = (event as any).properties
        trayState.pendingSessions.push({
          sessionID,
          type: "permission",
          timestamp: Date.now()
        })
        updateTrayState()
      }

      // 处理问题请求
      if (eventType === "question.asked") {
        const { sessionID } = (event as any).properties
        trayState.pendingSessions.push({
          sessionID,
          type: "question",
          timestamp: Date.now()
        })
        updateTrayState()
      }

      // 处理权限回复
      if (eventType === "permission.replied") {
        const { sessionID } = (event as any).properties
        trayState.pendingSessions = trayState.pendingSessions.filter(
          s => !(s.sessionID === sessionID && s.type === "permission")
        )
        updateTrayState()
      }

      // 处理问题回复
      if (eventType === "question.replied") {
        const { sessionID } = (event as any).properties
        trayState.pendingSessions = trayState.pendingSessions.filter(
          s => !(s.sessionID === sessionID && s.type === "question")
        )
        updateTrayState()
      }
    }
  }
}

export default trafficLightPlugin
