# Changelog

## 0.2.1

- Bumped the visible add-on version and description so Blender's add-on UI clearly shows the updated bridge.
- Rebuilt both the normal release zip and the versioned release zip.

## 0.2.0

- Added `commands` and `status` for faster client-side connection checks.
- Added compatibility aliases for `execute_code`, `run_code`, `exec`, `scene`, and command-list requests.
- Added `get_object_info`.
- Added `get_animation_summary` for sounds, actions, fcurves, and keyframe counts.
- `execute_blender_code` now returns captured `stdout` and `stderr`.
- `get_scene_info` now includes fps/render engine and supports `params.max_objects`.

## 0.1.0

- Initial public package.
- Local-only bridge on `127.0.0.1:9877`.
- Scene inspection command.
- Trusted Python execution command.
- Compatibility aliases for easier AI client use:
  - `ping`
  - `get_scene_info`
  - `scene`
  - `exec`
  - `{"command":"execute_blender_code","code":"..."}`
- Add-on preferences with port, log path, auto start, and Start / Stop / Restart buttons.
- Cross-platform default log path.
- Codex Desktop prompt and Node client example.
- macOS install note for Safari auto-unzip behavior.
