import type { Plugin } from "@opencode-ai/plugin"
import { spawn, type ChildProcess } from "child_process"
import { join, dirname } from "path"
import { fileURLToPath } from "url"

const pluginDir = dirname(fileURLToPath(import.meta.url))

type PendingType = "permission" | "question"
type YellowSubtype = PendingType | "mixed"

const plugin: Plugin = async () => {
  let proc: ChildProcess | null = null
  let retryCount = 0
  const maxRetries = 3

  const busySessions = new Set<string>()
  const pendingSessions = new Map<string, PendingType>()

  function send(msg: Record<string, unknown>) {
    if (proc?.stdin) {
      proc.stdin.write(JSON.stringify(msg) + "\n")
    }
  }

  function update() {
    let overall: "red" | "yellow" | "green" = "green"
    let yellowSubtype: YellowSubtype | undefined

    if (pendingSessions.size > 0) {
      overall = "yellow"
      const types = new Set(pendingSessions.values())
      yellowSubtype = types.size === 1 ? [...types][0] : "mixed"
    } else if (busySessions.size > 0) {
      overall = "red"
    }

    const tooltips: Record<string, string> = {
      green: "OpenCode Idle",
      red: "OpenCode Busy...",
    }
    const yellowTooltips: Record<YellowSubtype, string> = {
      permission: "OpenCode awaits permission",
      question: "OpenCode awaits input",
      mixed: "OpenCode is waiting",
    }

    const tooltip = overall === "yellow" && yellowSubtype
      ? yellowTooltips[yellowSubtype]
      : tooltips[overall]

    send({
      type: "state-update",
      overall,
      yellowSubtype: overall === "yellow" ? yellowSubtype : undefined,
      tooltip,
    })
  }

  let stdoutBuf = ""
  const MAX_STDOUT_BUF = 65536
  let trayReady = false

  function startTray() {
    proc = spawn("pythonw", [join(pluginDir, "tray.py")], {
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
      env: { ...process.env, PYTHONIOENCODING: "utf-8" },
    })
    retryCount = 0

    proc.stdout?.on("data", (data: Buffer) => {
      stdoutBuf += data.toString()
      if (stdoutBuf.length > MAX_STDOUT_BUF) stdoutBuf = stdoutBuf.slice(-MAX_STDOUT_BUF)
      const lines = stdoutBuf.split("\n")
      stdoutBuf = lines.pop() ?? ""

      for (const line of lines) {
        const trimmed = line.trim()
        if (!trimmed) continue
        try {
          const msg = JSON.parse(trimmed)
          if (msg.type === "tray-ready" && !trayReady) { trayReady = true; update() }
        } catch {
          console.error("[traffic-light] invalid message:", trimmed.slice(0, 200))
        }
      }
    })

    proc.stderr?.on("data", (data: Buffer) => {
      console.error("[traffic-light]", data.toString().trim())
    })

    proc.on("exit", (code) => {
      proc = null
      if (code !== 0 && code !== null && retryCount < maxRetries) {
        retryCount++
        const delay = retryCount * 1000
        console.error(`[traffic-light] process exited (${code}), retry ${retryCount}/${maxRetries} in ${delay}ms`)
        setTimeout(startTray, delay)
      }
    })
  }

  startTray()

  return {
    dispose: async () => {
      const p = proc
      if (p) {
        send({ type: "exit" })
        await Promise.race([
          new Promise<void>(resolve => p.once("exit", () => resolve())),
          new Promise<void>(resolve => setTimeout(resolve, 3000)),
        ])
        if (!p.killed) p.kill()
        proc = null
      }
    },

    event: async ({ event }) => {
      const { type, properties } = event as any

      if (type === "session.status" && (properties.status.type === "busy" || properties.status.type === "retry")) {
        busySessions.add(properties.sessionID)
        update()
      }

      if (type === "session.idle") {
        busySessions.delete(properties.sessionID)
        pendingSessions.delete(properties.sessionID)
        update()
      }

      if (type === "permission.asked") {
        pendingSessions.set(properties.sessionID, "permission")
        update()
      }

      if (type === "question.asked") {
        pendingSessions.set(properties.sessionID, "question")
        update()
      }

      if (type === "permission.replied" && pendingSessions.get(properties.sessionID) === "permission") {
        pendingSessions.delete(properties.sessionID)
        update()
      }

      if (type === "question.replied" && pendingSessions.get(properties.sessionID) === "question") {
        pendingSessions.delete(properties.sessionID)
        update()
      }
    },
  }
}

export default plugin
