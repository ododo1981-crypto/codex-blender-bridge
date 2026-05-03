# Codex Blender Bridge

Codex Blender Bridge is a small Blender add-on that opens a local-only bridge on `127.0.0.1:9877`.
It lets a trusted local client inspect the current Blender scene and execute Python code inside Blender.

This was made for workflows where Codex or another local automation tool needs a simple, reliable way to talk to Blender without sharing the same port as other Blender MCP setups.

## Security Notice

This add-on can execute Python code inside Blender.

Only enable it on a trusted machine. Do not expose the bridge port to a network. Do not send code from untrusted sources to this bridge.

By default the server binds only to `127.0.0.1`, not to your LAN address.

## Features

- Starts a local bridge on `127.0.0.1:9877`
- Keeps the bridge separate from common Blender MCP ports such as `9876`
- Supports simple `ping`
- Supports scene inspection
- Supports executing trusted Blender Python
- Includes a small add-on preferences panel
- Includes Start / Stop / Restart operators in the Preferences UI

## Tested With

- Blender 5.1.1
- Windows 11

Other Blender versions and operating systems may work, but are not tested yet.

## Installation

1. Download `codex_blender_bridge_addon.zip` from the GitHub Release.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. Click `Install from Disk`.
5. Select `codex_blender_bridge_addon.zip`.
6. Search for `Codex Blender Bridge`.
7. Enable the checkbox.
8. Save preferences if you want it to start automatically next time.

When enabled, the bridge starts automatically unless you disable Auto Start in the add-on preferences.

## Usage

The bridge accepts one JSON command per TCP connection.

### Ping

```json
{"type":"ping","params":{}}
```

### Get Scene Info

```json
{"type":"get_scene_info","params":{}}
```

### Execute Blender Python

```json
{"type":"execute_blender_code","params":{"code":"import bpy\nprint(len(bpy.data.objects))"}}
```

## Python Client Example

```python
import json
import socket

payload = json.dumps({"type": "ping", "params": {}}).encode("utf-8")

with socket.create_connection(("127.0.0.1", 9877), timeout=10) as sock:
    sock.sendall(payload)
    response = sock.recv(65536)

print(response.decode("utf-8"))
```

## Port

Default port: `9877`

You can change the port in the add-on preferences. Restart the bridge after changing the port.

## Troubleshooting

If Codex or your local client cannot connect:

- Confirm the add-on is enabled.
- Confirm Blender is running.
- Confirm the bridge is started in the add-on preferences.
- Confirm no other process is using the selected port.
- Check the log file shown in the add-on preferences.

On Windows, the default log path is:

```text
C:\tmp\codex_blender_bridge.log
```

## Why Not Use Port 9876?

Many Blender MCP setups use `9876`. This add-on uses `9877` by default so it can coexist with Claude Desktop / Claude Code Blender MCP configurations.

Recommended split:

- Claude / Blender MCP: `9876`
- Codex Blender Bridge: `9877`

Avoid editing the same Blender scene from multiple tools at the exact same time.

## License

MIT License. See [LICENSE](LICENSE).
