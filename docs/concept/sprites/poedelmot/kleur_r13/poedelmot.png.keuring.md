# Keuring poedelmot kleur r13 (onafhankelijke keurder, 6 nov)

Bron: `docs/concept/sprites/poedelmot/kleur_r13/poedelmot.png` tegen model `referenties/samengesteld.png` (mapping sil.py: x 139–854 → 62 px, offset (1,17)).
8×: `/tmp/claude-0/-home-user/00176e0d-eaf6-508f-a6c5-463bdec7182b/scratchpad/keur_r13/heel8.png`; zones 12×/14×: `z_kop.png`, `z_gezicht.png`, `z_linksvl.png`, `z_rechtsvl.png`, `z_poten.png`, `z_poten2.png`; spritelijnen als rode stippen óver het model: `lijnen_over_model.png`; Gen 3-vergelijk (Dustox, Venomoth): `gen3_vergelijk.png` (zelfde map).
1×: `.../keur_r13/1x.png`.
Toetsen: alpha-diff met silhouet 0 (1782 px), open randen 0, losse pixels 0, clusters < 3 px 0 (eigen controle + controle_uitvoer.txt).

## Eis 1: accuraat op het model
| Onderdeel | Oordeel |
|---|---|
| Ogen | **Accuraat.** Links x16–19 y32–39 (model 16,5–20,3 / 32–40), glans x17 y34–35; rechts x26–33 y33–40, glans 2×2 linksboven (x27–28 y34–35), olijfreflex B rechtsonder (x30–31 y37–38), tan ring rechts/onder (x33, y40 x28–31) zoals het model. |
| Kop/kin | **Accuraat.** Kinlijn x18–28 y41–42 ligt op de modellijn (overlay); tussen de ogen wit, zoals het model (gemeten 254,246,244). Kuif tussen de sprieten x22–27 y27 met tan selout = model (x 22–27, y 25). |
| Sprieten | **Accuraat.** Links: middennerf C (3,18)→(19,28), ribben 1/4 met periode 3 px. Rechts: nerf langs de bovenrand, punt x52–53 y18–20 (model x 53, y 18). |
| Bontkraag | **Grotendeels accuraat**, wijkt af in de onderrand: model = rafelige vachtpunten over de poten; sprite heeft rechte stukken op y48 (x24–28 vijf 3's op rij, x34–38). |
| Linkervleugel | **Accuraat** in vorm en kleur (wit, tan binnenschaduw, twee lobben rond het oog). |
| Rechter voorvleugel | **Wijkt af in** (a) onderrand: model geschulpt (3 bogen), sprite een rechte lijn y35 x39–49 (11 px) + y36 x50–56 (7 px); (b) wolkenpatroon: model 3–4 rijen tan schulpen met bruine boogjes, sprite grote vlakke 6/7-vlekken (y22–33 x44–57), schulpen niet leesbaar. |
| Rechter achtervleugel | **Grotendeels accuraat** (tan links, crème rechts), wijkt af in de onderrand naar poot D: model geschulpt, sprite recht y46 x45–53 (9 px). |
| Middenstuk | **Accuraat** in kleur (model grijsbruin 140,118,108 → 8/9 klopt) en plaats x30–33 y49–56; leest als smal verticaal strookje, maar dat is in het model ook een smalle donkere naad. |
| Poten (5 + middenpootje) | **Plaats en aantal accuraat** (overlay): A x15–21 y48–54 klauw x18–20 y55–57; B x23–30 y48–56 klauw x25–29 y57–59; middenpootje klauw x32–34 y57–58; C x35–41 y53–60 klauwen x35–39 y60–61 (2 teentjes); D x42–48 y49–57 klauw x43–46 y57–59. **Wijkt af in de belijning:** model = ronde donspluimen; sprite heeft platte toppen/rechte naden (C-top y53 x36–40, B/kraag y48 x24–28), waardoor de onderkant als "baksteentjes" leest. |
| Belijning algemeen | Volgt de modellijnen overal op ±1 px (overlay), maar te recht op de geschulpte/donzige plekken hierboven. |

## Eis 2: Gen 3 (SPRITE_KERN), naast Dustox/Venomoth
- Palet 12 kleuren, netheid ok (clusters/losse pixels 0), contrast-stappen ±30–40 ok, licht linksboven ok, geen pillow shading.
- **Fout:** rechte stukken waar de vorm rond/geschulpt is (y35 11 px, y36 7 px, y46 9 px, y48 5 px, y53 5 px). Dustox/Venomoth: vleugelranden en binnenlijnen als vloeiende curven/trapjes van 1–2.
- **Fout (klein):** 2 en 3 om en om op de buitenrand bij de klauwtjes (y55 x18–20 "232", x22–24 "232", y59 x24–26 "232", y60 x35–39 "23323", y58–59 x43–46 "2323"/"232").
- Binnenlijnen onderlijf te veel en even dik (cellenraster); Gen 3 laat binnenlijnen taps uitlopen in een donkere vlaktint.

## Top-5 reparaties
1. Voorvleugel-onderrand y35 x39–49 + y36 x50–56: maak er 3 schulpbogen van zoals het model (bijv. bogen van 4–5 px, top op y34, dal op y36), lijnkleur 3, uiteinden taps in 6.
2. Achtervleugel/poot D-grens y46 x45–53: 2 bogen (dal y47 bij x48 en x52), niet als rechte 9-px-lijn.
3. Pluimen B en C rond maken: C-top y53 x36–40 als koepel (x37–39 op y52 in 3, x36/x40 op y53), B/kraag-grens y48 x24–28 rafelig (afwisselend y47/y48 met A-punten erin, zoals de vachtpunten in het model); naden tussen pluimen taps laten uitlopen in 6/7 i.p.v. volle 3-lijnen.
4. Wolkenpatroon voorvleugel y22–33 x44–57: 3 rijen kleine schulpen (boogjes 3 px in 6 met een 4/3-onderrand) op crème 7/C, zoals het model, i.p.v. grote vlakke 6-vlekken.
5. Klauwtjes: geen 2/3 om en om op de buitenrand; buitenrand 2, teentje in 3/4 ín de klauw (y55 x18–24, y59 x24–26, y60 x35–39, y58–59 x43–46).

Oordeel: FAIL
