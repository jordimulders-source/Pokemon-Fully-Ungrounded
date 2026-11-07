# Studie vóór kleur r4 (kort)

## Uit de Spriting Guide (Dragonfly Cave) en SPRITING.md §0–§8
- **Licht linksboven, grens basis/schaduw op de evenaar**; schaduw na de evenaar is één vlakke tint (geen verloop). Hooglicht klein, alleen waar het licht loodrecht valt. Slagschaduw van een ander lichaamsdeel (vleugel op lijf, kop op schouder) altijd in de schaduwtint.
- **3 tinten per kleur + omlijning**; meer tinten/verlopen = "overshaden" = nep. R/S gebruikt veel van de lichte tint (te weinig licht = te donker).
- **Omlijning per kleurgroep**: zwart alleen aan de schaduwkant, aan de lichtkant de donkere tint van de kleur; 1 px breed, geen klonten; anti-aliasing alleen binnen de lijn.
- **Banding/pillow shading** (staat niet met die woorden in de OCR-tekst, wel de regel erachter): schaduw volgt de 3D-vorm vanaf één lichtbron, niet de omtrek; banden van gelijke breedte langs de rand en licht-in-het-midden/donker-rondom zijn fout.
- **Jaggies/curven**: segmentlengtes lopen geleidelijk op/af, geen spijkertjes. **Dithering**: hooguit spaarzaam bij vacht/veren; hier niet nodig.
- **Ogen**: witte glans + gekleurde reflectie aan de andere kant geven diepte; geen opgeplakte ring.

## Uit de echte sprites (8×, pixel voor pixel)
- **Taillow**: kop rood met één donkerder rood vlak eronder (twee tinten, grote vlakken); buik wit met grijze sikkel onderaan/rechts, 2–3 px dither, geen banden. Vleugel: groot licht vlak, donkere basistint onder/achter, veerpunten als korte donkere inkepingen onderaan; zwarte lijn alleen aan onder-/achterkant. Pootjes: oranje 3 tinten, teentjes als 1 px lichte kolommetjes met zwart ertussen en eronder.
- **Starly**: vleugel = licht vlak linksboven, middentint onder, korte tapse streepjes (2–3 px) in de schaduwtint als veerrijen; pootjes afwisselend oranje/donker per teen met zwarte onderrand.
- **Pidgey/Swablu/Natu/Wingull/Fletchling**: bolle kop/lijf met 3–4 tinten, schaduw als sikkel rechtsonder, hooglicht klein linksboven; Swablu-pootjes 5×3 (licht-zwart-licht).
- **Oog met gekleurde iris** (gezocht in graphics/pokemon/): **Latias** (6×6: rand in donkere gezichtstint, iris goud donker+licht, zwarte pupil, witte glans voor, oogwit achter), **Combusken** (4×5: rand in gezichtsbruin, witte glans, rode iris licht+donker, pupil linksonder), **Skarmory** (4×3: zwart lid, gele iris twee tinten, pupil midden, géén glans). Ook bekeken: Noctowl, Hoothoot, Treecko, Celebi, Murkrow (te groot, te klein of zonder glans).
