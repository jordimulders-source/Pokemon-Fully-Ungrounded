# Steenmozaïek-jaguar (eigen lijn, 2 fases): SPEC

Werkwijze: `docs/lessen/GEMINI.md` + `docs/lessen/SPRITE_WERKWIJZE.md` (Gemini-model namaken) + `docs/lessen/SPRITE_KERN.md`. Idee: `docs/concept/IDEEEN.md` (Steenmozaïek-katachtige). Gemini-rondes: `gemini/README.md`.

## Jordi's woorden (letterlijk)
- 10 nov: "ok we maken een nieuwe" · "het is sowieso een katachtige. en dan zou ik daar een rock type van willen maken" · "hier een pokemon van maken lijkt me ook wel tof"
- 13 nov: "Ik wil een soort rock jaguar lijn maken gebaseerd op mijn beeldje uit mexico, 2 fases"
- 13 nov (keuzes): type **beide puur Rock**; **beide fases uit het beeldje**; verschil **welp → volwassen**; pose **staand op 4 poten**; werkwijze **Claude schrijft Gemini-prompts**, Jordi draait Gemini en kiest.
- 13 nov: "Beide zijn geinspireerd door die beelden, maar fase 2 is nog mooier en geavanceerder qua materiaal en kleur dan 1"

## Bron
- `referenties/beeldje_jordi_mexico.png`: het beeldje. Wat de foto toont: een kop met open muil en witte hoektanden, een rond zwart oog, ingelegd met hoekige stukjes blauw/lila, roodbruin, zwart en crèmekleurig gesteente, gescheiden door dunne voegen.

## Model (fase 2, gekozen 13 nov)
- `referenties/model_gekozen.png` (= `gemini/fase2_ronde5.png`). Jordi (letterlijk): "De staart groter maken was mijn eigen touch. Ik ben tevreden op een soort van extra oog na op de wang, maar die kan je zelf wel weghalen, dat blijft die doen gek genoeg, bouw hier maar een sprite van, net zoals bij de poedelmot. Dus niet zelf onderdelen opnieuw gaan tekenen"
- Wangoog: het oog zonder glans op het crèmestuk (native x40–43, y35–38) is weggehaald (13 pixels → crème van dat stuk); het oog met glans blijft. Keuze welk oog "extra" is: Claude (ter controle aan Jordi).
- Sprite-onderlaag: `sprite/natief.png` (Gemini-raster terug, 120×95 modelpixels, `sprite/natief2.py`), `sprite/natief_zonder_wangoog.png`; sprite = 2×-reductie (±60×48).

## Open
- Naam, formaat per fase (pas bij het silhouet), welk Gemini-model gekozen wordt.
