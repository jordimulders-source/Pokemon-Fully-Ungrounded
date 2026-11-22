# Keuring Picaraio sprite v2, r3 (19 nov)

Gekeurd: `picaraio.png` + `normal.pal` tegen `gemini/r9_prompt_v6.png`. Vergeleken: sprite op 10× met raster naast het model, verkleind op dezelfde bbox (25–998 × 10–962 → 64×62, geplakt op y=1), plus de lijnen in de kuif per kolom gemeten in het model (donkerste pixel per spritekolom, naar de spriterij omgerekend).

## Oordeel: FAIL (klein; nog één ronde)

De acht punten van r2 zijn goed uitgevoerd:
- het achterhoofd buigt nu (x28 → x29 vanaf y14);
- de rechterpoot is donkergrijs zoals links;
- de verre vleugel heeft geen zwarte klont meer;
- de overgang van de bliksem naar het koord is schoon;
- de vleugelpunten rechts hebben inkepingen in de achtergrond tussen de veren;
- de twee kuifslierten lopen apart.

Er blijven twee echte punten over: de kuifbogen missen hun top (eis 1), en de buiksikkel is een band van gelijke breedte (eis 2). Daarnaast zijn er twee kleine technische punten.

## Reparaties (op belang)

1. **Kuifslierten: de top van beide bogen ontbreekt, waardoor ze lezen als twee rechte "rails".** Gemeten in het model (spriterij = vloer van de modelpositie):
   - **Bovenste sliert:** model (21–22,3), (23–26,2), **(27–31,1)**, (32–34,2), (35–36,3), (37,4), (38,5), (39,6). De sprite heeft één platte run (24–33,2) van 10 px. Zet **(27–31,1)** en haal (27–31,2) weg. Verschuif ook (34,3) naar (34,2) en (36,4) naar (36,3). De runs worden dan 3‑4‑5‑3‑2‑1‑1, een boog.
   - **Onderste sliert:** model (21–22,7), (23–24,6), (25–27,5), **(28–33,4)**, (34–37,5). De sprite heeft (24–35,5) plat en (36–37,6). Zet **(28–33,4)**, haal (28–33,5) weg, en zet (36–37,5) in plaats van (36–37,6) zodat hij via (38,7), (39,8) en (40,9) naar het haakje loopt (dat blijft zoals het is).
   - De afstand tussen de slierten blijft 2–3 px, zoals in het model. De krul (43–46,4–7) en het haakje (39–42,8–10) zijn goed.
2. **Buiksikkel = banding.** `c` loopt als een band van constant 3 px breed van (20–22,23) diagonaal tot (25–27,40) en daarna langs de onderkant (21–29,41–42). Daaronder ligt nog een tweede band `b` van 1 px, (21–30,43). Beide liggen parallel aan de rand. In het model is de buik bovenaan bij de schouder licht en wordt hij pas naar rechtsonder tan. Laat de sikkel taps toelopen:
   - rijen 23–27: hooguit 1 px `c` tegen het bruin (x 22–24);
   - rijen 28–34: 2 px;
   - rijen 35–42: 3–4 px, het breedst rechtsonder.
   - `b` alleen rechtsonder als donkerste kern, ±(26–30,42–43), niet als een doorlopende rij onder de hele buik.
3. **Binnenlijnen in de onderste vleugelveren zijn zwart.** Het gaat om (30–31,33), (31–33,34), (32–34,35), (35,33), (36,34), (36–38,35), (39–40,33) en (40–42,34). Ze liggen binnen de bruine vleugel. In het model zijn dit donkerbruine veerscheidingen, en volgens SPRITE_KERN worden binnenlijnen in een donkere tint van het vlak gezet. Maak ze `u` (98,48,26). Pixels die op de buitenrand tegen de achtergrond liggen, blijven zwart.
4. **(klein) Rechte onderrand van de onderste slagpen, (50–55,28):** een lijn van 6 px. In het model loopt die rand licht schuin omhoog naar de punt. Neem de helling over als (50–52,28) en (53–55,27), en zet (55–57,27) als punt aan op (57,26).

Bevroren en goed: het oog, de wang, de snavel, de stippen, het staartkoord, de poten, de bliksem met zijn overgang naar het koord, het achterhoofd, de verre vleugel, de vleugelpunten rechts (y 3–24) en de selout `u` langs de bovenkant.
