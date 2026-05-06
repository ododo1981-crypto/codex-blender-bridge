# AI Client Prompt

Use this when starting a fresh AI chat that should control Blender through Codex Blender Bridge.

## Short Prompt

```text
Codex Blender Bridge v0.2.1: not MCP. Use a TCP socket at 127.0.0.1:9877 with ping, commands, status, get_scene_info, get_object_info, get_animation_summary, and execute_blender_code. execute_code is also accepted.
```

## Codex Desktop Prompt

```text
Blender has Codex Blender Bridge installed and enabled.
This is not Blender MCP. Do not use Blender MCP tools.

Use the Node REPL tool first, if available, to connect to 127.0.0.1:9877 with a normal TCP socket.
Do not waste time trying Blender MCP.
Do not try multiple shell runtimes before Node REPL.

Send one JSON object per connection.

Examples:
{"type":"ping","params":{}}
{"type":"commands","params":{}}
{"type":"status","params":{}}
{"type":"get_scene_info","params":{}}
{"type":"get_object_info","params":{"name":"Cube"}}
{"type":"get_animation_summary","params":{}}
{"type":"execute_blender_code","params":{"code":"import bpy\nprint('OK')"}}

First send ping, then commands, then get_scene_info. After that, use execute_blender_code or execute_code to edit the scene.
If Node REPL is unavailable and local TCP is blocked, request permission/escalation once.
```

## General Local AI Prompt

```text
Blender has Codex Blender Bridge installed and enabled.
This is not Blender MCP. Do not use Blender MCP tools.

Connect with a normal TCP socket to 127.0.0.1:9877.
Send JSON objects with "type" and "params".

Examples:
{"type":"ping","params":{}}
{"type":"commands","params":{}}
{"type":"status","params":{}}
{"type":"get_scene_info","params":{}}
{"type":"get_object_info","params":{"name":"Cube"}}
{"type":"get_animation_summary","params":{}}
{"type":"execute_blender_code","params":{"code":"import bpy\nprint('OK')"}}

First send ping, then commands, then get_scene_info. Use execute_blender_code or execute_code when you need to edit the scene.
If local TCP or local process execution is blocked by the sandbox, request permission/escalation.
```
