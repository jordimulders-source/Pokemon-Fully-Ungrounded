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
- Claudes eigen modelaanpassing `model/model_hand3.png` is afgekeurd ("dat ziet er echt totaal niet uit"): niet gebruiken.

## Volgende stap
Frontsprite volgens de poedelmot-methode (zoals de charlatan-Alakazam, `alakazam_regional/`): onderlaag = model verkleind, alleen de hand + armpose als benoemde afwijking.
