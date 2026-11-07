# Kleur ronde 4 (maker-agent, 2 nov)

Jordi: "1 ja warmer, rest zoals het nu is, blijf vergelijken met andere sprites, dragonflycave guide etc en laat agents keuren". Basis `ronde3.txt`; `rijen_ronde4.py` → `ronde4.txt`, `ronde4.png`, `ronde4.pal`, vel `vel_ronde4.png` (`vel4.py`: 4x licht/donker van ronde 4 en ronde 3; 2x/1x naast olinguito, Coathief, zangoose, sneasel, linoone, ursaring, furret, sentret). Alpha-diff 0, geen open randen. Pixels: 17 gewijzigd (alleen de staarthaak); verder alleen het palet.

**Palet (warmer, meer contrast, hue shift):**
- **Vacht:** van koel grijs naar warm grijsbruin (de familie van olinguito en Coathief). Luma 58 / 86 / 114 / 145, plus hooglicht 3 = 182: stappen van ±30, de schaduw dieper en het hooglicht lichter dan in ronde 3. Het licht schuift naar geel/warm, de schaduw iets koeler en dieper (SPRITING §2, Dragonfly Cave: hue shifting).
- **Masker/onderarmen/ringen:** warm zwart (24,15,12) / (46,34,28).
- **Crème:** warm wit (244,236,218) → crème → oker-schaduw (172,150,118), zoals Mareep/Ponyta (SPRITING: crème hue-shift naar oker); luma 153 / 199 / 236.
- **Buidel:** eigen roodbruin (88,56,36) / (128,84,52) / (166,118,76) uit de Coathief-familie, luma 63 / 94 / 128. Duidelijk anders dan de warmere grijsbruine vacht. Ook de crème selout van de verre klauw (c) wordt daardoor oker-bruin.
- **Iris:** iets warmer.

**Staarthaak** (Furret/Sentret: elk deel van de krul eigen licht en schaduw): de terugkrullende punt (x 49–50, y 22–29) staat los van de schacht door een donkere binnenlijn 1 op x 51. Punt en schacht hebben elk licht 4 links en kernschaduw 1 rechts.

Bevroren gehouden: crème handen/klauwen, verre oog, buidel als eigen tint, borst, klauwvorm, masker, pose, silhouet.

## Eigen zwakke punten (eerlijk)
- **Staarthaak:** leest op 1x nog vooral als donkere knots. De binnenlijn (1 naast 2) heeft te weinig contrast, en zonder opening in het silhouet kan een haak alleen met licht/schaduw lezen. Furret/Sentret lossen dat op met lichte ringen over de krul; hier is de haakkop een donkere ring (render).
- **Bovenarm:** op 1x nog steeds nauwelijks te zien (vacht op vacht); het warmere contrast helpt maar weinig.
- **Zakmond:** op 4x een opening, op 1x een klein donker streepje; de plooi leest beter door de lichte d.
- **Klauwinkeping:** de nabije klauw is op 1x een lichte vlek, de inkeping zie je pas op 2x.
- **Buidel:** de tint ligt dicht bij Coathiefs vacht; naast de nu warmere wasbeervacht onderscheidt hij zich goed, maar hij kan als "Coathief-bruin" lezen.

## Lessen
- Een palet warmer maken met dezelfde lumastappen houdt de leesbaarheid gelijk; contrast komt pas met grotere lumastappen (±30 per tint) en een lichter hooglicht.
