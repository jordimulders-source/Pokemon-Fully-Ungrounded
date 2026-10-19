#include "global.h"
#include "test/battle.h"

// Project Grounded: vierde ronde signature moves en abilities
// (Burrow Maze, Pitcher Trap, Praise Helix, Silk Trap, Fake Foliage, Landfill, Hive Queen).

// Burrow Maze: elke uitweg ontwijkt één aanval, max. 3, niet als Furret vastzit.
SINGLE_BATTLE_TEST("Burrow Maze: each tunnel dodges one attack")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_BURROW_MAZE) == EFFECT_BURROW_MAZE);
        PLAYER(SPECIES_FURRET) { Speed(10); }
        OPPONENT(SPECIES_ZIGZAGOON) { Speed(5); }
    } WHEN {
        TURN { MOVE(player, MOVE_BURROW_MAZE); }
        TURN { MOVE(opponent, MOVE_SCRATCH); }
        TURN { MOVE(opponent, MOVE_SCRATCH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BURROW_MAZE, player);
        MESSAGE("Furret dug another way out! (1/3)");
        MESSAGE("The opposing Zigzagoon used Scratch!");
        MESSAGE("Furret slipped into a burrow!");
        NOT HP_BAR(player);
        MESSAGE("The opposing Zigzagoon used Scratch!");
        HP_BAR(player);
    } THEN {
        EXPECT_EQ((u32)player->volatiles.burrowMaze, 0);
    }
}

SINGLE_BATTLE_TEST("Burrow Maze: status moves are dodged too")
{
    GIVEN {
        PLAYER(SPECIES_FURRET) { Speed(10); }
        OPPONENT(SPECIES_ZIGZAGOON) { Speed(5); }
    } WHEN {
        TURN { MOVE(player, MOVE_BURROW_MAZE); MOVE(opponent, MOVE_THUNDER_WAVE); }
    } SCENE {
        MESSAGE("Furret slipped into a burrow!");
        NOT STATUS_ICON(player, paralysis: TRUE);
    } THEN {
        EXPECT_EQ(player->status1, 0);
    }
}

SINGLE_BATTLE_TEST("Burrow Maze: fails after three tunnels")
{
    GIVEN {
        PLAYER(SPECIES_FURRET);
        OPPONENT(SPECIES_ZIGZAGOON);
    } WHEN {
        TURN { MOVE(player, MOVE_BURROW_MAZE); }
        TURN { MOVE(player, MOVE_BURROW_MAZE); }
        TURN { MOVE(player, MOVE_BURROW_MAZE); }
        TURN { MOVE(player, MOVE_BURROW_MAZE); }
    } SCENE {
        MESSAGE("Furret dug another way out! (1/3)");
        MESSAGE("Furret dug another way out! (2/3)");
        MESSAGE("Furret dug another way out! (3/3)");
        MESSAGE("Furret used Burrow Maze!");
        MESSAGE("But it failed!");
    } THEN {
        EXPECT_EQ((u32)player->volatiles.burrowMaze, 3);
    }
}

SINGLE_BATTLE_TEST("Burrow Maze: moves that never miss hit and keep the tunnel")
{
    GIVEN {
        ASSUME(GetMoveAccuracy(MOVE_SWIFT) == 0);
        PLAYER(SPECIES_FURRET) { Speed(10); }
        OPPONENT(SPECIES_ZIGZAGOON) { Speed(5); }
    } WHEN {
        TURN { MOVE(player, MOVE_BURROW_MAZE); MOVE(opponent, MOVE_SWIFT); }
    } SCENE {
        NOT MESSAGE("Furret slipped into a burrow!");
        HP_BAR(player);
    } THEN {
        EXPECT_EQ((u32)player->volatiles.burrowMaze, 1);
    }
}

SINGLE_BATTLE_TEST("Burrow Maze: tunnels don't work while the user is trapped")
{
    GIVEN {
        PLAYER(SPECIES_FURRET) { Speed(10); }
        OPPONENT(SPECIES_ZIGZAGOON) { Speed(5); }
    } WHEN {
        TURN { MOVE(player, MOVE_BURROW_MAZE); MOVE(opponent, MOVE_MEAN_LOOK); }
        TURN { MOVE(opponent, MOVE_SCRATCH); }
    } SCENE {
        NOT MESSAGE("Furret slipped into a burrow!"); // Mean Look mist nooit (accuracy 0)
        MESSAGE("The opposing Zigzagoon used Scratch!");
        HP_BAR(player);
    }
}

SINGLE_BATTLE_TEST("Burrow Maze: trapped Furret keeps its tunnels but can't use them")
{
    GIVEN {
        PLAYER(SPECIES_FURRET) { Speed(5); }
        OPPONENT(SPECIES_ZIGZAGOON) { Speed(10); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_MEAN_LOOK); MOVE(player, MOVE_BURROW_MAZE); }
        TURN { MOVE(opponent, MOVE_SCRATCH); }
    } SCENE {
        MESSAGE("Furret dug another way out! (1/3)");
        MESSAGE("The opposing Zigzagoon used Scratch!");
        NOT MESSAGE("Furret slipped into a burrow!");
        HP_BAR(player);
    } THEN {
        EXPECT_EQ((u32)player->volatiles.burrowMaze, 1);
    }
}

// Pitcher Trap: protect + vangen bij contact, daarna 1/8 per beurt (Bug 1/4) naar Victreebel.
SINGLE_BATTLE_TEST("Pitcher Trap: contact traps the attacker and drains 1/8 each turn")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_PITCHER_TRAP) == EFFECT_PROTECT);
        PLAYER(SPECIES_VICTREEBEL) { HP(100); MaxHP(300); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(400); MaxHP(400); }
        OPPONENT(SPECIES_WYNAUT);
    } WHEN {
        TURN { MOVE(player, MOVE_PITCHER_TRAP); MOVE(opponent, MOVE_SCRATCH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PITCHER_TRAP, player);
        MESSAGE("Victreebel protected itself!");
        MESSAGE("The opposing Wobbuffet slipped into the pitcher!");
        HP_BAR(opponent);
        MESSAGE("The opposing Wobbuffet is being digested!");
        HP_BAR(player);
    } THEN {
        EXPECT_EQ(opponent->hp, 350);
        EXPECT_EQ(player->hp, 150);
        EXPECT(opponent->volatiles.pitcherTrappedBy != 0);
        EXPECT(!CanBattlerEscape(1));
    }
}

SINGLE_BATTLE_TEST("Pitcher Trap: Bug types are digested twice as fast")
{
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_PINSIR, 0) == TYPE_BUG || GetSpeciesType(SPECIES_PINSIR, 1) == TYPE_BUG);
        PLAYER(SPECIES_VICTREEBEL);
        OPPONENT(SPECIES_PINSIR) { HP(400); MaxHP(400); }
    } WHEN {
        TURN { MOVE(player, MOVE_PITCHER_TRAP); MOVE(opponent, MOVE_SCRATCH); }
    } SCENE {
        MESSAGE("The opposing Pinsir slipped into the pitcher!");
        HP_BAR(opponent);
    } THEN {
        EXPECT_EQ(opponent->hp, 300);
    }
}

SINGLE_BATTLE_TEST("Pitcher Trap: non-contact moves don't get trapped")
{
    GIVEN {
        PLAYER(SPECIES_VICTREEBEL);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_PITCHER_TRAP); MOVE(opponent, MOVE_WATER_GUN); }
    } SCENE {
        MESSAGE("Victreebel protected itself!");
        NOT MESSAGE("The opposing Wobbuffet slipped into the pitcher!");
    } THEN {
        EXPECT_EQ((u32)opponent->volatiles.pitcherTrappedBy, 0);
    }
}

SINGLE_BATTLE_TEST("Pitcher Trap: the foe is released when Victreebel leaves the field")
{
    GIVEN {
        PLAYER(SPECIES_VICTREEBEL);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WYNAUT);
    } WHEN {
        TURN { MOVE(player, MOVE_PITCHER_TRAP); MOVE(opponent, MOVE_SCRATCH); }
        TURN { SWITCH(player, 1); }
    } THEN {
        EXPECT_EQ((u32)opponent->volatiles.pitcherTrappedBy, 0);
    }
}

// Silk Trap: -2 Speed en vast, ook nadat de gebruiker wisselt.
SINGLE_BATTLE_TEST("Silk Trap: contact harshly lowers Speed and traps the attacker for good")
{
    GIVEN {
        PLAYER(SPECIES_SPIDOPS);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WYNAUT);
    } WHEN {
        TURN { MOVE(player, MOVE_SILK_TRAP); MOVE(opponent, MOVE_SCRATCH); }
        TURN { SWITCH(player, 1); }
    } SCENE {
        MESSAGE("The opposing Wobbuffet's Speed harshly fell!");
        MESSAGE("The opposing Wobbuffet is stuck in the silk! It can't escape!");
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_SPEED], DEFAULT_STAT_STAGE - 2);
        EXPECT(opponent->volatiles.silkTrapped);
        EXPECT(!CanBattlerEscape(1));
    }
}

// Praise Helix: vier uitkomsten.
SINGLE_BATTLE_TEST("Praise Helix: the HELIX decides")
{
    u32 roll;
    PARAMETRIZE { roll = 0; }
    PARAMETRIZE { roll = 1; }
    PARAMETRIZE { roll = 2; }
    PARAMETRIZE { roll = 3; }
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_PRAISE_HELIX) == EFFECT_PRAISE_HELIX);
        PLAYER(SPECIES_OMASTAR) { HP(50); MaxHP(200); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_PRAISE_HELIX, WITH_RNG(RNG_PRAISE_HELIX, roll)); }
    } SCENE {
        MESSAGE("Omastar consulted the HELIX FOSSIL!");
        if (roll == 0)
            MESSAGE("DEMOCRACY!");
        else if (roll == 1)
            MESSAGE("ANARCHY!");
        else if (roll == 2)
            MESSAGE("BIRD JESUS!");
        else
            MESSAGE("The HELIX is silent.");
    } THEN {
        if (roll == 0) {
            EXPECT_EQ(player->statStages[STAT_SPATK], DEFAULT_STAT_STAGE + 1);
            EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
        } else if (roll == 1) {
            EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 2);
            EXPECT_EQ(player->statStages[STAT_SPATK], DEFAULT_STAT_STAGE + 2);
            EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 2);
            EXPECT_EQ(player->statStages[STAT_DEF], DEFAULT_STAT_STAGE - 1);
            EXPECT_EQ(player->statStages[STAT_SPDEF], DEFAULT_STAT_STAGE - 1);
        } else if (roll == 2) {
            EXPECT_EQ(player->hp, 150);
        } else {
            EXPECT_EQ(player->statStages[STAT_DEF], DEFAULT_STAT_STAGE + 2);
        }
    }
}

// Fake Foliage: STAB op Grass-moves, +1 Speed door Water-moves, heelt in Pollen Haze.
SINGLE_BATTLE_TEST("Fake Foliage gives Grass moves STAB", s16 damage)
{
    enum Ability ability;
    PARAMETRIZE { ability = ABILITY_STURDY; }
    PARAMETRIZE { ability = ABILITY_FAKE_FOLIAGE; }
    GIVEN {
        PLAYER(SPECIES_SUDOWOODO) { Ability(ability); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_VINE_WHIP); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Fake Foliage raises Speed when hit by a Water move")
{
    GIVEN {
        PLAYER(SPECIES_SUDOWOODO) { Ability(ABILITY_FAKE_FOLIAGE); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_WATER_GUN); }
    } SCENE {
        HP_BAR(player);
        ABILITY_POPUP(player, ABILITY_FAKE_FOLIAGE);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
    }
}

SINGLE_BATTLE_TEST("Fake Foliage heals in Pollen Haze like a Grass type")
{
    GIVEN {
        PLAYER(SPECIES_SUDOWOODO) { Ability(ABILITY_FAKE_FOLIAGE); HP(50); MaxHP(160); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_POLLEN_HAZE); }
    } THEN {
        EXPECT_EQ(player->hp, 60);
    }
}

// Landfill: +1 Def en +1 SpDef aan het eind van de beurt in Acid Rain.
SINGLE_BATTLE_TEST("Landfill raises Defense and Sp. Def at the end of each turn in Acid Rain")
{
    GIVEN {
        PLAYER(SPECIES_GARBODOR) { Ability(ABILITY_LANDFILL); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_ACID_RAIN); }
    } SCENE {
        ABILITY_POPUP(player, ABILITY_LANDFILL);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_DEF], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_SPDEF], DEFAULT_STAT_STAGE + 1);
    }
}

// Hive Queen: ruimt hazards op en raakt ze zelf nooit.
SINGLE_BATTLE_TEST("Hive Queen clears hazards on its own side when it enters, without taking damage")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        PLAYER(SPECIES_VESPIQUEN) { Ability(ABILITY_HIVE_QUEEN); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_STEALTH_ROCK); }
        TURN { MOVE(opponent, MOVE_TOXIC_SPIKES); }
        TURN { SWITCH(player, 1); }
    } SCENE {
        ABILITY_POPUP(player, ABILITY_HIVE_QUEEN);
        MESSAGE("Vespiquen's swarm cleared the way!");
        NOT HP_BAR(player);
    } THEN {
        EXPECT(!AreAnyHazardsOnSide(B_SIDE_PLAYER));
        EXPECT_EQ(player->hp, player->maxHP);
    }
}
