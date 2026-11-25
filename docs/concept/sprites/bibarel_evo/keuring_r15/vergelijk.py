# vergelijk.png: r15 naast Gen 3-vachtsprites en onze goedgekeurde sprites op 3x, met de meetgetallen eronder
import io, contextlib
from laad import *
from PIL import ImageDraw
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import meet
rows = {r[0]: r for r in meet.rows}
extra = [('dundragoon', ons('docs/concept/sprites/dundragoon/af/dundragoon.png'))]
items = [(n, ld()) for n, ld, f, c in meet.SETS] + extra
z = 3; cw = 64*z + 8
W = Image.new('RGB', (6*cw, 2*(64*z + 120) + 10), 'white'); d = ImageDraw.Draw(W)
for i, (n, (a, p)) in enumerate(items):
    X = (i % 6)*cw; Y = (i//6)*(64*z + 120)
    W.paste(rgb(a, p).resize((64*z, 64*z), Image.NEAREST), (X, Y + 14)); d.text((X, Y), n, fill='black')
    if n in rows:
        _, s, l, c = rows[n]
        t = [f"vacht {s['n']} px, {s['tinten']} tinten", f"stappen {s['stappen']}", f"eiland<3: {s['eil_lt3']}/100",
             f"vlak>=20: {s['gr_vlak_aandeel']}%  grens {s['grens_per100']}/100",
             f"zwart {l['zwart_pct']}%  rand l/s {l['rand_zwart_licht']}/{l['rand_zwart_schaduw']}%"]
        if c and c['n']: t.append(f"creme/2e: stappen {c['stappen']}")
        for k, line in enumerate(t): d.text((X, Y + 14 + 64*z + 2 + 13*k), line, fill='black')
W.save('vergelijk.png')
