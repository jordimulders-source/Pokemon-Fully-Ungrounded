# Picapau kleur r1: studie (5 nov)

Bekeken op 6x/8x (frame 1 van `graphics/pokemon/<naam>/anim_front.png`): Pikachu, Taillow, Trumbeak, Starly, Pikipek.

| sprite | wat ik overneem |
|---|---|
| **Pikachu** | Geelgroep van 4 + selout: licht (255,246,164), basis (246,230,82), schaduw (246,189,32), diep (222,148,0), lichtkant-rand bruin (156,82,0)/(98,49,8). Ik neem dezelfde opbouw, maar crèmiger: (255,248,192) / (244,218,108) / (218,180,72) / selout (152,100,24). Linkerrand (lichtkant) in goudbruine selout, rechts en onder zwart, net als Pikachu. **Oog pixel voor pixel overgenomen** (Pikachu rechteroog, 4x4: `3kk3 / Gwke / kkGe / 3kk3`, met glans linksboven). Wangvlek zonder omlijning, twee tinten rood (licht linksboven). Oorpunten zwart met één donkergrijze binnentint → kuiftoppen zwart. |
| **Taillow** | Zwarte buitenlijn aan de schaduwkant, korte snavel als 3 rijen (bovenrand donkerder geel, midden licht, onderrand donker); pootjes als afwisselend lichte teen/omlijning (`6c6c6`). Helderheidsstappen ±30–40 per tint. |
| **Trumbeak** | Rechtopstaande vogel met de snavel schuin omhoog: snavel lichte vulling met donkere onderlijn, kop als eigen ronde vorm boven een rank lijf. |
| **Starly** | Vleugel als donker vlak over het lijf, met binnenlijn in de donkerste tint van de vleugel (geen zwart), licht van linksboven. |
| **Pikipek** | Alleen ter controle dat het geen kopie wordt: Pikipek is zwart-wit-rood met een gedrongen lijf; Picapau deelt alleen "specht, kuif, snavel omhoog". Kleurgroepen bewust anders (geel/bruin/rood-wang). |

Toegepast:
- Licht linksboven (niet de Blender-belichting): hooglicht als vlek linksboven op kop en borst (niet als band langs de rand), schaduwsikkel onder de kop (scheidt kop en lijf) en langs de rechter-/onderkant van het lijf onder de vleugel.
- Vleugel: dekveren donkerbruin met rijen roomkleurige schubjes (u-vormen, zoals foto 3/5), slagpennen roodbruin met donkere scheidingslijnen evenwijdig aan de vleugelrand (foto 5).
- Staart: roodbruin, donkerbruine rand aan de lichtkant, zwart rechts, donkere vouwlijn op de knik (rij 51).
- Helderheid (luma): geel 244/213/179/107, bruin 117/86/53, wang 123/82: stappen ±30–35, zoals Taillow.
