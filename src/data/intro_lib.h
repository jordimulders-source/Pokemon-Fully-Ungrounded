// Project Grounded: gedeelde hulpjes voor de klasse-intro's (src/data/class_intros*.h): kleurmenging en de tijd sinds
// de start van de transitie. Wordt onderaan src/battle_transition.c ingevoegd. Al het andere (GI_/LI_/LI2_-hulpjes van de
// gymleider- en legendary-intro's) is in Fully Ungrounded met die intro's verdwenen.

#include "graphics.h"
#include "trainer_pokemon_sprites.h"

// ---------------- tijd en kleurmenging (namen uit de vroegere Tapu-intro's)
static u16 Tapu_Blend(u16 a, u16 b, s32 k)
{
    s32 ar = a & 31, ag = (a >> 5) & 31, ab = (a >> 10) & 31;
    s32 br = b & 31, bg = (b >> 5) & 31, bb = (b >> 10) & 31;
    if (k <= 0)
        return a;
    if (k >= 16)
        return b;
    ar += ((br - ar) * k) >> 4;
    ag += ((bg - ag) * k) >> 4;
    ab += ((bb - ab) * k) >> 4;
    return RGB(ar, ag, ab);
}

// frames sinds de start van de transitie (VBlanks), zie LaunchBattleTransitionTask
static s32 Tapu_Elapsed(void)
{
    u8 id = FindTaskIdByFunc(Task_BattleTransition);
    u32 start;
    if (id == TASK_NONE)
        return 0;
    start = (u16)gTasks[id].data[13] | ((u32)(u16)gTasks[id].data[14] << 16);
    return gMain.vblankCounter1 - start;
}
