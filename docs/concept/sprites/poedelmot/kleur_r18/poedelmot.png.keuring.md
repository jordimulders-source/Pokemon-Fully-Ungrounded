# Keuring poedelmot kleur_r18 (verse keurder, eerst blind geoordeeld)

Bron: `referenties/samengesteld.png`, mapping uit `silhouet/sil.py` (x 139–854 → 62 px, offset (1,17)). Per spritepixel gemeten: gemiddelde (`me`) en 15e percentiel (`mn`) van de modelhelderheid in het bijbehorende blok. Gen 3-vergelijking: Altaria en Dustox (`graphics/pokemon/*/anim_front_gba.png`).
8×: `scratchpad/keur_r18/side8.png` (model | sprite); 12×/16× per zone: `kop16.png`, `kraag.png`, `poten16.png`, `rvl16.png`, `rach16.png`, `lvl16.png`, `spr_l.png`, `spr_r.png`. Overlays (spritelijnen/-nerf/-glans over het model): `ov_kop.png`, `nerf_l.png`, `nerf_r.png`, `oog_hl.png`. 1×: `gids_vs.png` (modelgemiddelde | sprite), `vgl6.png` (sprite | Altaria | Dustox). Alle bestanden in `/tmp/claude-0/-home-user/00176e0d-eaf6-508f-a6c5-463bdec7182b/scratchpad/keur_r18/`.
1×: houding, massa, ogen, kraag, beide vleugels en de zes klauwgroepen staan goed. Wat meteen anders leest: de sprieten. In het model lopen ze als een donkerbruin geveerd blad met een gebogen lichte nerf hoog in het blad. In de sprite loopt een rechte witte nerf schuin door het midden.

Controle: alpha-diff met het silhouet 0, geen lichte kleur op de buitenrand, geen open randen, 13 kleuren.

## Per onderdeel
| Onderdeel | Oordeel |
|---|---|
| Silhouet | Accuraat (diff 0, bevroren). |
| Linkeroog | **Wijkt af in de glans.** De vorm x16–19 y32–39 klopt (model y33–39, de top 1 rij hoger). De glans staat op (17,34–35), waar het model donker is (77/42). De glans in het model staat op (18,34) (206) en (18,35) (119). Hij staat dus 1 px te ver links. |
| Rechteroog | **Wijkt af in de glans en de rechterrand.** De glans 2×2 staat op (27–28,34–35). In het model is (27–28,34) donker (51/39) en staat de glans op (27,35) (237), (28,35) (159) en (27,36) (188). Hij staat dus 1 rij te hoog en is te breed. Rechterrand x32 y34–37 is donker (2/1). In het model is dat de tan ring (163–170), met een donkerder rand op x33 y35–36 (116/129). In de sprite staat x33 in 6 (168). De ring is dus omgekeerd en het oog 1 px te breed. Olijfglinster (28–30,37–38) en de onderrand kloppen. |
| Kop/kin | Masker, ring boven het oog en de kinlijn kloppen, op de uiteinden na. Links loopt de kinlijn 2 px te ver door: (19,41) en (20,40), waar het model licht is (210/205). Rechts loopt (26,42) te lang (model 201). Het model stijgt daar al op (25–28,41) (110–134). In de sprite staat (25–26,41) licht. De snuit y38–40 x20–24 is in het model beige (205–216), in de sprite wit. Dat is alleen kleur, een klein punt. |
| Sprieten | **Wijkt af in de middennerf**, gemeten als de lichte nerfrun per kolom. Links: model x10 y20,2, x12 y21, x14 y22,4, x16 y23,8, x18 ±25. Sprite (C): y21, y22, y24, y25, y27. Vanaf x10 ligt de nerf dus 1–2 px te laag, en 19 van de C-pixels liggen op donker model (lum 2–61). Rechts: model x34 ±23, x36 22,5, x38 21,3, x40 21, x42 20,5, x44 20. Sprite: y25, 24, 23, 22, 21, 20. Bij x34–40 ligt hij dus 1,5–2 px te laag. In het model is de nerf een boog die hoog in het blad ligt. In de sprite is hij een rechte diagonaal, waardoor het baardjesvlak boven de nerf te breed is en het vlak eronder te smal. De omtrek, de punten, de zwarte onderrand en de steile richting van de baardjes kloppen. |
| Bontkraag | De omtrek links (zigzag x13–16 y38–47), de onderlijn (16–17,47) → (22,53) en de rechterlijn x36–37 kloppen. **Wijkt af in:** een rechte crèmeband van 16 px op y43 (x20–35, index 7) met losse 7-tanden op y44–45. In het model is het daar wit (213–248) met losse verticale tan haarstreken. De band loopt parallel aan de kinlijn (banding). |
| Linkervleugel | Omtrek, zigzag en tan aders accuraat. Eén losse lijnpixel op (12,29) (3), waar het model licht is (226). |
| Rechter voorvleugel | Omtrek (selout 4 boven, 2 rechts), wortel (38–41,34) en golfrand accuraat. **Wijkt af in:** donkere streepjes binnen de rand op (58–60,24) en (58–59,29) (3, lum 74), waar het model wit/tan is (212–245). De naadlijn y35 begint op x39. In het model loopt de lijn op y34 tot x41 en begint hij op y35 pas bij x41. (39–40,35) is daar licht (202/216): een dubbele stomp van 2 px. |
| Rechter achtervleugel | Linkerlijn x40–43 y36–44, golflijn y46–47, tan plaatje en rechterrand accuraat. Eén losse lijnpixel op (54,37) (model 219). |
| Middenstuk/achterlijf | De bruine middenpoot (8/9 x30–34 y47–54) en het tan vlak x37–42 y45–52 accuraat. |
| Poten + klauwtjes | Alle zes klauwgroepen staan op de plek van het model (±1 px): A (18–20,55–57), B-boven (22–24,55–56), B-onder (24–26,58–59), midden (32–34,56–58), voor-midden (35–39,60–61), rechts (43–46,58–59). Ze sluiten aan op hun donsbol, en het aantal klopt. Losse lijnpixels waar het model licht is: (30,48), (35,48), (29,53), (46,56) (model 163–197). Een klein punt. |
| Belijning algemeen | Buitenlijn 1 px, zwart alleen aan de onderrand van de spriet, geen wisseling 1/2 op één rand, selout 4 aan de lichtkant. In orde. |

## Gen 3 (naast Altaria/Dustox)
- Tintstappen wit → crème: A 245 → 7 209 → D 190 → 6 168 → 5 146. Altaria gebruikt voor de wolk ook stappen van 16–24, dus in orde.
- Licht komt van linksboven en de schaduw ligt rechts en onder op de bollen. In orde.
- **Banding:** de rechte 7-band op y43 onder de kinlijn (zie kraag).
- De sprietnerf in C (226) op zwart leest op 1× als een harde witte streep. In het model is de nerf licht tan en dun, en hij krult. Dat volgt vanzelf uit reparatie 1.

## Top-5 reparaties
1. **Sprietnerf op de modelboog leggen.**
   - Links: C op x4–5 y18, x6–8 y19, x9–11 y20, x12–13 y21, x14 y22, x15–16 y23, x17 y24, x18 y25, x19 y26.
   - Rechts: C op x30 y27, x31–32 y26/25, x33 y24, x34–35 y23, x36–37 y22, x38–41 y21, x42–45 y20, x46–51 y19.
   - Zet de oude C-pixels terug in zwart of baardje (6), met de baardjes steil zoals nu.
2. **Ooglichten verplaatsen.**
   - Links: glans naar (18,34) A en (18,35) A. Zet (17,34–35) in 1.
   - Rechts: zet (27–28,34) in 1 en de glans op (27,35), (28,35) en (27,36).
3. **Rand van het rechteroog:** zet x32 y34–37 in 6 (ring) en x33 y35–36 in 4. De zwarte oogrand eindigt dan op x31, zoals in het model.
4. **Kraagband y43 (x20–35) naar A**, met alleen 3–4 korte verticale 7-streken (2–3 px lang) op de plekken van de tan haarstreken in het model. Weg met de losse 7-tanden op y44–45 die er niet onder vallen.
5. **Losse lijnpixels en stompjes weg waar het model licht is:**
   - Forewing (58–60,24) en (58–59,29) naar 7/D.
   - Achtervleugel (54,37) naar D.
   - Linkervleugel (12,29) naar 7.
   - Naadstomp (39–40,35) naar A/7.
   - Kinlijn: (19,41) en (20,40) naar licht, (26,42) naar 7, (25–26,41) naar 3.
   - Pootlijnen (30,48), (35,48), (29,53) en (46,56) nakijken tegen het model.

Oordeel: FAIL
