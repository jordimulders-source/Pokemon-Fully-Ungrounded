# TM-plaatsing TM60–TM88

Nieuwe TM's (Jordi, 19 okt). Alle TM's zijn herbruikbaar: elke TM ligt precies één keer in de wereld (of is op één plek te koop).
Item balls en verborgen items houden hun oude flag (alleen het item is vervangen); alleen Mustards beloning heeft een nieuwe flag
(`FLAG_RECEIVED_TM_ROLLING_THUNDER` = `FLAG_GROUNDED(1000)`, blok `tm_plaatsing` in `include/constants/flags.h`).

"Fase" = welke badges je ongeveer hebt als je er voor het eerst kunt komen.

| TM | Move | Kaart / plek | Hoe | Fase | Vervangt |
|---|---|---|---|---|---|
| TM60 | Rock Tomb | Granite Cave 1F (17,7) | item ball | na badge 1 (Dewford) | Escape Rope |
| TM61 | Snarl | Route 116 (34,7), noordkant | item ball | na badge 1 (Rustboro) | Potion |
| TM62 | Roost | Route 104 zuid (29,53), oostkant via de zuidoostingang van Petalburg Woods | item ball | vóór badge 1 | Poké Ball |
| TM63 | Bulk Up | Route 115 (31,56), het noordelijke deel (via Meteor Falls 1F, of met Surf) | item ball | badge 3–4 | Great Ball |
| TM64 | Charge Beam | Route 110 (30,69), zuidkant bij Slateport | item ball | badge 2–3 | Dire Hit |
| TM65 | Thunder Wave | Slateport City, markt (TM-kraam) | winkel (3000) | badge 2 | – |
| TM66 | Icy Wind | Slateport City, markt (TM-kraam) | winkel (3000) | badge 2 | – |
| TM67 | Poison Jab | Route 117 (16,18) | item ball | badge 3 | Great Ball |
| TM68 | Will-O-Wisp | Jagged Pass (23,24) | item ball | badge 3–4 | Burn Heal |
| TM69 | Tailwind | Route 113 (79,5), oostkant (asregen) | item ball | badge 3–4 | Super Repel |
| TM70 | X-Scissor | Route 114 (31,19) | item ball | badge 3–4 | Energy Powder |
| TM71 | Heat Wave | Mt. Chimney Summit (4,25) (na badge 5 laat de vulkanoloog je door) | verborgen item | badge 5 | Star Piece |
| TM72 | Wild Charge | New Mauville, binnen (32,25) | item ball | badge 5 (Surf) | Ultra Ball |
| TM73 | Rolling Thunder | Kubfu-dojo (Route 112): Mustard, na het gevecht tegen hem (nadat Kubfu geëvolueerd is; wie hem al versloeg krijgt de TM bij het aanspreken) | NPC-beloning | badge 4–5 (Mustard lv 34) | – |
| TM74 | Heavy Slam | Route 118 (69,7), oostkant | item ball | badge 5 (Surf) | Hyper Potion |
| TM75 | Energy Ball | Route 119 (33,117), zuidkant (jungle) | item ball | badge 5 | Hyper Potion |
| TM76 | Bug Buzz | Route 120 (22,13), noordkant | item ball | badge 6 | Nest Ball |
| TM77 | Hex | Mt. Pyre 2F (0,10) | item ball | badge 6 | Ultra Ball |
| TM78 | Substitute | Lilycove Department Store 4F, rechterverkoper | winkel (3000) | badge 6 | – |
| TM79 | Baton Pass | Lilycove Department Store 4F, rechterverkoper | winkel (3000) | badge 6 | – |
| TM80 | Focus Blast | Route 121 (60,10) | item ball | badge 6 | Revive |
| TM81 | Knock Off | Aqua Hideout B2F (3,13) | item ball | badge 6–7 | Nest Ball |
| TM82 | Earth Power | Magma Hideout 3F-3R (9,19) | item ball | badge 6–7 | Escape Rope |
| TM83 | Dragon Pulse | Meteor Falls, grot achter de waterval (MeteorFalls_HiddenFalls (15,10)) | item ball | badge 8 (Waterfall) | Max Elixir |
| TM84 | Stone Edge | Victory Road B2F (13,8) (Surf) | item ball | badge 8 | Full Heal |
| TM85 | High Horsepower | Victory Road 1F (30,39) | verborgen item | badge 8 | Ultra Ball |
| TM86 | Dragon Dance | Meteor Falls, Draconid-gangen (MeteorFalls_Tunnels (42,35)) | item ball | badge 8 (Waterfall) | Stardust |
| TM87 | Close Combat | Artisan Cave B1F (32,38) (Battle Frontier) | item ball | post-game | HP Up |
| TM88 | Swords Dance | Artisan Cave 1F (14,5) (Battle Frontier) | item ball | post-game | Carbos |

## Generatoren
De vervangen items in kaarten van een bouwscript staan ook in dat script, zodat opnieuw draaien ze niet terugzet:
`meteor_falls_ext.py` (Hidden Falls, Tunnels) en `chimney_ext.py` (Summit, verborgen item). De flagnamen bleven gelijk
(bijv. `FLAG_ITEM_METEOR_FALLS_TUNNELS_STARDUST`), zodat bestaande saves kloppen.

## Tas
De TM/HM-pocket had 64 plekken (te weinig: 88 TM's + 8 HM's). Hij staat nu achteraan SaveBlock1 (`bagTMsHMs`, 100 plekken);
oude saves verhuizen hun TM's bij het laden (`MigrateLegacyBagItems`), net als eerder de Items-pocket.
