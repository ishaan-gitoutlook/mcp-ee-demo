import json
import urllib.request
import os
import subprocess

config_path = r"C:\Users\Ishaan\.gemini\config\mcp_config.json"
try:
    with open(config_path, "r") as f:
        config = json.load(f)
    token = config["mcpServers"]["github"]["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"]
except Exception as e:
    exit(1)

subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat: Add Streamlit Web UI module"], capture_output=True)

res = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True)
clone_url = res.stdout.strip()
auth_url = clone_url.replace("https://", f"https://{token}@")

subprocess.run(["git", "remote", "remove", "origin"], capture_output=True) 
subprocess.run(["git", "remote", "add", "origin", auth_url], check=True)

push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)

subprocess.run(["git", "remote", "remove", "origin"], check=True)
subprocess.run(["git", "remote", "add", "origin", clone_url], check=True)
