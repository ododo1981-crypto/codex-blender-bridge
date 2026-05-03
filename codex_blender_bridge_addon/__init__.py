bl_info = {
    "name": "Codex Blender Bridge",
    "author": "Codex Blender Bridge contributors",
    "version": (0, 1, 0),
    "blender": (5, 1, 0),
    "location": "Edit > Preferences > Add-ons > Codex Blender Bridge",
    "description": "Starts a local-only Blender bridge on 127.0.0.1:9877.",
    "category": "System",
}

import json
import queue
import socket
import threading
import traceback
from pathlib import Path

import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences, Operator


ADDON_ID = __name__
HOST = "127.0.0.1"

_task_queue = queue.Queue()
_server_thread = None
_server_socket = None
_running = False
_timer_registered = False
_current_port = None


def _addon_preferences():
    return bpy.context.preferences.addons[ADDON_ID].preferences


def _log(message):
    try:
        prefs = _addon_preferences()
        path = Path(bpy.path.abspath(prefs.log_path))
    except Exception:
        path = Path(r"C:\tmp\codex_blender_bridge.log")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(message + "\n")
    except Exception:
        pass


def _scene_info():
    scene = bpy.context.scene
    return {
        "file": bpy.data.filepath,
        "frame": scene.frame_current,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "object_count": len(bpy.data.objects),
        "camera": scene.camera.name if scene.camera else None,
        "objects": [
            {
                "name": obj.name,
                "type": obj.type,
                "location": [float(v) for v in obj.location],
                "rotation": [float(v) for v in obj.rotation_euler],
                "scale": [float(v) for v in obj.scale],
            }
            for obj in bpy.data.objects[:200]
        ],
    }


def _execute_python(code):
    namespace = {"bpy": bpy}
    exec(code, namespace, namespace)
    return {"ok": True}


def _run_in_blender_thread(func, *args, **kwargs):
    done = threading.Event()
    box = {}
    _task_queue.put((func, args, kwargs, done, box))
    done.wait(180)
    if "error" in box:
        raise box["error"]
    if "result" not in box:
        raise TimeoutError("Timed out waiting for Blender main thread")
    return box["result"]


def _pump_tasks():
    while True:
        try:
            func, args, kwargs, done, box = _task_queue.get_nowait()
        except queue.Empty:
            break
        try:
            box["result"] = func(*args, **kwargs)
        except Exception as exc:
            box["error"] = exc
            box["traceback"] = traceback.format_exc()
        finally:
            done.set()
    return 0.05 if _running else None


def _handle_command(command):
    command_type = command.get("type")
    params = command.get("params") or {}
    prefs = _addon_preferences()

    if prefs.auth_token:
        token = params.get("token") or command.get("token")
        if token != prefs.auth_token:
            return {"status": "error", "message": "invalid auth token"}

    if command_type == "ping":
        return {
            "status": "ok",
            "result": {
                "message": "codex-blender-bridge addon alive",
                "host": HOST,
                "port": _current_port,
                "file": bpy.data.filepath,
            },
        }
    if command_type == "get_scene_info":
        return {"status": "ok", "result": _run_in_blender_thread(_scene_info)}
    if command_type == "execute_blender_code":
        return {"status": "ok", "result": _run_in_blender_thread(_execute_python, params.get("code", ""))}
    return {"status": "error", "message": f"unknown command: {command_type}"}


def _client_thread(conn):
    try:
        chunks = []
        conn.settimeout(3)
        while True:
            try:
                chunk = conn.recv(65536)
            except socket.timeout:
                break
            if not chunk:
                break
            chunks.append(chunk)
            try:
                json.loads(b"".join(chunks).decode("utf-8"))
                break
            except json.JSONDecodeError:
                continue
        command = json.loads(b"".join(chunks).decode("utf-8"))
        response = _handle_command(command)
    except Exception as exc:
        response = {"status": "error", "message": str(exc), "traceback": traceback.format_exc()}
    try:
        conn.sendall(json.dumps(response, ensure_ascii=False).encode("utf-8"))
    finally:
        conn.close()


def _server_loop(port):
    global _server_socket, _running, _current_port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((HOST, port))
    except OSError as exc:
        _log(f"port unavailable {HOST}:{port}: {exc}")
        _running = False
        _current_port = None
        return
    sock.listen(8)
    sock.settimeout(1)
    _server_socket = sock
    _current_port = port
    _log(f"listening on {HOST}:{port}")
    while _running:
        try:
            conn, _addr = sock.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        threading.Thread(target=_client_thread, args=(conn,), daemon=True).start()
    try:
        sock.close()
    except Exception:
        pass
    _server_socket = None
    _current_port = None
    _log("server stopped")


def start_server():
    global _server_thread, _running, _timer_registered
    if _running:
        return
    prefs = _addon_preferences()
    _running = True
    if not _timer_registered:
        bpy.app.timers.register(_pump_tasks, persistent=True)
        _timer_registered = True
    _server_thread = threading.Thread(target=_server_loop, args=(prefs.port,), daemon=True)
    _server_thread.start()
    _log("server start requested")


def stop_server():
    global _running, _server_socket
    _running = False
    if _server_socket:
        try:
            _server_socket.close()
        except Exception:
            pass
        _server_socket = None


class CODEXBRIDGE_OT_start(Operator):
    bl_idname = "codex_bridge.start"
    bl_label = "Start Codex Bridge"
    bl_description = "Start the local Codex Blender Bridge server"

    def execute(self, _context):
        start_server()
        return {"FINISHED"}


class CODEXBRIDGE_OT_stop(Operator):
    bl_idname = "codex_bridge.stop"
    bl_label = "Stop Codex Bridge"
    bl_description = "Stop the local Codex Blender Bridge server"

    def execute(self, _context):
        stop_server()
        return {"FINISHED"}


class CODEXBRIDGE_OT_restart(Operator):
    bl_idname = "codex_bridge.restart"
    bl_label = "Restart Codex Bridge"
    bl_description = "Restart the local Codex Blender Bridge server"

    def execute(self, _context):
        stop_server()
        start_server()
        return {"FINISHED"}


class CodexBridgePreferences(AddonPreferences):
    bl_idname = ADDON_ID

    auto_start: BoolProperty(
        name="Auto Start",
        description="Start the bridge when the add-on is enabled or Blender starts",
        default=True,
    )
    port: IntProperty(
        name="Port",
        description="Local bridge port",
        default=9877,
        min=1024,
        max=65535,
    )
    log_path: StringProperty(
        name="Log Path",
        description="Path for bridge logs",
        subtype="FILE_PATH",
        default=r"C:\tmp\codex_blender_bridge.log",
    )
    auth_token: StringProperty(
        name="Auth Token",
        description="Optional token. If set, clients must include it as params.token or command token.",
        subtype="PASSWORD",
        default="",
    )

    def draw(self, _context):
        layout = self.layout
        layout.label(text="Local bridge: 127.0.0.1")
        layout.prop(self, "port")
        layout.prop(self, "auto_start")
        layout.prop(self, "log_path")
        layout.prop(self, "auth_token")
        status = f"Running on {HOST}:{_current_port}" if _running else "Stopped"
        layout.label(text=f"Status: {status}")
        row = layout.row(align=True)
        row.operator("codex_bridge.start", icon="PLAY")
        row.operator("codex_bridge.stop", icon="PAUSE")
        row.operator("codex_bridge.restart", icon="FILE_REFRESH")
        layout.separator()
        layout.label(text="Security: only use this on trusted local machines.")
        layout.label(text="It can execute Python code inside Blender.")


classes = (
    CODEXBRIDGE_OT_start,
    CODEXBRIDGE_OT_stop,
    CODEXBRIDGE_OT_restart,
    CodexBridgePreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    _log("register Codex Blender Bridge")
    try:
        if _addon_preferences().auto_start:
            start_server()
    except Exception as exc:
        _log(f"auto start failed: {exc}")


def unregister():
    _log("unregister Codex Blender Bridge")
    stop_server()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
