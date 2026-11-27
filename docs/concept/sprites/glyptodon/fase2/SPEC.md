# Glyptodon-lijn fase 2 (eindvorm) – SPEC

Regionaal fossiel, **Rock/Normal**, wall, eigen ability (later). 2 fases; fase 1 = "gewoon een kleinere variant, minder ontwikkeld, beetje cranidos/rampardos, shieldon/bastiodon idee". Tegenhanger: terreurvogel (Rock/Fighting). Achtergrond: `docs/concept/IDEEEN.md` → "Regionale fossielen".

## Jordi letterlijk (27 nov)
- "glyptodon eindfase eerst."
- Staart: "staart zoals op de foto, soort van drill, of wordt dat dan teveel dunsparce? Anders knots" (`referenties/jordi_staart_foto.png`: ringen van bolle botplaten, taps toelopend).
- "Hij moet duidelijk gepantserd zijn, we kunnen het schild niet heel veel kleine vakjes geven, dus dat wordt meer smooth"
- "hij staat klaar om zich te bracen met zijn schild" / "dus met zijn hoofd wel eruit, maar een beetje gebukt"

## Open
- Kleuren (niet besproken; prompt r1 laat ze aan Gemini).
- Staart fase 2: Jordi "2 dan de knots", maar "drill en knots kunnen we weer allebei kijken" (r2 A en B). Fase 2: "massiever, zwaarder, dreigender, misschien wat stekels op het schild". Fase 1-kandidaat: r1 A.

## Model (27 nov)
`model.png` = r4 + stekel met band van r6 (plek en hoek als r6) + staart van r3_3 + schildstrepen van r6, geplakt op het natieve Gemini-raster (100×100, zie `gemini/PROMPTS.md`). Jordi: "let erop dat door het copy pasten er wat pixel blur is ontstaan".
- **Jordi (27 nov):** "het fase 2 model is echt super slordig geknipt en geplakt dus zorg dat de agent daar rekening mee houdt" / "anders gaat het helemaal fout". Afspraak met de maker: per onderdeel vanaf het scherpe bronplaatje werken (r4: lijf, kop, poten, schildvorm, vizier; r6: stekel+band en schildstrepen; r3_3: staart); `model.png` bepaalt alleen plek, hoek en overlap.
- Over sprite r2 (27 nov): "best netjes al, vooral heel veel losse zwarte pixels die nog opgeruimd moeten worden, maar dit begint zeker ergens op te lijken, als je de lijnen om het oog nog iets minder donker kan maken is het oog ook al goed".
