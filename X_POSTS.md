# X Post Drafts

Replace the URL with your GitHub repository or release URL before posting.

## Short

```text
I made Codex Blender Bridge, a small Blender add-on for local AI workflows.

It opens a local-only TCP bridge at 127.0.0.1:9877 so tools like Codex can inspect the current Blender scene and run trusted Blender Python.

It is not Blender MCP, so it can coexist with common MCP setups on a separate port.

GitHub:
https://github.com/ododo1981-crypto/codex-blender-bridge

#Blender #b3d #AI
```

## Friendly

```text
I built a small Blender add-on for controlling Blender from Codex and other local AI tools.

Codex Blender Bridge

What it does:
- Starts a local-only bridge inside Blender
- Lets local tools inspect the current scene
- Lets trusted local tools run Blender Python
- Uses 127.0.0.1:9877 by default

It is separate from Blender MCP, so it can coexist with Claude / MCP workflows.

GitHub:
https://github.com/ododo1981-crypto/codex-blender-bridge

#Blender #b3d #AI
```

## Thread

```text
1/
I made Codex Blender Bridge, a small Blender add-on for local AI workflows.

It opens a local-only TCP bridge at 127.0.0.1:9877 so tools like Codex can talk to Blender without using Blender MCP.

#Blender #b3d #AI
```

```text
2/
What it can do:

- ping the bridge
- inspect the current Blender scene
- run trusted Blender Python
- edit the scene from a local AI tool

It uses simple JSON over a TCP socket.
```

```text
3/
Why not just use the common MCP port?

Many Blender MCP setups use 9876.
Codex Blender Bridge uses 9877 by default, so it can coexist with Claude / Blender MCP setups more easily.
```

```text
4/
Security note:

This add-on can execute Python inside Blender.
Use it only on a trusted machine with trusted local clients.
Do not expose the bridge port to a network or the internet.
```

```text
5/
Install:

Download the release zip and install it in Blender:
Edit > Preferences > Add-ons > Install from Disk

GitHub:
https://github.com/ododo1981-crypto/codex-blender-bridge

#Blender #b3d #AI
```

## Japanese Draft

Keep Japanese drafts outside this file if your editor or upload path causes mojibake.
