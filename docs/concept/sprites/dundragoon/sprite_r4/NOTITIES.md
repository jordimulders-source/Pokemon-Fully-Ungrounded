# Dundragoon frontsprite, ronde 4 = eindkeuring (Dragonfly Cave)

Bestanden: `dundragoon_r4.png` (64×64, P, index 0 transparant, 12 kleuren, palet ongewijzigd t.o.v. r3), `dundragoon_r4_8x.png`, `bouw.py` (r3 + lijst tintwissels met controle van de oude index; drukt het bewijs af), `vel.py` → `vel.png` (r4 | r3 | model op 8×; daaronder r4, r3 op 1× en r4 op 2× op wit, crème, donkergrijs, zwart).
Bouwen: `cd docs/concept/sprites/dundragoon && python3 sprite_r4/bouw.py && python3 sprite_r4/vel.py`.

## Bestudeerd (Gen 3, `anim_front_gba.png` op 8×)
- **Dunsparce**: geel lijf als cilinder: lichtste tint bovenop, brede middentint, schaduwtint als band onderaan vlak boven het blauwe buikdeel; de schaduw volgt de buikrand en wordt naar de staart breder. Boor: lichte streep op de lichtkant van elke winding, donkere lijnen tussen de windingen, geen licht dat een lijn kruist.
- **Gulpin**: groot rond middenvlak; licht als breed vlak linksboven, schaduwsikkel rechts die onderlangs doorloopt en naar onder breder wordt; geen concentrische banden (geen pillow shading).
- **Dragonair**: lang cilinderlijf met een tapse glansstreep langs de lengte op de bolling, schaduw langs de onderrand.
- **Whiscash**: groot donker vlak met licht op de bovenbolling en een donkere band boven de lichte buik.
- **Altaria/Flygon**: vleugels/wolk met gekleurde selout aan de lichtkant, zwart aan de schaduwkant; zelfde patroon als de Dundragoon-vleugels (blauwgrijze rand links/boven, zwart rechts).

## Oordeel per onderdeel (alleen uitvoering)
- Kop, oog, hoorns: volume al goed (groot lichtvlak linksboven, schaduw onder); niets veranderd.
- Vleugels: gekleurde selout links/boven, zwart rechts, vaantjes met lichte vlakken; als bij Altaria. Niets veranderd.
- Boor: leest op 1× en 8× als gedraaide kegel (licht per winding rechtsboven, lijnen op modelplek); niets veranderd.
- Pootjes en buik: in orde; niets veranderd.
- **Lijf (KAN-punt vorige keurder)**: het grote middengele vlak had alleen een smal hooglicht linksboven en schaduw rechts; de onderkant boven de buik was vlak. Opgelost met twee tintwissels (zie hieronder).

## Wijzigingen (24 px, alleen index 4 → 3 of 4 → 5, palet ongewijzigd)
- **lijf_sikkel (18 px, middengeel 4 → schaduwgeel 3):** schaduwsikkel langs de onderkant van het lijf, net boven de donkerblauwe buiklijn: punt van 1 px bij de lijfflap (32,34), via (32–33,35), (33–34,36), (35–37,37), (37–40,38) tot (39–44,39), waar hij aansluit op de bestaande schaduw rechts en de schaduwrij 40. Smal bovenaan, breder naar de boor, zoals bij Dunsparce en Gulpin.
- **lijf_hooglicht (6 px, middengeel 4 → licht 5):** het bestaande rughooglicht (eindigde op (30,26)) loopt taps door in een boogje om de punt van de eerste rugband heen over de bolling: (31,27), (31,28), (32,29), (33,29), (33,30), (34,30). Kruist geen lijn of band; 1 px breed, eindigt vrij in het middengeel.

## Bewijs (uitvoer `bouw.py`)
```
alpha-diff (pixels waar transparant/niet-transparant verschilt): 0
gewijzigde pixels totaal: 24
  lijf_sikkel 18
  lijf_hooglicht 6
```
Gewijzigd totaal = som van de twee lijfzones, dus 0 px gewijzigd in kop, oog, hoorns, vleugels, rugbanden, buik, pootjes, boor en alle lijnen (index 1, 2, 6–11 ongemoeid). `gereedschap/controle.py`: 12 kleuren, ≤3 tinten per groep + lijn, geen lichte buitenrand, geen losse zwarte pixels, zwart 13,7 %.

## Ter info voor Jordi (niet uitgevoerd)
- Geen ontwerpvragen; het model is ongewijzigd gevolgd.
