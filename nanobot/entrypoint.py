#!/usr/bin/env python3
"""
Entrypoint for nanobot Docker container.

Resolves environment variables into config.json at runtime,
then launches `nanobot gateway`.
"""

import json
import os
import sys

def main():
    # Read the base config.json
    config_path = "/app/nanobot/config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    # Override providers.custom from env vars
    if "LLM_API_KEY" in os.environ:
        config["providers"]["custom"]["apiKey"] = os.environ["LLM_API_KEY"]
    
    if "LLM_API_BASE_URL" in os.environ:
        config["providers"]["custom"]["apiBase"] = os.environ["LLM_API_BASE_URL"]
    
    if "LLM_API_MODEL" in os.environ:
        config["agents"]["defaults"]["model"] = os.environ["LLM_API_MODEL"]

    # Override gateway settings from env vars
    if "NANOBOT_GATEWAY_CONTAINER_ADDRESS" in os.environ:
        config.setdefault("gateway", {})["host"] = os.environ["NANOBOT_GATEWAY_CONTAINER_ADDRESS"]
    
    if "NANOBOT_GATEWAY_CONTAINER_PORT" in os.environ:
        config.setdefault("gateway", {})["port"] = int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"])

    # Override MCP LMS server env vars
    if "tools" in config and "mcpServers" in config["tools"] and "lms" in config["tools"]["mcpServers"]:
        lms_env = config["tools"]["mcpServers"]["lms"].setdefault("env", {})
        if "NANOBOT_LMS_BACKEND_URL" in os.environ:
            lms_env["NANOBOT_LMS_BACKEND_URL"] = os.environ["NANOBOT_LMS_BACKEND_URL"]
        if "NANOBOT_LMS_API_KEY" in os.environ:
            lms_env["NANOBOT_LMS_API_KEY"] = os.environ["NANOBOT_LMS_API_KEY"]

    # Override MCP observability server env vars
    if "tools" in config and "mcpServers" in config["tools"] and "observability" in config["tools"]["mcpServers"]:
        obs_env = config["tools"]["mcpServers"]["observability"].setdefault("env", {})
        if "NANOBOT_VICTORIALOGS_URL" in os.environ:
            obs_env["NANOBOT_VICTORIALOGS_URL"] = os.environ["NANOBOT_VICTORIALOGS_URL"]
        if "NANOBOT_VICTORIATRACES_URL" in os.environ:
            obs_env["NANOBOT_VICTORIATRACES_URL"] = os.environ["NANOBOT_VICTORIATRACES_URL"]

    # Configure webchat channel
    if "NANOBOT_WEBCHAT_CONTAINER_ADDRESS" in os.environ:
        config.setdefault("channels", {}).setdefault("webchat", {})["host"] = os.environ["NANOBOT_WEBCHAT_CONTAINER_ADDRESS"]
    
    if "NANOBOT_WEBCHAT_CONTAINER_PORT" in os.environ:
        config.setdefault("channels", {}).setdefault("webchat", {})["port"] = int(os.environ["NANOBOT_WEBCHAT_CONTAINER_PORT"])
    
    # Enable webchat channel
    config.setdefault("channels", {})["webchat"] = config.get("channels", {}).get("webchat", {})
    config["channels"]["webchat"]["enabled"] = True
    config["channels"]["webchat"]["allowFrom"] = ["*"]

    # Configure MCP webchat server
    if "NANOBOT_ACCESS_KEY" in os.environ:
        config.setdefault("tools", {}).setdefault("mcpServers", {}).setdefault("webchat", {})
        config["tools"]["mcpServers"]["webchat"]["command"] = "python"
        config["tools"]["mcpServers"]["webchat"]["args"] = ["-m", "mcp_webchat"]
        config["tools"]["mcpServers"]["webchat"]["env"] = {
            "MCP_WEBCHAT_UI_RELAY_URL": f"ws://{os.environ.get('NANOBOT_WEBCHAT_CONTAINER_ADDRESS', 'localhost')}:{os.environ.get('NANOBOT_WEBCHAT_CONTAINER_PORT', '8080')}/relay",
            "MCP_WEBCHAT_TOKEN": os.environ["NANOBOT_ACCESS_KEY"]
        }

    # Write the resolved config to /tmp for permission reasons
    resolved_config_path = "/tmp/config.resolved.json"
    with open(resolved_config_path, "w") as f:
        json.dump(config, f, indent=2)

    # Get workspace path
    workspace = config.get("agents", {}).get("defaults", {}).get("workspace", "./workspace")
    if not workspace.startswith("/"):
        workspace = f"/app/nanobot/{workspace}"

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config_path, "--workspace", workspace])

if __name__ == "__main__":
    main()
