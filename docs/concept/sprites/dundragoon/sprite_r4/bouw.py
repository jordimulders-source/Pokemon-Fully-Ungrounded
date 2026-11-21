# bouw.py: r4 = r3 + eindkeuring (alleen tintwissels binnen het silhouet, palet ongewijzigd)
# Draaien vanuit docs/concept/sprites/dundragoon:  python3 sprite_r4/bouw.py
import numpy as np
from PIL import Image

r3 = Image.open('sprite_r3/dundragoon_r3.png')
a = np.array(r3)

# (x, y, van, naar) per zone; 'van' wordt gecontroleerd zodat niets per ongeluk overschreven wordt
WISSELS = {
    # Lijf: schaduwsikkel langs de onderkant boven de buik (middengeel 4 -> schaduwgeel 3),
    # punt (1 px) bij de lijfflap, naar de boor toe breder en aansluitend op de bestaande schaduw rechts.
    'lijf_sikkel': [(32, 34), (32, 35), (33, 35), (33, 36), (34, 36),
                    (35, 37), (36, 37), (37, 37),
                    (37, 38), (38, 38), (39, 38), (40, 38),
                    (39, 39), (40, 39), (41, 39), (42, 39), (43, 39), (44, 39)],
    # Lijf: rughooglicht loopt in een taps boogje door om de punt van de eerste rugband heen,
    # over de bolling van de romp (middengeel 4 -> licht 5). Gaat niet over een lijn of band heen.
    'lijf_hooglicht': [(31, 27), (31, 28), (32, 29), (33, 29), (33, 30), (34, 30)],
}
VAN_NAAR = {'lijf_sikkel': (4, 3), 'lijf_hooglicht': (4, 5)}

for zone, pts in WISSELS.items():
    van, naar = VAN_NAAR[zone]
    for x, y in pts:
        assert a[y, x] == van, (zone, x, y, a[y, x])
        a[y, x] = naar

out = Image.fromarray(a.astype(np.uint8), 'P')
out.putpalette(r3.getpalette())
out.info['transparency'] = 0
out.save('sprite_r4/dundragoon_r4.png', transparency=0)

# Bewijs: alpha-diff 0 en telling per zone
b = np.array(r3)
print('alpha-diff (pixels waar transparant/niet-transparant verschilt):', int(((a == 0) != (b == 0)).sum()))
print('gewijzigde pixels totaal:', int((a != b).sum()))
for zone, pts in WISSELS.items():
    print(' ', zone, len(pts))
