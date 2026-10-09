// Project Grounded: leven in de Ultra Space-werelden (tools/grounded/maptools/ultra_worlds_b.py).
//
// Per-stap-callback STEP_CB_ULTRA_WORLDS (map-script ON_RESUME: setstepcallback STEP_CB_ULTRA_WORLDS); draait elke
// frame in de overworld:
//  - Ogen (OBJ_EVENT_GFX_ULTRA_EYE, Stakataka-doolhof): kijken altijd naar de speler.
//  - Rampen per wereld, af en toe en willekeurig (alleen als de speler vrij rondloopt en er geen fade bezig is):
//      Poipole (buitenaards): aardbevingen, bliksemflitsen, meteorietinslagen (schud + flits), zwaartekrachtgolf.
//      Guzzlord (verwoest Lilycove): gerommel uit de verte en instortend puin (licht schudden).
//      Blacephalon (circus): knallende ballonnen en vuurwerkflitsen.
//      Necrozma (prismagrot): lichtpulsen (zachte witte flits).
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "palette.h"
#include "constants/rgb.h"
#include "random.h"
#include "script.h"
#include "sound.h"
#include "task.h"
#include "constants/event_objects.h"
#include "constants/maps.h"
#include "constants/songs.h"
#include "ultra_worlds.h"

#define tCallbackId data[0]
#define tTimer      data[1]
#define tNext       data[2]
#define tFx         data[3]
#define tFxTime     data[4]
#define tFxParam    data[5]

enum
{
    FX_NONE,
    FX_QUAKE,        // lang schudden
    FX_RUMBLE,       // kort, zacht schudden
    FX_FLASH,        // witte bliksemflits
    FX_IMPACT,       // inslag: flits + schudden
    FX_PULSE,        // zachte lichtpuls
    FX_POP,          // gekleurde flits (vuurwerk/ballon)
};

static bool32 OnMap(u32 group, u32 num)
{
    return gSaveBlock1Ptr->location.mapGroup == group && gSaveBlock1Ptr->location.mapNum == num;
}

#define ON_MAP(m) OnMap(MAP_GROUP(m), MAP_NUM(m))

static void UpdateEyes(void)
{
    u32 i;
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *obj = &gObjectEvents[i];
        s32 dx, dy;
        u32 dir;

        if (!obj->active || obj->graphicsId != OBJ_EVENT_GFX_ULTRA_EYE)
            continue;
        dx = player->currentCoords.x - obj->currentCoords.x;
        dy = player->currentCoords.y - obj->currentCoords.y;
        if (dx == 0 && dy == 0)
            continue;
        if (abs(dx) > abs(dy))
            dir = dx > 0 ? DIR_EAST : DIR_WEST;
        else
            dir = dy > 0 ? DIR_SOUTH : DIR_NORTH;
        if (obj->facingDirection != dir)
            ObjectEventTurn(obj, dir);
    }
}

static void Flash(u32 coeff, u32 color)
{
    BlendPalettes(PALETTES_BG, coeff, color);
}

static void Unflash(void)
{
    BlendPalettes(PALETTES_BG, 0, RGB_BLACK);
}

// geeft TRUE zolang het effect loopt
static bool32 RunFx(s16 *data)
{
    s32 t = tFxTime++;
    s32 amp;

    switch (tFx)
    {
    case FX_QUAKE:
        if (t == 0)
            PlaySE(SE_M_EARTHQUAKE);
        if (t >= 64)
        {
            SetCameraPanning(0, 0);
            return FALSE;
        }
        amp = t < 48 ? 3 : 1;
        SetCameraPanning((t & 2) ? amp : -amp, (t & 4) ? 1 : -1);
        return TRUE;
    case FX_RUMBLE:
        if (t == 0)
            PlaySE(tFxParam ? tFxParam : SE_M_STRENGTH);
        if (t >= 24)
        {
            SetCameraPanning(0, 0);
            return FALSE;
        }
        SetCameraPanning(0, (t & 2) ? 1 : -1);
        return TRUE;
    case FX_FLASH:
        if (t == 0)
        {
            PlaySE(SE_THUNDER);
            Flash(12, RGB_WHITE);
        }
        else if (t == 3)
            Flash(4, RGB_WHITE);
        else if (t == 6)
            Flash(10, RGB_WHITE);
        else if (t == 9)
        {
            Unflash();
            return FALSE;
        }
        return TRUE;
    case FX_IMPACT:
        if (t == 0)
        {
            PlaySE(SE_M_EXPLOSION);
            Flash(9, RGB(31, 20, 12));
        }
        else if (t == 4)
            Unflash();
        if (t >= 40)
        {
            SetCameraPanning(0, 0);
            return FALSE;
        }
        amp = t < 20 ? 4 : 2;
        SetCameraPanning((t & 2) ? amp : -amp, (t & 2) ? -amp / 2 : amp / 2);
        return TRUE;
    case FX_PULSE:
        if (t == 0)
            PlaySE(SE_M_REFLECT);
        if (t < 16)
            Flash(t < 8 ? t : 16 - t, RGB(31, 31, 31));
        else
        {
            Unflash();
            return FALSE;
        }
        return TRUE;
    case FX_POP:
        if (t == 0)
        {
            PlaySE(SE_BALLOON_RED + (Random() % 3));
            Flash(5, tFxParam);
        }
        else if (t == 4)
        {
            Unflash();
            return FALSE;
        }
        return TRUE;
    }
    return FALSE;
}

static const u16 sPopColors[] = { RGB(31, 8, 8), RGB(31, 28, 6), RGB(8, 20, 31), RGB(28, 10, 31), RGB(10, 31, 12) };

void UltraWorlds_StepCallback(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    u32 r;

    UpdateEyes();
    if (tFx != FX_NONE)
    {
        if (!RunFx(data))
            tFx = FX_NONE;
        return;
    }
    if (ArePlayerFieldControlsLocked() || gPaletteFade.active)
        return;
    if (tNext == 0)
        tNext = 240 + Random() % 240;
    if (++tTimer < tNext)
        return;
    tTimer = 0;
    tFxTime = 0;
    tFxParam = 0;
    r = Random() % 100;
    if (ON_MAP(MAP_ULTRA_SPACE_POIPOLE))
    {
        tNext = 150 + Random() % 300;
        if (r < 30)
            tFx = FX_FLASH;
        else if (r < 55)
            tFx = FX_IMPACT;
        else if (r < 75)
            tFx = FX_QUAKE;
        else
        {
            tFx = FX_RUMBLE;
            tFxParam = SE_M_SANDSTORM;
        }
    }
    else if (ON_MAP(MAP_ULTRA_SPACE_GUZZLORD))
    {
        tNext = 360 + Random() % 480;
        tFx = r < 70 ? FX_RUMBLE : FX_QUAKE;
        if (r < 35)
            tFxParam = SE_M_SPIT_UP;
    }
    else if (ON_MAP(MAP_ULTRA_SPACE_BLACEPHALON))
    {
        tNext = 200 + Random() % 400;
        tFx = FX_POP;
        tFxParam = sPopColors[Random() % ARRAY_COUNT(sPopColors)];
    }
    else if (ON_MAP(MAP_ULTRA_SPACE_NECROZMA))
    {
        tNext = 300 + Random() % 420;
        tFx = FX_PULSE;
    }
    else
    {
        tNext = 0x7FFF;
    }
}
