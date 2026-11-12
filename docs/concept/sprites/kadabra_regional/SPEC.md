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
- Eerste eigen modelaanpassing van Claude was afgekeurd ("dat ziet er echt totaal niet uit") en is verwijderd. Tweede poging (12 nov): `model/model_hand3_v2.png`, Jordi: "de middelste vinger lijkt nu net alsof die gebroken is, die moet iets natuurlijker gepositioneerd, dan is die goed" → `model/model_hand3_v3.png` (middelvinger recht en taps, `model/h4.py`; wacht op Jordi). v2 = ronde 8 (Gemini-hand met klauwtjes) met de vierde vinger weggehaald, dus 3 vingers in Gemini's eigen stijl (`model/h3.py`, vergelijking met de Gen 3-Kadabra/Alakazam: `model/hand_v2_vergelijking.png`).

## Volgende stap
Frontsprite volgens de poedelmot-methode (zoals de charlatan-Alakazam, `alakazam_regional/`): onderlaag = model verkleind, alleen de hand + armpose als benoemde afwijking.
