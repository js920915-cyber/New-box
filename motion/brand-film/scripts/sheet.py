# Usage: python3 scripts/sheet.py out.png img1 img2 ... (2 columns, labelled)
import sys
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size
cols = 2
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (w * cols + 10 * (cols - 1), h * rows + 10 * (rows - 1)), (255, 0, 255))
d = ImageDraw.Draw(sheet)
for i, im in enumerate(ims):
    x, y = (i % cols) * (w + 10), (i // cols) * (h + 10)
    sheet.paste(im, (x, y))
    d.text((x + 8, y + 8), files[i].split('/')[-1], fill=(255, 255, 0))
sheet.save(out)
