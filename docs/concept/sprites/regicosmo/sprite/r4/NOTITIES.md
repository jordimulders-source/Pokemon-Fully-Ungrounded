# Regicosmo frontsprite, ronde 4 (maker): r4a / r4b / r4c op basis van r3

Jordi (28 nov): "nee de bollen lezen allemaal nog niet echt rond, middelste ook niet. Wat je kan doen is sowieso de twee bovenste een pixel lijn naar rechts schuiven. De twee planeten die ook 'arm' zijn nog iets naar boven schuiven en de twee 'voeten' ook 1 pixel naar boven en kijken hoe dat werkt. Ik vind saturnus er wel prima uit zien, maar misschien kan je nog een versie maken waar je die en de ijsplaneet iets groter maakt als een soort schouders".
Bouwen: `cd docs/concept/sprites/regicosmo && python3 sprite/r4/bouw.py && python3 sprite/r4/vel.py`. Code: `rond.py` (cirkelfit, cirkel, verschuiven), `saturnus4.py` (Saturnus/ijs op maat), `bouw.py`.
Bestanden: `regicosmo_r4a.png`, `regicosmo_r4b.png`, `regicosmo_r4c.png` (64×64, P, index 0 transparant, 16 kleuren, 7 losse delen, x0–63 y16–61), `vel.png` (r3 | r4a | r4b | r4c op 8×, daaronder elk 1× en 2× op wit en donker + model 1×).

## 1. Rondheid
- Cirkelfit (kleinste kwadraten) op de modelomtrek per bol, omgerekend naar de sprite: Mars c=(29,83; 31,88) r=16,48 → **diameter 33**, middelpunt (29,5; 31,5); maan c=(52,76; 46,96) r=5,10 → **diameter 10**, middelpunt (53; 47); ijs diameter 10 (maat r3, fit 9,2), middelpunt (6; 30); Saturnusbol was al een cirkel van 10 (r3, onveranderd).
- Rand = ideale pixelcirkel (pixel erin als zijn middelpunt binnen d/2 ligt; middelpunt op een pixelhoek bij even, op een pixelmidden bij oneven diameter): Mars rijlengtes 9-13-17-21-23-25-27… symmetrisch, geen platte stukken buiten de bovenste 9 en geen uitstulpingen.
- Binnenwerk: r3 waar het al binnenwerk was; pixels die nieuw binnen de cirkel vallen of oude buitenlijn waren → kleur uit de modelcel (zelfde gewogen reductie als `kaal.py`). Daarna buitenlijn op de nieuwe rand (normaal vanuit het middelpunt; zwart aan de schaduwkant, selout aan de lichtkant). IJs: de r2-regel (modelhelderheid < 208 → cyaan, anders bijna-wit) over de hele bol. Stippen ongewijzigd.

## 2. Posities (t.o.v. r3)
- IJs en Saturnus 1 px naar rechts: Saturnus zat al tot x63, dus alle andere delen 1 px naar links (komt relatief op hetzelfde neer).
- Armen (asteroïde, maan): r4a 1 px omhoog, r4b 2 px omhoog. Voeten 1 px omhoog.
- Daarna alles 1 px omlaag, zodat de onderkant op rij 61 blijft (Gen 3); relatief verandert er niets.
- Kleinste tussenruimte r4a en r4b: 1 px (Mars–ijs), daarna 2 (Mars–blauwe voet), 3 (Mars–Saturnus).

## 3. r4c schouders (= r4b + ijs en Saturnusbol 12 px)
- IJs: modelijs geschaald naar diameter 12 (x0–11). Op de r4b-hoogte raakt het Mars; de laagste plek met ≥ 1 px tussenruimte is **6 px hoger** (middelpunt (6; 25)). Saturnus op dezelfde hoogte (schouders gelijk), bol 12 px, middelpunt (55; 25), modelbol geschaald.
- Ring: zelfde kanteling en verhouding als r3; de lengte die binnen x63 en met ≥ 1 px tot Mars past is a = 7,90 (r3: 8,48 bij bol 10), dus de lussen steken maar ±1,5 px buiten de bol.
- Mars niet verkleind. Kleinste tussenruimte 1 px (Mars–ijs, Mars–Saturnus).

## Twijfels
- r4c: de breedte is de grens (12 + 1 + 33 + 1 + Saturnus ≤ 64): ijs en Saturnus moesten 6 px omhoog, en de ring is te kort voor de grotere bol (leest minder als ring dan in r3/r4b).
- Mars–ijs 1 px tussenruimte in alle drie.
