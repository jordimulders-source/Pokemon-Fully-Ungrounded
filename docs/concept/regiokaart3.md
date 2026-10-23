# Regiokaart variant 3 (voorstel)

`regiokaart3.png` (kaal) en `regiokaart3_namen.png` (met namen en legenda), gemaakt met `tools/concept/regiokaart3.py`. Basis is variant 2 (door Jordi gekozen); de vorm van het continent, de binnenzee en de landmarks zijn gelijk gebleven. **Variant 2 blijft de basis tot Jordi kiest.**

## Nieuw ten opzichte van variant 2
- **Gyms op de kaart** (geel vakje met nummer bij de naam): 1 Uyuni, 2 Cordillera Real, 3 San Pedro, 4 Cuzco, 5 Buenos Aires, 6 Rio, 7 Paramaribo, 8 diepe jungle; **L** = Machu Picchu (League).
- **Hoofdpad volgens ROUTEPLAN.md** getekend: La Paz → over de altiplano (langs de zoutvlakte) → Uyuni → **trein** via Oruro terug → La Paz → Cordillera Real → Lípez → San Pedro → kustwoestijn → Arequipa → Nazca → Cuzco → terug door Atacama (Valle de la Luna) → Humahuaca → Salta → Cafayate → Mendoza → Patagonië (Bariloche, Perito Moreno) → Valdés → Buenos Aires → Iguazú → Florianópolis → Rio → (Fly) Andes-noord: Chavín → Quito → Galápagos → Salento → Medellín → Cartagena → Paramaribo → door het oerwoud de Amazone in, de rivier af tot het einde (gym 8). Cuzco → **Inca Trail** → Machu Picchu.
- **Spoorlijn** Uyuni – Oruro – La Paz als rails over de route (nieuw symbool; Hoenn kent geen spoor).
- **Zuid-Bolivia groter:** Uyuni, Lípez en de zoutvlakte schuiven naar het zuiden (links), Licancabur en Laguna Colorada liggen nu tussen Lípez en San Pedro, de puna-woestijn loopt verder door.
- **Lussen:** Uyuni – Lípez – San Pedro – Humahuaca – Uyuni (de Quebrada terug naar Bolivia), heen over de altiplano / terug met de trein, Cuzco – Inca Trail, de Amazone (Paramaribo → monding → binnenzee) tegenover de post-game-boot Rio → Belém.
- **Nieuwe plekken:** Oruro, Potosí (mijn), Titicaca (één icoon voor Isla del Sol, Uros, Wanaku en Tiwanaku), Valle de la Luna, Chavín, Humahuaca, Cafayate, Chiloé (nu een echt eiland met zeestraat), Perito Moreno, Florianópolis (Zuid-Brazilië), tepui (Mew), verdronken woud, diepe jungle (gym 8).
- **Weg (ruimte en leesbaarheid):** Lima, Huacachina, Torres del Paine, Vuurland-, Paaseiland- en Noronha-icoon (de eilanden staan er nog), Amazone-stad, de routes Salta → Buenos Aires, Potosí → Pantanal, Medellín → tepui en Salvador → binnenzee (die zouden het hoofdpad afsnijden).
- **Legenda onder de kaart:** hoofdpad in volgorde, gyms, en een lijst van wat níet als icoon op de kaart staat (zoals op een Town Map: treinkerkhof en Isla Incahuasi, de mijn van de Cerro Rico, Moray, Intipunku, de Patagonische grotten, Catatumbo, Kaieteur, rest houses, Zarude, Paititi, El Dorado, Caleuche).
- Het script controleert zelf: landroutes niet op open zee, zeeroutes (BFS uit variant 2) niet dwars over land, en labels die elkaar overlappen.

## Twijfels (Claude)
- **"De Amazone af tot het einde":** ik heb gym 8 aan het einde van de rivier gezet, aan de Andes-kant (westkant van de binnenzee), en je komt er vanaf Paramaribo via de monding stroomopwaarts. Op de kaart ligt dat dicht bij Bolivia/Cuzco (zoals het echte Madre de Dios), maar er loopt bewust geen landroute heen. Als Jordi "af" als stroomafwaarts bedoelt, moet gym 8 bij de monding liggen (minder afgelegen).
- **Atacama ↔ Peru** is één corridor die je twee keer loopt (heen naar Cuzco, terug in segment 5). Dat is volgens Jordi bewust (nieuwe dungeons bij terugkeer), maar een tweede weg (bijv. via de westoever van de Titicaca) paste niet zonder parallelle routes vlak naast elkaar.
- **Rio → Andes-noord** heeft geen getekende route: ik ga uit van Fly (na gym 4 beschikbaar). Een landverbinding over het binnenland zou de post-game-boot ondergraven.
- **Galápagos vóór of na Colombia** blijft open; de kaart werkt voor beide.
- **Chavín** staat bij de noordroute (segment 7); het kan ook bij Cuzco (segment 4).
- Pantanal, Salvador, Lençóis en Belém staan er nog als optionele plekken uit variant 2; Jordi heeft er niets over besloten.
- De rails zijn een eigen toevoeging aan de Hoenn-stijl; kan ook gewoon een route zijn.
