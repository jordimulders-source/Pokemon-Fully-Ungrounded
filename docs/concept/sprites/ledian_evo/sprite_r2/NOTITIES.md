# Ledian-evolutie, frontsprite ronde 2: kleurronde (27 nov)

Jordi: "ja houd het kleurpatroon van ledian maar aan, mooi design verder" · keuze "2, maar mag net iets roder" (tinten van Ledian, verdeling van r6).

Basis: `../sprite_r1/ledian_evo_r1.png`. Vorm en kleurverdeling bevroren; alleen tinten. Scripts vanuit de repo-root: `bouw.py` (→ `ledian_evo_r2.png`, `rood_a/b/c.png`), `vel.py` (→ `vel.png`, `vergelijk.png`, 8×-bestanden).

## Wat er gebeurt
1. Elke r1-index krijgt 1-op-1 de Ledian-tint van dezelfde rol (licht/midden/schaduw/selout). Waar licht en donker zit komt dus uit het model (r1 = gekwantiseerd model); er is geen grens verschoven.
2. Donkergrijze binnenlijnen in rood (1 px dik, ≥ 2 rode buren, geen 2×2-blok donker) → rode selout. Stippen, het ruitje op het voorhoofd, sprieten, gewrichten en de donkere vleugelband blijven donkergrijs (blokken, geen lijnen).
3. Zwarte buitenlijn aan de lichtkant (transparant boven/links, niet onder/rechts, grenst aan rood) → rode selout.

## Palet (hoofdversie = rood b, 13 incl. transparant)
0 transparant · 1 zwart 101010 · 2 donkergrijs 393939 (was 2a2929; Ledian heeft geen tussentint) · 3 grijs 6a6a6a · 4 b4b4b4 · 5 d5d5d5 · 6 wit ffffff · 7 selout 832210 · 8 schaduw c52110 · 9 basis ff3c20 · 10 licht ffb483 · 11 geel f6e673 · 12 goud cdb439.

Roodvarianten (Ledians ramp met de hue lager, zelfde S en V):
| | graden | selout | schaduw | basis | licht |
|---|---|---|---|---|---|
| Ledian | 0 | 833110 | c53910 | ff5a20 | ffc583 |
| a | −5 | 832710 | c52a10 | ff4720 | ffbb83 |
| **b (hoofd)** | −8 | 832210 | c52110 | ff3c20 | ffb483 |
| c | −11 | 831c10 | c51810 | ff3120 | ffae83 |

## Bewijs / wijzigingen
- Silhouetdiff t.o.v. r1: **0** (assert in `bouw.py`).
- Indexwijzigingen: 83 px. Hoofd 26 (binnenlijn) + 5 (lichtkant-buitenlijn); romp/armen 26 + 1; vleugel 3; benen 14 + 8. Oog, mond, vuisten, sprieten, voeten: 0.

## Zwakke punten (eerlijk)
- Modellicht (f47371, 135 px) → Ledians lichttint (perzik). Ledian gebruikt die tint spaarzaam (47 px); hier staan perzikbanden op kop, romp en benen. Is het te veel/te bleek, dan is de volgende stap een lichttint dichter bij de basis (geen nieuwe grenzen).
- Donkergrijs 393939 is geen Ledian-tint; zonder die tint verdwijnt het volume van stippen/sprieten.
- Schaduw (c52110, 327 px) is nog altijd het grootste roodvlak: het model is donker; verdeling bewust niet aangepast.
- Lichtkant-selout is maar 14 px: het grootste deel van de buitenlijn grenst aan grijs/zwart of ligt aan de schaduwkant.
- Nog geen keurder gezien.
