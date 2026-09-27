import json
import urllib.request
import os
import subprocess

# 1. Read token
config_path = r"C:\Users\Ishaan\.gemini\config\mcp_config.json"
try:
    with open(config_path, "r") as f:
        config = json.load(f)
    token = config["mcpServers"]["github"]["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"]
except Exception as e:
    print("Failed to read token:", e)
    exit(1)

if token == "<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>":
    print("Token is still the placeholder!")
    exit(1)

# 2. Initialize git if needed
if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)
    
subprocess.run(["git", "add", "."], check=True)
res = subprocess.run(["git", "commit", "-m", "Initial commit: Enterprise MCP EE Demo"], capture_output=True)
print(res.stdout.decode())

# 3. Create repo
repo_name = "mcp-ee-demo"
req = urllib.request.Request(
    "https://api.github.com/user/repos",
    data=json.dumps({
        "name": repo_name,
        "description": "An interactive enterprise MCP server demo for Electrical Engineering",
        "private": False
    }).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python"
    }
)

try:
    with urllib.request.urlopen(req) as response:
        repo_data = json.loads(response.read().decode())
        clone_url = repo_data["clone_url"]
        owner = repo_data["owner"]["login"]
        print(f"Created repository: {repo_data['html_url']}")
except urllib.error.HTTPError as e:
    print("HTTP Error creating repo:", e.code, e.read().decode())
    if e.code == 422: # Already exists
        # Let's get the username
        req_user = urllib.request.Request("https://api.github.com/user", headers={"Authorization": f"Bearer {token}", "User-Agent": "Python"})
        with urllib.request.urlopen(req_user) as u_resp:
            owner = json.loads(u_resp.read().decode())["login"]
        clone_url = f"https://github.com/{owner}/{repo_name}.git"
        print("Repository already exists. Using:", clone_url)
    else:
        exit(1)

# 4. Push to github
# We insert the token into the URL for authentication
auth_url = clone_url.replace("https://", f"https://{token}@")

subprocess.run(["git", "branch", "-M", "main"], check=True)
subprocess.run(["git", "remote", "remove", "origin"], capture_output=True) # ignore if fails
subprocess.run(["git", "remote", "add", "origin", auth_url], check=True)

print("Pushing to GitHub...")
push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
if push_res.returncode == 0:
    print("Successfully pushed to GitHub!")
else:
    print("Error pushing:", push_res.stderr)
    
# Remove remote with token and add normal remote for safety
subprocess.run(["git", "remote", "remove", "origin"], check=True)
subprocess.run(["git", "remote", "add", "origin", clone_url], check=True)

