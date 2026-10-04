#include "global.h"
#include "test/battle.h"

// Project Grounded: tweede ronde signature moves (Solrock/Lunatone, Spinda, Castform, Dustox, Linoone,
// Chimecho, Relicanth, Swalot, Delcatty). Let op: Wobbuffet is in deze rom Psychic/Normal.

// Eclipse: Rock (fysiek) als Atk hoger is, anders Psychic (speciaal); x1,5 op het eigen moment van de dag.
SINGLE_BATTLE_TEST("Eclipse is Rock-type for a physical user and Psychic-type for a special user")
{
    u32 species;
    PARAMETRIZE { species = SPECIES_SOLROCK; }
    PARAMETRIZE { species = SPECIES_LUNATONE; }
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_ECLIPSE) == EFFECT_ECLIPSE);
        ASSUME(GetSpeciesType(SPECIES_CHARMANDER, 0) == TYPE_FIRE && GetSpeciesType(SPECIES_CHARMANDER, 1) == TYPE_FIRE);
        PLAYER(species);
        OPPONENT(SPECIES_CHARMANDER);
    } WHEN {
        TURN { MOVE(player, MOVE_ECLIPSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ECLIPSE, player);
        HP_BAR(opponent);
        if (species == SPECIES_SOLROCK)
            MESSAGE("It's super effective!");
        else
            NOT MESSAGE("It's super effective!");
    }
}

TEST("Eclipse is boosted by day for physical users and by night for special users")
{
    EXPECT(IsEclipseTimeBoosted(TRUE, TIME_MORNING));
    EXPECT(IsEclipseTimeBoosted(TRUE, TIME_DAY));
    EXPECT(!IsEclipseTimeBoosted(TRUE, TIME_NIGHT));
    EXPECT(IsEclipseTimeBoosted(FALSE, TIME_EVENING));
    EXPECT(IsEclipseTimeBoosted(FALSE, TIME_NIGHT));
    EXPECT(!IsEclipseTimeBoosted(FALSE, TIME_DAY));
}

// Tipsy Waltz: 50% verwarring; dubbele kracht als Spinda zelf verward is, en dan raakt hij zichzelf niet.
SINGLE_BATTLE_TEST("Tipsy Waltz confuses the target 50% of the time")
{
    PASSES_RANDOMLY(50, 100, RNG_SECONDARY_EFFECT);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_TIPSY_WALTZ, MOVE_EFFECT_CONFUSION));
        PLAYER(SPECIES_SPINDA);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_TIPSY_WALTZ); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TIPSY_WALTZ, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
    }
}

SINGLE_BATTLE_TEST("Tipsy Waltz doubles in power when the user is confused and never hurts itself", s16 damage)
{
    bool32 confused;
    PARAMETRIZE { confused = FALSE; }
    PARAMETRIZE { confused = TRUE; }
    GIVEN {
        PLAYER(SPECIES_SPINDA) { Speed(5); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); }
    } WHEN {
        TURN { MOVE(opponent, confused ? MOVE_CONFUSE_RAY : MOVE_CELEBRATE); MOVE(player, MOVE_TIPSY_WALTZ, WITH_RNG(RNG_CONFUSION, TRUE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TIPSY_WALTZ, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
        NOT MESSAGE("It hurt itself in its confusion!");
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[1].damage);
    }
}

// Weather Report: zet het weer waar het doelwit het zwakst tegen is (vuur -> regen) en slaat als Weather Ball toe.
SINGLE_BATTLE_TEST("Weather Report sets the weather the target is weakest to and hits with it")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_WEATHER_REPORT) == EFFECT_WEATHER_REPORT);
        PLAYER(SPECIES_CASTFORM);
        OPPONENT(SPECIES_CHARMANDER);
    } WHEN {
        TURN { MOVE(player, MOVE_WEATHER_REPORT); }
    } SCENE {
        MESSAGE("It started to rain!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WEATHER_REPORT, player);
        HP_BAR(opponent);
        MESSAGE("It's super effective!");
    } THEN {
        EXPECT(gBattleWeather & B_WEATHER_RAIN);
    }
}

// Venom Dust: vergiftigt beide tegenstanders en verlaagt hun Speed.
DOUBLE_BATTLE_TEST("Venom Dust poisons both opponents and lowers their Speed")
{
    GIVEN {
        ASSUME(GetMoveTarget(MOVE_VENOM_DUST) == MOVE_TARGET_BOTH);
        PLAYER(SPECIES_DUSTOX);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_VENOM_DUST); }
    } THEN {
        EXPECT(opponentLeft->status1 & STATUS1_POISON);
        EXPECT(opponentRight->status1 & STATUS1_POISON);
        EXPECT_EQ(opponentLeft->statStages[STAT_SPEED], DEFAULT_STAT_STAGE - 1);
        EXPECT_EQ(opponentRight->statStages[STAT_SPEED], DEFAULT_STAT_STAGE - 1);
    }
}

// Straight Line: +1 prioriteit, dubbele kracht als hij de beurt ervoor ook Straight Line gebruikte.
SINGLE_BATTLE_TEST("Straight Line has +1 priority")
{
    GIVEN {
        ASSUME(GetMovePriority(MOVE_STRAIGHT_LINE) == 1);
        PLAYER(SPECIES_LINOONE) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(player, MOVE_STRAIGHT_LINE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STRAIGHT_LINE, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
    }
}

SINGLE_BATTLE_TEST("Straight Line doubles in power when used twice in a row", s16 damage1, s16 damage2)
{
    PARAMETRIZE {}
    GIVEN {
        PLAYER(SPECIES_LINOONE);
        OPPONENT(SPECIES_WOBBUFFET) { MaxHP(999); HP(999); }
    } WHEN {
        TURN { MOVE(player, MOVE_STRAIGHT_LINE); }
        TURN { MOVE(player, MOVE_STRAIGHT_LINE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STRAIGHT_LINE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage1);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STRAIGHT_LINE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage2);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage1, Q_4_12(2.0), results[0].damage2);
    }
}

// Wind Chime: healt het eigen team 1/8 (1/4 met Tailwind); dubbele kracht met Tailwind, x1,5 tegen een doelwit met status.
SINGLE_BATTLE_TEST("Wind Chime heals the user by 1/8 of its max HP")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_WIND_CHIME) == EFFECT_WIND_CHIME);
        PLAYER(SPECIES_CHIMECHO) { MaxHP(160); HP(80); }
        OPPONENT(SPECIES_CHARMANDER);
    } WHEN {
        TURN { MOVE(player, MOVE_WIND_CHIME); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WIND_CHIME, player);
        HP_BAR(opponent);
        HP_BAR(player, damage: -20);
        MESSAGE("Chimecho was soothed by the wind chime!");
    }
}

SINGLE_BATTLE_TEST("Wind Chime doubles in power under Tailwind", s16 damage)
{
    bool32 tailwind;
    PARAMETRIZE { tailwind = FALSE; }
    PARAMETRIZE { tailwind = TRUE; }
    GIVEN {
        PLAYER(SPECIES_CHIMECHO);
        OPPONENT(SPECIES_CHARMANDER) { MaxHP(999); HP(999); }
    } WHEN {
        TURN { MOVE(player, tailwind ? MOVE_TAILWIND : MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_WIND_CHIME); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WIND_CHIME, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Wind Chime is 1.5x stronger against a target with a status condition", s16 damage)
{
    u32 status;
    PARAMETRIZE { status = STATUS1_NONE; }
    PARAMETRIZE { status = STATUS1_PARALYSIS; }
    GIVEN {
        PLAYER(SPECIES_CHIMECHO);
        OPPONENT(SPECIES_CHARMANDER) { MaxHP(999); HP(999); Status1(status); }
    } WHEN {
        TURN { MOVE(player, MOVE_WIND_CHIME); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WIND_CHIME, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[1].damage);
    }
}

DOUBLE_BATTLE_TEST("Wind Chime hits both opponents and heals the user and its partner once")
{
    GIVEN {
        PLAYER(SPECIES_CHIMECHO) { MaxHP(160); HP(80); }
        PLAYER(SPECIES_WOBBUFFET) { MaxHP(160); HP(80); }
        OPPONENT(SPECIES_CHARMANDER);
        OPPONENT(SPECIES_CHARMANDER);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_WIND_CHIME); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WIND_CHIME, playerLeft);
        HP_BAR(opponentLeft);
        HP_BAR(opponentRight);
        HP_BAR(playerLeft, damage: -20);
        HP_BAR(playerRight, damage: -20);
        NOT HP_BAR(playerLeft);
    }
}

// Primeval Ward: +1 Def en +1 Sp. Def, en tegenstanders kunnen zijn stats niet meer verlagen.
SINGLE_BATTLE_TEST("Primeval Ward raises Defense and Sp. Def and blocks stat drops from foes")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_PRIMEVAL_WARD) == EFFECT_PRIMEVAL_WARD);
        PLAYER(SPECIES_RELICANTH) { Speed(10); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(5); }
    } WHEN {
        TURN { MOVE(player, MOVE_PRIMEVAL_WARD); MOVE(opponent, MOVE_GROWL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PRIMEVAL_WARD, player);
        MESSAGE("Relicanth refuses to change!");
    } THEN {
        EXPECT_EQ(player->statStages[STAT_DEF], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_SPDEF], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE);
    }
}

// Gulp Down: slikt het item van het doelwit in en healt 25%; Leftovers werkt daarna vanuit Swalot's maag.
SINGLE_BATTLE_TEST("Gulp Down swallows the target's Leftovers, heals, and the Leftovers then work for Swalot")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_GULP_DOWN) == EFFECT_GULP_DOWN);
        PLAYER(SPECIES_SWALOT) { MaxHP(160); HP(40); }
        OPPONENT(SPECIES_WOBBUFFET) { Item(ITEM_LEFTOVERS); }
    } WHEN {
        TURN { MOVE(player, MOVE_GULP_DOWN); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_GULP_DOWN, player);
        HP_BAR(opponent);
        MESSAGE("Swalot gulped down the opposing Wobbuffet's Leftovers!");
        HP_BAR(player, damage: -40);
        MESSAGE("The Leftovers now works from inside its stomach!");
        HP_BAR(player, damage: -10); // Leftovers aan het eind van de beurt
    } THEN {
        EXPECT_EQ(opponent->item, ITEM_NONE);
        EXPECT_EQ(player->item, ITEM_NONE);
    }
}

SINGLE_BATTLE_TEST("Gulp Down eats a Berry right away")
{
    GIVEN {
        PLAYER(SPECIES_SWALOT) { MaxHP(160); HP(40); }
        OPPONENT(SPECIES_WOBBUFFET) { Item(ITEM_SITRUS_BERRY); }
    } WHEN {
        TURN { MOVE(player, MOVE_GULP_DOWN); }
    } SCENE {
        MESSAGE("Swalot gulped down the opposing Wobbuffet's Sitrus Berry!");
        HP_BAR(player, damage: -40);
        HP_BAR(player, damage: -40); // Sitrus Berry
    } THEN {
        EXPECT_EQ(opponent->item, ITEM_NONE);
    }
}

// Nine Lives: één keer per gevecht een KO overleven met 1 HP; de tweede keer faalt hij.
SINGLE_BATTLE_TEST("Nine Lives lets the user survive the next KO once per battle")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_NINE_LIVES) == EFFECT_NINE_LIVES);
        PLAYER(SPECIES_DELCATTY) { HP(1); Speed(10); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(5); }
    } WHEN {
        TURN { MOVE(player, MOVE_NINE_LIVES); MOVE(opponent, MOVE_SCRATCH); }
        TURN { MOVE(player, MOVE_NINE_LIVES); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_NINE_LIVES, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
        MESSAGE("Delcatty landed on its feet! Eight lives to go.");
        MESSAGE("Delcatty used Nine Lives!");
        MESSAGE("But it failed!");
    } THEN {
        EXPECT_EQ(player->hp, 1);
    }
}
