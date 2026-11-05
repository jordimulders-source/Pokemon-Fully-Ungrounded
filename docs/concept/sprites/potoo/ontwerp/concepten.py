"""Great potoo, stap 1: drie ontwerprichtingen als modelschets (alleen om te praten, geen bron voor de sprite).
Jordi (5 nov): "we gaan niet een potoo namaken", "we maken een pokemon", "dus hij mag nog wat geestachtiger",
"grote ogen, grote mond", "misschien dat we de vacht heel licht maken als mooi contrast".\nKleur en patroon zijn nog open ("moeten nog nadenken over kleur, patroon etc"); hier overal een lichte vacht. Pose (besloten): 3/4 naar links, licht voorover, bek open, op een onzichtbare tak.
Render: node + playwright (zie onderaan)."""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))

KOP = '<path d="M78 112 Q74 56 140 44 Q210 40 226 96 Q232 140 196 156 Q150 166 112 156 Q82 146 78 112 Z" fill="{kop}" stroke="#222" stroke-width="4"/>'
LIJF = '<path d="M104 150 Q70 220 92 292 Q112 334 160 330 Q214 304 220 220 Q222 160 196 148 Z" fill="{lijf}" stroke="#222" stroke-width="4"/>'
BUIK = '<path d="M108 190 Q96 250 116 300 Q140 318 160 300 Q170 240 150 186 Z" fill="{buik}" opacity=".9"/>'
VLEUGEL = '<path d="M186 160 Q226 220 214 300 Q206 336 196 350 Q182 300 170 250 Q164 200 186 160 Z" fill="{vleugel}" stroke="#222" stroke-width="3.5"/>'
MUIL = ('<path d="M74 178 Q122 168 172 136 Q156 184 104 198 Q80 198 74 178 Z" fill="{kop}" stroke="#222" stroke-width="4"/>'
        '<path d="M64 116 Q112 110 174 136 Q124 166 74 178 Q58 150 64 116 Z" fill="{muil}" stroke="#222" stroke-width="4"/>'
        '<path d="M82 160 Q120 152 150 140" stroke="{tong}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        '<path d="M64 116 l-9 9 l13 1 Z" fill="#3a3530" stroke="#222" stroke-width="2"/>')
def OGEN(ring, iris, glans, gloed=''):
    return (f'<circle cx="122" cy="88" r="27" fill="{ring}" stroke="#222" stroke-width="3"/>'
            f'<circle cx="122" cy="88" r="21" fill="{iris}"/>{gloed}'
            f'<circle cx="114" cy="79" r="6" fill="{glans}"/><circle cx="129" cy="98" r="2.5" fill="{glans}" opacity=".7"/>'
            f'<ellipse cx="190" cy="84" rx="15" ry="18" fill="{ring}" stroke="#222" stroke-width="3"/>'
            f'<ellipse cx="192" cy="84" rx="11" ry="14" fill="{iris}"/><circle cx="187" cy="78" r="3.5" fill="{glans}"/>')

def paneel(x, titel, sub, achter, voor, kleuren, ogen):
    k = kleuren
    lagen = achter + VLEUGEL + LIJF + BUIK + voor + KOP + MUIL + ogen
    lagen = lagen.format(**k)
    return (f'<g transform="translate({x},0)"><rect width="330" height="430" fill="#ece9e2"/>'
            f'<text x="14" y="28" font-family="sans-serif" font-size="19" font-weight="bold" fill="#222">{titel}</text>'
            f'<text x="14" y="48" font-family="sans-serif" font-size="12.5" fill="#444">{sub}</text>'
            f'<g transform="translate(20,40)">{lagen}</g></g>')

A = paneel(0, 'A  Rouwsluier', 'onderlijf rafelt uit tot sluier/rook',
    '<path d="M100 270 Q92 330 70 380 Q100 352 112 372 Q118 340 136 378 Q146 344 166 380 Q170 340 192 372 Q196 330 214 260 Z" fill="#b8b2c9" opacity=".75" stroke="#55506a" stroke-width="2.5"/>',
    '<path d="M108 120 Q150 104 200 124 Q170 150 112 150 Z" fill="#d9d4e4" opacity=".55"/>',
    dict(kop='#f3f0ea', lijf='#e4e0d8', buik='#fbfaf6', vleugel='#bdb5a8', muil='#b8476e', tong='#e889a6'),
    OGEN('#e9e4f2', '#0e0c14', '#ffffff'))
B = paneel(340, 'B  Knoestogen', 'ogen als holtes in dood hout, licht van binnen',
    '<path d="M150 320 L156 372 L168 340 L176 380 L186 336 L198 366 L204 318 Z" fill="#6b5a48" stroke="#2a221a" stroke-width="3"/>',
    '<path d="M120 200 q10 30 4 60 M150 210 q8 40 0 80 M178 180 q12 50 4 110" stroke="#5c4d3e" stroke-width="3" fill="none"/>'
    '<path d="M118 242 q8 -6 14 2 M168 262 q8 -6 14 2" stroke="#9fae8a" stroke-width="5" fill="none"/>',
    dict(kop='#efebe3', lijf='#ddd7cc', buik='#f8f5ef', vleugel='#a99d8c', muil='#3a1f2a', tong='#7be0c8'),
    OGEN('#8a7a66', '#140f0c', '#7be0c8', '<circle cx="124" cy="90" r="7" fill="#7be0c8" opacity=".8"/>'))
C = paneel(680, 'C  Klaagzang', 'de roep wordt zichtbaar: geestslierten uit de muil',
    '<path d="M110 280 Q100 330 120 370 Q140 340 160 372 Q176 336 200 360 Q214 310 210 270 Z" fill="#c9c4d8" opacity=".5"/>',
    '<path d="M60 150 Q20 130 30 90 Q40 60 20 40 M66 176 Q10 180 4 140 M84 204 Q50 240 14 230" stroke="#9d93c4" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>',
    dict(kop='#f1f0f5', lijf='#e0dee8', buik='#faf9fc', vleugel='#b4afc4', muil='#c2436a', tong='#f2a0b8'),
    OGEN('#d9d4e4', '#08070c', '#ffffff'))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1010" height="430">{A}{B}{C}</svg>'
open(os.path.join(HERE, 'concepten.svg'), 'w').write(svg)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1010,height:430},deviceScaleFactor:2});"
      f"await p.goto('file://{HERE}/concepten.svg');await p.screenshot({{path:'{HERE}/concepten.png'}});await b.close()}})()")
subprocess.run(['node', '-e', js], check=True)
