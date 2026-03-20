import subprocess
import json

schema = [
    {
        "type": "function",
        "function": {
            "name": "list_active_windows",
            "description": (
                "List all currently open windows and which workspace each one is on. "
                "Use this when the user asks 'what windows are open', 'list active windows', "
                "'what's running', 'where is my terminal', 'which workspace has Firefox', "
                "'show me all open apps', or 'what do I have open'."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "switch_workspace",
            "description": (
                "Switch the active desktop to a specific workspace number. "
                "Use this when the user says 'switch to workspace 2', 'go to desktop 3', "
                "'move to workspace 1', 'jump to workspace 5', or 'change workspace'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "workspace_number": {
                        "type": "integer",
                        "description": "The workspace number to switch to (e.g. 1, 2, 3)"
                    }
                },
                "required": ["workspace_number"]
            }
        }
    },
]


def list_active_windows() -> str:
    clients = json.loads(subprocess.check_output(["hyprctl", "clients", "-j"]))
    workspaces: dict[int, list[str]] = {}
    for c in clients:
        ws = c.get("workspace", {}).get("id", "?")
        title = c.get("title") or c.get("class") or "Unknown"
        workspaces.setdefault(ws, []).append(title)
    if not workspaces:
        return "No windows found."
    lines = []
    for ws in sorted(workspaces):
        lines.append(f"Workspace {ws}:")
        for title in workspaces[ws]:
            lines.append(f"  - {title}")
    return "\n".join(lines)


def switch_workspace(workspace_number: int) -> str:
    subprocess.run(["hyprctl", "dispatch", "workspace", str(workspace_number)], check=True)
    return f"Switched to workspace {workspace_number}"


func = {
    "list_active_windows": list_active_windows,
    "switch_workspace": switch_workspace,
}