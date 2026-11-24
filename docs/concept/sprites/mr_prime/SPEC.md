# Mr. Prime (eindvorm Mime-lijn: Mime Jr. → bokser-Mr. Mime → Mr. Prime)

Middenfase en alle rondes daarvan: `docs/concept/sprites/mrmime_regional/SPEC.md` (branch `claude/funny-ptolemy-meuol6`), frontsprite `mrmime_regional/bokser/sprite_r23/`, model `bokser/r12.png` (prompt `bokser/PROMPT_r11.md`).

## Jordi, letterlijk
- 9 nov: "en daarna een oude gentleman wordt met een wandelstok" (bartitsu); naam Mr. Prime "hilarisch en perfect".
- 22 nov: "mr rime is een jolly danser en mr prime wordt een volledige gentleman qua pose, dat en qua kleur is echt genoeg verschil".
- 23 nov (wat blijft): "de kuiven, het feit dat het een gentleman is, dat zwart wit kleurgebruik, de mr mime vormen, beetje zoals mr rime dadt ook redelijk behoudt, alleen wordt mr prime net wat anders."
- 23 nov: "Fighting/Psychic nog steeds idd. Snor wordt wat groter. Hij krijgt een hoed (net als mr rime)"
- 23 nov: "Monocle en beetje pak ook, maar het pak moet geen kleding zijn, maar gewoon de lichaamsvorm. Kaarsrecht met de stok klaar om te vechten, maar niet te breed, anders gaat het ten koste van de sprite"

## Besloten
- Type **Fighting/Psychic**.
- Zwart-witpalet; Mr. Mime-vormen (zoals Mr. Rime ze ook redelijk houdt); de kuiven van de bokser.
- Snor wat groter dan bij de bokser; hoed (net als Mr. Rime); monocle; pak = lichaamsvorm, geen kleding.
- Pose: kaarsrecht, stok klaar om te vechten, niet te breed.
- Formaat: mag groter/zwaarder dan de bokser (±53×59).

## Open
- Vorm van de hoed (alleen "net als mr rime" gezegd), evolutiemethode, wat er van de bokser (schouderballen, getapete vingers, V) overblijft.

## Rondes
- Prompt r1: `gemini/PROMPT_r1.md` (nieuw gesprek, geen bijlage; opbouw van bokser-prompt r11, die het gekozen model gaf).
- r1 (`gemini/r1.png`; hoge hoed, Mr. Mime-pieken opzij, ronde Mr. Mime-vorm, leunt op de stok, korte gebogen benen), Jordi: "dit is niet voldoende een evolutie, kijk meer naar mr rime, ook voor de hoed, de oren zijn weer zoals mr mime, de vorm ook, de stok is niet in een gevechtshouding, hij staat niet kaarsrecht, echt heel slecht".
- Prompt r2: `gemini/PROMPT_r2.md` (nieuw gesprek, geen bijlage): Mr. Rime als leidraad voor vorm, verhoudingen en hoed; pieken plat achterover; stok als wapen opgeheven (niet op de grond); benen recht tegen elkaar (posezinnen van bokser-r11, die werkten).
- r2 (`gemini/r2.png`; kaarsrecht, stok schuin voor het lijf, maar mens in een rokkostuum met broek, losse hoge hoed, witte pieken weer opzij), Jordi: "nog niet heel veel beter". Claude vraagt wat het zwaarst weegt.
- Jordi bij r2: "zelfde feedback als eerder" (= r1: niet genoeg evolutie, meer Mr. Rime ook de hoed, oren/vorm Mr. Mime, stok niet in gevechtshouding, niet kaarsrecht). Claude: alleen de naam "Mr. Rime" werkt niet (Gemini gaf een mens in rokkostuum); r3 beschrijft de Mr. Rime-bouw in woorden en noemt Mr. Mime niet meer (les Emolga-evo).
- Prompt r3: `gemini/PROMPT_r3.md` (nieuw gesprek, geen bijlage).
- r3 (`gemini/r3.png`; bollijf met vest/strik, stok naar voren, losse hoge hoed met één piek erachter, heel lange zwarte benen), Jordi: "iets beter, maar nog steeds veel dezelfde issues, de houding met de stok is wel naar voren, maar geen vechterstand, het lichaam klopt nog niet helemaal goed, de benen zijn komisch lang, hoed en oren moeten 1 zijn zoals bij mr rime, kleding is teveel kleding en niet lichaamsvorm".
- Prompt r4: `gemini/PROMPT_r4.md` (nieuw gesprek, basis r3): hoed + pieken één vorm, benen korter, geen kraag/strik/knopen/vest, vechterstand (rug recht, korte schermstand).
- Jordi bij r3 (erna): "ogen te klein"; "het is geen pokemon". In prompt r4 erbij: grote ogen zoals Mr. Rime, blok Pokémon-verhoudingen (kop ±1/3, ronde vormen; zoals bij bokser/Hitmongroove).
- r4 (`gemini/r4.png`; schermstand met stok naar voren, wit eivormig lijf, losse bolhoed met pieken opzij), Jordi: "pose is goed, maar het lichaam is nu een kaal ei geworden".
- Jordi (erna): "vertaalt nog niet voldoende naar een sprite ook".
- Jordi (erna): "en het is ook nog net niet genoeg de mr mime lijn". Drie punten = te veel voor bijsturen (`PROMPT_r5_bijsturen.md` vervalt): startprompt r5 (`gemini/PROMPT_r5.md`, nieuw gesprek) = r4 + pak als lijfvorm, Mr. Mime-gezicht met wangcirkels en ronde schouders (bokser had ze ook), spritemaat.
- r5 (`gemini/r5.png`; pose als r4, donkere rokpanden, ronde schouderbal, grijze wang, pieken opzij, losse hoed), Jordi: "pak wat beter, maar hij is teveel mr mime nog, het moet een counterpart van mr rime zijn".
- Prompt r6: `gemini/PROMPT_r6.md` (nieuw gesprek): "counterpart/broer van Mr. Rime" als kader; Claude's eigen Mr. Mime-toevoegingen van r5 (schouders, wangcirkels) eruit; pieken naar achteren.
- r6 (`gemini/r6.png`), Jordi: "deze is echt waardeloos, ik heb het gevoel dat je prompts ook gewoon niet goed zijn".
- **Fout Claude (r2–r6):** Mr. Rime uit het geheugen beschreven als lang en slank met lange dunne benen en een hoge hoed; dat klopt niet. Nagekeken in de repo (`graphics/pokemon/mr_rime/front.png`, vel `gemini/ref_mr_rime_mr_mime.png`): Mr. Rime is gedrongen, groot rond donker lijf dat als jas leest, korte benen, grote ronde schoenen, grote witte handen, ronde hoed met rand waaruit twee platte gekartelde haarvleugels opzij komen (hoed + haar één vorm), grote ronde ogen, snor. Daarnaast noemde de prompt Mr. Rime 8× terwijl Gemini hem niet kent (gaf telkens een losse hoge hoed), en groeide elke ronde met losse reparaties.
- Jordi (24 nov): "gemini snapt niet like mr rime, je moet de vormen duidelijker beschrijven, alle details". Prompt r7 (`gemini/PROMPT_r7.md`, nieuw gesprek): geen namen meer; Mr. Rime's bouw vorm voor vorm met maten (hoed met rand + 2 platte gekartelde haarvleugels naar achteren als één vorm, grote ogen, dikke snor, tonlijf als rokkostuum met witte V, korte benen, balschoenen, grote witte handen); pose r4.
- r7 (`gemini/r7.png`; tonlijf met rokpanden en witte V, balschoenen, losse grijze hoed, vleermuisvleugels opzij), Jordi: "kijk lichaam prima, pose niet, nog niet gentlemanly genoeg en ik wil de stok meer diagonaal hebben, ogen nog niet tevreden, maar dat kunnen we in de sprite doen, beetje een pose van de man links, maar niet volledig want dat vertaalt niet naar de sprite. Je mag me wel uitleggen waarom die vleermuisvleugeloren heeft en de hoed weer los zit". Foto: `gemini/pose_bartitsu_foto.png` (niet als bijlage naar Gemini).
- Uitleg Claude: "like a bat wing" stond letterlijk in prompt r7 (eigen vergelijking voor de gekartelde vorm); "hat crown with a wide brim" beschrijft een hoed, dus tekent Gemini een hoed, en "grow out of the brim" zegt niet dat er geen naad/kleurverschil mag zijn.
- r8 bijsturen (zelfde gesprek als r7): `gemini/PROMPT_r8_bijsturen.md`; lijf blijft; (1) pose naar de man links, ingekort; (2) haar + hoed één vorm, geen vleugels. Ogen later in de sprite.
- Jordi (erna): "en de snor mag iets groter, iets meer cartoony" → punt 3 in de r8-bijsturing.
- r8 (`gemini/r8.png`; krulsnor, stok schuin omhoog, bolhoed met grijze golvende lokken erachter, benen onveranderd), Jordi: "haren en hoed niet goed, snor en arm pose wel, lichaamspose niet, stok te klein".
- r9 bijsturen (zelfde gesprek): `gemini/PROMPT_r9_bijsturen.md`, alleen lichaamspose (benen) + stok groter. Hoed/haar: voorstel Claude in de sprite (zie chat).
- r9 (`gemini/r9.png`; uitval: voorbeen gebogen, achterbeen gestrekt ver naar rechts; stok dikker en iets langer; kop/snor/armen gelijk aan r8). Wacht op Jordi.
- Jordi bij r9: "denk je dat je hier iets van kan maken?"; "en de ogen dan minder geschokt maar iets meer serieus dan mr rime".
- Kale reductie r9 (`gemini/r9_kale_reductie_64_8x.png`): 64×55, breedte is de grens (uitval + stok); kop ±20 px breed (Mr. Mime-maat). Open: hoed/haar (A sprite uit Mr. Rime-pixels / B Gemini), formaat (achterbeen inkorten?), monocle (r9 heeft ringen om beide ogen).
- Jordi: "de stok is ook nog te dun eigenlijk" (voorstel Claude: in de sprite dikker, met omlijning en hooglicht).
- Jordi: "2, het lijkt geen echte wandelstok, en als je nog 1 keer wil prompten moet je het zeggen". r10 bijsturen (zelfde gesprek): `gemini/PROMPT_r10_bijsturen.md`, alleen de stok (dik, echte wandelstok met crookhandvat en metalen punt).
