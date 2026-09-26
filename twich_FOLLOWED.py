import json
import shutil
import subprocess
import sys

USER_CHANNEL_ID = "555862343"

# 检查 Twitch CLI
if shutil.which("twitch") is None:
    raise RuntimeError(
        "twitch.exe was not found in PATH. "
        "Install the Twitch CLI and try again."
    )

# 获取关注的频道
try:
    result = subprocess.run(
        ["twitch", "api", "get", "channels/followed",
         "-q", f"user_id={USER_CHANNEL_ID}"],
        capture_output=True,
        text=True,
        check=True,
    )
except subprocess.CalledProcessError:
    print("Failed to get followed channels.", file=sys.stderr)
    sys.exit(1)

followed_response = result.stdout

if not followed_response.strip():
    print("No followed channels returned.")
    sys.exit(0)

followed = json.loads(followed_response)

logins = [
    item["broadcaster_login"]
    for item in followed.get("data", [])
    if item.get("broadcaster_login")
]

if not logins:
    print("No followed channels found.")
    sys.exit(0)

# 查询这些关注频道中当前正在直播的频道
query = "&".join(f"user_login={login}" for login in logins)

result = subprocess.run(
    ["twitch", "api", "get", "streams", "-q", query],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)

print(result.stdout)
