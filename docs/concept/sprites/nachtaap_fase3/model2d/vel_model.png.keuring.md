# Keuring vel_model.png (nachtaap fase 3, 2D-model kop + achtervoeten, 5 nov)

Bron: Blender-render `../blender/render_snel.png` (pose/massa bevroren); foto 4 en 5 (gezicht), foto 2 en 3 (voeten); SPEC "Overdracht (5 nov)"; SPRITE_NORM; les lama fase 3 (model moet op 64 px leesbaar zijn).
Bekeken: model groot (2×), close-ups, en verkleind naar spritemaat 64 px op 8× en 1×/2× (`model_64.png`).

Onafhankelijke keurder (ronde 1): FAIL op kop-vorm (wangbult), schild 49 % en spits, ogen 1,3 px, neusgaten/sproeten/mond/sikkel < 1 px, bovenste voet als bokshandschoen, teenlijnen, knieschaduw zwart. Alles verwerkt:
- Kop-vorm: lijkt op een ronde vachtbol rond het gezicht (foto 4) / wijkt af in: kop 1,3× (bewuste Pokémon-overdrijving voor de sprite); wangbult weg.
- Gezichtsschild: lijkt op foto 4/5 (donker, kaal, rechte wenkbrauwlijn, breed op ooghoogte, ronde kaak, donkere kin) / wijkt af in: strakke rand (grafisch).
- Ogen: lijkt op klein, dicht bij elkaar, lichtblauw, geen bovenlid; rechte wenkbrauw snijdt de bovenkant iets af (streng) / wijkt af in: niets; op 64 ±2 px elk.
- Snuit/neus/mond: lijkt op foto 4 (lichte neusrug → brede snuit met lippen, mond erin, donkere kin) / wijkt af in: geen sproeten (ruis op 64), lila i.p.v. roze (lijnkleuren).
- Maansikkel: lijkt op de lijn (fase 2), kort, ±2 px dik / wijkt af in: niets.
- Bovenste voet: lijkt op een grijpende muriqui-voet (lange zool, tenen als want over de tak, grote teen tegenover) / wijkt af in: kleurstap bij de enkel (oude render), wordt in de kleurronde gladgezet.
- Onderste voet: lijkt op foto 2/3 (slap, lange zool, tenen licht gekruld, grote teen los) / wijkt af in: niets.
- Vertaalbaarheid 64 px: schild, ogen, snuit, sikkel, haakvoet en spiraal lezen op 1×.
- Naden: lichte restnaad tussen kop en schouder uit de render; het silhouet gebruikt alleen de alpha, dus geen invloed.

Oordeel: PASS (als model/bron voor het silhouet). Smaakvragen voor Jordi: kop recht naar de kijker (norm zegt 3/4), lila of roze snuit.
