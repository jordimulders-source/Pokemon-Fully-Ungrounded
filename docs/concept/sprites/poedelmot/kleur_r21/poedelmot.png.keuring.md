# Keuring poedelmot kleur r21 (onafhankelijk, blind geoordeeld; eerdere keuring pas daarna gelezen)

Bron: `referenties/samengesteld.png` (mapping sil.py: x 139–854 → 62 px, offset (1,17)); sprite `kleur_r21/poedelmot.png` (64×64, 14 kleuren + transparant).
8×: per onderdeel naast het model met raster (scratch `keur_r21/g_kop.png`, `g_vl.png`, `g_vr.png`, `g_mid.png`, `g_pl.png`, `g_pr.png`), plus per pixel gemeten (px.py / BOX-model, gem/p15).
1×: naast het BOX-verkleinde model (`keur_r21/full8.png`, `1x3.png`) en naast Dustox/Venomoth (`gen3.png`).

## EIS 1: accuraat t.o.v. het model
- **Ogen:** lijkt op. Linkeroog x16–19, y32–39 (model 16,5–20,2 / 32,6–40,1); glans (18,34) = model 17,2–18,4 / 34–35,5. Rechteroog x25/26–31, y33–40 (model 25–31 / 33–40); glans (27–28,35)+(27,36) = model 26,5–28 / 34,5–37; olijfreflex rechtsonder (30,37),(28–29,38) = model 28,5–30,5 / 37–39. Tan ring om het rechteroog (6 op x32–33, rij 32 en 40) zoals het model.
- **Kop/kin:** lijkt op. Snuit tan tussen de ogen y37–41; kinlijn (19,39)→(20,41)→(21–25,42)→(25–28,40–41); model donker op precies die pixels (p15 2–6), ook de dubbele rij 40/41 onder het rechteroog (model p15 2–3 op beide).
- **Sprieten:** lijkt op. Middennerf links (4–5,18)…(19,26) valt ≤1 px op de modelnerf (helderste rij per kolom); rand en lengte = bevroren silhouet. De lichte dwarsstrepen hebben in het model een periode van ±1,4 px: niet weer te geven, de C-strepen als textuur zijn correct. Rechterspriet idem.
- **Bontkraag/kruin:** lijkt op. Witte kraag rond de kop, haarstrengen in 7/3; kruinrand (22–29,24–27) volgt het model; scheidingslijnen kraag–poten (16–19,46–49) en kraag–vleugel (37–41,31–34) op de modelpixels (p15 < 10).
- **Linkervleugel:** lijkt op. Wit boven, tan vlekkenband y30–34, inkeping (10–13,36–38) zoals het model.
- **Rechter voorvleugel:** lijkt op. Voorrand + witte strook (40–43,28–33) aansluitend op (40,34); krullijnen (5) op de modelkrullen; naad met de achtervleugel op y35 (x41–51) en (52–54,36), gat (54,36) dicht.
- **Rechter achtervleugel:** lijkt op. Lijf-vleugellijn x41–42, y36–44 = model 40,5–42; tan midden, onderrand (44–53,45–46).
- **Middenstuk:** lijkt op. Tan achterlijf (6) x39–44, y45–53 met segmentlijnen op de modellijn ((42,43)→(36,49)); de ene modelpixel (41,45) p15 3 valt naast de sprietlijn (40,45): kleiner dan 1 px, geen afwijking.
- **Poten + klauwtjes:** lijkt op, alle vijf aangesloten en omlijnd. Linkerpluim x15–21/y47–54, klauwtjes (18–20,55–57) = model 17,5–21/55–57. Voorpoot links: grote pluim x21–30/y47–54 + voetpluim (26–30,56–57), klauwtjes (24–26,59) = model 24–27/58–59,5. Middenpoot (9/8) x30–35, donkere punt (30–31,55–56) = model zwart (31,55–56); (35–36,50) in 4 = model p15 3–5. Voorpoot rechts x35–39/y54–59, klauwtjes y60–61 = model 60,5–62 (pluim ±1 px smaller dan model 34,5–41: binnen wat 64 px kan). Rechterpluim x41–47/y50–57, klauwtjes (43–45,58–59) = model 43–46,5/58–59,3. Geen extra poten.
- **Belijning:** lijkt op; alle modellijnen aanwezig en aansluitend, geen open randen. Binnenlijnen zijn 3 (donkere vlaktint) waar het model zwart is: dat is de Gen 3-eis, geen afwijking.

## EIS 2: Gen 3
- Netheid (controle.py zelf gedraaid): alpha-diff 0 met het bevroren silhouet, open randen 0, losse pixels 0, tintclusters < 3 px 0.
- Buitenlijn 1 px: 2 (120) aan de schaduwkant, 3/4 als selout op de lichtkant (4 in 2 reeksen van 7 en 8 px), 1 alleen in de zwarte sprietranden; geen 1/2 om en om op één rand, geen lichte kleur op de buitenrand.
- Kleurgroepen ≤ 3 tinten + lijn (wit A/7/D, tan 6/5/4, mauve 8/9, spriet E/C/D); licht linksboven, geen banding of pillow shading gezien op 8×.
- Naast Dustox/Venomoth op 1×: zelfde lijndikte, contrast en leesbaarheid; ogen lezen als Pokémon-ogen.

## Reparaties
Geen. (De vier reparaties uit r20, achteraf gelezen, zijn alle vier uitgevoerd en kloppen met het model.)

Oordeel: PASS
