# Publishing Checklist

## 1. Create a GitHub Repository

Repository name:

```text
codex-blender-bridge
```

Recommended visibility:

```text
Public
```

Recommended options:

- Add README: off if you are uploading these files manually.
- Add .gitignore: not needed, this package already includes one.
- License: MIT, or upload the included `LICENSE`.

## 2. Upload Files

Upload the source files from this folder:

```text
codex-blender-bridge/
```

The repository root should contain:

```text
README.md
LICENSE
SECURITY.md
CHANGELOG.md
PUBLISHING.md
X_POSTS.md
AI_CLIENT_PROMPT.md
codex_blender_bridge_addon/
examples/
```

Do not upload generated files or cache folders as source files:

```text
__pycache__/
dist/
*.zip
```

The release zip is attached to GitHub Releases separately.

## 3. Create the Release Zip

Use the generated file:

```text
dist/codex_blender_bridge_addon.zip
```

The zip must contain:

```text
codex_blender_bridge_addon/__init__.py
```

## 4. Create a GitHub Release

Release tag:

```text
v0.2.1
```

Release title:

```text
Codex Blender Bridge v0.2.1
```

Attach:

```text
codex_blender_bridge_addon.zip
```

Optional extra asset:

```text
codex_blender_bridge_addon_v0.2.1.zip
```

Copy the text from:

```text
release-notes-v0.2.1.md
```

## 5. Post on X

Use one of the drafts in:

```text
X_POSTS.md
```

Replace:

```text
https://github.com/ododo1981-crypto/codex-blender-bridge
```

with your actual GitHub repository URL.

## 6. First Support Reply Template

If someone says it does not connect:

```text
Please check:
1. Blender is open.
2. The Codex Blender Bridge add-on is enabled.
3. The add-on preferences show the bridge as running.
4. Nothing else is using port 9877.
5. You are connecting to 127.0.0.1, not a LAN IP.
```

If someone is using Codex Desktop, point them to:

```text
AI_CLIENT_PROMPT.md
```

If they see `os error 5`, `PermissionDenied`, or `CreateProcessAsUserW failed: 5`, the issue is their Codex local process access, not the Blender add-on.
