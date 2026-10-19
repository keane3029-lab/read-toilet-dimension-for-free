from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()
out = Path("pages")
out.mkdir(exist_ok=True)

def convert(src, dest):
    Image.open(src).convert("RGB").save(dest, quality=90)
    print("converted", src, "->", dest.name)

# loose files in the heic folder keep their own names
for f in Path("heic").glob("*.heic"):
    convert(f, out / (f.stem + ".jpg"))

# folders like "Arc 6" become prefix "arc6"
for d in Path(".").iterdir():
    if not d.is_dir() or d.name in ("pages", "heic", ".git"):
        continue
    files = sorted(d.glob("*.heic"))
    if not files:
        continue
    prefix = d.name.lower().replace("folder", "").replace(" ", "")
    if len(files) == 1:
        convert(files[0], out / f"{prefix}-whole.jpg")
    else:
        for i, f in enumerate(files, 1):
            convert(f, out / f"{prefix}-{i}.jpg")