#include "global.h"
#include "test/battle.h"

// Project Grounded: vierde ronde signature moves (Masquerain, Absol, Kecleon, Lopunny, Skuntank,
// Vanilluxe, Escavalier, Stonjourner, Revavroom).
// Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Project Grounded signature moves round 4 have the agreed data")
{
    EXPECT_EQ(GetMoveEffect(MOVE_EYE_SPOTS), EFFECT_EYE_SPOTS);
    EXPECT_EQ(GetMoveType(MOVE_EYE_SPOTS), TYPE_BUG);
    EXPECT_EQ(GetMoveCategory(MOVE_EYE_SPOTS), DAMAGE_CATEGORY_STATUS);
    EXPECT_EQ(GetMovePower(MOVE_OMEN_STRIKE), 75);
    EXPECT_EQ(GetMoveCriticalHitStage(MOVE_OMEN_STRIKE), 1);
    EXPECT(MoveMakesContact(MOVE_OMEN_STRIKE));
    EXPECT_EQ(GetMoveType(MOVE_MIMIC_SHADE), TYPE_NORMAL);
    EXPECT_EQ(GetMovePower(MOVE_MIMIC_SHADE), 70);
    EXPECT_EQ(GetMoveEffect(MOVE_BUNNY_HOP), EFFECT_DRAGON_DANCE);
    EXPECT(IsDanceMove(MOVE_BUNNY_HOP));
    EXPECT_EQ(GetMovePP(MOVE_BUNNY_HOP), 20);
    EXPECT(!MoveMakesContact(MOVE_SKUNK_SPRAY));
    EXPECT_EQ(GetMovePower(MOVE_SKUNK_SPRAY), 70);
    EXPECT_EQ(GetMoveCategory(MOVE_BRAIN_FREEZE), DAMAGE_CATEGORY_SPECIAL);
    EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_BRAIN_FREEZE, 0)->chance, 20);
    EXPECT_EQ(GetMovePower(MOVE_JOUST), 60);
    EXPECT_EQ(GetMovePriority(MOVE_JOUST), 0);
    EXPECT_EQ(GetMoveTarget(MOVE_SOLSTICE_GATE), MOVE_TARGET_BOTH);
    EXPECT_EQ(GetMoveAccuracy(MOVE_SOLSTICE_GATE), 90);
    EXPECT_EQ(GetMovePriority(MOVE_REV_UP), 1);
    EXPECT_EQ(GetMovePower(MOVE_REV_UP), 40);
}

// Eye Spots: -2 Attack en -1 Speed; in Pollen Haze ook verward.
SINGLE_BATTLE_TEST("Eye Spots lowers Attack by 2 and Speed by 1")
{
    GIVEN {
        PLAYER(SPECIES_MASQUERAIN);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_EYE_SPOTS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_EYE_SPOTS, player);
        NOT MESSAGE("The opposing Wobbuffet became confused!");
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ATK], DEFAULT_STAT_STAGE - 2);
        EXPECT_EQ(opponent->statStages[STAT_SPEED], DEFAULT_STAT_STAGE - 1);
    }
}

SINGLE_BATTLE_TEST("Eye Spots also confuses in Pollen Haze")
{
    GIVEN {
        PLAYER(SPECIES_MASQUERAIN) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_POLLEN_HAZE); MOVE(player, MOVE_EYE_SPOTS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_POLLEN_HAZE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_EYE_SPOTS, player);
        MESSAGE("The opposing Wobbuffet became confused!");
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ATK], DEFAULT_STAT_STAGE - 2);
    }
}

// Omen Strike: dubbele kracht als het doelwit een statusmove koos of wisselt.
SINGLE_BATTLE_TEST("Omen Strike doubles in power against a status move or a switch", s16 damage)
{
    u32 type;
    PARAMETRIZE { type = 0; }
    PARAMETRIZE { type = 1; }
    PARAMETRIZE { type = 2; }
    GIVEN {
        PLAYER(SPECIES_ABSOL) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
    } WHEN {
        if (type == 0)
            TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_OMEN_STRIKE, criticalHit: FALSE); }
        else if (type == 1)
            TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_OMEN_STRIKE, criticalHit: FALSE); }
        else
            TURN { SWITCH(opponent, 1); MOVE(player, MOVE_OMEN_STRIKE, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OMEN_STRIKE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[1].damage);
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[2].damage);
    }
}

// Mimic Shade: type van de laatste move die de gebruiker raakte, anders Normal.
SINGLE_BATTLE_TEST("Mimic Shade takes the type of the last move that hit the user")
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_WATER_GUN; }
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_CHARMANDER, 0) == TYPE_FIRE);
        ASSUME(GetSpeciesType(SPECIES_CHARMANDER, 1) == TYPE_FIRE);
        PLAYER(SPECIES_KECLEON) { Speed(1); Ability(ABILITY_COLOR_CHANGE); }
        OPPONENT(SPECIES_CHARMANDER) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_MIMIC_SHADE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MIMIC_SHADE, player);
        HP_BAR(opponent);
        if (move == MOVE_WATER_GUN)
            MESSAGE("It's super effective!");
        else
            NOT MESSAGE("It's super effective!");
    }
}

// Bunny Hop: +1 Attack en +1 Speed.
SINGLE_BATTLE_TEST("Bunny Hop raises Attack and Speed")
{
    GIVEN {
        PLAYER(SPECIES_LOPUNNY);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_BUNNY_HOP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BUNNY_HOP, player);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
    }
}

// Skunk Spray: wist alle stat-veranderingen van het doelwit.
SINGLE_BATTLE_TEST("Skunk Spray resets the target's stat changes")
{
    GIVEN {
        PLAYER(SPECIES_SKUNTANK) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SWORDS_DANCE); MOVE(player, MOVE_SKUNK_SPRAY); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SWORDS_DANCE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SKUNK_SPRAY, player);
        HP_BAR(opponent);
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ATK], DEFAULT_STAT_STAGE);
    }
}

// Brain Freeze: in Snow altijd een crit.
SINGLE_BATTLE_TEST("Brain Freeze always crits in Snow")
{
    GIVEN {
        PLAYER(SPECIES_VANILLUXE) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SNOWSCAPE); MOVE(player, MOVE_BRAIN_FREEZE, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SNOWSCAPE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BRAIN_FREEZE, player);
        HP_BAR(opponent);
        MESSAGE("A critical hit!");
    }
}

// Joust: tegen een sneller doelwit +1 prioriteit en 100 BP.
SINGLE_BATTLE_TEST("Joust strikes first against a faster target")
{
    GIVEN {
        PLAYER(SPECIES_ESCAVALIER) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_JOUST); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_JOUST, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
    }
}

SINGLE_BATTLE_TEST("Joust hits harder against a faster target", s16 damage)
{
    u32 speed;
    PARAMETRIZE { speed = 1; }
    PARAMETRIZE { speed = 200; }
    GIVEN {
        PLAYER(SPECIES_ESCAVALIER) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(speed); }
    } WHEN {
        TURN { MOVE(player, MOVE_JOUST, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_JOUST, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_GT(results[1].damage, results[0].damage);
    }
}

// Solstice Gate: x1,5 in zon en in Snow.
SINGLE_BATTLE_TEST("Solstice Gate is boosted in sun and snow", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_SUNNY_DAY; }
    PARAMETRIZE { move = MOVE_SNOWSCAPE; }
    GIVEN {
        PLAYER(SPECIES_STONJOURNER) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_SOLSTICE_GATE, hit: TRUE, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SOLSTICE_GATE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[1].damage);
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[2].damage);
    }
}

DOUBLE_BATTLE_TEST("Solstice Gate hits both foes")
{
    GIVEN {
        PLAYER(SPECIES_STONJOURNER);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_SOLSTICE_GATE, hit: TRUE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SOLSTICE_GATE, playerLeft);
        HP_BAR(opponentLeft);
        HP_BAR(opponentRight);
    }
}

// Rev Up: prioriteit +1, daarna +1 Speed en +1 Attack.
SINGLE_BATTLE_TEST("Rev Up moves first and raises Attack and Speed")
{
    GIVEN {
        PLAYER(SPECIES_REVAVROOM) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_REV_UP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_REV_UP, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
    }
}
