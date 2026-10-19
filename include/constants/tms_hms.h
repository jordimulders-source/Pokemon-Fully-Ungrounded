#ifndef GUARD_CONSTANTS_TMS_HMS_H
#define GUARD_CONSTANTS_TMS_HMS_H

#define FOREACH_TM(F) \
    F(FOCUS_PUNCH) \
    F(DRAGON_CLAW) \
    F(SCALD) \
    F(CALM_MIND) \
    F(STORED_POWER) \
    F(TOXIC) \
    F(HAIL) \
    F(DRAIN_PUNCH) \
    F(BULLET_SEED) \
    F(HIDDEN_POWER) \
    F(SUNNY_DAY) \
    F(TAUNT) \
    F(ICE_BEAM) \
    F(BLIZZARD) \
    F(HYPER_BEAM) \
    F(LIGHT_SCREEN) \
    F(PROTECT) \
    F(RAIN_DANCE) \
    F(GIGA_DRAIN) \
    F(U_TURN) \
    F(DAZZLING_GLEAM) \
    F(SOLAR_BEAM) \
    F(IRON_HEAD) \
    F(THUNDERBOLT) \
    F(THUNDER) \
    F(EARTHQUAKE) \
    F(RETURN) \
    F(DIG) \
    F(PSYCHIC) \
    F(SHADOW_BALL) \
    F(BRICK_BREAK) \
    F(DOUBLE_TEAM) \
    F(REFLECT) \
    F(VOLT_SWITCH) \
    F(FLAMETHROWER) \
    F(SLUDGE_BOMB) \
    F(SANDSTORM) \
    F(FIRE_BLAST) \
    F(STEALTH_ROCK) \
    F(BRAVE_BIRD) \
    F(NASTY_PLOT) \
    F(FACADE) \
    F(SECRET_POWER) \
    F(REST) \
    F(OVERKILL) /* Project Grounded: TM45, was Attract */ \
    F(TRICK_ROOM) \
    F(FLASH_CANNON) \
    F(DARK_PULSE) \
    F(PLAY_ROUGH) \
    F(FLARE_BLITZ) /* Project Grounded: TM50, was Overheat (Flannery) */ \
    F(SELTZER_SURGE) /* Project Grounded: TM51, Team Aqua's bruiswater */ \
    F(LAGER_LAGOON) /* Project Grounded: TM52, bier-Surf */ \
    F(VINTAGE_SPILL) /* Project Grounded: TM53, wijn; beloning van de laatste gym */ \
    F(MACHINE_LEARNING) /* Project Grounded: TM54, beloning van Wattson */ \
    F(LASER_BEAM) /* Project Grounded: TM55, beloning van Tate & Liza */ \
    F(SHADOW_SIPHON) /* Project Grounded: TM56, Mt. Pyre 3F */ \
    F(ACID_RAIN) /* Project Grounded: TM57, van een Aqua-grunt in de Aqua Hideout */ \
    F(POLLEN_HAZE) /* Project Grounded: TM58, van een Bug Maniac boven de Mimic Circle (Route 119) */ \
    F(WEATHER_BALL) /* Project Grounded: TM59, Scorched Slab (zonnesanctum) */ \
    F(ROCK_TOMB) /* Project Grounded: TM60, Granite Cave 1F */ \
    F(SNARL) /* Project Grounded: TM61, Route 116 */ \
    F(ROOST) /* Project Grounded: TM62, Route 104 */ \
    F(BULK_UP) /* Project Grounded: TM63, Route 115 */ \
    F(CHARGE_BEAM) /* Project Grounded: TM64, Route 110 */ \
    F(THUNDER_WAVE) /* Project Grounded: TM65, winkel Slateport */ \
    F(ICY_WIND) /* Project Grounded: TM66, winkel Slateport */ \
    F(POISON_JAB) /* Project Grounded: TM67, Route 117 */ \
    F(WILL_O_WISP) /* Project Grounded: TM68, Jagged Pass */ \
    F(TAILWIND) /* Project Grounded: TM69, Route 113 */ \
    F(X_SCISSOR) /* Project Grounded: TM70, Route 114 */ \
    F(HEAT_WAVE) /* Project Grounded: TM71, Mt. Chimney Summit (verborgen) */ \
    F(WILD_CHARGE) /* Project Grounded: TM72, New Mauville */ \
    F(ROLLING_THUNDER) /* Project Grounded: TM73, Mustard (Kubfu-dojo) */ \
    F(HEAVY_SLAM) /* Project Grounded: TM74, Route 118 */ \
    F(ENERGY_BALL) /* Project Grounded: TM75, Route 119 */ \
    F(BUG_BUZZ) /* Project Grounded: TM76, Route 120 */ \
    F(HEX) /* Project Grounded: TM77, Mt. Pyre 2F */ \
    F(SUBSTITUTE) /* Project Grounded: TM78, Lilycove Dept. Store 4F */ \
    F(BATON_PASS) /* Project Grounded: TM79, Lilycove Dept. Store 4F */ \
    F(FOCUS_BLAST) /* Project Grounded: TM80, Route 121 */ \
    F(KNOCK_OFF) /* Project Grounded: TM81, Aqua Hideout B2F */ \
    F(EARTH_POWER) /* Project Grounded: TM82, Magma Hideout 3F */ \
    F(DRAGON_PULSE) /* Project Grounded: TM83, Meteor Falls (grot achter de waterval) */ \
    F(STONE_EDGE) /* Project Grounded: TM84, Victory Road B2F */ \
    F(HIGH_HORSEPOWER) /* Project Grounded: TM85, Victory Road 1F (verborgen) */ \
    F(DRAGON_DANCE) /* Project Grounded: TM86, Meteor Falls (Draconid-gangen) */ \
    F(CLOSE_COMBAT) /* Project Grounded: TM87, Artisan Cave B1F (post-game) */ \
    F(SWORDS_DANCE) /* Project Grounded: TM88, Artisan Cave 1F (post-game) */ \
    F(COLD_SHOULDER) /* Project Grounded: TM89 */ \
    F(JUMP_SCARE) /* Project Grounded: TM90 */ \
    F(DIM_MAK) /* Project Grounded: TM91 */ \
    F(UPDRAFT) /* Project Grounded: TM92 */ \
    F(POWER_GEM) /* Project Grounded: TM93 */ \
    F(WOOD_HAMMER) /* Project Grounded: TM94 */ \
    F(DRAGON_RUSH) /* Project Grounded: TM95 */ \
    F(COUNTERFEIT_BALL) /* Project Grounded: TM96 */ \
    F(SHELL_SMASH) /* Project Grounded: TM97 */ \
    F(FAKE_OUT) /* Project Grounded: TM98 */ \
    F(DISCO_INFERNO) /* Project Grounded: TM99 */ \
    F(SUPER_SPLASH) /* Project Grounded: TM100 */

#define FOREACH_HM(F) \
    F(CUT) \
    F(FLY) \
    F(SURF) \
    F(STRENGTH) \
    F(FLASH) \
    F(ROCK_SMASH) \
    F(WATERFALL) \
    F(DIVE)

#define FOREACH_TMHM(F) \
    FOREACH_TM(F) \
    FOREACH_HM(F)

#endif
