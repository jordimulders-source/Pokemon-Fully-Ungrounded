#include "global.h"
#include "test/battle.h"
#include "text.h"

// Project Grounded: achtste ronde signature moves (Accelgor, Pyukumuku, Hitmonchan, Beheeyem/Orbeetle).
// Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Project Grounded signature moves round 8 have the agreed data")
{
    EXPECT_EQ(GetMoveEffect(MOVE_KUSARIGAMA), EFFECT_KUSARIGAMA);
    EXPECT_EQ(GetMoveType(MOVE_KUSARIGAMA), TYPE_BUG);
    EXPECT_EQ(GetMoveCategory(MOVE_KUSARIGAMA), DAMAGE_CATEGORY_PHYSICAL);
    EXPECT_EQ(GetMovePower(MOVE_KUSARIGAMA), 80);
    EXPECT(!MoveMakesContact(MOVE_KUSARIGAMA));

    EXPECT_EQ(GetMoveType(MOVE_INNARD_PUNCH), TYPE_FIGHTING);
    EXPECT_EQ(GetMovePriority(MOVE_INNARD_PUNCH), -4);
    EXPECT(MoveMakesContact(MOVE_INNARD_PUNCH));
    EXPECT(IsPunchingMove(MOVE_INNARD_PUNCH));

    EXPECT_EQ(GetMoveStrikeCount(MOVE_COMBINATION), 3);
    EXPECT_EQ(GetMovePower(MOVE_COMBINATION), 20);
    EXPECT(IsPunchingMove(MOVE_COMBINATION));

    EXPECT_EQ(GetMovePower(MOVE_SPINNING_BACKFIST), 90);
    EXPECT(IsPunchingMove(MOVE_SPINNING_BACKFIST));
    EXPECT(MoveIgnoresDefenseEvasionStages(MOVE_SPINNING_BACKFIST));
    EXPECT(MoveIgnoresSubstitute(MOVE_SPINNING_BACKFIST));

    EXPECT_EQ(GetMoveEffect(MOVE_ABDUCTION), EFFECT_HIT_SWITCH_TARGET);
    EXPECT_EQ(GetMoveType(MOVE_ABDUCTION), TYPE_PSYCHIC);
    EXPECT_EQ(GetMoveCategory(MOVE_ABDUCTION), DAMAGE_CATEGORY_SPECIAL);
    EXPECT_EQ(GetMovePriority(MOVE_ABDUCTION), -6);
}

// Kusarigama: dubbele kracht als het doelwit wisselt (niet bij een statusmove).
SINGLE_BATTLE_TEST("Kusarigama doubles in power against a switch, not against a status move", s16 damage)
{
    u32 type;
    PARAMETRIZE { type = 0; }
    PARAMETRIZE { type = 1; }
    PARAMETRIZE { type = 2; }
    GIVEN {
        PLAYER(SPECIES_ACCELGOR) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
    } WHEN {
        if (type == 0)
            TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_KUSARIGAMA, criticalHit: FALSE); }
        else if (type == 1)
            TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_KUSARIGAMA, criticalHit: FALSE); }
        else
            TURN { SWITCH(opponent, 1); MOVE(player, MOVE_KUSARIGAMA, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_KUSARIGAMA, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[2].damage);
    }
}

// Innard Punch: geraakt deze beurt = 2x de schade terug (fysiek en speciaal).
SINGLE_BATTLE_TEST("Innard Punch deals twice the damage the user took this turn")
{
    u32 move;
    s16 taken, dealt;
    PARAMETRIZE { move = MOVE_SCRATCH; }
    PARAMETRIZE { move = MOVE_WATER_GUN; }
    GIVEN {
        PLAYER(SPECIES_PYUKUMUKU) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); HP(400); MaxHP(400); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_INNARD_PUNCH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, opponent);
        HP_BAR(player, captureDamage: &taken);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_INNARD_PUNCH, player);
        HP_BAR(opponent, captureDamage: &dealt);
    } THEN {
        EXPECT_EQ(dealt, taken * 2);
    }
}

SINGLE_BATTLE_TEST("Innard Punch adds up multiple hits taken this turn")
{
    s16 hit1, hit2, dealt;
    GIVEN {
        ASSUME(GetMoveStrikeCount(MOVE_DOUBLE_KICK) == 2);
        PLAYER(SPECIES_PYUKUMUKU) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); HP(400); MaxHP(400); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_DOUBLE_KICK); MOVE(player, MOVE_INNARD_PUNCH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DOUBLE_KICK, opponent);
        HP_BAR(player, captureDamage: &hit1);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DOUBLE_KICK, opponent);
        HP_BAR(player, captureDamage: &hit2);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_INNARD_PUNCH, player);
        HP_BAR(opponent, captureDamage: &dealt);
    } THEN {
        EXPECT_EQ(dealt, (hit1 + hit2) * 2);
    }
}

SINGLE_BATTLE_TEST("Innard Punch is a normal 50 power hit when the user was not hit", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_INNARD_PUNCH; }
    PARAMETRIZE { move = MOVE_MACH_PUNCH; }
    GIVEN {
        ASSUME(GetMovePower(MOVE_MACH_PUNCH) == 40);
        PLAYER(SPECIES_PYUKUMUKU);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, move, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[1].damage, Q_4_12(1.25), results[0].damage);
    }
}

// Combination: 20, 20, 60 en de derde klap is altijd een crit.
SINGLE_BATTLE_TEST("Combination hits 20, 20 and a critical 60")
{
    s16 firstHit, secondHit, thirdHit;
    GIVEN {
        PLAYER(SPECIES_HITMONCHAN);
        OPPONENT(SPECIES_WOBBUFFET) { HP(500); MaxHP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_COMBINATION); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COMBINATION, player);
        HP_BAR(opponent, captureDamage: &firstHit);
        NOT MESSAGE("A critical hit!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COMBINATION, player);
        HP_BAR(opponent, captureDamage: &secondHit);
        NOT MESSAGE("A critical hit!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COMBINATION, player);
        HP_BAR(opponent, captureDamage: &thirdHit);
        MESSAGE("A critical hit!");
    } THEN {
        EXPECT_EQ(firstHit, secondHit);
        EXPECT_MUL_EQ(firstHit, Q_4_12(4.5), thirdHit);
    }
}

// Spinning Backfist: negeert Defense-boosts en raakt door Substitute heen.
SINGLE_BATTLE_TEST("Spinning Backfist ignores the target's Defense boosts", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_IRON_DEFENSE; }
    GIVEN {
        PLAYER(SPECIES_HITMONCHAN) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_SPINNING_BACKFIST, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SPINNING_BACKFIST, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Spinning Backfist hits through a Substitute")
{
    GIVEN {
        PLAYER(SPECIES_HITMONCHAN) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SUBSTITUTE); MOVE(player, MOVE_SPINNING_BACKFIST); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUBSTITUTE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SPINNING_BACKFIST, player);
        NOT MESSAGE("The substitute took damage for the opposing Wobbuffet!");
        HP_BAR(opponent);
    }
}

// Abduction: prioriteit -6, in Trick Room 0; dwingt het doelwit te wisselen.
SINGLE_BATTLE_TEST("Abduction moves last normally and drags out a replacement")
{
    GIVEN {
        PLAYER(SPECIES_BEHEEYEM) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_BULBASAUR) { Speed(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_ABDUCTION); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ABDUCTION, player);
        MESSAGE("The opposing Bulbasaur was dragged out!");
    }
}

SINGLE_BATTLE_TEST("Abduction has priority 0 in Trick Room, so a slow user moves first")
{
    GIVEN {
        PLAYER(SPECIES_BEHEEYEM) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_BULBASAUR) { Speed(100); }
    } WHEN {
        TURN { MOVE(player, MOVE_TRICK_ROOM); MOVE(opponent, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_ABDUCTION); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TRICK_ROOM, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ABDUCTION, player);
        MESSAGE("The opposing Bulbasaur was dragged out!");
    }
}

// Namen en beschrijvingen passen op de schermen (de algemene text.c-test stopt bij de lege nummers 902-914).
TEST("Project Grounded signature moves round 8 names and descriptions fit")
{
    static const u16 moves[] = {MOVE_KUSARIGAMA, MOVE_INNARD_PUNCH, MOVE_COMBINATION, MOVE_SPINNING_BACKFIST, MOVE_ABDUCTION};
    u32 i, move = MOVE_NONE;
    for (i = 0; i < ARRAY_COUNT(moves); i++)
    {
        PARAMETRIZE_LABEL("%S", GetMoveName(moves[i])) { move = moves[i]; }
    }
    EXPECT_LE(GetStringWidth(FONT_NARROWER, GetMoveName(move), 0), 64);
    if (move != MOVE_SPINNING_BACKFIST) // staat in de uitzonderingslijst van text.c (contestscherm)
        EXPECT_LE(GetStringWidth(FONT_NARROWER, GetMoveName(move), 0), 59);
    EXPECT_LE(GetStringWidth(FONT_NARROWER, GetMoveName(move), 0), 72);
    EXPECT_LE(GetStringWidth(FONT_NORMAL, GetMoveDescription(move), 0), 152);
}
