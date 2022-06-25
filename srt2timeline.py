import json
import sys
from base64 import b64encode
from pathlib import Path
import srt

template = Path("template.xml").read_text()
clipitem = Path("clipitem.xml").read_text()
subtitles = srt.parse(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))

clipitems = []
for i, sub in enumerate(subtitles):
    convert = lambda td: int((td.seconds + td.microseconds / 1000000) * 30)

    start, end = convert(sub.start), convert(sub.end)

    value = {"mTextParam": {"mStyleSheet": {"mText": sub.content}}, "mUseLegacyTextBox": False, "mVersion": 1.0}
    value = "\u0F0F\uFFFD\uFFFD\uFFFD" + json.dumps(value)
    value = b64encode(value.encode("utf-16le")).decode("ascii")

    clipitems.append(clipitem.format(id=i, start=start, end=end, name=sub.content, value=value))

Path(sys.argv[1]).with_suffix(".xml").write_text(template.format(duration=end, clipitems="\n".join(clipitems)))
