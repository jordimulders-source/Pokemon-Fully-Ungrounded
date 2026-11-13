# SPEC regionale Kadabra (charlatan-leerling, Dark/Psychic), frontsprite

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken" + `GEMINI.md` + `SPRITE_KERN.md`. Gemini-rondes: `gemini/README.md`.

## Jordi (letterlijk)
- "Die toont 1 kaart in een 'is this your card pose', die is consistent in het design met alakazam, maar nog niet zo'n zeer ervaren charlatan, nog meer een apprentice."
- "ik wil toch voor een klaver gaan ipv een hart ook" + kleur: "rood".
- "buiten dat is als enige rood op zijn hoofd voldoende" (geen keelwam, alleen de rode klaver).
- Ronde 5: "Helemaal perfect, behalve dat de rechterhand 5 vingers heeft ipv 3 en het mensenvingers zijn".
- "Vergeet niet dat de arm echt in een tahdah/voila pose moet" (de open arm).
- Niet Jordi laten tekenen: "het is niet de bedoeling dat ik ga tekenen".

## Model
- Basis: `gemini/ronde5.png` ("helemaal perfect" op de open hand na). `gemini/ronde8_hand_klauwen5.png` heeft wel klauwtjes maar 5 vingers.
- Open hand (rechts in beeld): **3 vingers met klauwtjes**, Kadabra-stijl (zie `referenties/kadabra_artwork_hand.webp` en de voeten van het model), de arm in een **"tahdah/voilà"-pose**. Dit lost de maker-agent op in de sprite (Gemini telt de vingers niet goed); Jordi tekent niet.
- Eerste eigen modelaanpassing van Claude was afgekeurd ("dat ziet er echt totaal niet uit") en is verwijderd. Tweede poging (12 nov): `model/model_hand3_v2.png`, Jordi: "de middelste vinger lijkt nu net alsof die gebroken is, die moet iets natuurlijker gepositioneerd, dan is die goed" → `model/model_hand3_v3.png` (middelvinger recht en taps, `model/h4.py`); Jordi: "nee het is de verbinding aan de hand die nog steeds krom is" → `model/model_hand3_v4.png` (gladde randen, vinger loopt zonder inkeping over in de handpalm, `model/h5.py`; wacht op Jordi). v2 = ronde 8 (Gemini-hand met klauwtjes) met de vierde vinger weggehaald, dus 3 vingers in Gemini's eigen stijl (`model/h3.py`, vergelijking met de Gen 3-Kadabra/Alakazam: `model/hand_v2_vergelijking.png`).

- v7/v8 (Claude haalde de duim weg / tekende klauwtjes): afgekeurd ("het is zo duidelijk te zien dat die nu geen duim heeft, het klopt niet"). De hand heeft dus een **duim + twee vingers**, elk met klauwtje. Claude tekent niet meer aan het model; nieuwe complete Gemini-prompt: `gemini/PROMPT_v5.md`.

## Volgende stap
Frontsprite volgens de poedelmot-methode (zoals de charlatan-Alakazam, `alakazam_regional/`): onderlaag = model verkleind, alleen de hand + armpose als benoemde afwijking.
- **Handpose naar Jordi's schets (12 nov):** `referenties/jordi_schets_hand.png`; Jordi: "het is niet mogelijk om de pose van de hand te doen zoals in mijn zeer lelijke schets hier?". Claude: `model/model_hand_v5.png` (ronde handpalm, drie vingers als waaier naar rechts, elk met klauwtje; `model/h6.py`); wacht op Jordi.
- **v7 (12 nov):** Gemini volgde Jordi's schets maar tekende te veel vingers (`gemini/ronde9_schets_hand5.png`; Jordi: "gemini heeft evident discalculie, maar kan je hier iets mee?"). Claude haalde de duim linksboven weg: `model/model_hand_v7.png` (drie vingers als waaier naar rechts, `model/h8.py`); wacht op Jordi.
- **Model = ronde 10 B (12–13 nov).** Jordi: "de 2e is beter, alleen beide handen hebben 4 vingers, kan je dit fixen?" en "de handen poses maken me niet meer uit, zolang ze maar natuurlijk zijn". Claude: `model/model_B_hand3.png` (`model/h10.py`): open hand = onderste vinger weg (duim, vinger omhoog, vinger schuin rechts, Gemini's eigen pixels); kaarthand: Jordi: "de hele hand klopt niet. Als je een kaart zo houdt zouden wij als kijker de binnenkant van de hand moeten zien, nu is die omgekeerd en lelijker" → handpalm naar de kijker onder de kaart, duim met klauwtje over de kaart, vingers achter de kaart. Wacht op Jordi. Bronnen van Jordi: `referenties/kadabra_artwork_groot.webp`, `kadabra_sprite_a.png`, `kadabra_sprite_b.png`, `kadabra_render.png`.
