"""Run from your repository: python3 make_flyer_updated.py"""
from pathlib import Path
import argparse
import matplotlib
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--assets', type=Path, default=ROOT / 'assets')
parser.add_argument('--output', type=Path, default=ROOT / 'assets')
args = parser.parse_args()
ASSETS, OUT = args.assets, args.output
for name in ['MH.jpg', 'swansea.png', 'lms.png', 'ini.png']:
    if not (ASSETS / name).is_file():
        raise FileNotFoundError(f'Missing image: {ASSETS / name}')
OUT.mkdir(parents=True, exist_ok=True)
fonts = Path(matplotlib.get_data_path()) / 'fonts/ttf'
pdfmetrics.registerFont(TTFont('Serif', str(fonts / 'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('Sans', str(fonts / 'DejaVuSans.ttf')))
W, H = 595.276, 841.89
c = canvas.Canvas(str(OUT / 'MartinHelmer-Flyer.pdf'), pagesize=(W, H))
c.setTitle('Computational Algebraic Geometry in Memory of Martin Helmer')
c.setAuthor('Conference organisers')
navy = HexColor('#18354a')
blue = HexColor('#285f85')

def text(x, y, words, size=11, font='Sans', color=navy):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, words)

def para(words, x, top, width, size=10.5, leading=15):
    p = Paragraph(words, ParagraphStyle('body', fontName='Sans',
        fontSize=size, leading=leading, textColor=navy))
    _, height = p.wrap(width, H)
    p.drawOn(c, x, top - height)

text(36, 797, 'Computational', 30, 'Serif')
text(36, 757, 'Algebraic Geometry', 30, 'Serif')
text(36, 727, 'In Memory of Martin Helmer', 17, 'Serif', blue)

# Smaller full photograph: preserve its proportions and keep Martin visible.
im = ImageReader(str(ASSETS / 'MH.jpg'))
iw, ih = im.getSize()
photo_h = 258
photo_w = photo_h * iw / ih
c.drawImage(im, (W-photo_w)/2, 447, photo_w, photo_h, mask='auto')

text(36, 418, '15-16 July 2027', 23, 'Serif', blue)
text(36, 394, 'Swansea University, UK', 15)
text(36, 374, 'Computational Foundry · Bay Campus', 10.5)
para('A two-day meeting bringing together friends, colleagues and collaborators to celebrate Martin’s life and mathematical contributions, and to share mathematics and memories.', 36, 353, W-72)

text(36, 293, 'ORGANISERS', 9, color=blue)
organisers = [
    ('Jeff Giansiracusa · Durham University', 'https://www.durham.ac.uk/staff/jeffrey-giansiracusa/'),
    ('Heather Harrington · MPI-CBG and University of Oxford', 'https://www.mpi-cbg.de/research/researchgroups/currentgroups/heather-harrington'),
    ('Katharine Turner · Australian National University', 'https://maths.anu.edu.au/people/katharine-turner'),
    ('Nelly Villamizar · Swansea University', 'https://sites.google.com/site/nvillami'),
]
for i, (label, url) in enumerate(organisers):
    y = 275 - i*16
    text(36, y, label, 10)
    c.linkURL(url, (36, y-3, 36+pdfmetrics.stringWidth(label,'Sans',10), y+12))

text(36, 199, 'REGISTRATION', 9, color=blue)
text(36, 181, 'Nelly Villamizar · n.y.villamizar@swansea.ac.uk', 11)
c.linkURL('mailto:n.y.villamizar@swansea.ac.uk', (36,177,470,193))
text(36, 153, 'Preceding SIAM AG27 · 19-23 July 2027 · Osnabrück, Germany', 9)
c.linkURL('https://www.siam.org/conferences-events/siam-conferences/ag27', (36,149,W-36,164))
c.setStrokeColor(HexColor('#dce4ea'))
c.line(36, 133, W-36, 133)
text(36, 114, 'SUPPORTED BY', 8, color=blue)

def logo(name, x, y, w, h):
    im = ImageReader(str(ASSETS / name))
    iw, ih = im.getSize()
    scale = min(w/iw, h/ih)
    c.drawImage(im, x+(w-iw*scale)/2, y+(h-ih*scale)/2,
                iw*scale, ih*scale, mask='auto')

logo('swansea.png', 36, 38, 150, 60)
logo('lms.png', 203, 38, 205, 60)
logo('ini.png', 440, 38, 110, 60)
c.showPage()
c.save()
with pymupdf.open(OUT / 'MartinHelmer-Flyer.pdf') as doc:
    assert len(doc) == 1
    doc[0].get_pixmap(matrix=pymupdf.Matrix(2,2), alpha=False).save(
        OUT / 'MartinHelmer-Flyer.png')
print(f'Created PDF and PNG in {OUT}')
