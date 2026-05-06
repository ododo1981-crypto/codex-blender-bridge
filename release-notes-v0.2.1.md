# Codex Blender Bridge v0.2.1

Codex-ready local Blender bridge for trusted local AI tools.

This project is unofficial and is not affiliated with OpenAI or Blender Foundation.

## What It Does

- Opens a local-only bridge at `127.0.0.1:9877`.
- Lets trusted local tools inspect the current Blender scene.
- Lets trusted local tools execute Python code inside Blender.
- Keeps Codex workflows separate from common Blender MCP setups that use `9876`.
- Returns clear connection metadata with `ping`, `commands`, and `status`.
- Supports object inspection with `get_object_info`.
- Supports animation inspection with `get_animation_summary`.
- Accepts compatibility aliases such as `execute_code`, `run_code`, `exec`, `scene`, and `list_commands`.
- Captures `stdout` and `stderr` from executed Blender Python.

## Install

Download `codex_blender_bridge_addon.zip`, then install it in Blender:

`Edit > Preferences > Add-ons > Install from Disk`

After installing, enable `Codex Blender Bridge`.

## AI Client Quick Prompt

```text
Codex Blender Bridge v0.2.1: not MCP. Use a TCP socket at 127.0.0.1:9877 with ping, commands, status, get_scene_info, get_object_info, get_animation_summary, and execute_blender_code. execute_code is also accepted.
```

## Commands

```json
{"type":"ping","params":{}}
{"type":"commands","params":{}}
{"type":"status","params":{}}
{"type":"get_scene_info","params":{}}
{"type":"get_object_info","params":{"name":"Cube"}}
{"type":"get_animation_summary","params":{}}
{"type":"execute_blender_code","params":{"code":"import bpy\nprint('OK')"}}
{"type":"execute_code","params":{"code":"import bpy\nprint('OK')"}}
```

## Security

This add-on can execute Python code inside Blender. Enable it only on a trusted machine and do not expose the bridge port to a network.
