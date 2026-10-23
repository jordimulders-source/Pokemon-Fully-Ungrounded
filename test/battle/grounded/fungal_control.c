#include "global.h"
#include "test/battle.h"

// Project Grounded: Fungal Control (Parasect) - de gebruiker kiest 3 beurten lang de move van het doelwit.
// In tests (en voor de AI) kiest de game automatisch de move die het doelwit het meest schaadt.
ASSUMPTIONS
{
    ASSUME(GetMoveEffect(MOVE_FUNGAL_CONTROL) == EFFECT_FUNGAL_CONTROL);
    ASSUME(GetMoveAccuracy(MOVE_FUNGAL_CONTROL) == 60);
}

SINGLE_BATTLE_TEST("Fungal Control forces the target's chosen move for 3 turns")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_FUNGAL_CONTROL, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_TACKLE, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_FUNGAL_CONTROL); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); }
        TURN { MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FUNGAL_CONTROL, player);
        MESSAGE("The opposing Wobbuffet is now\na fungus puppet!\pIt can only use Celebrate!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
    }
}

SINGLE_BATTLE_TEST("Fungal Control prefers a self-destructive move")
{
    GIVEN {
        ASSUME(IsExplosionMove(MOVE_EXPLOSION));
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_FUNGAL_CONTROL, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_TACKLE, MOVE_CELEBRATE, MOVE_EXPLOSION); }
    } WHEN {
        TURN { MOVE(player, MOVE_FUNGAL_CONTROL); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FUNGAL_CONTROL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_EXPLOSION, opponent);
    }
}

SINGLE_BATTLE_TEST("Fungal Control fails on a target that is already controlled")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_FUNGAL_CONTROL, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_TACKLE, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_FUNGAL_CONTROL); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_FUNGAL_CONTROL); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FUNGAL_CONTROL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        MESSAGE("But it failed!");
    }
}

SINGLE_BATTLE_TEST("Fungal Control overrides an ongoing Uproar")
{
    GIVEN {
        ASSUME(MoveHasAdditionalEffectSelf(MOVE_UPROAR, MOVE_EFFECT_UPROAR));
        PLAYER(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_FUNGAL_CONTROL, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_UPROAR, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_UPROAR); MOVE(player, MOVE_FUNGAL_CONTROL); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_UPROAR, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FUNGAL_CONTROL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_UPROAR, opponent);
    }
}

SINGLE_BATTLE_TEST("Fungal Control ends with its own message")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_FUNGAL_CONTROL, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_TACKLE, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_FUNGAL_CONTROL); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        MESSAGE("The opposing Wobbuffet\nshook off the fungus!\pIt's back in control!");
    }
}
