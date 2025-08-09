#!/usr/bin/env python3
import json, re
from pathlib import Path
IMAGE_EXTS={".jpg",".jpeg",".png",".webp",".svg"}
VIDEO_EXTS={".mp4",".webm",".mov"}
def friendly(n): import re; from pathlib import Path as P; return re.sub(r'[_-]+',' ',P(n).stem).title()
def parse_youtube(p):
    out=[]; p=Path(p)
    if not p.exists(): return out
    for line in p.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#"): continue
        title,url=("YouTube Video",line)
        if "|" in line: title,url=[x.strip() for x in line.split("|",1)]
        import re; m=re.search(r"v=([A-Za-z0-9_-]{6,})",url); vid=m.group(1) if m else None
        embed=f"https://www.youtube.com/embed/{vid}" if vid else url
        out.append({"type":"youtube","src":embed,"title":title})
    return out
def build(root="."):
    root=Path(root); g=root/"assets/gallery"; v=root/"assets/videos"
    g.mkdir(parents=True,exist_ok=True); v.mkdir(parents=True,exist_ok=True)
    photos=[{"src":p.relative_to(root).as_posix(),"alt":friendly(p.name)} for p in sorted(g.rglob("*")) if p.suffix.lower() in IMAGE_EXTS and p.is_file()]
    videos=[{"type":"mp4","src":p.relative_to(root).as_posix(),"title":friendly(p.name)} for p in sorted(v.rglob("*")) if p.suffix.lower() in VIDEO_EXTS and p.is_file()]
    videos+=parse_youtube(v/"youtube.txt")
    (g/"index.json").write_text(json.dumps({"photos":photos,"videos":videos},indent=2),encoding="utf-8")
if __name__=="__main__": build()
