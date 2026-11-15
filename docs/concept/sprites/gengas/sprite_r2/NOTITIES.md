# Gengas frontsprite – ronde 2 (maker)

Start: `../sprite_r1/raster.txt`. Opgeleverd: `gengas_r2.png`, `raster.txt`, `vel.png` (8× naast kleurgids, 1×/2× licht/donker, close-ups 12× gezicht + vier manen naast het model, onderaan r2 | r1), `maak.py`, `ronde2.py` (eenmalig: oude manen wissen en de met de hand getekende maangrids + wervelrijen plaatsen), `diff_r1.py` (bewijs diff 0), `controle.py`, `meet.py`, `pal.py`, `gezicht_px.py`, `closeup.py`, `vel.py`.

## Reparaties (volgorde van de opdracht)
1. **Manen als handen en voeten.** Handen opnieuw getekend naar Gengars rechterhand (`gengar/anim_front.png`, x 45–57, y 19–31): palm met drie stompe, gespreide vingers, inkepingen als zwarte lijnen die taps in de palm uitlopen. Boven: vingers naar links (zoals het model), 12×12. Rechtsonder: vingers omlaag (zoals het model), 12×12. Voeten in Gengars voetvorm (ovaal) met drie zichtbare teentjes gescheiden door zwarte inkepingen en een hobbelige onderrand; rechtsboven tenen omlaag (10×8), linksonder tenen naar links (8×10). Kraters ondergeschikt: 1 per maan (palm/voet), 3 px.
2. **Diepte.** Voor: 12×12, licht (170) met midden-sikkel rechtsonder, selout donkergrijs linksboven, zwart rechtsonder, zwart waar ze over de bol vallen. Achter: kleiner (10×8 en 8×10), alleen midden/donker grijs, zwart omlijnd. Rechtsboven ligt half achter de donkere gaslob van het verre oor en de bolrand (zichtbaar ±6–8 px breed); linksonder ligt met de rechterkant achter de bolrand.
3. **Grijs** dichter bij het neutrale modelgrijs (model 183/132/100): nu (170,167,162) / (127,124,119) / (88,85,81): iets donkerder dan het model, een tikje warm (R−B 7–8 i.p.v. 16 in r1). Tanden blijven het lichtst (250/217/179).
4. **Stormwervel rond**: een cirkel van 9×8 (x 38–46, y 32–39, de gemeten modelplek) met schuine hoeken (3-2-·-2-3), één doorlopende spiraallijn met opening linksonder en binnenhaak; lichte rand (idx 5) eromheen zoals in het model.
5. Lichtvlek-kern: niet terug. Het grijs heeft nog steeds 3 tinten nodig (licht/midden/donker); er is geen paletplek vrij.

## Controles
- `diff_r1.py`: **0 pixels anders dan r1 buiten de zones** (hand boven, voet rechtsboven, voet linksonder, hand rechtsonder, wervel). Binnen de zones zijn alleen 3 lijfpixels nieuw: (42,53), (43,52), (44,51), bolpixels die in r1 onder de oude hand lagen, met de kleuren uit de r1-lijfrijen hersteld.
- Gezicht: 98 px rood/wit/grijs, afwijkend 0. Kleuren: 16 incl. transparant. Bol: cirkelfit max 0,39 px.
- Vlakjes < 3 px: alleen taps lopende vingerlijnen/teenlijnen ((29,6), (5,44), (5,47), (53,58)–(52,59)), kraterbodem (48,55), krater A (32–33,5) en de halve krater van de achterste voet (53,26). Omlijning "in vlak": vingerlijn (29,3) en de bolrand vóór de gaslob, beide bedoeld.

## Zwakke punten die ik nog zie
- De hand boven heeft vingers naar links met horizontale inkepingen: leest als hand, maar het blijft vooral een vuist. Het model heeft wat meer gespreide knokkels.
- De voet linksonder (tenen naar links) kan op 1× ook als kleine hand gelezen worden. Tenen omlaag zou meer voet zijn, maar wijkt dan af van de modelhouding.
- De achterste voet rechtsboven is voor een groot deel verstopt: op 1× zie je vooral de tenen.
- De vóór-handen zijn iets kleiner dan de modelmanen (model ±13–15 px); ze zijn wel duidelijk groter dan de achterste.
