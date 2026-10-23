#include "global.h"
#include "test/battle.h"

// Project Grounded: signature moves 902-909 (Xatu, Donphan, Bouffalant, Araquanid, Drampa, Bewear,
// Eiscue, Arboliva). Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Project Grounded signature moves 902-909 have the agreed data")
{
    EXPECT_EQ(GetMovePower(MOVE_TOTEM_GAZE), 80);
    EXPECT_EQ(GetMoveType(MOVE_TOTEM_GAZE), TYPE_PSYCHIC);
    EXPECT_EQ(GetMoveCategory(MOVE_TOTEM_GAZE), DAMAGE_CATEGORY_SPECIAL);
    EXPECT_EQ(GetMoveEffect(MOVE_TUSK_TUMBLE), EFFECT_ROLLOUT);
    EXPECT_EQ(GetMoveType(MOVE_TUSK_TUMBLE), TYPE_GROUND);
    EXPECT_EQ(GetMoveAccuracy(MOVE_TUSK_TUMBLE), 90);
    EXPECT_EQ(GetMovePower(MOVE_AFRO_CHARGE), 120);
    EXPECT_EQ(GetMoveEffect(MOVE_AFRO_CHARGE), EFFECT_RECOIL);
    EXPECT_EQ(GetMoveRecoil(MOVE_AFRO_CHARGE), 25);
    EXPECT(MoveIgnoresProtect(MOVE_AFRO_CHARGE));
    EXPECT_EQ(GetMoveType(MOVE_BUBBLE_DOME), TYPE_WATER);
    EXPECT_EQ(GetMoveEffect(MOVE_THE_OLD_DAYS), EFFECT_THE_OLD_DAYS);
    EXPECT_EQ(GetMovePower(MOVE_BEAR_HUG), 80);
    EXPECT_EQ(GetMoveType(MOVE_BEAR_HUG), TYPE_FIGHTING);
    EXPECT(MoveHasAdditionalEffect(MOVE_BEAR_HUG, MOVE_EFFECT_WRAP));
    EXPECT_EQ(GetMovePower(MOVE_FACE_OFF), 85);
    EXPECT_EQ(GetMoveType(MOVE_FACE_OFF), TYPE_ICE);
    EXPECT(IsHealingMove(MOVE_OLIVE_OIL));
    EXPECT_EQ(GetMoveType(MOVE_OLIVE_OIL), TYPE_GRASS);
}

// Totem Gaze: de volgende schadelijke move tegen Xatu mist, één keer.
SINGLE_BATTLE_TEST("Totem Gaze makes the next damaging move against the user miss once")
{
    GIVEN {
        PLAYER(SPECIES_XATU) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_TOTEM_GAZE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TOTEM_GAZE, player);
        HP_BAR(opponent);
        MESSAGE("Xatu stared into\nthe future. It didn't blink.");
        MESSAGE("The opposing Wobbuffet used Tackle!");
        MESSAGE("Xatu saw it coming!");
        NOT HP_BAR(player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        HP_BAR(player);
    }
}

SINGLE_BATTLE_TEST("Totem Gaze is not used up by status moves")
{
    GIVEN {
        PLAYER(SPECIES_XATU) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_TOTEM_GAZE); MOVE(opponent, MOVE_GROWL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TOTEM_GAZE, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_GROWL, opponent);
    } THEN {
        EXPECT(player->volatiles.totemGaze);
    }
}

SINGLE_BATTLE_TEST("Totem Gaze wears off when the user switches out")
{
    GIVEN {
        PLAYER(SPECIES_XATU);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_TOTEM_GAZE); }
        TURN { SWITCH(player, 1); }
        TURN { SWITCH(player, 0); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        HP_BAR(player);
    }
}

// Tusk Tumble: ruimt hazards aan de eigen kant op, de eerste klap legt 1 laag Spikes.
SINGLE_BATTLE_TEST("Tusk Tumble clears the user's hazards and lays one layer of Spikes")
{
    GIVEN {
        PLAYER(SPECIES_DONPHAN) { Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_STEALTH_ROCK); MOVE(player, MOVE_TUSK_TUMBLE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); SKIP_TURN(player); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STEALTH_ROCK, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TUSK_TUMBLE, player);
        MESSAGE("Donphan blew away Stealth Rock!");
        MESSAGE("Spikes were scattered on the ground all around the opposing team!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TUSK_TUMBLE, player);
    } THEN {
        EXPECT(gSideTimers[B_SIDE_OPPONENT].spikesAmount == 1);
        EXPECT(!IsHazardOnSide(B_SIDE_PLAYER, HAZARDS_STEALTH_ROCK));
    }
}

// Afro Charge: door Protect heen, en het type van het terrein.
SINGLE_BATTLE_TEST("Afro Charge goes through Protect")
{
    GIVEN {
        PLAYER(SPECIES_BOUFFALANT) { Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_PROTECT); MOVE(player, MOVE_AFRO_CHARGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PROTECT, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_AFRO_CHARGE, player);
        HP_BAR(opponent);
        HP_BAR(player);
    }
}

SINGLE_BATTLE_TEST("Afro Charge becomes Electric-type on Electric Terrain")
{
    GIVEN {
        PLAYER(SPECIES_BOUFFALANT) { Speed(50); }
        OPPONENT(SPECIES_DIGLETT) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_ELECTRIC_TERRAIN); MOVE(player, MOVE_AFRO_CHARGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ELECTRIC_TERRAIN, opponent);
        NOT HP_BAR(opponent);
    }
}

// Bubble Dome: Reflect + Light Screen, alleen Araquanid; snijdende moves prikken hem door.
SINGLE_BATTLE_TEST("Bubble Dome sets Reflect and Light Screen for Araquanid")
{
    GIVEN {
        PLAYER(SPECIES_ARAQUANID);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_BUBBLE_DOME); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BUBBLE_DOME, player);
    } THEN {
        EXPECT(gSideStatuses[B_SIDE_PLAYER] & SIDE_STATUS_REFLECT);
        EXPECT(gSideStatuses[B_SIDE_PLAYER] & SIDE_STATUS_LIGHTSCREEN);
    }
}

SINGLE_BATTLE_TEST("Bubble Dome fails for anyone but Araquanid")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_BUBBLE_DOME); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_BUBBLE_DOME, player);
        MESSAGE("But it failed!");
    } THEN {
        EXPECT(!(gSideStatuses[B_SIDE_PLAYER] & SIDE_STATUS_REFLECT));
    }
}

SINGLE_BATTLE_TEST("Bubble Dome pops when a slicing move hits")
{
    GIVEN {
        ASSUME(IsSlicingMove(MOVE_SLASH));
        PLAYER(SPECIES_ARAQUANID) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_BUBBLE_DOME); MOVE(opponent, MOVE_SLASH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BUBBLE_DOME, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SLASH, opponent);
        HP_BAR(player);
        MESSAGE("The Bubble Dome was sliced\nopen! Pop.");
    } THEN {
        EXPECT(!(gSideStatuses[B_SIDE_PLAYER] & (SIDE_STATUS_REFLECT | SIDE_STATUS_LIGHTSCREEN)));
    }
}

// Zoals Brick Break: de koepel knapt vóór de schadeberekening, dus de snijdende treffer zelf is niet afgezwakt.
SINGLE_BATTLE_TEST("Bubble Dome does not weaken the slicing move that pops it", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_BUBBLE_DOME; }
    GIVEN {
        ASSUME(IsSlicingMove(MOVE_SLASH));
        ASSUME(GetMoveCategory(MOVE_SLASH) == DAMAGE_CATEGORY_PHYSICAL);
        PLAYER(SPECIES_ARAQUANID) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, move); MOVE(opponent, MOVE_SLASH, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SLASH, opponent);
        HP_BAR(player, captureDamage: &results[i].damage);
        if (move == MOVE_BUBBLE_DOME)
            MESSAGE("The Bubble Dome was sliced\nopen! Pop.");
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Bubble Dome still weakens a non-slicing move", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_BUBBLE_DOME; }
    GIVEN {
        ASSUME(!IsSlicingMove(MOVE_SCRATCH));
        PLAYER(SPECIES_ARAQUANID) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, move); MOVE(opponent, MOVE_SCRATCH, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
        HP_BAR(player, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_LT(results[1].damage, results[0].damage);
    }
}

// The Old Days: Yawn op het doelwit en +1 Sp. Atk.
SINGLE_BATTLE_TEST("The Old Days makes the target drowsy and raises Sp. Atk")
{
    GIVEN {
        PLAYER(SPECIES_DRAMPA);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_THE_OLD_DAYS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_THE_OLD_DAYS, player);
        MESSAGE("The opposing Wobbuffet grew drowsy!");
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, player);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_SPATK], DEFAULT_STAT_STAGE + 1);
        EXPECT(opponent->volatiles.yawn);
    }
}

SINGLE_BATTLE_TEST("The Old Days still raises Sp. Atk if the target can't get drowsy")
{
    GIVEN {
        PLAYER(SPECIES_DRAMPA);
        OPPONENT(SPECIES_WOBBUFFET) { Status1(STATUS1_PARALYSIS); }
    } WHEN {
        TURN { MOVE(player, MOVE_THE_OLD_DAYS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_THE_OLD_DAYS, player);
        NOT MESSAGE("The opposing Wobbuffet grew drowsy!");
    } THEN {
        EXPECT_EQ(player->statStages[STAT_SPATK], DEFAULT_STAT_STAGE + 1);
    }
}

// Bear Hug: bindt het doelwit.
SINGLE_BATTLE_TEST("Bear Hug traps the target")
{
    GIVEN {
        PLAYER(SPECIES_BEWEAR);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_BEAR_HUG); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BEAR_HUG, player);
        MESSAGE("The opposing Wobbuffet is being hugged\ntightly! There is no escape.");
    } THEN {
        EXPECT(opponent->volatiles.wrapped);
    }
}

// Face Off: dubbele kracht met een heel ijsblok.
SINGLE_BATTLE_TEST("Face Off doubles in power while Eiscue has its Ice Face", s16 damage)
{
    u32 species;
    PARAMETRIZE { species = SPECIES_EISCUE_NOICE; }
    PARAMETRIZE { species = SPECIES_EISCUE_ICE; }
    GIVEN {
        PLAYER(species);
        // Grote schade voor een nauwkeurige verhouding
        OPPONENT(SPECIES_WOBBUFFET) { Defense(10); MaxHP(9999); HP(9999); }
    } WHEN {
        TURN { MOVE(player, MOVE_FACE_OFF); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        // Relatieve marge (1%): EXPECT_MUL_EQ heeft een vaste marge van ±2, maar de vaste +2 in de
        // schadeformule wordt niet mee vermenigvuldigd, waardoor x2 op de schade een paar punten afwijkt.
        EXPECT_GE(results[1].damage * 100, results[0].damage * 198);
        EXPECT_LE(results[1].damage * 100, results[0].damage * 202);
    }
}

// Olive Oil: heelt de helft en zet Grassy Terrain.
SINGLE_BATTLE_TEST("Olive Oil heals half and sets Grassy Terrain")
{
    GIVEN {
        PLAYER(SPECIES_ARBOLIVA) { HP(1); MaxHP(200); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_OLIVE_OIL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OLIVE_OIL, player);
        HP_BAR(player, damage: -100);
        MESSAGE("Grass grew to cover the battlefield!");
    } THEN {
        EXPECT(gFieldTimers.terrain == B_TERRAIN_GRASSY);
    }
}

SINGLE_BATTLE_TEST("Olive Oil heals two thirds in Pollen Haze")
{
    GIVEN {
        PLAYER(SPECIES_ARBOLIVA) { HP(1); MaxHP(300); Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_POLLEN_HAZE); MOVE(player, MOVE_OLIVE_OIL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OLIVE_OIL, player);
        HP_BAR(player, damage: -200);
    }
}

SINGLE_BATTLE_TEST("Olive Oil fails at full HP on Grassy Terrain")
{
    GIVEN {
        PLAYER(SPECIES_ARBOLIVA) { Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_GRASSY_TERRAIN); MOVE(player, MOVE_OLIVE_OIL); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_OLIVE_OIL, player);
        MESSAGE("But it failed!");
    }
}
