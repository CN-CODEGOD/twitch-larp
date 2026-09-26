import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

PAGES = 5
FIRST = 10

if shutil.which("twitch") is None:
    raise RuntimeError("twitch CLI not found in PATH.")

all_streams = []
cursor = None

for page in range(PAGES):
    cmd = ["twitch", "api", "get", "streams", "-q", f"first={FIRST}"]
    if cursor:
        cmd.extend(["-q", f"after={cursor}"])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Page {page + 1} failed: {result.stderr}", file=sys.stderr)
        break

    response = json.loads(result.stdout)
    streams = response.get("data", [])
    all_streams.extend(streams)

    cursor = response.get("pagination", {}).get("cursor")
    if not cursor or not streams:
        break

root = ET.Element("top_streams")
root.set("pages", str(PAGES))
root.set("total", str(len(all_streams)))

for idx, s in enumerate(all_streams, start=1):
    stream = ET.SubElement(root, "stream")
    stream.set("rank", str(idx))
    ET.SubElement(stream, "user_id").text = s.get("user_id", "")
    ET.SubElement(stream, "user_login").text = s.get("user_login", "")
    ET.SubElement(stream, "user_name").text = s.get("user_name", "")
    ET.SubElement(stream, "title").text = s.get("title", "")
    ET.SubElement(stream, "game_name").text = s.get("game_name", "")
    ET.SubElement(stream, "viewer_count").text = str(s.get("viewer_count", 0))
    ET.SubElement(stream, "language").text = s.get("language", "")
    ET.SubElement(stream, "thumbnail_url").text = s.get("thumbnail_url", "")
    ET.SubElement(stream, "started_at").text = s.get("started_at", "")

xml_str = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")

with open("top_streams.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"Exported {len(all_streams)} top streams to top_streams.xml")
