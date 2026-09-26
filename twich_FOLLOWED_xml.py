import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

USER_CHANNEL_ID = "555862343"

if shutil.which("twitch") is None:
    raise RuntimeError("twitch CLI not found in PATH.")

result = subprocess.run(
    ["twitch", "api", "get", "channels/followed",
     "-q", f"user_id={USER_CHANNEL_ID}"],
    capture_output=True, text=True, check=True,
)

followed = json.loads(result.stdout)
data = followed.get("data", [])

root = ET.Element("followed_channels")
root.set("user_id", USER_CHANNEL_ID)
root.set("total", str(followed.get("total", len(data))))

for item in data:
    channel = ET.SubElement(root, "channel")
    ET.SubElement(channel, "broadcaster_id").text = item.get("broadcaster_id", "")
    ET.SubElement(channel, "broadcaster_login").text = item.get("broadcaster_login", "")
    ET.SubElement(channel, "broadcaster_name").text = item.get("broadcaster_name", "")
    ET.SubElement(channel, "followed_at").text = item.get("followed_at", "")

xml_str = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")

with open("followed_channels.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"Exported {len(data)} followed channels to followed_channels.xml")
