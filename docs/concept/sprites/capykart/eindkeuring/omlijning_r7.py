"""Capykart r7: omlijningsronde (Dragonfly Cave-eindkeuring) op r6.
Alleen lijnpixels en tintwissels binnen het bestaande palet; alpha ongewijzigd; gezicht ongemoeid.
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/capykart/eindkeuring/omlijning_r7.py
"""
from PIL import Image
import os
D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, '..', 'sprite', 'r6', 'capykart.png')
OUT = os.path.join(D, 'capykart_r7.png')

# Paletindices r6: 1 zwart, 4 donkerbruin (vacht/hout donkerst), 6 hout midden, 7 grijs (hoepel),
# 8 blauwgrijs (hoepel donkerst + blauw blok zijvlak), 10 blauw, 11 donkergroen, 13 donkerrood
G_BASE = "gids r.~160: 'we take the base outlining shade for every color and color all of the outline except the shadows in that color'"
G_SHAD = "gids r.~93: 'The \"outline shadows\" are always black' (schaduwkant rechts/onder, zoals capybarrel/af)"
G_CLUS = "gids r.~158: 'remove the clusters so that the outline is always one pixel wide'"
G_REC3 = "gids r.~110: 'The outline base and outline highlight colors are also colors ... you must also recolor the outlines'"
G_REC4 = "gids r.~114: 'The outlines must be reasonably dark'"

E = []  # (x, y, nieuw, onderdeel, reden, citaat)
def add(pts, new, part, why, cite):
    for p in pts: E.append((p[0], p[1], new, part, why, cite))

# --- groene driehoek: schuine zijden + top = lichtkant -> outline base donkergroen (11)
add([(49,1),(50,1),(51,1),(47,2),(48,2),(52,2),(46,3),(53,3),(45,4),(54,4),(44,5),(55,5),(43,6),(56,6),(42,7),(57,7)],
    11, 'groene driehoek', 'top en schuine zijden (lichtkant, zoals capybarrel-oor/ton-bovenrand) zwart -> eigen donkerste tint', G_BASE)
# --- geel blok: linkerzijde -> donkerste tint van zijn helling (E -> 5 -> 6 -> 4)
add([(44,9),(44,10),(44,11),(44,12),(44,13),(44,14)], 4, 'geel blok',
    'linkerzijde (lichtkant) zwart -> outline base; geel blok kleurt via 5/6 (zijvlak) naar 4, 6 is te licht als lijn', G_REC4)
# --- rood blok: linkerzijde -> donkerrood (13); verticale binnenlijn voor/zijvlak -> 13
add([(44,17),(44,18),(44,19),(44,20),(44,21),(44,22),(44,23)], 13, 'rood blok', 'linkerzijde (lichtkant) zwart -> outline base', G_BASE)
add([(50,19),(50,20),(50,21),(50,22),(50,23)], 13, 'rood blok',
    'binnenlijn tussen voor- en zijvlak van hetzelfde blok was zwart -> eigen donkerste tint (geel en blauw blok hebben hier ook geen zwarte lijn)', G_BASE)
# --- open rand rood op blauw sluiten (model r5 heeft een donkere lijn tussen de blokken)
add([(46,25),(47,25),(48,25)], 1, 'rood/blauw blok', 'open rand: rood lag zonder lijn op blauw; onderrand rood = schaduwkant -> zwart, sluit aan op (45,24) en (49,25)', G_SHAD)
# --- blauw blok: linkerzijde -> 8
add([(43,25),(43,26),(43,27)], 8, 'blauw blok', 'linkerzijde (lichtkant) zwart -> outline base (8 = donkerste blauwgrijs)', G_BASE)
# --- kop: oren en linkerzijde
add([(27,10),(25,11)], 4, 'linkeroor', 'top/linkerzijde oor zwart -> outline base (zoals capybarrel-oor: top in donkerbruin)', G_BASE)
add([(38,11)], 4, 'rechteroor', 'bovenste pixel oorpunt zwart -> outline base; rechterzijde blijft zwart', G_BASE)
add([(37,13),(36,14),(35,15)], 4, 'rechteroor', 'binnenlijn oor/kop was zwart -> donkerste eigen tint (binnenlijnen niet zwart)', G_BASE)
add([(15,20)], 4, 'kop links', 'losse zwarte pixel in de linker buitenlijn (rest is 4) -> geen zwart en selout om en om', G_BASE)
# --- kart achter: schuine bovenrand rechts
add([(59,32),(60,33),(61,34),(62,35)], 4, 'kart achter', 'schuine bovenrand (lichtkant) zwart -> outline base; verticale rechterzijde blijft zwart', G_BASE)
# --- kart voor: linkerzijde
add([(3,41),(2,43),(1,45)], 4, 'kart neus links', 'zwarte pixels tussen 4-en in de linker buitenlijn -> geen zwart en selout om en om', G_BASE)
add([(14,34)], 4, 'kart rand voor', 'bovenrand (lichtkant) zwart -> outline base', G_BASE)
# --- voorste hoepel (band over de neus)
add([(12,35),(13,35),(10,36),(11,36),(9,37)], 8, 'hoepel voor', 'bovenrand van de band aan de neuspunt (lichtkant) zwart -> 8; band loopt al met 8 als bovenrand (15-19,35)', G_BASE)
add([(14,35),(14,36)], 8, 'hoepel voor', 'zwarte binnenlijn dwars door de band -> donkerste eigen tint', G_BASE)
add([(21,35),(22,35),(23,35),(24,36),(25,36),(26,36),(27,37),(28,37),(29,38),(30,38),(31,39)], 8, 'hoepel voor',
    'bovenrand van de diagonale band (lichtkant) zwart -> 8, (23,35) was een open rand (hout direct boven grijs); steile/verticale rechterkant (31,40)+ blijft zwart', G_BASE)
add([(13,37),(14,37),(16,37),(17,37),(18,37),(26,40)], 1, 'hoepel voor',
    'open rand: onderkant band had hout direct onder grijs/8; onderrand = schaduwkant -> zwart, sluit de bestaande zwarte onderlijn', G_SHAD)
# --- rand van de cockpit (hout voor de vacht): bovenrand -> 4
add([(24,33),(25,33),(26,33),(28,34),(29,34),(30,34),(31,35),(32,35),(34,40),(35,40),(36,40),(38,39),(39,39),(40,39),(41,38),(42,38),(44,37),(45,37)],
    4, 'kart cockpitrand', 'binnenlijn: bovenrand van het hout dat voor de vacht ligt (lichtkant) was zwart -> outline base 4; verticale rechterzijden (33,36-37),(34,38-39) blijven zwart', G_BASE)
# --- rechter hoepel
add([(44,31),(45,32)], 1, 'hoepel rechts', 'onderrand bovenste (diagonale) deel wisselde 1-4-1 -> geheel zwart (onderkant = schaduw)', G_SHAD)
add([(47,34),(48,35),(48,36),(48,37),(48,38),(48,39),(48,40),(48,41),(48,45)], 8, 'hoepel rechts',
    'verticale linkerzijde (lichtkant) wisselde 1/4 -> outline base 8 (geen zwart en selout om en om)', G_BASE)
add([(48,42),(48,43),(48,44)], 8, 'hoepel rechts', 'open rand: hout 6 direct naast grijs 7 -> lijn in 8 (linkerzijde)', G_BASE)
add([(47,35),(47,36)], 4, 'vacht naast hoepel rechts', 'tweede zwarte pixel naast de hoepellijn (cluster, 2 px dik) -> vachtkleur van de buren (4)', G_CLUS)
add([(49,40)], 7, 'hoepel rechts', 'cluster: 2 zwarte pixels naast elkaar op de plek van de grijze band -> band (7) zoals rij 39 en 41', G_CLUS)
# --- wielen: bovenrand/linkerzijde = lichtkant -> 4 (wiel ligt voor de bak)
add([(27,47),(28,47),(29,47),(30,47),(25,48),(26,48),(24,49),(24,50),(23,51),(23,52),(22,53),(22,54),(22,55)], 4, 'voorwiel',
    'binnenlijn: boven-/linkerrand van het wiel (lichtkant) was zwart -> outline base; rechterzijde en linksonder blijven zwart', G_BASE)
add([(53,43),(54,43),(55,43),(56,43),(57,44),(58,44),(48,47),(48,50),(48,51),(48,52)], 4, 'achterwiel',
    'binnenlijn: boven-/linkerrand van het wiel (lichtkant) was zwart -> outline base; rechterzijde (60,48-49) en linksonder (48,53) blijven zwart', G_BASE)
# --- achterbak: binnenlijn bovenvlak/voorvlak
add([(52,33),(53,33),(54,33)], 4, 'kart achter', 'binnenlijn tussen boven- en voorvlak van hetzelfde stuk hout was zwart -> donkerste eigen tint', G_BASE)
add([(52,34)], 6, 'kart achter', 'cluster: zwart naast de nieuwe 4-lijn (51,34) -> houtkleur van de buur eronder (52,35)=6', G_CLUS)

if __name__ == '__main__':
    im = Image.open(SRC); px = im.load()
    seen = set()
    for x, y, new, *_ in E:
        assert (x, y) not in seen, (x, y); seen.add((x, y))
        assert px[x, y] != 0, ('transparant', x, y)
    log = []
    for x, y, new, part, why, cite in E:
        old = px[x, y]
        if old == new: continue
        px[x, y] = new
        log.append(f"({x:2d},{y:2d}) {old:2d} -> {new:2d} | {part} | {why} | {cite}")
    im.save(OUT, transparency=0)
    with open(os.path.join(D, 'log.txt'), 'w') as f:
        f.write("Capykart r6 -> r7: omlijningsronde (Dragonfly Cave). Paletindices: 1 zwart, 4 donkerbruin, 6 hout, 7 grijs, 8 blauwgrijs, 11 donkergroen, 13 donkerrood.\n")
        f.write("Regel (zoals capybarrel/af): buitenlijn boven/links = donkerste eigen tint (outline base), rechts/onder en linksonder = zwart (outline shadow); binnenlijnen in de donkerste tint van het voorste onderdeel, zwart alleen aan de schaduwkant.\n")
        f.write("Bewust ongemoeid (gezicht): oog, tanden (Bibarel-tanden zijn in Bibarel zelf zwart omlijnd), neusgat (15-16,22), mondlijn (18-19,28), morrillo, kinlijn (25-28,30).\n")
        f.write(f"Aantal gewijzigde pixels: {len(log)}\n\n")
        f.write("\n".join(log) + "\n")
    print(len(log), 'pixels gewijzigd')
