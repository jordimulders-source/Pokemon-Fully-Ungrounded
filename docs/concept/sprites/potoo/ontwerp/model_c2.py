"""Great potoo, model C2 (gebaseerd op concepten.py)
Jordi (5 nov): "C zie ik zitten qua vachtkleur, de ogen worden echt pikzwart, kijk naar andere pokemon die dat ook hebben. De mond maken we dan geestblauw/paars achtig"; "een zichtbare roep doen we niet, dat is niet pokemon".
Ogen: pikzwart met glans zoals Marill, Spheal, Togepi, Dedenne (referenties/pikzwarte_ogen.png).
Oorspronkelijk: stap 1: drie ontwerprichtingen als modelschets (alleen om te praten, geen bron voor de sprite).
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


ZWART = ('<circle cx="122" cy="88" r="25" fill="#050507" stroke="#222" stroke-width="3"/>'
         '<circle cx="112" cy="77" r="7" fill="#ffffff"/><circle cx="131" cy="99" r="3" fill="#ffffff" opacity=".8"/>'
         '<ellipse cx="191" cy="84" rx="13" ry="17" fill="#050507" stroke="#222" stroke-width="3"/><circle cx="186" cy="77" r="4" fill="#ffffff"/>')
C2 = paneel(0, 'C2  lichte vacht, pikzwarte ogen', 'muil geestblauw/paars; geen zichtbare roep',
    '<path d="M110 280 Q100 330 120 370 Q140 340 160 372 Q176 336 200 360 Q214 310 210 270 Z" fill="#c9c4d8" opacity=".5"/>', '',
    dict(kop='#f1f0f5', lijf='#e0dee8', buik='#faf9fc', vleugel='#b4afc4', muil='#4b3f9e', tong='#8f86e6'), ZWART)
DEFS = ('<defs><radialGradient id="keel" cx="0.85" cy="0.45" r="0.9"><stop offset="0" stop-color="#1c1640"/>'
        '<stop offset=".55" stop-color="#3d3290"/><stop offset="1" stop-color="#6a5fd0"/></radialGradient></defs>')
C2 = C2.replace('fill="#4b3f9e"', 'fill="url(#keel)"')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="330" height="430">{DEFS}{C2}</svg>'
open(os.path.join(HERE, 'model_c2.svg'), 'w').write(svg)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:330,height:430},deviceScaleFactor:2});"
      f"await p.goto('file://{HERE}/model_c2.svg');await p.screenshot({{path:'{HERE}/model_c2.png'}});await b.close()}})()")
subprocess.run(['node', '-e', js], check=True)
