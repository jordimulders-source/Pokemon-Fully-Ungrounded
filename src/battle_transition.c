#include "global.h"
#include "battle.h"
#include "battle_transition.h"
#include "battle_transition_frontier.h"
#include "bg.h"
#include "decompress.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_effect.h"
#include "field_weather.h"
#include "gpu_regs.h"
#include "main.h"
#include "m4a.h"
#include "malloc.h"
#include "overworld.h"
#include "palette.h"
#include "random.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "task.h"
#include "trig.h"
#include "util.h"
#include "battle_setup.h"
#include "data.h"
#include "constants/field_effects.h"
#include "constants/songs.h"
#include "constants/trainers.h"
#include "constants/rgb.h"
#include "starter_choose.h"
#include "constants/layouts.h"
#include "constants/region_map_sections.h"
#include "battle_anim.h"
#include "item_icon.h"
#include "menu.h"
#include "pokedex.h"
#include "string_util.h"
#include "text.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "fieldmap.h"
#include "constants/battle_anim.h"
#include "constants/items.h"

#define PALTAG_UNUSED_MUGSHOT 0x100A

#define B_TRANS_DMA_FLAGS (1 | ((DMA_SRC_INC | DMA_DEST_FIXED | DMA_REPEAT | DMA_16BIT | DMA_START_HBLANK | DMA_ENABLE) << 16))

// Used by each transition task to determine which of its functions to call
#define tState          data[0]

// Below are data defines for InitBlackWipe and UpdateBlackWipe, for the TransitionData data array.
// These will be re-used by any transitions that use these functions.
#define tWipeStartX data[0]
#define tWipeStartY data[1]
#define tWipeCurrX  data[2]
#define tWipeCurrY  data[3]
#define tWipeEndX   data[4]
#define tWipeEndY   data[5]
#define tWipeXMove  data[6]
#define tWipeYMove  data[7]
#define tWipeXDist  data[8]
#define tWipeYDist  data[9]
#define tWipeTemp   data[10]

#define SET_TILE(ptr, posY, posX, tile) \
{                                       \
    u32 index = (posY) * 32 + posX;     \
    ptr[index] = tile | (0xF0 << 8);    \
}

struct TransitionData
{
    vu8 VBlank_DMA;
    u16 WININ;
    u16 WINOUT;
    u16 WIN0H;
    u16 WIN0V;
    u16 unused1;
    u16 unused2;
    u16 BLDCNT;
    u16 BLDALPHA;
    u16 BLDY;
    s16 cameraX;
    s16 cameraY;
    s16 BG0HOFS_Lower;
    s16 BG0HOFS_Upper;
    s16 BG0VOFS; // used but not set
    s16 unused3;
    s16 counter;
    s16 unused4;
    s16 data[11];
};

struct RectangularSpiralLine
{
    u8 state;
    s16 position;
    u8 moveIndex;
    s16 reboundPosition;
    bool8 outward;
};

typedef bool8 (*TransitionStateFunc)(struct Task *task);
typedef bool8 (*TransitionSpriteCallback)(struct Sprite *sprite);
typedef bool8 (*TransitionSpriteCallbackPartner)(struct Sprite *sprite);

static bool8 Transition_StartIntro(struct Task *);
static bool8 Transition_WaitForIntro(struct Task *);
static bool8 Transition_StartMain(struct Task *);
static bool8 Transition_WaitForMain(struct Task *);

static void LaunchBattleTransitionTask(u8);
static void Task_BattleTransition(u8);
static void Task_Intro(u8);
static void Task_Blur(u8);
static void Task_Swirl(u8);
static void Task_Shuffle(u8);
static void Task_BigPokeball(u8);
static void Task_PokeballsTrail(u8);
static void Task_ClockwiseWipe(u8);
static void Task_Ripple(u8);
static void Task_Wave(u8);
static void Task_Slice(u8);
static void Task_WhiteBarsFade(u8);
static void Task_GridSquares(u8);
static void Task_AngledWipes(u8);
static void Task_Mugshot(u8);
static void Task_Aqua(u8);
static void Task_Magma(u8);
static void Task_Regice(u8);
static void Task_Registeel(u8);
static void Task_Regirock(u8);
static void Task_Kyogre(u8);
static void Task_Aurora(u8); // Project Grounded
static void Task_Regidrago(u8); // Project Grounded
static void Task_Regieleki(u8); // Project Grounded
static void Task_Regigigas(u8); // Project Grounded
static void Task_Dave(u8); // Project Grounded
static void Task_Deoxys(u8); // Project Grounded
static void Task_Birch(u8); // Project Grounded
static void Task_Raikou(u8); // Project Grounded
static void Task_Entei(u8); // Project Grounded
static void Task_RouteWave(u8); // Project Grounded
static void Task_RouteBeach(u8); // Project Grounded
static void Task_RouteBubbles(u8); // Project Grounded
static void Task_RouteSnow(u8); // Project Grounded
static void Task_RouteAsh(u8); // Project Grounded
static void Task_RouteSand(u8); // Project Grounded
static void Task_RouteHeat(u8); // Project Grounded
static void Task_RouteCycling(u8); // Project Grounded
static void Task_RoutePyre(u8); // Project Grounded
static void Task_RouteSky(u8); // Project Grounded
static void Task_RouteShort(u8); // Project Grounded
static void Task_RoutePaint(u8); // Project Grounded
static void Task_RouteSafari(u8); // Project Grounded
static void Task_RouteMeteor(u8); // Project Grounded
static void Task_RouteJagged(u8); // Project Grounded
static void Task_RouteRainforest(u8); // Project Grounded
static void Task_Pikachu(u8); // Project Grounded
static void Task_Magikarp(u8); // Project Grounded
static void Task_ViagraBoys(u8); // Project Grounded
static void Task_Psyduck(u8); // Project Grounded
static void Task_Koffing(u8); // Project Grounded
static void Task_GabbyTy(u8); // Project Grounded
static void Task_Poochyena(u8); // Project Grounded
static void Task_Beachball(u8); // Project Grounded
static void Task_Colress(u8); // Project Grounded
static void Task_Zangoose(u8); // Project Grounded
static void Task_Seviper(u8); // Project Grounded
static void Task_Heatran(u8); // Project Grounded
static void Task_Shaymin(u8); // Project Grounded
static void Task_Genesect(u8); // Project Grounded
static void Task_Mewtwo(u8); // Project Grounded
static void Task_Giratina(u8); // Project Grounded
static void Task_Victini(u8); // Project Grounded
static void Task_Jirachi(u8); // Project Grounded
static void Task_Darkrai(u8); // Project Grounded
static void Task_NeoPlasma(u8); // Project Grounded
static void Task_SickBlik(u8); // Project Grounded
static void Task_Steven(u8); // Project Grounded
static void Task_WallyVhs(u8); // Project Grounded
static void Task_RayquazaPillar(u8); // Project Grounded
static void Task_Mimi(u8); // Project Grounded
static void Task_Keccles(u8); // Project Grounded
static void Task_Burglar(u8); // Project Grounded
static void Task_GymRoxanne(u8); // Project Grounded (src/data/gym_intros_a.h)
static void Task_GymBrawly(u8); // Project Grounded
static void Task_GymWattson(u8); // Project Grounded
static void Task_GymFlannery(u8); // Project Grounded

static void Task_TapuKoko(u8); // Project Grounded
static void Task_TapuLele(u8);
static void Task_TapuBulu(u8);
static void Task_TapuFini(u8);
static void Task_GymNorman(u8); // Project Grounded (src/data/gym_intros_b.h)
static void Task_GymWinona(u8); // Project Grounded (src/data/gym_intros_b.h)
static void Task_GymTateLiza(u8); // Project Grounded (src/data/gym_intros_b.h)
static void Task_GymWallace(u8); // Project Grounded (src/data/gym_intros_b.h)
static void Task_LegendLugia(u8); // Project Grounded (src/data/legend_intros.h)
static void Task_LegendHooh(u8);
static void Task_LegendVolcanion(u8);
static void Task_LegendHoopa(u8);
static void Task_LegendForces(u8);
static void Task_LegendArticuno(u8); // Project Grounded (src/data/legend_intros2.h)
static void Task_LegendZapdos(u8);
static void Task_LegendMoltres(u8);
static void Task_LegendZacian(u8);
static void Task_LegendZamazenta(u8);
static void Task_LegendXerneas(u8);
static void Task_LegendYveltal(u8);
static void Task_Wario(u8); // Project Grounded (src/data/wario_intro.h)
static void Task_Boo(u8); // Project Grounded (src/data/boo_intro.h)
static void Task_ShyGuy(u8); // Project Grounded (src/data/shyguy_intro.h)
static void Task_LegendDialga(u8); // Project Grounded (src/data/legend_intros_dp.h)
static void Task_LegendPalkia(u8);
static void Task_LegendArceus(u8);
static void Task_LegendMew(u8);
static void Task_LegendCrown(u8); // Project Grounded (src/data/legend_intros_cheap2.h)
static void Task_LegendCelebi(u8);
static void Task_LegendLake(u8);
static void Task_LegendMeloetta(u8);
static void Task_LegendZeraora(u8);
static void Task_LegendZygarde(u8);
static void Task_LegendEon(u8);
static void Task_LegendCresselia(u8);
static void Task_LegendNecrozma(u8);
static void Task_LegendGalarZapdos(u8);
static void Task_LegendGalarMoltres(u8);
static void Task_LegendSwords(u8); // Project Grounded (src/data/legend_intros_cheap1.h)
static void Task_LegendUltraBeast(u8);
static void Task_LegendParadoxPast(u8);
static void Task_LegendParadoxFuture(u8);
static void Task_LegendEternatus(u8);
static void Task_LegendMarshadow(u8);
static void Task_LegendTerapagos(u8);
static void Task_LegendPecharunt(u8);
static void Task_RivalIntro(u8); // Project Grounded (src/data/rival_intros.h)
static void Task_ClassIntro(u8); // Project Grounded (src/data/class_intros.h)
static void Task_KyogreMural(u8); // Project Grounded
static void Task_GroudonMural(u8); // Project Grounded
static void Task_Ogerpon(u8); // Project Grounded
static void Task_WeatherService(u8); // Project Grounded
static void Task_Rocket(u8); // Project Grounded
static void Task_Zarude(u8); // Project Grounded
static void Task_PoisonChain(u8); // Project Grounded
static void Task_AquaMagma(u8); // Project Grounded
static bool8 AquaMagma_Init(struct Task *);
static bool8 Regidrago_Init(struct Task *);
static bool8 Regieleki_Init(struct Task *);
static bool8 Regigigas_Init(struct Task *);
static void Task_Groudon(u8);
static void Task_Rayquaza(u8);
static void Task_ShredSplit(u8);
static void Task_Blackhole(u8);
static void Task_BlackholePulsate(u8);
static void Task_RectangularSpiral(u8);
static void Task_FrontierLogoWiggle(u8);
static void Task_FrontierLogoWave(u8);
static void Task_FrontierSquares(u8);
static void Task_FrontierSquaresScroll(u8);
static void Task_FrontierSquaresSpiral(u8);
static void VBlankCB_BattleTransition(void);
static void VBlankCB_Swirl(void);
static void HBlankCB_Swirl(void);
static void VBlankCB_Shuffle(void);
static void HBlankCB_Shuffle(void);
static void VBlankCB_PatternWeave(void);
static void VBlankCB_CircularMask(void);
static void VBlankCB_ClockwiseWipe(void);
static void VBlankCB_Ripple(void);
static void HBlankCB_Ripple(void);
static void VBlankCB_FrontierLogoWave(void);
static void HBlankCB_FrontierLogoWave(void);
static void VBlankCB_Wave(void);
static void VBlankCB_Slice(void);
static void HBlankCB_Slice(void);
static void VBlankCB_WhiteBarsFade(void);
static void VBlankCB_WhiteBarsFade_Blend(void);
static void HBlankCB_WhiteBarsFade(void);
static void VBlankCB_AngledWipes(void);
static void VBlankCB_Rayquaza(void);
static bool8 Blur_Init(struct Task *);
static bool8 Blur_Main(struct Task *);
static bool8 Blur_End(struct Task *);
static bool8 Swirl_Init(struct Task *);
static bool8 Swirl_End(struct Task *);
static bool8 Shuffle_Init(struct Task *);
static bool8 Shuffle_End(struct Task *);
static bool8 Aqua_Init(struct Task *);
static bool8 Aqua_SetGfx(struct Task *);
static bool8 Magma_Init(struct Task *);
static bool8 Magma_SetGfx(struct Task *);
static bool8 FramesCountdown(struct Task *);
static bool8 Regi_Init(struct Task *);
static bool8 Regice_SetGfx(struct Task *);
static bool8 Registeel_SetGfx(struct Task *);
static bool8 Regirock_SetGfx(struct Task *);
static bool8 WeatherTrio_BgFadeBlack(struct Task *);
static bool8 WeatherTrio_WaitFade(struct Task *);
static bool8 Kyogre_Init(struct Task *);
static bool8 Kyogre_PaletteFlash(struct Task *);
static bool8 Kyogre_PaletteBrighten(struct Task *);
static bool8 Groudon_Init(struct Task *);
static bool8 Groudon_PaletteFlash(struct Task *);
static bool8 Groudon_PaletteBrighten(struct Task *);
static bool8 WeatherDuo_FadeOut(struct Task *);
static bool8 WeatherDuo_End(struct Task *);
static bool8 BigPokeball_Init(struct Task *);
static bool8 BigPokeball_SetGfx(struct Task *);
static bool8 PatternWeave_Blend1(struct Task *);
static bool8 PatternWeave_Blend2(struct Task *);
static bool8 PatternWeave_FinishAppear(struct Task *);
static bool8 PatternWeave_CircularMask(struct Task *);
static bool8 PokeballsTrail_Init(struct Task *);
static bool8 PokeballsTrail_Main(struct Task *);
static bool8 PokeballsTrail_End(struct Task *);
static bool8 ClockwiseWipe_Init(struct Task *);
static bool8 ClockwiseWipe_TopRight(struct Task *);
static bool8 ClockwiseWipe_Right(struct Task *);
static bool8 ClockwiseWipe_Bottom(struct Task *);
static bool8 ClockwiseWipe_Left(struct Task *);
static bool8 ClockwiseWipe_TopLeft(struct Task *);
static bool8 ClockwiseWipe_End(struct Task *);
static bool8 Ripple_Init(struct Task *);
static bool8 Ripple_Main(struct Task *);
static bool8 Wave_Init(struct Task *);
static bool8 Wave_Main(struct Task *);
static bool8 Wave_End(struct Task *);
static bool8 Slice_Init(struct Task *);
static bool8 Slice_Main(struct Task *);
static bool8 Slice_End(struct Task *);
static bool8 WhiteBarsFade_Init(struct Task *);
static bool8 WhiteBarsFade_StartBars(struct Task *);
static bool8 WhiteBarsFade_WaitBars(struct Task *);
static bool8 WhiteBarsFade_BlendToBlack(struct Task *);
static bool8 WhiteBarsFade_End(struct Task *);
static bool8 GridSquares_Init(struct Task *);
static bool8 GridSquares_Main(struct Task *);
static bool8 GridSquares_End(struct Task *);
static bool8 AngledWipes_Init(struct Task *);
static bool8 AngledWipes_SetWipeData(struct Task *);
static bool8 AngledWipes_DoWipe(struct Task *);
static bool8 AngledWipes_TryEnd(struct Task *);
static bool8 AngledWipes_StartNext(struct Task *);
static bool8 ShredSplit_Init(struct Task *);
static bool8 ShredSplit_Main(struct Task *);
static bool8 ShredSplit_End(struct Task *);
static bool8 Blackhole_Init(struct Task *);
static bool8 Blackhole_Vibrate(struct Task *);
static bool8 Blackhole_GrowEnd(struct Task *);
static bool8 BlackholePulsate_Main(struct Task *);
static bool8 RectangularSpiral_Init(struct Task *);
static bool8 RectangularSpiral_Main(struct Task *);
static bool8 RectangularSpiral_End(struct Task *);
static bool8 FrontierLogoWiggle_Init(struct Task *);
static bool8 FrontierLogoWiggle_SetGfx(struct Task *);
static bool8 FrontierLogoWave_Init(struct Task *);
static bool8 FrontierLogoWave_SetGfx(struct Task *);
static bool8 FrontierLogoWave_InitScanline(struct Task *);
static bool8 FrontierLogoWave_Main(struct Task *);
static bool8 Rayquaza_Init(struct Task *);
static bool8 Rayquaza_SetGfx(struct Task *);
static bool8 Rayquaza_PaletteFlash(struct Task *);
static bool8 Rayquaza_FadeToBlack(struct Task *);
static bool8 Rayquaza_WaitFade(struct Task *);
static bool8 Rayquaza_SetBlack(struct Task *);
static bool8 Rayquaza_TriRing(struct Task *);
static bool8 FrontierSquares_Init(struct Task *);
static bool8 FrontierSquares_Draw(struct Task *);
static bool8 FrontierSquares_Shrink(struct Task *);
static bool8 FrontierSquares_End(struct Task *);
static bool8 FrontierSquaresSpiral_Init(struct Task *);
static bool8 FrontierSquaresSpiral_Outward(struct Task *);
static bool8 FrontierSquaresSpiral_SetBlack(struct Task *);
static bool8 FrontierSquaresSpiral_Inward(struct Task *);
static bool8 FrontierSquaresScroll_Init(struct Task *);
static bool8 FrontierSquaresScroll_Draw(struct Task *);
static bool8 FrontierSquaresScroll_SetBlack(struct Task *);
static bool8 FrontierSquaresScroll_Erase(struct Task *);
static bool8 FrontierSquaresScroll_End(struct Task *);
static bool8 Mugshot_Init(struct Task *);
static bool8 Mugshot_SetGfx(struct Task *);
static bool8 Mugshot_ShowBanner(struct Task *);
static bool8 Mugshot_StartOpponentSlide(struct Task *);
static bool8 Mugshot_WaitStartPlayerSlide(struct Task *);
static bool8 Mugshot_WaitPlayerSlide(struct Task *);
static bool8 Mugshot_GradualWhiteFade(struct Task *);
static bool8 Mugshot_InitFadeWhiteToBlack(struct Task *);
static bool8 Mugshot_FadeToBlack(struct Task *);
static bool8 Mugshot_End(struct Task *);
static void Mugshots_CreateTrainerPics(struct Task *);
static void VBlankCB_Mugshots(void);
static void VBlankCB_MugshotsFadeOut(void);
static void HBlankCB_Mugshots(void);
static void InitTransitionData(void);
static void FadeScreenBlack(void);
static void CreateIntroTask(s16, s16, s16, s16, s16);
static void SetCircularMask(u16 *, s16, s16, s16);
static void SetSinWave(s16 *, s16, s16, s16, s16, s16);
static void GetBg0TilemapDst(u16 **);
static void InitBlackWipe(s16 *, s16, s16, s16, s16, s16, s16);
static bool8 UpdateBlackWipe(s16 *, bool8, bool8);
static void SetTrainerPicSlideDirection(s16, s16);
static void IncrementTrainerPicState(s16);
static s16 IsTrainerPicSlideDone(s16);
static bool8 TransitionIntro_FadeToGray(struct Task *);
static bool8 TransitionIntro_FadeFromGray(struct Task *);
static bool8 IsIntroTaskDone(void);
static bool16 UpdateRectangularSpiralLine(const s16 *const *, struct RectangularSpiralLine *);
static void SpriteCB_FldEffPokeballTrail(struct Sprite *);
static void SpriteCB_MugshotTrainerPic(struct Sprite *);
static void SpriteCB_MugshotTrainerPicPartner(struct Sprite *);
static void SpriteCB_WhiteBarFade(struct Sprite *);
static bool8 MugshotTrainerPic_Pause(struct Sprite *);
static bool8 MugshotTrainerPic_Init(struct Sprite *);
static bool8 MugshotTrainerPic_Slide(struct Sprite *);
static bool8 MugshotTrainerPic_SlideSlow(struct Sprite *);
static bool8 MugshotTrainerPic_SlidePartner(struct Sprite *);
static bool8 MugshotTrainerPic_SlideOffscreen(struct Sprite *);

static s16 sDebug_RectangularSpiralData;
static u8 sTestingTransitionId;
static u8 sTestingTransitionState;
static struct RectangularSpiralLine sRectangularSpiralLines[4];

EWRAM_DATA static struct TransitionData *sTransitionData = NULL;

#define RT_SMOL 0   // Project Grounded: grootte 0 = tiles zijn smol-gecomprimeerd (v0.9.230)
static const u32 sBigPokeball_Tileset[] = INCBIN_U32("graphics/battle_transitions/big_pokeball.4bpp");
static const u32 sPokeballTrail_Tileset[] = INCBIN_U32("graphics/battle_transitions/pokeball_trail.4bpp");
static const u8 sPokeball_Gfx[] = INCBIN_U8("graphics/battle_transitions/pokeball.4bpp");
static const u32 sEliteFour_Tileset[] = INCBIN_U32("graphics/battle_transitions/elite_four_bg.4bpp");
static const u8 sUnusedBrendan_Gfx[] = INCBIN_U8("graphics/battle_transitions/unused_brendan.4bpp");
static const u8 sUnusedLass_Gfx[] = INCBIN_U8("graphics/battle_transitions/unused_lass.4bpp");
static const u32 sShrinkingBoxTileset[] = INCBIN_U32("graphics/battle_transitions/shrinking_box.4bpp");
static const u16 sEvilTeam_Palette[] = INCBIN_U16("graphics/battle_transitions/evil_team.gbapal");
static const u32 sTeamAqua_Tileset[] = INCBIN_U32("graphics/battle_transitions/team_aqua.4bpp.smol");
static const u32 sTeamAqua_Tilemap[] = INCBIN_U32("graphics/battle_transitions/team_aqua.bin.smolTM");
static const u32 sTeamMagma_Tileset[] = INCBIN_U32("graphics/battle_transitions/team_magma.4bpp.smol");
static const u32 sTeamMagma_Tilemap[] = INCBIN_U32("graphics/battle_transitions/team_magma.bin.smolTM");
static const u32 sRegis_Tileset[] = INCBIN_U32("graphics/battle_transitions/regis.4bpp");
static const u16 sRegice_Palette[] = INCBIN_U16("graphics/battle_transitions/regice.gbapal");
static const u16 sRegisteel_Palette[] = INCBIN_U16("graphics/battle_transitions/registeel.gbapal");
static const u16 sRegirock_Palette[] = INCBIN_U16("graphics/battle_transitions/regirock.gbapal");
static const u32 sRegice_Tilemap[] = INCBIN_U32("graphics/battle_transitions/regice.bin");
static const u32 sRegisteel_Tilemap[] = INCBIN_U32("graphics/battle_transitions/registeel.bin");
static const u32 sRegirock_Tilemap[] = INCBIN_U32("graphics/battle_transitions/regirock.bin");
static const u16 sUnused_Palette[] = INCBIN_U16("graphics/battle_transitions/unused.gbapal");
static const u32 sKyogre_Tileset[] = INCBIN_U32("graphics/battle_transitions/kyogre.4bpp.smol");
static const u32 sKyogre_Tilemap[] = INCBIN_U32("graphics/battle_transitions/kyogre.bin.smolTM");
static const u32 sGroudon_Tileset[] = INCBIN_U32("graphics/battle_transitions/groudon.4bpp.smol");
static const u32 sGroudon_Tilemap[] = INCBIN_U32("graphics/battle_transitions/groudon.bin.smolTM");
static const u16 sKyogre1_Palette[] = INCBIN_U16("graphics/battle_transitions/kyogre_pt1.gbapal");
static const u16 sKyogre2_Palette[] = INCBIN_U16("graphics/battle_transitions/kyogre_pt2.gbapal");
// Project Grounded: noorderlicht-transitie (Suicune), gegenereerd met tools/grounded/aurora_transition.py
static const u32 sAurora_Tileset[] = INCBIN_U32("graphics/battle_transitions/aurora.4bpp.smol");
static const u16 sAurora_Tilemap[] = INCBIN_U16("graphics/battle_transitions/aurora.bin");
static const u16 sAurora_Palette[] = INCBIN_U16("graphics/battle_transitions/aurora.gbapal");
static const u32 sRegidrago_Tileset[] = INCBIN_U32("graphics/battle_transitions/regidrago.4bpp.smol");
static const u16 sRegidrago_Tilemap[] = INCBIN_U16("graphics/battle_transitions/regidrago.bin");
static const u16 sRegidrago_Palette[] = INCBIN_U16("graphics/battle_transitions/regidrago.gbapal");
static const u32 sRegieleki_Tileset[] = INCBIN_U32("graphics/battle_transitions/regieleki.4bpp.smol");
static const u16 sRegieleki_Tilemap[] = INCBIN_U16("graphics/battle_transitions/regieleki.bin");
static const u16 sRegieleki_Palette[] = INCBIN_U16("graphics/battle_transitions/regieleki.gbapal");
static const u32 sRegigigas_Tileset[] = INCBIN_U32("graphics/battle_transitions/regigigas.4bpp.smol");
static const u16 sRegigigas_Tilemap[] = INCBIN_U16("graphics/battle_transitions/regigigas.bin");
static const u16 sRegigigas_Palette[] = INCBIN_U16("graphics/battle_transitions/regigigas.gbapal");
static const u16 sDeoxys_Tileset[] = INCBIN_U16("graphics/battle_transitions/deoxys.4bpp");
static const u16 sDeoxys_Tilemap[] = INCBIN_U16("graphics/battle_transitions/deoxys.bin");
static const u16 sDeoxys_Palette[] = INCBIN_U16("graphics/battle_transitions/deoxys.gbapal");
static const u16 sBirch_Tileset[] = INCBIN_U16("graphics/battle_transitions/birch.4bpp");
static const u16 sBirch_Palette[] = INCBIN_U16("graphics/battle_transitions/birch.gbapal");
static const u32 sRaikou_Tileset[] = INCBIN_U32("graphics/battle_transitions/raikou.4bpp.smol");
static const u16 sRaikou_Tilemap[] = INCBIN_U16("graphics/battle_transitions/raikou.bin");
static const u16 sRaikou_Palette[] = INCBIN_U16("graphics/battle_transitions/raikou.gbapal");
static const u16 sEntei_Tileset[] = INCBIN_U16("graphics/battle_transitions/entei.4bpp");
static const u16 sEntei_Palette[] = INCBIN_U16("graphics/battle_transitions/entei.gbapal");
static const u32 sRouteWave_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_wave.4bpp.smol");
static const u16 sRouteWave_Palette[] = INCBIN_U16("graphics/battle_transitions/route_wave.gbapal");
static const u32 sRouteBeach_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_beach.4bpp.smol");
static const u16 sRouteBeach_Palette[] = INCBIN_U16("graphics/battle_transitions/route_beach.gbapal");
static const u32 sRouteBubbles_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_bubbles.4bpp.smol");
static const u16 sRouteBubbles_Palette[] = INCBIN_U16("graphics/battle_transitions/route_bubbles.gbapal");
static const u32 sRouteSnow_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_snow.4bpp.smol");
static const u16 sRouteSnow_Palette[] = INCBIN_U16("graphics/battle_transitions/route_snow.gbapal");
static const u32 sRouteAsh_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_ash.4bpp.smol");
static const u16 sRouteAsh_Palette[] = INCBIN_U16("graphics/battle_transitions/route_ash.gbapal");
static const u32 sRouteSand_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_sand.4bpp.smol");
static const u16 sRouteSand_Palette[] = INCBIN_U16("graphics/battle_transitions/route_sand.gbapal");
static const u32 sRouteCycling_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_cycling.4bpp.smol");
static const u16 sRouteCycling_Tilemap[] = INCBIN_U16("graphics/battle_transitions/route_cycling.bin");
static const u16 sRouteCycling_Palette[] = INCBIN_U16("graphics/battle_transitions/route_cycling.gbapal");
static const u32 sRoutePyre_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_pyre.4bpp.smol");
static const u16 sRoutePyre_Palette[] = INCBIN_U16("graphics/battle_transitions/route_pyre.gbapal");
static const u32 sRouteSky_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_sky.4bpp.smol");
static const u16 sRouteSky_Palette[] = INCBIN_U16("graphics/battle_transitions/route_sky.gbapal");
static const u16 sRouteShort_Tileset[] = INCBIN_U16("graphics/battle_transitions/route_short.4bpp");
static const u16 sRouteShort_Palette[] = INCBIN_U16("graphics/battle_transitions/route_short.gbapal");
static const u32 sRoutePaint_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_paint.4bpp.smol");
static const u16 sRoutePaint_Palette[] = INCBIN_U16("graphics/battle_transitions/route_paint.gbapal");
static const u32 sRouteSafari_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_safari.4bpp.smol");
static const u16 sRouteSafari_Palette[] = INCBIN_U16("graphics/battle_transitions/route_safari.gbapal");
static const u32 sRouteMeteor_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_meteor.4bpp.smol");
static const u16 sRouteMeteor_Palette[] = INCBIN_U16("graphics/battle_transitions/route_meteor.gbapal");
static const u32 sRouteJagged_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_jagged.4bpp.smol");
static const u16 sRouteJagged_Tilemap[] = INCBIN_U16("graphics/battle_transitions/route_jagged.bin");
static const u16 sRouteJagged_Palette[] = INCBIN_U16("graphics/battle_transitions/route_jagged.gbapal");
static const u32 sRouteRainforest_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_rainforest.4bpp.smol");
static const u16 sRouteRainforest_Palette[] = INCBIN_U16("graphics/battle_transitions/route_rainforest.gbapal");
static const u16 sPikachu_Tileset[] = INCBIN_U16("graphics/battle_transitions/route_pikachu.4bpp");
static const u16 sPikachu_Palette[] = INCBIN_U16("graphics/battle_transitions/route_pikachu.gbapal");
static const u32 sMagikarp_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_magikarp.4bpp.smol");
static const u16 sMagikarp_Palette[] = INCBIN_U16("graphics/battle_transitions/route_magikarp.gbapal");
static const u32 sMagikarpPile_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_magikarp_pile.4bpp.smol");
static const u16 sMagikarpPile_Tilemap[] = INCBIN_U16("graphics/battle_transitions/route_magikarp_pile.bin");
static const u16 sMagikarpPile_Palette[] = INCBIN_U16("graphics/battle_transitions/route_magikarp_pile.gbapal");
static const u32 sMagikarpSprite_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_magikarp.4bpp");
static const u16 sMagikarpSprite_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_magikarp.gbapal");
static const u32 sGabbyTy_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_camera.4bpp.smol");
static const u16 sGabbyTy_Palette[] = INCBIN_U16("graphics/battle_transitions/route_camera.gbapal");
static const u32 sKoffing_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_koffing.4bpp.smol");
static const u16 sKoffing_Tilemap[] = INCBIN_U16("graphics/battle_transitions/route_koffing.bin");
static const u16 sKoffing_Palette[] = INCBIN_U16("graphics/battle_transitions/route_koffing.gbapal");
static const u32 sBeachball_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_beachball.4bpp.smol");
static const u16 sBeachball_Tilemap[] = INCBIN_U16("graphics/battle_transitions/route_beachball.bin");
static const u16 sBeachball_Palette[] = INCBIN_U16("graphics/battle_transitions/route_beachball.gbapal");
static const u32 sQuestionSprite_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_question.4bpp");
static const u16 sQuestionSprite_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_question.gbapal");
static const u32 sPoochyenaSprite_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_poochyena.4bpp");
static const u16 sPoochyenaSprite_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_poochyena.gbapal");
static const u32 sGearSprite_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_gear.4bpp");
static const u16 sGearSprite_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_gear.gbapal");
static const u32 sZangoose_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_zangoose.4bpp.smol");
static const u16 sZangoose_Palette[] = INCBIN_U16("graphics/battle_transitions/route_zangoose.gbapal");
static const u32 sZangooseClaw_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_zangoose_claw.4bpp");
static const u16 sZangooseClaw_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_zangoose_claw.gbapal");
static const u32 sSeviper_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_seviper.4bpp.smol");
static const u32 sHeatran_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_heatran.4bpp.smol");
static const u16 sHeatran_Palette[] = INCBIN_U16("graphics/battle_transitions/route_heatran.gbapal");
static const u32 sShaymin_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_shaymin.4bpp.smol");
static const u16 sShaymin_Palette[] = INCBIN_U16("graphics/battle_transitions/route_shaymin.gbapal");
static const u8 sShaymin_Petals[] = INCBIN_U8("graphics/battle_transitions/route_shaymin_petals.bin");
static const u8 sShaymin_Carpet[] = INCBIN_U8("graphics/battle_transitions/route_shaymin_carpet.bin");
static const u32 sGenesect_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_genesect.4bpp.smol");
static const u16 sGenesect_Palette[] = INCBIN_U16("graphics/battle_transitions/route_genesect.gbapal");
static const u32 sMewtwo_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_mewtwo.4bpp.smol");
static const u16 sMewtwo_Palette[] = INCBIN_U16("graphics/battle_transitions/route_mewtwo.gbapal");
static const u16 sMewtwo_Lab[] = INCBIN_U16("graphics/battle_transitions/route_mewtwo_lab.bin");
static const u16 sMewtwo_Crack[] = INCBIN_U16("graphics/battle_transitions/route_mewtwo_crack.bin");
static const u16 sMewtwo_Page[] = INCBIN_U16("graphics/battle_transitions/route_mewtwo_page.bin");
static const u16 sMewtwo_Burst[] = INCBIN_U16("graphics/battle_transitions/route_mewtwo_burst.bin");
static const u32 sGiratina_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_giratina.4bpp.smol");
static const u16 sGiratina_Palette[] = INCBIN_U16("graphics/battle_transitions/route_giratina.gbapal");
static const u16 sGiratina_Crack[] = INCBIN_U16("graphics/battle_transitions/route_giratina_crack.bin");
static const u8 sGiratina_CrackTime[] = INCBIN_U8("graphics/battle_transitions/route_giratina_crack_t.bin");
static const u16 sGiratina_Wing[] = INCBIN_U16("graphics/battle_transitions/route_giratina_wing.bin");
static const u32 sVictini_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_victini.4bpp.smol");
static const u16 sVictini_Palette[] = INCBIN_U16("graphics/battle_transitions/route_victini.gbapal");
static const u16 sVictini_V[] = INCBIN_U16("graphics/battle_transitions/route_victini_v.bin");
static const u32 sJirachi_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_jirachi.4bpp.smol");
static const u16 sJirachi_Palette[] = INCBIN_U16("graphics/battle_transitions/route_jirachi.gbapal");
static const u32 sJirachiStar_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_jirachi_star.4bpp");
static const u16 sJirachiStar_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_jirachi_star.gbapal");
static const u32 sDarkrai_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_darkrai.4bpp.smol");
static const u32 sNeoPlasma_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_neo_plasma.4bpp.smol"); // Project Grounded
static const u16 sNeoPlasma_Palette[] = INCBIN_U16("graphics/battle_transitions/route_neo_plasma.gbapal");
static const u16 sNeoPlasma_Maps[] = INCBIN_U16("graphics/battle_transitions/route_neo_plasma.bin");
// Project Grounded: SickBlik (tools/grounded/sickblik_transition.py)
static const u32 sSickBlik_TableTiles[] = INCBIN_U32("graphics/battle_transitions/sickblik_table_tiles.bin");
static const u16 sSickBlik_TableMap[] = INCBIN_U16("graphics/battle_transitions/sickblik_table_map.bin");
static const u16 sSickBlik_TablePals[] = INCBIN_U16("graphics/battle_transitions/sickblik_table_pals.bin");
static const u32 sSickBlik_TopStatic[] = INCBIN_U32("graphics/battle_transitions/sickblik_top_static.bin");
static const u32 sSickBlik_TopDyn[] = INCBIN_U32("graphics/battle_transitions/sickblik_top_dyn_lz.bin"); // LZ77 per sleutelbeeld
static const u16 sSickBlik_TopMaps[] = INCBIN_U16("graphics/battle_transitions/sickblik_top_maps.bin");
static const u16 sSickBlik_TopPals[] = INCBIN_U16("graphics/battle_transitions/sickblik_top_pals.bin");
#include "data/sickblik_transition.h"
static const u16 sDarkrai_Palette[] = INCBIN_U16("graphics/battle_transitions/route_darkrai.gbapal");
static const u32 sDarkraiEye_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_darkrai_eye.4bpp");
static const u16 sDarkraiEye_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_darkrai_eye.gbapal");
static const u32 sRocket_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_rocket.4bpp.smol");
static const u16 sRocket_Palette[] = INCBIN_U16("graphics/battle_transitions/route_rocket.gbapal");
static const u32 sRocketR_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_rocket_r.4bpp");
static const u16 sRocketR_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_rocket_r.gbapal");
static const u32 sZarude_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_zarude.4bpp.smol"); // Project Grounded
static const u16 sZarude_Palette[] = INCBIN_U16("graphics/battle_transitions/route_zarude.gbapal");
static const u16 sZarude_Claws[] = INCBIN_U16("graphics/battle_transitions/route_zarude_claws.bin");
static const u8 sZarude_Depth[] = INCBIN_U8("graphics/battle_transitions/route_zarude_depth.bin");
static const u32 sDave_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_dave.4bpp.smol"); // Project Grounded
static const u16 sDave_Palette[] = INCBIN_U16("graphics/battle_transitions/route_dave.gbapal");
static const u16 sDave_Maps[] = INCBIN_U16("graphics/battle_transitions/route_dave.bin");
static const s16 sDave_Ball[] = INCBIN_S16("graphics/battle_transitions/route_dave_ball.bin");
static const u32 sDaveBall_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_dave_ball.4bpp");
static const u16 sDaveBall_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_dave_ball.gbapal");
static const u32 sPoisonChain_Tileset[] = INCBIN_U32("graphics/battle_transitions/route_poisonchain.4bpp.smol"); // Project Grounded
static const u16 sPoisonChain_Palette[] = INCBIN_U16("graphics/battle_transitions/route_poisonchain.gbapal");
static const u16 sPoisonChain_Map[] = INCBIN_U16("graphics/battle_transitions/route_poisonchain_map.bin");
static const u16 sPoisonChain_Anim[] = INCBIN_U16("graphics/battle_transitions/route_poisonchain_anim.bin");
static const u32 sZarudeSil_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_zarude_silhouette.4bpp");
static const u16 sZarudeSil_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_zarude_silhouette.gbapal");
static const u16 sSeviper_Palette[] = INCBIN_U16("graphics/battle_transitions/route_seviper.gbapal");
static const u16 sSeviper_Upper[] = INCBIN_U16("graphics/battle_transitions/route_seviper_upper.bin");
static const u16 sSeviper_Lower[] = INCBIN_U16("graphics/battle_transitions/route_seviper_lower.bin");
static const u32 sBeachballSprite_Gfx[] = INCBIN_U32("graphics/battle_transitions/sprite_beachball.4bpp");
static const u16 sBeachballSprite_Palette[] = INCBIN_U16("graphics/battle_transitions/sprite_beachball.gbapal");
static const u32 sAquaMagma_Tileset[] = INCBIN_U32("graphics/battle_transitions/aqua_magma.4bpp.smol");
static const u16 sAquaMagma_Tilemap[] = INCBIN_U16("graphics/battle_transitions/aqua_magma.bin");
static const u16 sGroudon1_Palette[] = INCBIN_U16("graphics/battle_transitions/groudon_pt1.gbapal");
static const u16 sGroudon2_Palette[] = INCBIN_U16("graphics/battle_transitions/groudon_pt2.gbapal");
static const u16 sRayquaza_Palette[] = INCBIN_U16("graphics/battle_transitions/rayquaza.gbapal");
static const u32 sRayquaza_Tileset[] = INCBIN_U32("graphics/battle_transitions/rayquaza.4bpp");
static const u32 sRayquaza_Tilemap[] = INCBIN_U32("graphics/battle_transitions/rayquaza.bin");
static const u16 sFrontierLogo_Palette[] = INCBIN_U16("graphics/battle_transitions/frontier_logo.gbapal");
static const u32 sFrontierLogo_Tileset[] = INCBIN_U32("graphics/battle_transitions/frontier_logo.4bpp.smol");
static const u32 sFrontierLogo_Tilemap[] = INCBIN_U32("graphics/battle_transitions/frontier_logo.bin.smolTM");
static const u16 sFrontierSquares_Palette[] = INCBIN_U16("graphics/battle_transitions/frontier_squares_blanktiles.gbapal");
static const u32 sFrontierSquares_FilledBg_Tileset[] = INCBIN_U32("graphics/battle_transitions/frontier_square_1.4bpp.smol");
static const u32 sFrontierSquares_EmptyBg_Tileset[] = INCBIN_U32("graphics/battle_transitions/frontier_square_2.4bpp.smol");
static const u32 sFrontierSquares_Shrink1_Tileset[] = INCBIN_U32("graphics/battle_transitions/frontier_square_3.4bpp.smol");
static const u32 sFrontierSquares_Shrink2_Tileset[] = INCBIN_U32("graphics/battle_transitions/frontier_square_4.4bpp.smol");
static const u32 sFrontierSquares_Tilemap[] = INCBIN_U32("graphics/battle_transitions/frontier_squares.bin");

// All battle transitions use the same intro
static const TaskFunc sTasks_Intro[B_TRANSITION_COUNT] =
{
    [0 ... B_TRANSITION_COUNT - 1] = &Task_Intro,
    [B_TRANSITION_ARCEUS] = NULL, // Project Grounded: geen flits vooraf, de wereld trilt meteen op de eerste stoot
};

// After the intro each transition has a unique main task.
// This task will call the functions that do the transition effects.
static const TaskFunc sTasks_Main[B_TRANSITION_COUNT] =
{
    [B_TRANSITION_BLUR] = Task_Blur,
    [B_TRANSITION_SWIRL] = Task_Swirl,
    [B_TRANSITION_SHUFFLE] = Task_Shuffle,
    [B_TRANSITION_BIG_POKEBALL] = Task_BigPokeball,
    [B_TRANSITION_POKEBALLS_TRAIL] = Task_PokeballsTrail,
    [B_TRANSITION_CLOCKWISE_WIPE] = Task_ClockwiseWipe,
    [B_TRANSITION_RIPPLE] = Task_Ripple,
    [B_TRANSITION_WAVE] = Task_Wave,
    [B_TRANSITION_SLICE] = Task_Slice,
    [B_TRANSITION_WHITE_BARS_FADE] = Task_WhiteBarsFade,
    [B_TRANSITION_GRID_SQUARES] = Task_GridSquares,
    [B_TRANSITION_ANGLED_WIPES] = Task_AngledWipes,
    [B_TRANSITION_MUGSHOT] = Task_Mugshot,
    [B_TRANSITION_AQUA] = Task_Aqua,
    [B_TRANSITION_MAGMA] = Task_Magma,
    [B_TRANSITION_REGICE] = Task_Regice,
    [B_TRANSITION_REGISTEEL] = Task_Registeel,
    [B_TRANSITION_REGIROCK] = Task_Regirock,
    [B_TRANSITION_KYOGRE] = Task_Kyogre,
    [B_TRANSITION_GROUDON] = Task_Groudon,
    [B_TRANSITION_RAYQUAZA] = Task_Rayquaza,
    [B_TRANSITION_SHRED_SPLIT] = Task_ShredSplit,
    [B_TRANSITION_BLACKHOLE] = Task_Blackhole,
    [B_TRANSITION_BLACKHOLE_PULSATE] = Task_BlackholePulsate,
    [B_TRANSITION_RECTANGULAR_SPIRAL] = Task_RectangularSpiral,
    [B_TRANSITION_FRONTIER_LOGO_WIGGLE] = Task_FrontierLogoWiggle,
    [B_TRANSITION_FRONTIER_LOGO_WAVE] = Task_FrontierLogoWave,
    [B_TRANSITION_FRONTIER_SQUARES] = Task_FrontierSquares,
    [B_TRANSITION_FRONTIER_SQUARES_SCROLL] = Task_FrontierSquaresScroll,
    [B_TRANSITION_FRONTIER_SQUARES_SPIRAL] = Task_FrontierSquaresSpiral,
    [B_TRANSITION_FRONTIER_CIRCLES_MEET] = Task_FrontierCirclesMeet,
    [B_TRANSITION_FRONTIER_CIRCLES_CROSS] = Task_FrontierCirclesCross,
    [B_TRANSITION_FRONTIER_CIRCLES_ASYMMETRIC_SPIRAL] = Task_FrontierCirclesAsymmetricSpiral,
    [B_TRANSITION_FRONTIER_CIRCLES_SYMMETRIC_SPIRAL] = Task_FrontierCirclesSymmetricSpiral,
    [B_TRANSITION_FRONTIER_CIRCLES_MEET_IN_SEQ] = Task_FrontierCirclesMeetInSeq,
    [B_TRANSITION_FRONTIER_CIRCLES_CROSS_IN_SEQ] = Task_FrontierCirclesCrossInSeq,
    [B_TRANSITION_FRONTIER_CIRCLES_ASYMMETRIC_SPIRAL_IN_SEQ] = Task_FrontierCirclesAsymmetricSpiralInSeq,
    [B_TRANSITION_FRONTIER_CIRCLES_SYMMETRIC_SPIRAL_IN_SEQ] = Task_FrontierCirclesSymmetricSpiralInSeq,
    [B_TRANSITION_AURORA] = Task_Aurora, // Project Grounded
    [B_TRANSITION_REGIDRAGO] = Task_Regidrago, // Project Grounded
    [B_TRANSITION_REGIELEKI] = Task_Regieleki, // Project Grounded
    [B_TRANSITION_DEOXYS] = Task_Deoxys, // Project Grounded
    [B_TRANSITION_BIRCH] = Task_Birch, // Project Grounded
    [B_TRANSITION_AQUA_MAGMA] = Task_AquaMagma, // Project Grounded
    [B_TRANSITION_RAIKOU] = Task_Raikou, // Project Grounded
    [B_TRANSITION_ENTEI] = Task_Entei, // Project Grounded
    [B_TRANSITION_ROUTE_WAVE] = Task_RouteWave, // Project Grounded
    [B_TRANSITION_ROUTE_BEACH] = Task_RouteBeach, // Project Grounded
    [B_TRANSITION_ROUTE_BUBBLES] = Task_RouteBubbles, // Project Grounded
    [B_TRANSITION_ROUTE_SNOW] = Task_RouteSnow, // Project Grounded
    [B_TRANSITION_ROUTE_ASH] = Task_RouteAsh, // Project Grounded
    [B_TRANSITION_ROUTE_SAND] = Task_RouteSand, // Project Grounded
    [B_TRANSITION_ROUTE_HEAT] = Task_RouteHeat, // Project Grounded
    [B_TRANSITION_ROUTE_CYCLING] = Task_RouteCycling, // Project Grounded
    [B_TRANSITION_ROUTE_PYRE] = Task_RoutePyre, // Project Grounded
    [B_TRANSITION_ROUTE_SKY] = Task_RouteSky, // Project Grounded
    [B_TRANSITION_ROUTE_SHORT] = Task_RouteShort, // Project Grounded
    [B_TRANSITION_ROUTE_PAINT] = Task_RoutePaint, // Project Grounded
    [B_TRANSITION_ROUTE_SAFARI] = Task_RouteSafari, // Project Grounded
    [B_TRANSITION_ROUTE_METEOR] = Task_RouteMeteor, // Project Grounded
    [B_TRANSITION_ROUTE_JAGGED] = Task_RouteJagged, // Project Grounded
    [B_TRANSITION_ROUTE_RAINFOREST] = Task_RouteRainforest, // Project Grounded
    [B_TRANSITION_PIKACHU] = Task_Pikachu, // Project Grounded
    [B_TRANSITION_MAGIKARP] = Task_Magikarp, // Project Grounded
    [B_TRANSITION_VIAGRA_BOYS] = Task_ViagraBoys, // Project Grounded
    [B_TRANSITION_PSYDUCK] = Task_Psyduck, // Project Grounded
    [B_TRANSITION_KOFFING] = Task_Koffing, // Project Grounded
    [B_TRANSITION_GABBY_TY] = Task_GabbyTy, // Project Grounded
    [B_TRANSITION_POOCHYENA] = Task_Poochyena, // Project Grounded
    [B_TRANSITION_BEACHBALL] = Task_Beachball, // Project Grounded
    [B_TRANSITION_COLRESS] = Task_Colress, // Project Grounded
    [B_TRANSITION_ZANGOOSE] = Task_Zangoose, // Project Grounded
    [B_TRANSITION_SEVIPER] = Task_Seviper, // Project Grounded
    [B_TRANSITION_HEATRAN] = Task_Heatran, // Project Grounded
    [B_TRANSITION_SHAYMIN] = Task_Shaymin, // Project Grounded
    [B_TRANSITION_GENESECT] = Task_Genesect, // Project Grounded
    [B_TRANSITION_MEWTWO] = Task_Mewtwo, // Project Grounded
    [B_TRANSITION_GIRATINA] = Task_Giratina, // Project Grounded
    [B_TRANSITION_VICTINI] = Task_Victini, // Project Grounded
    [B_TRANSITION_JIRACHI] = Task_Jirachi, // Project Grounded
    [B_TRANSITION_DARKRAI] = Task_Darkrai, // Project Grounded
    [B_TRANSITION_NEO_PLASMA] = Task_NeoPlasma, // Project Grounded
    [B_TRANSITION_SICKBLIK] = Task_SickBlik, // Project Grounded
    [B_TRANSITION_ROCKET] = Task_Rocket, // Project Grounded
    [B_TRANSITION_ZARUDE] = Task_Zarude, // Project Grounded
    [B_TRANSITION_POISON_CHAIN] = Task_PoisonChain, // Project Grounded
    [B_TRANSITION_REGIGIGAS] = Task_Regigigas, // Project Grounded
    [B_TRANSITION_DAVE] = Task_Dave, // Project Grounded
    [B_TRANSITION_STEVEN] = Task_Steven, // Project Grounded
    [B_TRANSITION_WALLY_VHS] = Task_WallyVhs, // Project Grounded
    [B_TRANSITION_RAYQUAZA_PILLAR] = Task_RayquazaPillar, // Project Grounded
    [B_TRANSITION_MIMI] = Task_Mimi, // Project Grounded
    [B_TRANSITION_KECCLES] = Task_Keccles, // Project Grounded
    [B_TRANSITION_BURGLAR] = Task_Burglar, // Project Grounded
    [B_TRANSITION_GYM_ROXANNE] = Task_GymRoxanne, // Project Grounded
    [B_TRANSITION_GYM_BRAWLY] = Task_GymBrawly, // Project Grounded
    [B_TRANSITION_GYM_WATTSON] = Task_GymWattson, // Project Grounded
    [B_TRANSITION_GYM_FLANNERY] = Task_GymFlannery, // Project Grounded
    [B_TRANSITION_TAPU_KOKO] = Task_TapuKoko, // Project Grounded
    [B_TRANSITION_TAPU_LELE] = Task_TapuLele,
    [B_TRANSITION_TAPU_BULU] = Task_TapuBulu,
    [B_TRANSITION_TAPU_FINI] = Task_TapuFini,
    [B_TRANSITION_GYM_NORMAN] = Task_GymNorman, // Project Grounded
    [B_TRANSITION_GYM_WINONA] = Task_GymWinona, // Project Grounded
    [B_TRANSITION_GYM_TATE_LIZA] = Task_GymTateLiza, // Project Grounded
    [B_TRANSITION_GYM_WALLACE] = Task_GymWallace, // Project Grounded
    [B_TRANSITION_LUGIA] = Task_LegendLugia, // Project Grounded
    [B_TRANSITION_HO_OH] = Task_LegendHooh,
    [B_TRANSITION_VOLCANION] = Task_LegendVolcanion,
    [B_TRANSITION_HOOPA] = Task_LegendHoopa,
    [B_TRANSITION_FORCES] = Task_LegendForces,
    [B_TRANSITION_ARTICUNO] = Task_LegendArticuno, // Project Grounded (src/data/legend_intros2.h)
    [B_TRANSITION_ZAPDOS] = Task_LegendZapdos,
    [B_TRANSITION_MOLTRES] = Task_LegendMoltres,
    [B_TRANSITION_ZACIAN] = Task_LegendZacian,
    [B_TRANSITION_ZAMAZENTA] = Task_LegendZamazenta,
    [B_TRANSITION_XERNEAS] = Task_LegendXerneas,
    [B_TRANSITION_YVELTAL] = Task_LegendYveltal,
    [B_TRANSITION_WARIO] = Task_Wario, // Project Grounded (src/data/wario_intro.h)
    [B_TRANSITION_SHY_GUY] = Task_ShyGuy, // Project Grounded (src/data/shyguy_intro.h)
    [B_TRANSITION_DIALGA] = Task_LegendDialga, // Project Grounded (src/data/legend_intros_dp.h)
    [B_TRANSITION_PALKIA] = Task_LegendPalkia,
    [B_TRANSITION_ARCEUS] = Task_LegendArceus,
    [B_TRANSITION_MEW] = Task_LegendMew,
    [B_TRANSITION_KYOGRE_MURAL] = Task_KyogreMural, // Project Grounded
    [B_TRANSITION_GROUDON_MURAL] = Task_GroudonMural, // Project Grounded
    [B_TRANSITION_OGERPON] = Task_Ogerpon, // Project Grounded
    [B_TRANSITION_WEATHER_SERVICE] = Task_WeatherService, // Project Grounded
    [B_TRANSITION_BOO] = Task_Boo, // Project Grounded (src/data/boo_intro.h)
    [B_TRANSITION_LEGEND_CROWN] = Task_LegendCrown, // Project Grounded (src/data/legend_intros_cheap2.h)
    [B_TRANSITION_LEGEND_CELEBI] = Task_LegendCelebi,
    [B_TRANSITION_LEGEND_LAKE] = Task_LegendLake,
    [B_TRANSITION_LEGEND_MELOETTA] = Task_LegendMeloetta,
    [B_TRANSITION_LEGEND_ZERAORA] = Task_LegendZeraora,
    [B_TRANSITION_LEGEND_ZYGARDE] = Task_LegendZygarde,
    [B_TRANSITION_LEGEND_EON] = Task_LegendEon,
    [B_TRANSITION_LEGEND_CRESSELIA] = Task_LegendCresselia,
    [B_TRANSITION_LEGEND_NECROZMA] = Task_LegendNecrozma,
    [B_TRANSITION_LEGEND_GALAR_ZAPDOS] = Task_LegendGalarZapdos,
    [B_TRANSITION_LEGEND_GALAR_MOLTRES] = Task_LegendGalarMoltres,
    [B_TRANSITION_SWORDS_SLASH] = Task_LegendSwords, // Project Grounded (src/data/legend_intros_cheap1.h)
    [B_TRANSITION_ULTRA_BEAST] = Task_LegendUltraBeast,
    [B_TRANSITION_PARADOX_PAST] = Task_LegendParadoxPast,
    [B_TRANSITION_PARADOX_FUTURE] = Task_LegendParadoxFuture,
    [B_TRANSITION_ETERNATUS] = Task_LegendEternatus,
    [B_TRANSITION_MARSHADOW] = Task_LegendMarshadow,
    [B_TRANSITION_TERAPAGOS] = Task_LegendTerapagos,
    [B_TRANSITION_PECHARUNT] = Task_LegendPecharunt,
    [B_TRANSITION_RIVAL_INTRO] = Task_RivalIntro, // Project Grounded (src/data/rival_intros.h)
    [B_TRANSITION_CLASS_INTRO] = Task_ClassIntro, // Project Grounded (src/data/class_intros.h)
};

static const TransitionStateFunc sTaskHandlers[] =
{
    &Transition_StartIntro,
    &Transition_WaitForIntro,
    &Transition_StartMain,
    &Transition_WaitForMain
};

static const TransitionStateFunc sBlur_Funcs[] =
{
    Blur_Init,
    Blur_Main,
    Blur_End
};

static const TransitionStateFunc sSwirl_Funcs[] =
{
    Swirl_Init,
    Swirl_End,
};

static const TransitionStateFunc sShuffle_Funcs[] =
{
    Shuffle_Init,
    Shuffle_End,
};

static const TransitionStateFunc sAqua_Funcs[] =
{
    Aqua_Init,
    Aqua_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    FramesCountdown,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sMagma_Funcs[] =
{
    Magma_Init,
    Magma_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    FramesCountdown,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sBigPokeball_Funcs[] =
{
    BigPokeball_Init,
    BigPokeball_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sRegice_Funcs[] =
{
    Regi_Init,
    Regice_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

// Project Grounded: Aqua- en Magma-logo naast elkaar (Archie + Maxie, Sootopolis)
static const TransitionStateFunc sAquaMagma_Funcs[] =
{
    AquaMagma_Init,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    FramesCountdown,
    PatternWeave_CircularMask
};

// Project Grounded: Regidrago en Regieleki (eigen stippatroon, zelfde weef-effect)
static const TransitionStateFunc sRegidrago_Funcs[] =
{
    Regidrago_Init,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sRegieleki_Funcs[] =
{
    Regieleki_Init,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sRegigigas_Funcs[] =
{
    Regigigas_Init,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sRegisteel_Funcs[] =
{
    Regi_Init,
    Registeel_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sRegirock_Funcs[] =
{
    Regi_Init,
    Regirock_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sKyogre_Funcs[] =
{
    WeatherTrio_BgFadeBlack,
    WeatherTrio_WaitFade,
    Kyogre_Init,
    Kyogre_PaletteFlash,
    Kyogre_PaletteBrighten,
    FramesCountdown,
    WeatherDuo_FadeOut,
    WeatherDuo_End
};

static const TransitionStateFunc sPokeballsTrail_Funcs[] =
{
    PokeballsTrail_Init,
    PokeballsTrail_Main,
    PokeballsTrail_End
};

#define NUM_POKEBALL_TRAILS 5
static const s16 sPokeballsTrail_StartXCoords[2] = { -16, DISPLAY_WIDTH + 16 };
static const s16 sPokeballsTrail_Delays[NUM_POKEBALL_TRAILS] = {0, 32, 64, 18, 48};
static const s16 sPokeballsTrail_Speeds[2] = {8, -8};

static const TransitionStateFunc sClockwiseWipe_Funcs[] =
{
    ClockwiseWipe_Init,
    ClockwiseWipe_TopRight,
    ClockwiseWipe_Right,
    ClockwiseWipe_Bottom,
    ClockwiseWipe_Left,
    ClockwiseWipe_TopLeft,
    ClockwiseWipe_End
};

static const TransitionStateFunc sRipple_Funcs[] =
{
    Ripple_Init,
    Ripple_Main
};

static const TransitionStateFunc sWave_Funcs[] =
{
    Wave_Init,
    Wave_Main,
    Wave_End
};

static const TransitionStateFunc sMugshot_Funcs[] =
{
    Mugshot_Init,
    Mugshot_SetGfx,
    Mugshot_ShowBanner,
    Mugshot_StartOpponentSlide,
    Mugshot_WaitStartPlayerSlide,
    Mugshot_WaitPlayerSlide,
    Mugshot_GradualWhiteFade,
    Mugshot_InitFadeWhiteToBlack,
    Mugshot_FadeToBlack,
    Mugshot_End
};

static const TransitionSpriteCallback sMugshotTrainerPicFuncs[] =
{
    MugshotTrainerPic_Pause,
    MugshotTrainerPic_Init,
    MugshotTrainerPic_Slide,
    MugshotTrainerPic_SlideSlow,
    MugshotTrainerPic_Pause,
    MugshotTrainerPic_SlideOffscreen,
    MugshotTrainerPic_Pause
};

static const TransitionSpriteCallbackPartner sMugshotTrainerPicFuncsPartner[] =
{
    MugshotTrainerPic_Pause,
    MugshotTrainerPic_Init,
    MugshotTrainerPic_SlidePartner,
    MugshotTrainerPic_SlideSlow,
    MugshotTrainerPic_Pause,
    MugshotTrainerPic_SlideOffscreen,
    MugshotTrainerPic_Pause
};

// One element per slide direction.
// Sign of acceleration is opposite speed, so slide decelerates.
static const s16 sTrainerPicSlideSpeeds[2] = {12, -12};
static const s16 sTrainerPicSlideAccels[2] = {-1,   1};

static const TransitionStateFunc sSlice_Funcs[] =
{
    Slice_Init,
    Slice_Main,
    Slice_End
};

static const TransitionStateFunc sShredSplit_Funcs[] =
{
    ShredSplit_Init,
    ShredSplit_Main,
    ShredSplit_End
};

static const u8 sShredSplit_SectionYCoords[] = {39, DISPLAY_HEIGHT - 41};
static const s16 sShredSplit_SectionMoveDirs[] = {1, -1};

static const TransitionStateFunc sBlackhole_Funcs[] =
{
    Blackhole_Init,
    Blackhole_Vibrate,
    Blackhole_GrowEnd
};

static const TransitionStateFunc sBlackholePulsate_Funcs[] =
{
    Blackhole_Init,
    BlackholePulsate_Main
};

// Blackhole rapidly alternates adding these values to the radius,
// resulting in a vibrating shrink/grow effect.
static const s16 sBlackhole_Vibrations[] = {-6, 4};

static const TransitionStateFunc sRectangularSpiral_Funcs[] =
{
    RectangularSpiral_Init,
    RectangularSpiral_Main,
    RectangularSpiral_End
};

#define SPIRAL_END (-1)
#define SPIRAL_REBOUND (-2)

// Note that the directions are inverted for the lines originating at the bottom.
// i.e. MOVE_RIGHT is a right move for the top lines and a left move for the inverted bottom lines.
enum {
    MOVE_RIGHT = 1,
    MOVE_LEFT,
    MOVE_UP,
    MOVE_DOWN,
};

// Offsets of the movement data for spiraling in either direction.
#define SPIRAL_INWARD_START  0
#define SPIRAL_INWARD_END    3
#define SPIRAL_OUTWARD_START 4
#define SPIRAL_OUTWARD_END   7

static const s16 sRectangularSpiral_Major_InwardRight[]  = {MOVE_RIGHT,  27, 275, SPIRAL_END};
static const s16 sRectangularSpiral_Major_InwardLeft[]   = {MOVE_LEFT,  486, SPIRAL_END};
static const s16 sRectangularSpiral_Major_InwardUp[]     = {MOVE_UP,    262, SPIRAL_END};
static const s16 sRectangularSpiral_Major_InwardDown[]   = {MOVE_DOWN,  507, SPIRAL_REBOUND};

static const s16 sRectangularSpiral_Minor_InwardRight[]  = {MOVE_RIGHT, 213, SPIRAL_END};
static const s16 sRectangularSpiral_Minor_InwardLeft[]   = {MOVE_LEFT,  548, SPIRAL_REBOUND};
static const s16 sRectangularSpiral_Minor_InwardUp[]     = {MOVE_UP,    196, SPIRAL_END};
static const s16 sRectangularSpiral_Minor_InwardDown[]   = {MOVE_DOWN,  573, 309, SPIRAL_END};

static const s16 sRectangularSpiral_Minor_OutwardRight[] = {MOVE_RIGHT, 474, SPIRAL_END};
static const s16 sRectangularSpiral_Minor_OutwardLeft[]  = {MOVE_LEFT,  295, 32, SPIRAL_END};
static const s16 sRectangularSpiral_Minor_OutwardUp[]    = {MOVE_UP,     58, SPIRAL_END};
static const s16 sRectangularSpiral_Minor_OutwardDown[]  = {MOVE_DOWN,  455, SPIRAL_END};

static const s16 sRectangularSpiral_Major_OutwardRight[] = {MOVE_RIGHT, 540, SPIRAL_END};
static const s16 sRectangularSpiral_Major_OutwardLeft[]  = {MOVE_LEFT,  229, SPIRAL_END};
static const s16 sRectangularSpiral_Major_OutwardUp[]    = {MOVE_UP,    244, 28, SPIRAL_END};
static const s16 sRectangularSpiral_Major_OutwardDown[]  = {MOVE_DOWN,  517, SPIRAL_END};

// Move data for spiral lines starting in the top left / bottom right
static const s16 *const sRectangularSpiral_MoveDataTable_MajorDiagonal[] =
{
    [SPIRAL_INWARD_START] =
    sRectangularSpiral_Major_InwardRight,
    sRectangularSpiral_Major_InwardDown,
    sRectangularSpiral_Major_InwardLeft,
    sRectangularSpiral_Major_InwardUp,

    [SPIRAL_OUTWARD_START] =
    sRectangularSpiral_Major_OutwardUp,
    sRectangularSpiral_Major_OutwardLeft,
    sRectangularSpiral_Major_OutwardDown,
    sRectangularSpiral_Major_OutwardRight
};

// Move data for spiral lines starting in the top right / bottom left
static const s16 *const sRectangularSpiral_MoveDataTable_MinorDiagonal[] =
{
    [SPIRAL_INWARD_START] =
    sRectangularSpiral_Minor_InwardDown,
    sRectangularSpiral_Minor_InwardLeft,
    sRectangularSpiral_Minor_InwardUp,
    sRectangularSpiral_Minor_InwardRight,

    [SPIRAL_OUTWARD_START] =
    sRectangularSpiral_Minor_OutwardLeft,
    sRectangularSpiral_Minor_OutwardDown,
    sRectangularSpiral_Minor_OutwardRight,
    sRectangularSpiral_Minor_OutwardUp
};

static const s16 *const *const sRectangularSpiral_MoveDataTables[] =
{
    sRectangularSpiral_MoveDataTable_MajorDiagonal,
    sRectangularSpiral_MoveDataTable_MinorDiagonal
};

static const TransitionStateFunc sGroudon_Funcs[] =
{
    WeatherTrio_BgFadeBlack,
    WeatherTrio_WaitFade,
    Groudon_Init,
    Groudon_PaletteFlash,
    Groudon_PaletteBrighten,
    FramesCountdown,
    WeatherDuo_FadeOut,
    WeatherDuo_End
};

static const TransitionStateFunc sRayquaza_Funcs[] =
{
    WeatherTrio_BgFadeBlack,
    WeatherTrio_WaitFade,
    Rayquaza_Init,
    Rayquaza_SetGfx,
    Rayquaza_PaletteFlash,
    Rayquaza_FadeToBlack,
    Rayquaza_WaitFade,
    Rayquaza_SetBlack,
    Rayquaza_TriRing,
    Blackhole_Vibrate,
    Blackhole_GrowEnd
};

static const TransitionStateFunc sWhiteBarsFade_Funcs[] =
{
    WhiteBarsFade_Init,
    WhiteBarsFade_StartBars,
    WhiteBarsFade_WaitBars,
    WhiteBarsFade_BlendToBlack,
    WhiteBarsFade_End
};

#define NUM_WHITE_BARS 8
static const s16 sWhiteBarsFade_StartDelays[NUM_WHITE_BARS] = {0, 20, 15, 40, 10, 25, 35, 5};

static const TransitionStateFunc sGridSquares_Funcs[] =
{
    GridSquares_Init,
    GridSquares_Main,
    GridSquares_End
};

static const TransitionStateFunc sAngledWipes_Funcs[] =
{
    AngledWipes_Init,
    AngledWipes_SetWipeData,
    AngledWipes_DoWipe,
    AngledWipes_TryEnd,
    AngledWipes_StartNext
};

#define NUM_ANGLED_WIPES 7

static const s16 sAngledWipes_MoveData[NUM_ANGLED_WIPES][5] =
{
// startX          startY          endX            endY            yDirection
    {56,            0,              0,              DISPLAY_HEIGHT, 0},
    {104,           DISPLAY_HEIGHT, DISPLAY_WIDTH,  88,             1},
    {DISPLAY_WIDTH, 72,             56,             0,              1},
    {0,             32,             144,            DISPLAY_HEIGHT, 0},
    {144,           DISPLAY_HEIGHT, 184,            0,              1},
    {56,            0,              168,            DISPLAY_HEIGHT, 0},
    {168,           DISPLAY_HEIGHT, 48,             0,              1},
};

static const s16 sAngledWipes_EndDelays[NUM_ANGLED_WIPES] = {8, 4, 2, 1, 1, 1, 0};

static const TransitionStateFunc sTransitionIntroFuncs[] =
{
    TransitionIntro_FadeToGray,
    TransitionIntro_FadeFromGray
};

static const struct SpriteFrameImage sSpriteImage_Pokeball[] =
{
    {sPokeball_Gfx, sizeof(sPokeball_Gfx)}
};

static const union AnimCmd sSpriteAnim_Pokeball[] =
{
    ANIMCMD_FRAME(0, 1),
    ANIMCMD_END
};

static const union AnimCmd *const sSpriteAnimTable_Pokeball[] =
{
    sSpriteAnim_Pokeball
};

static const union AffineAnimCmd sSpriteAffineAnim_Pokeball1[] =
{
    AFFINEANIMCMD_FRAME(0, 0, -4, 1),
    AFFINEANIMCMD_JUMP(0)
};

static const union AffineAnimCmd sSpriteAffineAnim_Pokeball2[] =
{
    AFFINEANIMCMD_FRAME(0, 0, 4, 1),
    AFFINEANIMCMD_JUMP(0)
};

static const union AffineAnimCmd *const sSpriteAffineAnimTable_Pokeball[] =
{
    sSpriteAffineAnim_Pokeball1,
    sSpriteAffineAnim_Pokeball2
};

static const struct SpriteTemplate sSpriteTemplate_Pokeball =
{
    .tileTag = TAG_NONE,
    .paletteTag = FLDEFF_PAL_TAG_POKEBALL_TRAIL,
    .oam = &gObjectEventBaseOam_32x32,
    .anims = sSpriteAnimTable_Pokeball,
    .images = sSpriteImage_Pokeball,
    .affineAnims = sSpriteAffineAnimTable_Pokeball,
    .callback = SpriteCB_FldEffPokeballTrail
};

static const struct OamData sOam_UnusedBrendanLass =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(64x64),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(64x64),
    .tileNum = 0,
    .priority = 0,
    .paletteNum = 0,
    .affineParam = 0,
};

static const struct SpriteFrameImage sImageTable_UnusedBrendan[] =
{
    {sUnusedBrendan_Gfx, sizeof(sUnusedBrendan_Gfx)}
};

static const struct SpriteFrameImage sImageTable_UnusedLass[] =
{
    {sUnusedLass_Gfx, sizeof(sUnusedLass_Gfx)}
};

static const union AnimCmd sSpriteAnim_UnusedBrendanLass[] =
{
    ANIMCMD_FRAME(0, 1),
    ANIMCMD_END
};

static const union AnimCmd *const sSpriteAnimTable_UnusedBrendanLass[] =
{
    sSpriteAnim_UnusedBrendanLass
};

static const struct SpriteTemplate sSpriteTemplate_UnusedBrendan =
{
    .tileTag = TAG_NONE,
    .paletteTag = PALTAG_UNUSED_MUGSHOT,
    .oam = &sOam_UnusedBrendanLass,
    .anims = sSpriteAnimTable_UnusedBrendanLass,
    .images = sImageTable_UnusedBrendan,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_MugshotTrainerPic
};

static const struct SpriteTemplate sSpriteTemplate_UnusedLass =
{
    .tileTag = TAG_NONE,
    .paletteTag = PALTAG_UNUSED_MUGSHOT,
    .oam = &sOam_UnusedBrendanLass,
    .anims = sSpriteAnimTable_UnusedBrendanLass,
    .images = sImageTable_UnusedLass,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_MugshotTrainerPic
};

static const u16 sFieldEffectPal_Pokeball[] = INCBIN_U16("graphics/field_effects/palettes/pokeball.gbapal");

const struct SpritePalette gSpritePalette_Pokeball = {sFieldEffectPal_Pokeball, FLDEFF_PAL_TAG_POKEBALL_TRAIL};

static const u16 sMugshotPal_Purple[] = INCBIN_U16("graphics/battle_transitions/purple_bg.gbapal");
static const u16 sMugshotPal_Green[]  = INCBIN_U16("graphics/battle_transitions/green_bg.gbapal");
static const u16 sMugshotPal_Pink[]   = INCBIN_U16("graphics/battle_transitions/pink_bg.gbapal");
static const u16 sMugshotPal_Blue[]   = INCBIN_U16("graphics/battle_transitions/blue_bg.gbapal");
static const u16 sMugshotPal_Yellow[] = INCBIN_U16("graphics/battle_transitions/yellow_bg.gbapal");
static const u16 sMugshotPal_Brendan[] = INCBIN_U16("graphics/battle_transitions/brendan_bg.gbapal");
static const u16 sMugshotPal_May[] = INCBIN_U16("graphics/battle_transitions/may_bg.gbapal");

static const u16 *const sOpponentMugshotsPals[MUGSHOT_COLOR_COUNT] =
{
    [MUGSHOT_COLOR_PURPLE] = sMugshotPal_Purple,
    [MUGSHOT_COLOR_GREEN]  = sMugshotPal_Green,
    [MUGSHOT_COLOR_PINK]   = sMugshotPal_Pink,
    [MUGSHOT_COLOR_BLUE]   = sMugshotPal_Blue,
    [MUGSHOT_COLOR_YELLOW] = sMugshotPal_Yellow
};

static const u16 *const sPlayerMugshotsPals[GENDER_COUNT] =
{
    [MALE] = sMugshotPal_Brendan,
    [FEMALE] = sMugshotPal_May
};

static const u16 sUnusedTrainerPalette[] = INCBIN_U16("graphics/battle_transitions/unused_trainer.gbapal");
static const struct SpritePalette sSpritePalette_UnusedTrainer = {sUnusedTrainerPalette, PALTAG_UNUSED_MUGSHOT};

static const u16 sBigPokeball_Tilemap[] = INCBIN_U16("graphics/battle_transitions/big_pokeball_map.bin");
static const u16 sMugshotsTilemap[] = INCBIN_U16("graphics/battle_transitions/elite_four_bg_map.bin");

static const TransitionStateFunc sFrontierLogoWiggle_Funcs[] =
{
    FrontierLogoWiggle_Init,
    FrontierLogoWiggle_SetGfx,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static const TransitionStateFunc sFrontierLogoWave_Funcs[] =
{
    FrontierLogoWave_Init,
    FrontierLogoWave_SetGfx,
    FrontierLogoWave_InitScanline,
    FrontierLogoWave_Main
};

static const TransitionStateFunc sFrontierSquares_Funcs[] =
{
    FrontierSquares_Init,
    FrontierSquares_Draw,
    FrontierSquares_Shrink,
    FrontierSquares_End
};

static const TransitionStateFunc sFrontierSquaresSpiral_Funcs[] =
{
    FrontierSquaresSpiral_Init,
    FrontierSquaresSpiral_Outward,
    FrontierSquaresSpiral_SetBlack,
    FrontierSquaresSpiral_Inward,
    FrontierSquares_End
};

static const TransitionStateFunc sFrontierSquaresScroll_Funcs[] =
{
    FrontierSquaresScroll_Init,
    FrontierSquaresScroll_Draw,
    FrontierSquaresScroll_SetBlack,
    FrontierSquaresScroll_Erase,
    FrontierSquaresScroll_End
};

#define SQUARE_SIZE 4
#define MARGIN_SIZE 1 // Squares do not fit evenly across the width, so there is a margin on either side.
#define NUM_SQUARES_PER_ROW ((DISPLAY_WIDTH - (MARGIN_SIZE * 8 * 2)) / (SQUARE_SIZE * 8))
#define NUM_SQUARES_PER_COL (DISPLAY_HEIGHT / (SQUARE_SIZE * 8))
#define NUM_SQUARES         (NUM_SQUARES_PER_ROW * NUM_SQUARES_PER_COL)

// The order in which the squares should appear/disappear to create
// the spiral effect. Spiraling inward starts with the first element,
// and spiraling outward starts with the last. The positions are the
// squares numbered left-to-right top-to-bottom.
static const u8 sFrontierSquaresSpiral_Positions[NUM_SQUARES] = {
    28, 29, 30, 31, 32, 33, 34,
    27, 20, 13,  6,  5,  4,  3,
     2,  1,  0,  7, 14, 21, 22,
    23, 24, 25, 26, 19, 12, 11,
    10,  9,  8, 15, 16, 17, 18
};

// In the scrolling version the squares appear/disappear in a "random" order
// dictated by the list below.
static const u8 sFrontierSquaresScroll_Positions[] = {
     0, 16, 41, 22, 44,  2, 43, 21,
    46, 27,  9, 48, 38,  5, 57, 59,
    12, 63, 35, 28, 10, 53,  7, 49,
    39, 23, 55,  1, 62, 17, 61, 30,
     6, 34, 15, 51, 32, 58, 13, 45,
    37, 52, 11, 24, 60, 19, 56, 33,
    29, 50, 40, 54, 14,  3, 47, 20,
    18, 25,  4, 36, 26, 42, 31,  8
};

//---------------------------
// Main transition functions
//---------------------------

static void CB2_TestBattleTransition(void)
{
    switch (sTestingTransitionState)
    {
    case 0:
        LaunchBattleTransitionTask(sTestingTransitionId);
        sTestingTransitionState++;
        break;
    case 1:
        if (IsBattleTransitionDone())
        {
            sTestingTransitionState = 0;
            SetMainCallback2(CB2_ReturnToField);
        }
        break;
    }

    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

static void UNUSED TestBattleTransition(u8 transitionId)
{
    sTestingTransitionId = transitionId;
    SetMainCallback2(CB2_TestBattleTransition);
}

void BattleTransition_StartOnField(u8 transitionId)
{
    gMain.callback2 = CB2_OverworldBasic;
    LaunchBattleTransitionTask(transitionId);
}

void BattleTransition_Start(u8 transitionId)
{
    LaunchBattleTransitionTask(transitionId);
}

// main task that launches sub-tasks for phase1 and phase2
#define tTransitionId   data[1]
#define tTransitionDone data[15]

bool8 IsBattleTransitionDone(void)
{
    u8 taskId = FindTaskIdByFunc(Task_BattleTransition);
    if (gTasks[taskId].tTransitionDone)
    {
        DestroyTask(taskId);
        FREE_AND_SET_NULL(sTransitionData);
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}

static void LaunchBattleTransitionTask(u8 transitionId)
{
    u8 taskId = CreateTask(Task_BattleTransition, 2);
    gTasks[taskId].tTransitionId = transitionId;
    // Project Grounded: startmoment (VBlanks) bewaren, zodat een transitie op de muziek kan eindigen (Tapu's)
    gTasks[taskId].data[13] = gMain.vblankCounter1;
    gTasks[taskId].data[14] = gMain.vblankCounter1 >> 16;
    sTransitionData = AllocZeroed(sizeof(*sTransitionData));
}

static void Task_BattleTransition(u8 taskId)
{
    while (sTaskHandlers[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Transition_StartIntro(struct Task *task)
{
    SetWeatherScreenFadeOut();
    // cause all shadow sprites to destroy themselves,
    // freeing up sprite slots for the transition
    gWeatherPtr->noShadows = TRUE;
    CpuCopy32(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
    if (sTasks_Intro[task->tTransitionId] != NULL)
    {
        CreateTask(sTasks_Intro[task->tTransitionId], 4);
        task->tState++;
        return FALSE;
    }
    else
    {
        task->tState = 2;
        return TRUE;
    }
}

static bool8 Transition_WaitForIntro(struct Task *task)
{
    if (FindTaskIdByFunc(sTasks_Intro[task->tTransitionId]) == TASK_NONE)
    {
        task->tState++;
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}

static bool8 Transition_StartMain(struct Task *task)
{
    CreateTask(sTasks_Main[task->tTransitionId], 0);
    task->tState++;
    return FALSE;
}

static bool8 Transition_WaitForMain(struct Task *task)
{
    task->tTransitionDone = FALSE;
    if (FindTaskIdByFunc(sTasks_Main[task->tTransitionId]) == TASK_NONE)
        task->tTransitionDone = TRUE;
    return FALSE;
}

#undef tTransitionId
#undef tTransitionDone

static void Task_Intro(u8 taskId)
{
    if (gTasks[taskId].tState == 0)
    {
        gTasks[taskId].tState++;
        CreateIntroTask(0, 0, 2, 4, 4); // Project Grounded: 2 snellere flitsen i.p.v. 3 (was 0, 0, 3, 2, 2)
    }
    else if (IsIntroTaskDone())
    {
        DestroyTask(taskId);
    }
}

//--------------------
// B_TRANSITION_BLUR
//--------------------

#define tDelay   data[1]
#define tCounter data[2]

static void Task_Blur(u8 taskId)
{
    while (sBlur_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Blur_Init(struct Task *task)
{
    SetGpuReg(REG_OFFSET_MOSAIC, 0);
    SetGpuRegBits(REG_OFFSET_BG1CNT, BGCNT_MOSAIC);
    SetGpuRegBits(REG_OFFSET_BG2CNT, BGCNT_MOSAIC);
    SetGpuRegBits(REG_OFFSET_BG3CNT, BGCNT_MOSAIC);
    task->tState++;
    return TRUE;
}

static bool8 Blur_Main(struct Task *task)
{
    if (task->tDelay != 0)
    {
        task->tDelay--;
    }
    else
    {
        task->tDelay = 4;
        if (++task->tCounter == 10)
            BeginNormalPaletteFade(PALETTES_ALL, -1, 0, 16, RGB_BLACK);
        SetGpuReg(REG_OFFSET_MOSAIC, (task->tCounter & 15) * 17);
        if (task->tCounter > 14)
            task->tState++;
    }
    return FALSE;
}

static bool8 Blur_End(struct Task *task)
{
    if (!gPaletteFade.active)
    {
        u8 taskId = FindTaskIdByFunc(Task_Blur);
        DestroyTask(taskId);
    }
    return FALSE;
}

#undef tDelay
#undef tCounter

//--------------------
// B_TRANSITION_SWIRL
//--------------------

#define tSinIndex  data[1]
#define tAmplitude data[2]

static void Task_Swirl(u8 taskId)
{
    while (sSwirl_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Swirl_Init(struct Task *task)
{
    InitTransitionData();
    ScanlineEffect_Clear();
    BeginNormalPaletteFade(PALETTES_ALL, 4, 0, 16, RGB_BLACK);
    SetSinWave((s16*)gScanlineEffectRegBuffers[1], sTransitionData->cameraX, 0, 2, 0, DISPLAY_HEIGHT);

    SetVBlankCallback(VBlankCB_Swirl);
    SetHBlankCallback(HBlankCB_Swirl);

    EnableInterrupts(INTR_FLAG_VBLANK | INTR_FLAG_HBLANK);

    task->tState++;
    return FALSE;
}

static bool8 Swirl_End(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    task->tSinIndex += 4;
    task->tAmplitude += 8;

    SetSinWave((s16*)gScanlineEffectRegBuffers[0], sTransitionData->cameraX, task->tSinIndex, 2, task->tAmplitude, DISPLAY_HEIGHT);

    if (!gPaletteFade.active)
    {
        u8 taskId = FindTaskIdByFunc(Task_Swirl);
        DestroyTask(taskId);
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static void VBlankCB_Swirl(void)
{
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
}

static void HBlankCB_Swirl(void)
{
    u16 var = gScanlineEffectRegBuffers[1][REG_VCOUNT];
    REG_BG1HOFS = var;
    REG_BG2HOFS = var;
    REG_BG3HOFS = var;
}

#undef tSinIndex
#undef tAmplitude

//----------------------
// B_TRANSITION_SHUFFLE
//----------------------

#define tSinVal    data[1]
#define tAmplitude data[2]

static void Task_Shuffle(u8 taskId)
{
    while (sShuffle_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Shuffle_Init(struct Task *task)
{
    InitTransitionData();
    ScanlineEffect_Clear();

    BeginNormalPaletteFade(PALETTES_ALL, 4, 0, 16, RGB_BLACK);
    memset(gScanlineEffectRegBuffers[1], sTransitionData->cameraY, DISPLAY_HEIGHT * 2);

    SetVBlankCallback(VBlankCB_Shuffle);
    SetHBlankCallback(HBlankCB_Shuffle);

    EnableInterrupts(INTR_FLAG_VBLANK | INTR_FLAG_HBLANK);

    task->tState++;
    return FALSE;
}

static bool8 Shuffle_End(struct Task *task)
{
    u8 i;
    u16 amplitude, sinVal;

    sTransitionData->VBlank_DMA = FALSE;
    sinVal = task->tSinVal;
    amplitude = task->tAmplitude >> 8;
    task->tSinVal += 4224;
    task->tAmplitude += 384;

    for (i = 0; i < DISPLAY_HEIGHT; i++, sinVal += 4224)
    {
        u16 sinIndex = sinVal / 256;
        gScanlineEffectRegBuffers[0][i] = sTransitionData->cameraY + Sin(sinIndex, amplitude);
    }

    if (!gPaletteFade.active)
        DestroyTask(FindTaskIdByFunc(Task_Shuffle));

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static void VBlankCB_Shuffle(void)
{
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
}

static void HBlankCB_Shuffle(void)
{
    u16 var = gScanlineEffectRegBuffers[1][REG_VCOUNT];
    REG_BG1VOFS = var;
    REG_BG2VOFS = var;
    REG_BG3VOFS = var;
}

#undef tSinVal
#undef tAmplitude

//------------------------------------------------------------------------
// B_TRANSITION_BIG_POKEBALL, B_TRANSITION_AQUA, B_TRANSITION_MAGMA,
// B_TRANSITION_REGICE, B_TRANSITION_REGISTEEL, B_TRANSITION_REGIROCK
// and B_TRANSITION_KYOGRE.
//
// With the exception of B_TRANSITION_KYOGRE, all of the above transitions
// use the same weave effect (see the PatternWeave functions).
// Unclear why Kyogre's was grouped here and not with Groudon/Rayquaza's.
//------------------------------------------------------------------------

#define tBlendTarget1 data[1]
#define tBlendTarget2 data[2]
#define tBlendDelay   data[3]

// Data 1-3 change purpose for PatternWeave_CircularMask
#define tRadius      data[1]
#define tRadiusDelta data[2]
#define tVBlankSet   data[3]

#define tSinIndex     data[4]
#define tAmplitude    data[5]
#define tEndDelay     data[8]

static void Task_BigPokeball(u8 taskId)
{
    while (sBigPokeball_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Aqua(u8 taskId)
{
    while (sAqua_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Magma(u8 taskId)
{
    while (sMagma_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Regice(u8 taskId)
{
    while (sRegice_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Registeel(u8 taskId)
{
    while (sRegisteel_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Regirock(u8 taskId)
{
    while (sRegirock_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_AquaMagma(u8 taskId)
{
    while (sAquaMagma_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Regidrago(u8 taskId)
{
    while (sRegidrago_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Regieleki(u8 taskId)
{
    while (sRegieleki_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Regigigas(u8 taskId)
{
    while (sRegigigas_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_Kyogre(u8 taskId)
{
    while (sKyogre_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void InitPatternWeaveTransition(struct Task *task)
{
    s32 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    task->tBlendTarget1 = 16;
    task->tBlendTarget2 = 0;
    task->tSinIndex = 0;
    task->tAmplitude = 0x4000;
    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = 0;
    sTransitionData->WIN0H = DISPLAY_WIDTH;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;
    sTransitionData->BLDCNT = BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_ALL;
    sTransitionData->BLDALPHA = BLDALPHA_BLEND(task->tBlendTarget2, task->tBlendTarget1);
    UpdateShadowColor(RGB_GRAY);

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = DISPLAY_WIDTH;

    SetVBlankCallback(VBlankCB_PatternWeave);
}

static bool8 Aqua_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    task->tEndDelay = 60;
    InitPatternWeaveTransition(task);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sTeamAqua_Tileset, tileset);
    LoadPalette(sEvilTeam_Palette, BG_PLTT_ID(15), sizeof(sEvilTeam_Palette));

    task->tState++;
    return FALSE;
}

static bool8 Magma_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    task->tEndDelay = 60;
    InitPatternWeaveTransition(task);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sTeamMagma_Tileset, tileset);
    LoadPalette(sEvilTeam_Palette, BG_PLTT_ID(15), sizeof(sEvilTeam_Palette));

    task->tState++;
    return FALSE;
}

static bool8 Regi_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    task->tEndDelay = 60;
    InitPatternWeaveTransition(task);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    CpuCopy16(sRegis_Tileset, tileset, 0x2000);

    task->tState++;
    return FALSE;
}

static void NewRegi_SetGfx(struct Task *task, const void *tileset_, u32 tilesetSize, const u16 *tilemap_, const u16 *palette)
{
    u16 *tilemap, *tileset;

    task->tEndDelay = 60;
    InitPatternWeaveTransition(task);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    if (tilesetSize == RT_SMOL)
        DecompressDataWithHeaderVram(tileset_, tileset);
    else
        CpuCopy16(tileset_, tileset, tilesetSize);
    LoadPalette(palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    CpuCopy16(tilemap_, tilemap, 0x500);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);
    task->tState++;
}

static bool8 AquaMagma_Init(struct Task *task)
{
    NewRegi_SetGfx(task, sAquaMagma_Tileset, RT_SMOL, sAquaMagma_Tilemap, sEvilTeam_Palette);
    return FALSE;
}

static bool8 Regidrago_Init(struct Task *task)
{
    NewRegi_SetGfx(task, sRegidrago_Tileset, RT_SMOL, sRegidrago_Tilemap, sRegidrago_Palette);
    return FALSE;
}

static bool8 Regieleki_Init(struct Task *task)
{
    NewRegi_SetGfx(task, sRegieleki_Tileset, RT_SMOL, sRegieleki_Tilemap, sRegieleki_Palette);
    return FALSE;
}

static bool8 Regigigas_Init(struct Task *task)
{
    NewRegi_SetGfx(task, sRegigigas_Tileset, RT_SMOL, sRegigigas_Tilemap, sRegigigas_Palette);
    return FALSE;
}

static bool8 BigPokeball_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    InitPatternWeaveTransition(task);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    CpuCopy16(sBigPokeball_Tileset, tileset, sizeof(sBigPokeball_Tileset));
    LoadPalette(sFieldEffectPal_Pokeball, BG_PLTT_ID(15), sizeof(sFieldEffectPal_Pokeball));

    task->tState++;
    return FALSE;
}

static bool8 BigPokeball_SetGfx(struct Task *task)
{
    s16 i, j;
    u16 *tilemap, *tileset;
    const u16 *bigPokeballMap;

    GetBg0TilesDst(&tilemap, &tileset);
    bigPokeballMap = sBigPokeball_Tilemap;
    for (i = 0; i < 20; i++)
    {
        for (j = 0; j < 30; j++, bigPokeballMap++)
            SET_TILE(tilemap, i, j, *bigPokeballMap);
    }

    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return TRUE;
}

static bool8 Aqua_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sTeamAqua_Tilemap, tilemap);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return FALSE;
}

static bool8 Magma_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sTeamMagma_Tilemap, tilemap);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return FALSE;
}

static bool8 Regice_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    LoadPalette(sRegice_Palette, BG_PLTT_ID(15), sizeof(sRegice_Palette));
    CpuCopy16(sRegice_Tilemap, tilemap, 0x500);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return FALSE;
}

static bool8 Registeel_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    LoadPalette(sRegisteel_Palette, BG_PLTT_ID(15), sizeof(sRegisteel_Palette));
    CpuCopy16(sRegisteel_Tilemap, tilemap, 0x500);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return FALSE;
}

static bool8 Regirock_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    LoadPalette(sRegirock_Palette, BG_PLTT_ID(15), sizeof(sRegirock_Palette));
    CpuCopy16(sRegirock_Tilemap, tilemap, 0x500);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return FALSE;
}

#define tTimer data[1]

static bool8 Kyogre_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sKyogre_Tileset, tileset);
    DecompressDataWithHeaderVram(sKyogre_Tilemap, tilemap);

    task->tState++;
    return FALSE;
}

static bool8 Kyogre_PaletteFlash(struct Task *task)
{
    if (task->tTimer % 3 == 0)
    {
        u16 offset = task->tTimer % 30;
        offset /= 3;
        LoadPalette(&sKyogre1_Palette[offset * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    }
    if (++task->tTimer > 58)
    {
        task->tState++;
        task->tTimer = 0;
    }

    return FALSE;
}

static bool8 Kyogre_PaletteBrighten(struct Task *task)
{
    if (task->tTimer % 5 == 0)
    {
        s16 offset = task->tTimer / 5;
        LoadPalette(&sKyogre2_Palette[offset * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    }
    if (++task->tTimer > 68)
    {
        task->tState++;
        task->tTimer = 0;
        task->tEndDelay = 30;
    }

    return FALSE;
}

static bool8 WeatherDuo_FadeOut(struct Task *task)
{
    BeginNormalPaletteFade(PALETTES_OBJECTS | (1 << 15), 1, 0, 16, RGB_BLACK);
    task->tState++;
    return FALSE;
}

static bool8 WeatherDuo_End(struct Task *task)
{
    if (!gPaletteFade.active)
    {
        DmaStop(0);
        FadeScreenBlack();
        DestroyTask(FindTaskIdByFunc(task->func));
    }
    return FALSE;
}

#undef tTimer

// The PatternWeave_ functions are used by several different transitions.
// They create an effect where a pattern/image (such as the Magma emblem) is
// formed by a shimmering weave effect.
static bool8 PatternWeave_Blend1(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    if (task->tBlendDelay == 0 || --task->tBlendDelay == 0)
    {
        task->tBlendTarget2++;
        task->tBlendDelay = 2;
    }
    sTransitionData->BLDALPHA = BLDALPHA_BLEND(task->tBlendTarget2, task->tBlendTarget1);
    if (task->tBlendTarget2 > 15)
        task->tState++;
    task->tSinIndex += 8;
    task->tAmplitude -= 256;

    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude >> 8, DISPLAY_HEIGHT);

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 PatternWeave_Blend2(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    if (task->tBlendDelay == 0 || --task->tBlendDelay == 0)
    {
        task->tBlendTarget1--;
        task->tBlendDelay = 2;
    }
    sTransitionData->BLDALPHA = BLDALPHA_BLEND(task->tBlendTarget2, task->tBlendTarget1);
    if (task->tBlendTarget1 == 0)
        task->tState++;
    task->tSinIndex += 8;
    task->tAmplitude -= 256;

    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude >> 8, DISPLAY_HEIGHT);

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 PatternWeave_FinishAppear(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    task->tSinIndex += 8;
    task->tAmplitude -= 256;

    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude >> 8, DISPLAY_HEIGHT);

    if (task->tAmplitude <= 0)
    {
        task->tState++;
        task->tRadius = DISPLAY_HEIGHT;
        task->tRadiusDelta = 1 << 8;
        task->tVBlankSet = FALSE;
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 FramesCountdown(struct Task *task)
{
    if (--task->tEndDelay == 0)
        task->tState++;
    return FALSE;
}

static bool8 WeatherTrio_BgFadeBlack(struct Task *task)
{
    BeginNormalPaletteFade(PALETTES_BG, 1, 0, 16, RGB_BLACK);
    task->tState++;
    return FALSE;
}

static bool8 WeatherTrio_WaitFade(struct Task *task)
{
    if (!gPaletteFade.active)
        task->tState++;
    return FALSE;
}

// Do a shrinking circular mask to go to a black screen after the pattern appears.
static bool8 PatternWeave_CircularMask(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    if (task->tRadiusDelta < (4 << 8))
        task->tRadiusDelta += 128; // 256 is 1 unit of speed. Speed up every other frame (128 / 256)
    if (task->tRadius != 0)
    {
        task->tRadius -= task->tRadiusDelta >> 8;
        if (task->tRadius < 0)
            task->tRadius = 0;
    }
    SetCircularMask(gScanlineEffectRegBuffers[0], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, task->tRadius);
    if (task->tRadius == 0)
    {
        SetVBlankCallback(NULL);
        DmaStop(0);
        FadeScreenBlack();
        DestroyTask(FindTaskIdByFunc(task->func));
    }
    else
    {
        if (!task->tVBlankSet)
        {
            task->tVBlankSet++;
            SetVBlankCallback(VBlankCB_CircularMask);
        }
        sTransitionData->VBlank_DMA++;
    }
    return FALSE;
}

static void VBlankCB_SetWinAndBlend(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    REG_BLDCNT = sTransitionData->BLDCNT;
    REG_BLDALPHA = sTransitionData->BLDALPHA;
}

static void VBlankCB_PatternWeave(void)
{
    VBlankCB_SetWinAndBlend();
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_BG0HOFS, B_TRANS_DMA_FLAGS);
}

static void VBlankCB_CircularMask(void)
{
    VBlankCB_SetWinAndBlend();
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

#undef tAmplitude
#undef tSinIndex
#undef tBlendTarget1
#undef tBlendTarget2
#undef tRadius
#undef tRadiusDelta
#undef tVBlankSet

//------------------------------
// B_TRANSITION_POKEBALLS_TRAIL
//------------------------------

#define sSide  data[0]
#define sDelay data[1]
#define sPrevX data[2]

static void Task_PokeballsTrail(u8 taskId)
{
    while (sPokeballsTrail_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 PokeballsTrail_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuSet(sPokeballTrail_Tileset, tileset, 0x20);
    CpuFill32(0, tilemap, BG_SCREEN_SIZE);
    LoadPalette(sFieldEffectPal_Pokeball, BG_PLTT_ID(15), sizeof(sFieldEffectPal_Pokeball));

    task->tState++;
    return FALSE;
}

static bool8 PokeballsTrail_Main(struct Task *task)
{
    s16 i;
    s16 side;
    s16 startX[ARRAY_COUNT(sPokeballsTrail_StartXCoords)];
    s16 delays[ARRAY_COUNT(sPokeballsTrail_Delays)];
    memcpy(startX, sPokeballsTrail_StartXCoords, sizeof(sPokeballsTrail_StartXCoords));
    memcpy(delays, sPokeballsTrail_Delays, sizeof(sPokeballsTrail_Delays));

    // Randomly pick which side the first ball should start on.
    // The side is then flipped for each subsequent ball.
    side = Random() & 1;
    for (i = 0; i < NUM_POKEBALL_TRAILS; i++, side ^= 1)
    {
        gFieldEffectArguments[0] = startX[side];   // x
        gFieldEffectArguments[1] = (i * 32) + 16;  // y
        gFieldEffectArguments[2] = side;
        gFieldEffectArguments[3] = delays[i];
        FieldEffectStart(FLDEFF_POKEBALL_TRAIL);
    }

    task->tState++;
    return FALSE;
}

static bool8 PokeballsTrail_End(struct Task *task)
{
    if (!FieldEffectActiveListContains(FLDEFF_POKEBALL_TRAIL))
    {
        FadeScreenBlack();
        DestroyTask(FindTaskIdByFunc(Task_PokeballsTrail));
    }
    return FALSE;
}

bool8 FldEff_PokeballTrail(void)
{
    u8 spriteId = CreateSpriteAtEnd(&sSpriteTemplate_Pokeball, gFieldEffectArguments[0], gFieldEffectArguments[1], 0);
    gSprites[spriteId].oam.priority = 0;
    gSprites[spriteId].oam.affineMode = ST_OAM_AFFINE_NORMAL;
    gSprites[spriteId].sSide = gFieldEffectArguments[2];
    gSprites[spriteId].sDelay = gFieldEffectArguments[3];
    gSprites[spriteId].sPrevX = -1;
    InitSpriteAffineAnim(&gSprites[spriteId]);
    StartSpriteAffineAnim(&gSprites[spriteId], gFieldEffectArguments[2]);
    return FALSE;
}

static void SpriteCB_FldEffPokeballTrail(struct Sprite *sprite)
{
    s16 speeds[ARRAY_COUNT(sPokeballsTrail_Speeds)];
    memcpy(speeds, sPokeballsTrail_Speeds, sizeof(sPokeballsTrail_Speeds));

    if (sprite->sDelay != 0)
    {
        sprite->sDelay--;
    }
    else
    {
        if (sprite->x >= 0 && sprite->x <= DISPLAY_WIDTH)
        {
            // Set Pokéball position
            s16 posX = sprite->x >> 3;
            s16 posY = sprite->y >> 3;

            // If Pokéball moved forward clear trail behind it
            if (posX != sprite->sPrevX)
            {
                u32 var;
                u16 *ptr;

                sprite->sPrevX = posX;
                var = ((REG_BG0CNT >> 8) & 0x1F) << 11;
                ptr = (u16 *)(BG_VRAM + var);

                SET_TILE(ptr, posY - 2, posX, 1);
                SET_TILE(ptr, posY - 1, posX, 1);
                SET_TILE(ptr, posY - 0, posX, 1);
                SET_TILE(ptr, posY + 1, posX, 1);
            }
        }
        sprite->x += speeds[sprite->sSide];
        if (sprite->x < -15 || sprite->x > DISPLAY_WIDTH + 15)
            FieldEffectStop(sprite, FLDEFF_POKEBALL_TRAIL);
    }
}

#undef sSide
#undef sDelay
#undef sPrevX

//-----------------------------
// B_TRANSITION_CLOCKWISE_WIPE
//-----------------------------

static void Task_ClockwiseWipe(u8 taskId)
{
    while (sClockwiseWipe_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 ClockwiseWipe_Init(struct Task *task)
{
    u16 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    sTransitionData->WININ = 0;
    sTransitionData->WINOUT = WINOUT_WIN01_ALL;
    sTransitionData->WIN0H = WIN_RANGE(DISPLAY_WIDTH, DISPLAY_WIDTH + 1);
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = ((DISPLAY_WIDTH + 3) << 8) | (DISPLAY_WIDTH + 4);

    SetVBlankCallback(VBlankCB_ClockwiseWipe);
    sTransitionData->tWipeEndX = DISPLAY_WIDTH / 2;

    task->tState++;
    return TRUE;
}

static bool8 ClockwiseWipe_TopRight(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;

#ifdef UBFIX
    InitBlackWipe(sTransitionData->data, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, sTransitionData->tWipeEndX, 0, 1, 1);
#else
    InitBlackWipe(sTransitionData->data, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, sTransitionData->tWipeEndX, -1, 1, 1);
#endif
    do
    {
        gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] = (sTransitionData->tWipeCurrX + 1) | ((DISPLAY_WIDTH / 2) << 8);
    } while (!UpdateBlackWipe(sTransitionData->data, TRUE, TRUE));

    sTransitionData->tWipeEndX += 16;
    if (sTransitionData->tWipeEndX >= DISPLAY_WIDTH)
    {
        sTransitionData->tWipeEndY = 0;
        task->tState++;
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 ClockwiseWipe_Right(struct Task *task)
{
    s16 start, end;
    vu8 finished = FALSE;

    sTransitionData->VBlank_DMA = FALSE;

    InitBlackWipe(sTransitionData->data, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, DISPLAY_WIDTH, sTransitionData->tWipeEndY, 1, 1);

    while (1)
    {
        start = DISPLAY_WIDTH / 2, end = sTransitionData->tWipeCurrX + 1;
        if (sTransitionData->tWipeEndY >= DISPLAY_HEIGHT / 2)
            start = sTransitionData->tWipeCurrX, end = DISPLAY_WIDTH;
        gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] = end | (start << 8);
        if (finished)
            break;
        finished = UpdateBlackWipe(sTransitionData->data, TRUE, TRUE);
    }

    sTransitionData->tWipeEndY += 8;
    if (sTransitionData->tWipeEndY >= DISPLAY_HEIGHT)
    {
        sTransitionData->tWipeEndX = DISPLAY_WIDTH;
        task->tState++;
    }
    else
    {
        while (sTransitionData->tWipeCurrY < sTransitionData->tWipeEndY)
            gScanlineEffectRegBuffers[0][++sTransitionData->tWipeCurrY] = end | (start << 8);
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 ClockwiseWipe_Bottom(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;

    InitBlackWipe(sTransitionData->data, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, sTransitionData->tWipeEndX, DISPLAY_HEIGHT, 1, 1);
    do
    {
        gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] = (sTransitionData->tWipeCurrX << 8) | DISPLAY_WIDTH;
    } while (!UpdateBlackWipe(sTransitionData->data, TRUE, TRUE));

    sTransitionData->tWipeEndX -= 16;
    if (sTransitionData->tWipeEndX <= 0)
    {
        sTransitionData->tWipeEndY = DISPLAY_HEIGHT;
        task->tState++;
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 ClockwiseWipe_Left(struct Task *task)
{
    s16 end, start, temp;
    vu8 finished = FALSE;

    sTransitionData->VBlank_DMA = FALSE;

    InitBlackWipe(sTransitionData->data, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, 0, sTransitionData->tWipeEndY, 1, 1);

    while (1)
    {
        end = (gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY]) & 0xFF;
        start = sTransitionData->tWipeCurrX;
        if (sTransitionData->tWipeEndY <= DISPLAY_HEIGHT / 2)
            start = DISPLAY_WIDTH / 2, end = sTransitionData->tWipeCurrX;
        temp = end | (start << 8);
        gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] = temp;
        if (finished)
            break;
        finished = UpdateBlackWipe(sTransitionData->data, TRUE, TRUE);
    }

    sTransitionData->tWipeEndY -= 8;
    if (sTransitionData->tWipeEndY <= 0)
    {
        sTransitionData->tWipeEndX = 0;
        task->tState++;
    }
    else
    {
        while (sTransitionData->tWipeCurrY > sTransitionData->tWipeEndY)
            gScanlineEffectRegBuffers[0][--sTransitionData->tWipeCurrY] = end | (start << 8);
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 ClockwiseWipe_TopLeft(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;

    InitBlackWipe(sTransitionData->data, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, sTransitionData->tWipeEndX, 0, 1, 1);
    do
    {
        s16 start, end;
        start = DISPLAY_WIDTH / 2, end = sTransitionData->tWipeCurrX;
        if (sTransitionData->tWipeCurrX >= DISPLAY_WIDTH / 2)
            start = 0, end = DISPLAY_WIDTH;
        gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] = end | (start << 8);
    } while (!UpdateBlackWipe(sTransitionData->data, TRUE, TRUE));

    sTransitionData->tWipeEndX += 16;
    if (sTransitionData->tWipeCurrX > DISPLAY_WIDTH / 2)
        task->tState++;

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 ClockwiseWipe_End(struct Task *task)
{
    DmaStop(0);
    FadeScreenBlack();
    DestroyTask(FindTaskIdByFunc(Task_ClockwiseWipe));
    return FALSE;
}

static void VBlankCB_ClockwiseWipe(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA != 0)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    REG_WIN0H = gScanlineEffectRegBuffers[1][0];
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

//---------------------
// B_TRANSITION_RIPPLE
//---------------------

#define tSinVal       data[1]
#define tAmplitudeVal data[2]
#define tTimer        data[3]
#define tFadeStarted  data[4]

static void Task_Ripple(u8 taskId)
{
    while (sRipple_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Ripple_Init(struct Task *task)
{
    u8 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = sTransitionData->cameraY;

    SetVBlankCallback(VBlankCB_Ripple);
    SetHBlankCallback(HBlankCB_Ripple);

    EnableInterrupts(INTR_FLAG_HBLANK);

    task->tState++;
    return TRUE;
}

static bool8 Ripple_Main(struct Task *task)
{
    u8 i;
    s16 amplitude;
    u16 sinVal, speed;

    sTransitionData->VBlank_DMA = FALSE;

    amplitude = task->tAmplitudeVal >> 8;
    sinVal = task->tSinVal;
    speed = 0x180;
    task->tSinVal += 0x400;
    if (task->tAmplitudeVal <= 0x1FFF)
        task->tAmplitudeVal += 0x180;

    for (i = 0; i < DISPLAY_HEIGHT; i++, sinVal += speed)
    {
        s16 sinIndex = sinVal >> 8;
        gScanlineEffectRegBuffers[0][i] = sTransitionData->cameraY + Sin(sinIndex & 0xffff, amplitude);
    }

    if (++task->tTimer == 81)
    {
        task->tFadeStarted++;
        BeginNormalPaletteFade(PALETTES_ALL, -2, 0, 16, RGB_BLACK);
    }

    if (task->tFadeStarted && !gPaletteFade.active)
        DestroyTask(FindTaskIdByFunc(Task_Ripple));

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static void VBlankCB_Ripple(void)
{
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
}

static void HBlankCB_Ripple(void)
{
    u16 var = gScanlineEffectRegBuffers[1][REG_VCOUNT];
    REG_BG1VOFS = var;
    REG_BG2VOFS = var;
    REG_BG3VOFS = var;
}

#undef tSinVal
#undef tAmplitudeVal
#undef tTimer
#undef tFadeStarted

//-------------------
// B_TRANSITION_WAVE
//-------------------

#define tX        data[1]
#define tSinIndex data[2]

static void Task_Wave(u8 taskId)
{
    while (sWave_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Wave_Init(struct Task *task)
{
    u8 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = 0;
    sTransitionData->WIN0H = DISPLAY_WIDTH;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = DISPLAY_WIDTH + 2;

    SetVBlankCallback(VBlankCB_Wave);

    task->tState++;
    return TRUE;
}

static bool8 Wave_Main(struct Task *task)
{
    u8 i, sinIndex;
    u16 *toStore;
    bool8 finished;

    sTransitionData->VBlank_DMA = FALSE;
    toStore = gScanlineEffectRegBuffers[0];
    sinIndex = task->tSinIndex;
    task->tSinIndex += 16;
    task->tX += 8;

    for (i = 0, finished = TRUE; i < DISPLAY_HEIGHT; i++, sinIndex += 4, toStore++)
    {
        s16 x = task->tX + Sin(sinIndex, 40);
        if (x < 0)
            x = 0;
        if (x > DISPLAY_WIDTH)
            x = DISPLAY_WIDTH;
        *toStore = (x << 8) | (DISPLAY_WIDTH + 1);
        if (x < DISPLAY_WIDTH)
            finished = FALSE;
    }
    if (finished)
        task->tState++;

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 Wave_End(struct Task *task)
{
    DmaStop(0);
    FadeScreenBlack();
    DestroyTask(FindTaskIdByFunc(Task_Wave));
    return FALSE;
}

static void VBlankCB_Wave(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA != 0)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

#undef tX
#undef tSinIndex

//----------------------------------------------------
// B_TRANSITION_MUGSHOT
// Where a banner shows the trainer pic of the player
// and their opponent.
//----------------------------------------------------

#define tSinIndex           data[1]
#define tTopBannerX         data[2]
#define tBottomBannerX      data[3]
#define tTimer              data[3] // Re-used
#define tFadeSpread         data[4]
#define tOpponentSpriteAId   data[11]
#define tOpponentSpriteBId   data[12]
#define tPlayerSpriteId     data[14]
#define tPartnerSpriteId    data[13]

// Sprite data for trainer sprites in mugshots
#define sState       data[0]
#define sSlideSpeed  data[1]
#define sSlideAccel  data[2]
#define sDone        data[6]
#define sSlideDir    data[7]

static void Task_Mugshot(u8 taskId)
{
    while (sMugshot_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Mugshot_Init(struct Task *task)
{
    u8 i;

    InitTransitionData();
    ScanlineEffect_Clear();
    Mugshots_CreateTrainerPics(task);

    task->tSinIndex = 0;
    task->tTopBannerX = 1;
    task->tBottomBannerX = DISPLAY_WIDTH - 1;
    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = WINOUT_WIN01_BG1 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ | WINOUT_WIN01_CLR;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = (DISPLAY_WIDTH << 8) | (DISPLAY_WIDTH + 1);

    SetVBlankCallback(VBlankCB_Mugshots);

    task->tState++;
    return FALSE;
}

static bool8 Mugshot_SetGfx(struct Task *task)
{
    s16 i, j;
    u16 *tilemap, *tileset;
    const u16 *mugshotsMap = sMugshotsTilemap;
    enum MugshotColor mugshotColor = GetTrainerMugshotColorFromId(TRAINER_BATTLE_PARAM.opponentA);

    GetBg0TilesDst(&tilemap, &tileset);
    CpuSet(sEliteFour_Tileset, tileset, 0xF0);

    if (mugshotColor >= ARRAY_COUNT(sOpponentMugshotsPals))
        mugshotColor = MUGSHOT_COLOR_PURPLE;

    LoadPalette(sOpponentMugshotsPals[mugshotColor], 0xF0, 0x20);
    LoadPalette(sPlayerMugshotsPals[gSaveBlock2Ptr->playerGender], BG_PLTT_ID(15) + 10, PLTT_SIZEOF(6));

    for (i = 0; i < 20; i++)
    {
        for (j = 0; j < 32; j++, mugshotsMap++)
            SET_TILE(tilemap, i, j, *mugshotsMap);
    }

    EnableInterrupts(INTR_FLAG_HBLANK);

    SetHBlankCallback(HBlankCB_Mugshots);
    task->tState++;
    return FALSE;
}

static bool8 Mugshot_ShowBanner(struct Task *task)
{
    u8 i, sinIndex;
    u16 *toStore;
    s16 x;
    s32 mergedValue;

    sTransitionData->VBlank_DMA = FALSE;

    toStore = gScanlineEffectRegBuffers[0];
    sinIndex = task->tSinIndex;
    task->tSinIndex += 16;

    // Update top banner
    for (i = 0; i < DISPLAY_HEIGHT / 2; i++, toStore++, sinIndex += 16)
    {
        x = task->tTopBannerX + Sin(sinIndex, 16);
        if (x < 0)
            x = 1;
        if (x > DISPLAY_WIDTH)
            x = DISPLAY_WIDTH;
        *toStore = x;
    }

    // Update bottom banner
    for (; i < DISPLAY_HEIGHT; i++, toStore++, sinIndex += 16)
    {
        x = task->tBottomBannerX - Sin(sinIndex, 16);
        if (x < 0)
            x = 0;
        if (x > DISPLAY_WIDTH - 1)
            x = DISPLAY_WIDTH - 1;
        *toStore = (x << 8) | DISPLAY_WIDTH;
    }

    // Slide banners across screen
    task->tTopBannerX += 8;
    task->tBottomBannerX -= 8;

    if (task->tTopBannerX > DISPLAY_WIDTH)
        task->tTopBannerX = DISPLAY_WIDTH;
    if (task->tBottomBannerX < 0)
        task->tBottomBannerX = 0;

    mergedValue = *(s32 *)(&task->tTopBannerX);
    if (mergedValue == DISPLAY_WIDTH)
        task->tState++;

    sTransitionData->BG0HOFS_Lower -= 8;
    sTransitionData->BG0HOFS_Upper += 8;
    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 Mugshot_StartOpponentSlide(struct Task *task)
{
    u8 i;
    u16 *toStore;

    sTransitionData->VBlank_DMA = FALSE;

    for (i = 0, toStore = gScanlineEffectRegBuffers[0]; i < DISPLAY_HEIGHT; i++, toStore++)
        *toStore = DISPLAY_WIDTH;

    task->tState++;

    // Clear old data
    task->tSinIndex = 0;
    task->tTopBannerX = 0;
    task->tBottomBannerX = 0;

    sTransitionData->BG0HOFS_Lower -= 8;
    sTransitionData->BG0HOFS_Upper += 8;

    SetTrainerPicSlideDirection(task->tOpponentSpriteAId, 0);
    if (TRAINER_BATTLE_PARAM.opponentB != TRAINER_NONE && gBattleTypeFlags & BATTLE_TYPE_TWO_OPPONENTS)
    {
            SetTrainerPicSlideDirection(task->tOpponentSpriteBId, 0);
    }
    SetTrainerPicSlideDirection(task->tPlayerSpriteId, 1);
    if (gPartnerTrainerId != TRAINER_PARTNER(PARTNER_NONE) && gBattleTypeFlags & BATTLE_TYPE_INGAME_PARTNER)
    {
        SetTrainerPicSlideDirection(task->tPartnerSpriteId, 1);
    }

    // Start opponent slide
    IncrementTrainerPicState(task->tOpponentSpriteAId);

    PlaySE(SE_MUGSHOT);

    if (TRAINER_BATTLE_PARAM.opponentB != TRAINER_NONE && gBattleTypeFlags & BATTLE_TYPE_TWO_OPPONENTS)
    {
        IncrementTrainerPicState(task->tOpponentSpriteBId);
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 Mugshot_WaitStartPlayerSlide(struct Task *task)
{
    sTransitionData->BG0HOFS_Lower -= 8;
    sTransitionData->BG0HOFS_Upper += 8;

    // Start player's slide in once the opponent is finished
    if (IsTrainerPicSlideDone(task->tOpponentSpriteAId))
    {
        task->tState++;
        if (gPartnerTrainerId != TRAINER_PARTNER(PARTNER_NONE) && gBattleTypeFlags & BATTLE_TYPE_INGAME_PARTNER)
        {
            IncrementTrainerPicState(task->tPartnerSpriteId);
        }
        IncrementTrainerPicState(task->tPlayerSpriteId);
    }
    return FALSE;
}

static bool8 Mugshot_WaitPlayerSlide(struct Task *task)
{
    sTransitionData->BG0HOFS_Lower -= 8;
    sTransitionData->BG0HOFS_Upper += 8;

    if (gPartnerTrainerId != TRAINER_PARTNER(PARTNER_NONE) && gBattleTypeFlags & BATTLE_TYPE_INGAME_PARTNER)
    {
        if (IsTrainerPicSlideDone(task->tPartnerSpriteId))
        {
            sTransitionData->VBlank_DMA = FALSE;
            SetVBlankCallback(NULL);
            DmaStop(0);
            memset(gScanlineEffectRegBuffers[0], 0, DISPLAY_HEIGHT * 2);
            memset(gScanlineEffectRegBuffers[1], 0, DISPLAY_HEIGHT * 2);
            SetGpuReg(REG_OFFSET_WIN0H, DISPLAY_WIDTH);
            SetGpuReg(REG_OFFSET_BLDY, 0);
            task->tState++;
            task->tTimer = 0;
            task->tFadeSpread = 0;
            sTransitionData->BLDCNT = BLDCNT_TGT1_ALL | BLDCNT_EFFECT_LIGHTEN;
            SetVBlankCallback(VBlankCB_MugshotsFadeOut);
        }
        else
        {
            return FALSE;
        }
    }
    else
    {
        if (IsTrainerPicSlideDone(task->tPlayerSpriteId))
        {
            sTransitionData->VBlank_DMA = FALSE;
            SetVBlankCallback(NULL);
            DmaStop(0);
            memset(gScanlineEffectRegBuffers[0], 0, DISPLAY_HEIGHT * 2);
            memset(gScanlineEffectRegBuffers[1], 0, DISPLAY_HEIGHT * 2);
            SetGpuReg(REG_OFFSET_WIN0H, DISPLAY_WIDTH);
            SetGpuReg(REG_OFFSET_BLDY, 0);
            task->tState++;
            task->tTimer = 0;
            task->tFadeSpread = 0;
            sTransitionData->BLDCNT = BLDCNT_TGT1_ALL | BLDCNT_EFFECT_LIGHTEN;
            SetVBlankCallback(VBlankCB_MugshotsFadeOut);
        }
        else
        {
            return FALSE;
        }
    }
    return FALSE;
}

static bool8 Mugshot_GradualWhiteFade(struct Task *task)
{
    bool32 active;

    sTransitionData->VBlank_DMA = FALSE;
    active = TRUE;
    sTransitionData->BG0HOFS_Lower -= 8;
    sTransitionData->BG0HOFS_Upper += 8;

    if (task->tFadeSpread < DISPLAY_HEIGHT / 2)
        task->tFadeSpread += 2;
    if (task->tFadeSpread > DISPLAY_HEIGHT / 2)
        task->tFadeSpread = DISPLAY_HEIGHT / 2;

    if (++task->tTimer & 1)
    {
        s16 i;
        for (i = 0, active = FALSE; i <= task->tFadeSpread; i++)
        {
            // Fade starts in middle of screen and
            // spreads outwards in both directions.
            s16 index1 = DISPLAY_HEIGHT / 2 - i;
            s16 index2 = DISPLAY_HEIGHT / 2 + i;
            if (gScanlineEffectRegBuffers[0][index1] <= 15)
            {
                active = TRUE;
                gScanlineEffectRegBuffers[0][index1]++;
            }
            if (gScanlineEffectRegBuffers[0][index2] <= 15)
            {
                active = TRUE;
                gScanlineEffectRegBuffers[0][index2]++;
            }
        }
    }

    if (task->tFadeSpread == DISPLAY_HEIGHT / 2 && !active)
        task->tState++;

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

// Set palette to white to replace the scanline white fade
// before the screen fades to black.
static bool8 Mugshot_InitFadeWhiteToBlack(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    BlendPalettes(PALETTES_ALL, 16, RGB_WHITE);
    sTransitionData->BLDCNT = 0xFF;
    task->tTimer = 0;

    task->tState++;
    return TRUE;
}

static bool8 Mugshot_FadeToBlack(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;

    task->tTimer++;
    memset(gScanlineEffectRegBuffers[0], task->tTimer, DISPLAY_HEIGHT * 2);
    if (task->tTimer > 15)
        task->tState++;

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 Mugshot_End(struct Task *task)
{
    DmaStop(0);
    FadeScreenBlack();
    DestroyTask(FindTaskIdByFunc(task->func));
    return FALSE;
}

static void VBlankCB_Mugshots(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA != 0)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    REG_BG0VOFS = sTransitionData->BG0VOFS;
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

static void VBlankCB_MugshotsFadeOut(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA != 0)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    REG_BLDCNT = sTransitionData->BLDCNT;
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_BLDY, B_TRANS_DMA_FLAGS);
}

static void HBlankCB_Mugshots(void)
{
    if (REG_VCOUNT < DISPLAY_HEIGHT / 2)
        REG_BG0HOFS = sTransitionData->BG0HOFS_Lower;
    else
        REG_BG0HOFS = sTransitionData->BG0HOFS_Upper;
}

static void Mugshots_CreateTrainerPics(struct Task *task)
{
    struct Sprite *opponentSpriteA, *opponentSpriteB=0, *playerSprite, *partnerSprite=0;

    u8 trainerAPicId = GetTrainerPicFromId(TRAINER_BATTLE_PARAM.opponentA);
    u8 trainerBPicId = GetTrainerPicFromId(TRAINER_BATTLE_PARAM.opponentB);
    u8 partnerPicId = GetTrainerPicFromId(gPartnerTrainerId);
    s16 opponentARotationScales = 0;
    s16 opponentBRotationScales = 0;

    gReservedSpritePaletteCount = 10;
    if (TRAINER_BATTLE_PARAM.opponentB != TRAINER_NONE && gBattleTypeFlags & BATTLE_TYPE_TWO_OPPONENTS)
    {
        task->tOpponentSpriteBId = CreateTrainerSprite(trainerBPicId,
                                                    gTrainerSprites[trainerBPicId].mugshotCoords.x - 240,
                                                    gTrainerSprites[trainerBPicId].mugshotCoords.y + 42,
                                                    0, NULL);
        opponentSpriteB = &gSprites[task->tOpponentSpriteBId];
        opponentSpriteB->callback = SpriteCB_MugshotTrainerPicPartner;
        opponentSpriteB->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
        opponentSpriteB->oam.matrixNum = AllocOamMatrix();
        opponentSpriteB->oam.shape = SPRITE_SHAPE(64x32);
        opponentSpriteB->oam.size = SPRITE_SIZE(64x32);
        CalcCenterToCornerVec(opponentSpriteB, SPRITE_SHAPE(64x32), SPRITE_SIZE(64x32), ST_OAM_AFFINE_DOUBLE);
        opponentBRotationScales = gTrainerSprites[trainerBPicId].mugshotRotation;
        SetOamMatrixRotationScaling(opponentSpriteB->oam.matrixNum, opponentBRotationScales, opponentBRotationScales, 0);
    }

    task->tOpponentSpriteAId = CreateTrainerSprite(trainerAPicId,
                                                  gTrainerSprites[trainerAPicId].mugshotCoords.x - 32,
                                                  gTrainerSprites[trainerAPicId].mugshotCoords.y + 42,
                                                  0, NULL);

    gReservedSpritePaletteCount = 12;
    if (gPartnerTrainerId != TRAINER_PARTNER(PARTNER_NONE) && gBattleTypeFlags & BATTLE_TYPE_INGAME_PARTNER)
    {
        task->tPartnerSpriteId = CreateTrainerSprite(partnerPicId,
                                                DISPLAY_WIDTH + 240,
                                                106,
                                                0, NULL);
        partnerSprite = &gSprites[task->tPartnerSpriteId];
        partnerSprite->callback = SpriteCB_MugshotTrainerPicPartner;
        partnerSprite->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
        partnerSprite->oam.matrixNum = AllocOamMatrix();
        partnerSprite->oam.shape = SPRITE_SHAPE(64x32);
        partnerSprite->oam.size = SPRITE_SIZE(64x32);
        CalcCenterToCornerVec(partnerSprite, SPRITE_SHAPE(64x32), SPRITE_SIZE(64x32), ST_OAM_AFFINE_DOUBLE);
        SetOamMatrixRotationScaling(partnerSprite->oam.matrixNum, -512, 512, 0);
    }

    task->tPlayerSpriteId = CreateTrainerSprite(PlayerGenderToFrontTrainerPicId(gSaveBlock2Ptr->playerGender),
                                                DISPLAY_WIDTH + 32,
                                                106,
                                                0, NULL);

    opponentSpriteA = &gSprites[task->tOpponentSpriteAId];
    playerSprite = &gSprites[task->tPlayerSpriteId];

    opponentSpriteA->callback = SpriteCB_MugshotTrainerPic;
    playerSprite->callback = SpriteCB_MugshotTrainerPic;

    opponentSpriteA->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    playerSprite->oam.affineMode = ST_OAM_AFFINE_DOUBLE;

    opponentSpriteA->oam.matrixNum = AllocOamMatrix();
    playerSprite->oam.matrixNum = AllocOamMatrix();

    opponentSpriteA->oam.shape = SPRITE_SHAPE(64x32);
    playerSprite->oam.shape = SPRITE_SHAPE(64x32);

    opponentSpriteA->oam.size = SPRITE_SIZE(64x32);
    playerSprite->oam.size = SPRITE_SIZE(64x32);

    CalcCenterToCornerVec(opponentSpriteA, SPRITE_SHAPE(64x32), SPRITE_SIZE(64x32), ST_OAM_AFFINE_DOUBLE);
    CalcCenterToCornerVec(playerSprite, SPRITE_SHAPE(64x32), SPRITE_SIZE(64x32), ST_OAM_AFFINE_DOUBLE);

    opponentARotationScales = gTrainerSprites[trainerAPicId].mugshotRotation;

    SetOamMatrixRotationScaling(opponentSpriteA->oam.matrixNum, opponentARotationScales, opponentARotationScales, 0);
    SetOamMatrixRotationScaling(playerSprite->oam.matrixNum, -512, 512, 0);
}

static void SpriteCB_MugshotTrainerPic(struct Sprite *sprite)
{
    while (sMugshotTrainerPicFuncs[sprite->sState](sprite));
}

static void SpriteCB_MugshotTrainerPicPartner(struct Sprite *sprite)
{
    while (sMugshotTrainerPicFuncsPartner[sprite->sState](sprite));
}


// Wait until IncrementTrainerPicState is called
static bool8 MugshotTrainerPic_Pause(struct Sprite *sprite)
{
    return FALSE;
}

static bool8 MugshotTrainerPic_Init(struct Sprite *sprite)
{
    s16 speeds[ARRAY_COUNT(sTrainerPicSlideSpeeds)];
    s16 accels[ARRAY_COUNT(sTrainerPicSlideAccels)];

    memcpy(speeds, sTrainerPicSlideSpeeds, sizeof(sTrainerPicSlideSpeeds));
    memcpy(accels, sTrainerPicSlideAccels, sizeof(sTrainerPicSlideAccels));

    sprite->sState++;
    sprite->sSlideSpeed = speeds[sprite->sSlideDir];
    sprite->sSlideAccel = accels[sprite->sSlideDir];
    return TRUE;
}

static bool8 MugshotTrainerPic_Slide(struct Sprite *sprite)
{
    sprite->x += sprite->sSlideSpeed;

    // Advance state when pic passes ~40% of screen
    if (sprite->sSlideDir && sprite->x < DISPLAY_WIDTH - 107)
        sprite->sState++;
    else if (!sprite->sSlideDir && sprite->x > 103)
        sprite->sState++;
    return FALSE;
}

static bool8 MugshotTrainerPic_SlidePartner(struct Sprite *sprite)
{
    sprite->x += sprite->sSlideSpeed;

    // Advance state when pic passes ~40% of screen
    if (sprite->sSlideDir && sprite->x < DISPLAY_WIDTH - 60)
        sprite->sState++;
    else if (!sprite->sSlideDir && sprite->x > 60)
        sprite->sState++;
    return FALSE;
}

static bool8 MugshotTrainerPic_SlideSlow(struct Sprite *sprite)
{
    // Add acceleration value to speed, then add speed.
    // For both sides acceleration is opposite speed, so slide slows down.
    sprite->sSlideSpeed += sprite->sSlideAccel;
    sprite->x += sprite->sSlideSpeed;

    // Advance state when slide comes to a stop
    if (sprite->sSlideSpeed == 0)
    {
        sprite->sState++;
        sprite->sSlideAccel = -sprite->sSlideAccel;
        sprite->sDone = TRUE;
    }
    return FALSE;
}

// Slides trainer pic offscreen. This is never reached, because it's preceded
// by a second MugshotTrainerPic_Pause, and IncrementTrainerPicState is
// only called once per trainer pic.
static bool8 MugshotTrainerPic_SlideOffscreen(struct Sprite *sprite)
{
    sprite->sSlideSpeed += sprite->sSlideAccel;
    sprite->x += sprite->sSlideSpeed;
    if (sprite->x < -31 || sprite->x > DISPLAY_WIDTH + 31)
        sprite->sState++;
    return FALSE;
}

static void SetTrainerPicSlideDirection(s16 spriteId, s16 dirId)
{
    gSprites[spriteId].sSlideDir = dirId;
}

static void IncrementTrainerPicState(s16 spriteId)
{
    gSprites[spriteId].sState++;
}

static s16 IsTrainerPicSlideDone(s16 spriteId)
{
    return gSprites[spriteId].sDone;
}

#undef sState
#undef sSlideSpeed
#undef sSlideAccel
#undef sDone
#undef sSlideDir
#undef tSinIndex
#undef tTopBannerX
#undef tBottomBannerX
#undef tTimer
#undef tFadeSpread
#undef tOpponentSpriteAId
#undef tOpponentSpriteBId
#undef tPlayerSpriteId
#undef tPartnerSpriteId

//--------------------
// B_TRANSITION_SLICE
//--------------------

#define tEffectX data[1]
#define tSpeed   data[2]
#define tAccel   data[3]

static void Task_Slice(u8 taskId)
{
    while (sSlice_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Slice_Init(struct Task *task)
{
    u16 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    task->tSpeed = 1 << 8;
    task->tAccel = 1;
    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = 0;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;
    sTransitionData->VBlank_DMA = FALSE;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        gScanlineEffectRegBuffers[1][i] = sTransitionData->cameraX;
        gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT + i] = DISPLAY_WIDTH;
    }

    EnableInterrupts(INTR_FLAG_HBLANK);
    SetGpuRegBits(REG_OFFSET_DISPSTAT, DISPSTAT_HBLANK_INTR);

    SetVBlankCallback(VBlankCB_Slice);
    SetHBlankCallback(HBlankCB_Slice);

    task->tState++;
    return TRUE;
}

static bool8 Slice_Main(struct Task *task)
{
    u16 i;

    sTransitionData->VBlank_DMA = FALSE;

    task->tEffectX += (task->tSpeed >> 8);
    if (task->tEffectX > DISPLAY_WIDTH)
        task->tEffectX = DISPLAY_WIDTH;
    if (task->tSpeed <= 0xFFF)
        task->tSpeed += task->tAccel;
    if (task->tAccel < 128)
        task->tAccel <<= 1; // multiplying by two

    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        u16 *storeLoc1 = &gScanlineEffectRegBuffers[0][i];
        u16 *storeLoc2 = &gScanlineEffectRegBuffers[0][i + DISPLAY_HEIGHT];

        // Alternate rows
        if (i % 2)
        {
            *storeLoc1 = sTransitionData->cameraX + task->tEffectX;
            *storeLoc2 = DISPLAY_WIDTH - task->tEffectX;
        }
        else
        {
            *storeLoc1 = sTransitionData->cameraX - task->tEffectX;
            *storeLoc2 = (task->tEffectX << 8) | (DISPLAY_WIDTH + 1);
        }
    }

    if (task->tEffectX >= DISPLAY_WIDTH)
        task->tState++;

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 Slice_End(struct Task *task)
{
    DmaStop(0);
    FadeScreenBlack();
    DestroyTask(FindTaskIdByFunc(Task_Slice));
    return FALSE;
}

static void VBlankCB_Slice(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 4);
    DmaSet(0, &gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

static void HBlankCB_Slice(void)
{
    if (REG_VCOUNT < DISPLAY_HEIGHT)
    {
        u16 var = gScanlineEffectRegBuffers[1][REG_VCOUNT];
        REG_BG1HOFS = var;
        REG_BG2HOFS = var;
        REG_BG3HOFS = var;
    }
}

#undef tEffectX
#undef tSpeed
#undef tAccel

//--------------------------
// B_TRANSITION_SHRED_SPLIT
//--------------------------

// Data starts at 4. Possible it shared data
// with Slice above, which ends at 3.
#define tDelayTimer data[4]
#define tExtent     data[5]
#define tDelay      data[6]

static void Task_ShredSplit(u8 taskId)
{
    while (sShredSplit_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 ShredSplit_Init(struct Task *task)
{
    u16 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = 0;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        gScanlineEffectRegBuffers[1][i] = sTransitionData->cameraX;
        gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT + i] = DISPLAY_WIDTH;
        gScanlineEffectRegBuffers[0][i] = sTransitionData->cameraX;
        gScanlineEffectRegBuffers[0][DISPLAY_HEIGHT + i] = DISPLAY_WIDTH;
        gScanlineEffectRegBuffers[0][DISPLAY_HEIGHT * 2 + i] = 0;
        gScanlineEffectRegBuffers[0][DISPLAY_HEIGHT * 3 + i] = 256;
        gScanlineEffectRegBuffers[0][DISPLAY_HEIGHT * 4 + i] = 1;
    }

    task->tDelayTimer = 0;
    task->tExtent = 0;
    task->tDelay = 7;

    EnableInterrupts(INTR_FLAG_HBLANK);

    SetVBlankCallback(VBlankCB_Slice);
    SetHBlankCallback(HBlankCB_Slice);

    task->tState++;
    return TRUE;
}

static bool8 ShredSplit_Main(struct Task *task)
{
    u16 i, j, k;
    u8 baseY[ARRAY_COUNT(sShredSplit_SectionYCoords)];
    s16 moveDirs[ARRAY_COUNT(sShredSplit_SectionMoveDirs)];
    u8 linesFinished;
    u16 *ptr4, *ptr3, *ptr1, *ptr2;
    s16 y;

    memcpy(baseY, sShredSplit_SectionYCoords, sizeof(baseY));
    memcpy(moveDirs, sShredSplit_SectionMoveDirs, sizeof(moveDirs));

    sTransitionData->VBlank_DMA = FALSE;
    linesFinished = 0;

    for (i = 0; i <= task->tExtent; i++)
    {
        // Slide half of the pixel rows (alternating) right
        for (j = 0; j < 2; j++)
        {
            for (k = 0; k < 2; k++)
            {
                y = baseY[j] + (moveDirs[k] * -i * 2);
                if (y >= 0 && (y != DISPLAY_HEIGHT / 2 - 1 || j != 1))
                {
                    ptr4 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT * 2];
                    ptr3 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT * 3];
                    ptr1 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT * 4];
                    if (*ptr4 >= DISPLAY_WIDTH)
                    {
                        *ptr4 = DISPLAY_WIDTH;
                        linesFinished++;
                    }
                    else
                    {
                        *ptr4 += (*ptr3 >> 8);
                        if (*ptr1 <= 0x7F)
                            *ptr1 *= 2;
                        if (*ptr3 <= 0xFFF)
                            *ptr3 += *ptr1;
                    }
                    ptr2 = &gScanlineEffectRegBuffers[0][y];
                    ptr3 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT];
                    *ptr2 = sTransitionData->cameraX + *ptr4;
                    *ptr3 = DISPLAY_WIDTH - *ptr4;

                    if (i == 0)
                        break;
                }
            }
        }

        // Slide the other half of the rows left
        for (j = 0; j < 2; j++)
        {
            for (k = 0; k < 2; k++)
            {
                y = baseY[j] + 1 + (moveDirs[k] * -i * 2);
                if (y <= DISPLAY_HEIGHT && (y != DISPLAY_HEIGHT / 2 || j != 1))
                {
                    ptr4 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT * 2];
                    ptr3 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT * 3];
                    ptr1 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT * 4];
                    if (*ptr4 >= DISPLAY_WIDTH)
                    {
                        *ptr4 = DISPLAY_WIDTH;
                        linesFinished++;
                    }
                    else
                    {
                        *ptr4 += (*ptr3 >> 8);
                        if (*ptr1 <= 0x7F)
                            *ptr1 *= 2;
                        if (*ptr3 <= 0xFFF)
                            *ptr3 += *ptr1;
                    }
                    ptr2 = &gScanlineEffectRegBuffers[0][y];
                    ptr3 = &gScanlineEffectRegBuffers[0][y + DISPLAY_HEIGHT];
                    *ptr2 = sTransitionData->cameraX - *ptr4;
                    *ptr3 = (*ptr4 << 8) | (DISPLAY_WIDTH + 1);

                    if (i == 0)
                        break;
                }
            }
        }
    }

    // Count down to next move
    if (--task->tDelayTimer < 0)
        task->tDelayTimer = 0;

    // Try increase effect's extent
    if (task->tDelayTimer <= 0 && task->tExtent + 1 <= DISPLAY_HEIGHT / 8)
    {
        task->tDelayTimer = task->tDelay;
        task->tExtent++;
    }

    // All lines have reached screen width, move on.
    if (linesFinished >= DISPLAY_HEIGHT)
        task->tState++;

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 ShredSplit_End(struct Task *task)
{
    DmaStop(0);
    FadeScreenBlack();
    DestroyTask(FindTaskIdByFunc(Task_ShredSplit));
    return FALSE;
}

#undef tDelayTimer
#undef tExtent
#undef tDelay

//-----------------------------------------------------------
// B_TRANSITION_BLACKHOLE and B_TRANSITION_BLACKHOLE_PULSATE
//-----------------------------------------------------------

#define tRadius    data[1]
#define tGrowSpeed data[2]
#define tSinIndex  data[5]
#define tVibrateId data[6]
#define tAmplitude data[6] // Used differently by the two transitions
#define tFlag      data[7] // Used generally to indicate an action has taken place.

static void Task_Blackhole(u8 taskId)
{
    while (sBlackhole_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_BlackholePulsate(u8 taskId)
{
    while (sBlackholePulsate_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

// Init is shared by both transitions
static bool8 Blackhole_Init(struct Task *task)
{
    s32 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    sTransitionData->WININ = 0;
    sTransitionData->WINOUT = WINOUT_WIN01_ALL;
    sTransitionData->WIN0H = DISPLAY_WIDTH;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = 0;

    SetVBlankCallback(VBlankCB_CircularMask);

    task->tState++;
    task->tRadius = 1;
    task->tGrowSpeed = 1 << 8;
    task->tFlag = FALSE;

    return FALSE;
}

static bool8 Blackhole_GrowEnd(struct Task *task)
{
    if (task->tFlag == TRUE)
    {
        DmaStop(0);
        SetVBlankCallback(NULL);
        DestroyTask(FindTaskIdByFunc(task->func));
    }
    else
    {
        sTransitionData->VBlank_DMA = FALSE;
        if (task->tGrowSpeed < 1024)
            task->tGrowSpeed += 128;
        if (task->tRadius < DISPLAY_HEIGHT)
            task->tRadius += task->tGrowSpeed >> 8;
        if (task->tRadius > DISPLAY_HEIGHT)
            task->tRadius = DISPLAY_HEIGHT;
        SetCircularMask(gScanlineEffectRegBuffers[0], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, task->tRadius);
        if (task->tRadius == DISPLAY_HEIGHT)
        {
            task->tFlag = TRUE;
            FadeScreenBlack();
        }
        else
        {
            sTransitionData->VBlank_DMA++;
        }
    }

    return FALSE;
}

static bool8 Blackhole_Vibrate(struct Task *task)
{
    sTransitionData->VBlank_DMA = FALSE;
    if (task->tFlag == FALSE)
    {
        task->tFlag++;
        task->tRadius = 48;
        task->tVibrateId = 0;
    }
    task->tRadius += sBlackhole_Vibrations[task->tVibrateId];
    task->tVibrateId = (task->tVibrateId + 1) % (int)ARRAY_COUNT(sBlackhole_Vibrations);
    SetCircularMask(gScanlineEffectRegBuffers[0], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, task->tRadius);
    if (task->tRadius < 9)
    {
        task->tState++;
        task->tFlag = FALSE;
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 BlackholePulsate_Main(struct Task *task)
{
    u16 index; // should be s16 I think
    s16 amplitude;

    sTransitionData->VBlank_DMA = FALSE;
    if (task->tFlag == FALSE)
    {
        task->tFlag++;
        task->tSinIndex = 2;
        task->tAmplitude = 2;
    }

    if (task->tRadius > DISPLAY_HEIGHT)
        task->tRadius = DISPLAY_HEIGHT;

    SetCircularMask(gScanlineEffectRegBuffers[0], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, task->tRadius);
    if (task->tRadius == DISPLAY_HEIGHT)
    {
        DmaStop(0);
        FadeScreenBlack();
        DestroyTask(FindTaskIdByFunc(task->func));
    }

    index = task->tSinIndex;
    if ((task->tSinIndex & 0xFF) <= 128)
    {
        amplitude = task->tAmplitude;
        task->tSinIndex += 8;
    }
    else
    {
        amplitude = task->tAmplitude - 1;
        task->tSinIndex += 16;
    }
    task->tRadius += Sin(index & 0xFF, amplitude);

    if (task->tRadius <= 0)
        task->tRadius = 1;

    if (task->tSinIndex >= 0xFF)
    {
        task->tSinIndex >>= 8;
        task->tAmplitude++;
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

#undef tRadius
#undef tGrowSpeed
#undef tSinIndex
#undef tVibrateId
#undef tAmplitude
#undef tFlag

//---------------------------------
// B_TRANSITION_RECTANGULAR_SPIRAL
//---------------------------------

static void Task_RectangularSpiral(u8 taskId)
{
    while (sRectangularSpiral_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 RectangularSpiral_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuCopy16(sShrinkingBoxTileset, tileset, 0x20);
    CpuCopy16(&sShrinkingBoxTileset[0x70], &tileset[0x20], 0x20);
    CpuFill16(0xF0 << 8, tilemap, BG_SCREEN_SIZE);
    LoadPalette(sFieldEffectPal_Pokeball, BG_PLTT_ID(15), sizeof(sFieldEffectPal_Pokeball));

    task->data[3] = 1;
    task->tState++;

    // Line starting in top left
    sRectangularSpiralLines[0].state = SPIRAL_INWARD_START;
    sRectangularSpiralLines[0].position = -1;
    sRectangularSpiralLines[0].moveIndex = 1;
    sRectangularSpiralLines[0].reboundPosition = 308;
    sRectangularSpiralLines[0].outward = FALSE;

    // Line starting in bottom right
    sRectangularSpiralLines[1].state = SPIRAL_INWARD_START;
    sRectangularSpiralLines[1].position = -1;
    sRectangularSpiralLines[1].moveIndex = 1;
    sRectangularSpiralLines[1].reboundPosition = 308;
    sRectangularSpiralLines[1].outward = FALSE;

    // Line starting in top right
    sRectangularSpiralLines[2].state = SPIRAL_INWARD_START;
    sRectangularSpiralLines[2].position = -3;
    sRectangularSpiralLines[2].moveIndex = 1;
    sRectangularSpiralLines[2].reboundPosition = 307;
    sRectangularSpiralLines[2].outward = FALSE;

    // Line starting in bottom left
    sRectangularSpiralLines[3].state = SPIRAL_INWARD_START;
    sRectangularSpiralLines[3].position = -3;
    sRectangularSpiralLines[3].moveIndex = 1;
    sRectangularSpiralLines[3].reboundPosition = 307;
    sRectangularSpiralLines[3].outward = FALSE;

    return FALSE;
}

static bool8 RectangularSpiral_Main(struct Task *task)
{
    u16 *tilemap, *tileset;
    u8 i;
    u16 j;
    bool32 done = TRUE;

    GetBg0TilesDst(&tilemap, &tileset);

    // Draw 2 tiles at a time for each spiral line
    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < ARRAY_COUNT(sRectangularSpiralLines); j++)
        {
            s16 position = 0;
            s16 x = 0, y = 0;

            if (UpdateRectangularSpiralLine(sRectangularSpiral_MoveDataTables[j / 2], &sRectangularSpiralLines[j]))
            {
                // The line moved to a new position, draw the tile.
                done = FALSE;
                position = sRectangularSpiralLines[j].position;

                // Invert position for the two lines that start at the bottom.
                if ((j % 2) == 1)
                    position = 637 - position;

                x = position % 32;
                y = position / 32;

                SET_TILE(tilemap, y, x, 2);
            }
        }
    }

    if (done == TRUE)
        task->tState++;
    return FALSE;
}

static bool8 RectangularSpiral_End(struct Task *task)
{
    DmaStop(0);
    FadeScreenBlack();
    DestroyTask(FindTaskIdByFunc(task->func));
    return FALSE;
}

// Returns TRUE if a tile should be drawn, FALSE otherwise
static bool16 UpdateRectangularSpiralLine(const s16 *const *moveDataTable, struct RectangularSpiralLine *line)
{
    const s16 *moveData = moveDataTable[line->state];

    // Has spiral finished?
    // Note that most move data arrays endsin SPIRAL_END but it is
    // only ever reached on the final array of spiraling outward.
    if (moveData[line->moveIndex] == SPIRAL_END)
        return FALSE;

    // Presumably saving data for debug.
    sDebug_RectangularSpiralData = moveData[0];
    sDebug_RectangularSpiralData = moveData[1];
    sDebug_RectangularSpiralData = moveData[2];
    sDebug_RectangularSpiralData = moveData[3];

    // Note that for the two lines originating at the bottom the
    // position is inverted, so the directions are flipped.
    // i.e. position += 1 is right for the top lines and left
    // for their inverted partners on the bottom.
    switch (moveData[0])
    {
    case MOVE_RIGHT:
        line->position += 1;
        break;
    case MOVE_LEFT:
        line->position -= 1;
        break;
    case MOVE_UP:
        line->position -= 32;
        break;
    case MOVE_DOWN:
        line->position += 32;
        break;
    }

    // Below check is never true.
    // SPIRAL_END was already checked, and position is never >= 640
    if (line->position >= 640 || moveData[line->moveIndex] == SPIRAL_END)
        return FALSE;

    if (!line->outward && moveData[line->moveIndex] == SPIRAL_REBOUND)
    {
        // Line has reached the final point of spiraling inward.
        // Time to flip and start spiraling outward.
        line->outward = TRUE;
        line->moveIndex = 1;
        line->position = line->reboundPosition;
        line->state = SPIRAL_OUTWARD_START;
    }

    // Reached move target, advance to next movement.
    if (line->position == moveData[line->moveIndex])
    {
        line->state++;
        if (line->outward == TRUE)
        {
            if (line->state > SPIRAL_OUTWARD_END)
            {
                // Still spiraling outward, loop back to the first state
                // but use the second set of move targets.
                // For example, the 28 in sRectangularSpiral_Major_OutwardUp
                line->moveIndex++;
                line->state = SPIRAL_OUTWARD_START;
            }
        }
        else
        {
            if (line->state > SPIRAL_INWARD_END)
            {
                // Still spiraling inward, loop back to the first state
                // but use the second set of move targets.
                // For example, the 275 in sRectangularSpiral_Major_InwardRight
                line->moveIndex++;
                line->state = SPIRAL_INWARD_START;
            }
        }
    }
    return TRUE;
}

//----------------------
// B_TRANSITION_GROUDON
//----------------------

#define tTimer data[1]

static void Task_Groudon(u8 taskId)
{
    while (sGroudon_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Groudon_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sGroudon_Tileset, tileset);
    DecompressDataWithHeaderVram(sGroudon_Tilemap, tilemap);

    task->tState++;
    task->tTimer = 0;
    return FALSE;
}

static bool8 Groudon_PaletteFlash(struct Task *task)
{
    if (task->tTimer % 3 == 0)
    {
        u16 offset = (task->tTimer % 30) / 3;
        LoadPalette(&sGroudon1_Palette[offset * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    }
    if (++task->tTimer > 58)
    {
        task->tState++;
        task->tTimer = 0;
    }

    return FALSE;
}

static bool8 Groudon_PaletteBrighten(struct Task *task)
{
    if (task->tTimer % 5 == 0)
    {
        s16 offset = task->tTimer / 5;
        LoadPalette(&sGroudon2_Palette[offset * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    }
    if (++task->tTimer > 68)
    {
        task->tState++;
        task->tTimer = 0;
        task->tEndDelay = 30;
    }

    return FALSE;
}

#undef tTimer
#undef tEndDelay

//-----------------------
// B_TRANSITION_RAYQUAZA
//-----------------------

#define tTimer     data[1]
#define tGrowSpeed data[2] // Shared from B_TRANSITION_BLACKHOLE
#define tFlag      data[7] // Shared from B_TRANSITION_BLACKHOLE

static void Task_Rayquaza(u8 taskId)
{
    while (sRayquaza_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 Rayquaza_Init(struct Task *task)
{
    u16 *tilemap, *tileset;
    u16 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_CHARBASE(2) | BGCNT_SCREENBASE(26) | BGCNT_TXT256x512);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    CpuCopy16(sRayquaza_Tileset, tileset, 0x2000);

    sTransitionData->counter = 0;
    task->tState++;
    LoadPalette(&sRayquaza_Palette[80], BG_PLTT_ID(15), PLTT_SIZE_4BPP);

    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        gScanlineEffectRegBuffers[0][i] = 0;
        gScanlineEffectRegBuffers[1][i] = 0x100;
    }

    SetVBlankCallback(VBlankCB_Rayquaza);
    return FALSE;
}

static bool8 Rayquaza_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuCopy16(sRayquaza_Tilemap, tilemap, sizeof(sRayquaza_Tilemap));
    task->tState++;
    return FALSE;
}

static bool8 Rayquaza_PaletteFlash(struct Task *task)
{
    if ((task->tTimer % 4) == 0)
    {
        u16 value = task->tTimer / 4;
        const u16 *palPtr = &sRayquaza_Palette[(value + 5) * 16];
        LoadPalette(palPtr, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    }
    if (++task->tTimer > 40)
    {
        task->tState++;
        task->tTimer = 0;
    }

    return FALSE;
}

static bool8 Rayquaza_FadeToBlack(struct Task *task)
{
    if (++task->tTimer > 20)
    {
        task->tState++;
        task->tTimer = 0;
        BeginNormalPaletteFade(PALETTES_OBJECTS | (1 << 15), 2, 0, 16, RGB_BLACK);
    }

    return FALSE;
}

static bool8 Rayquaza_WaitFade(struct Task *task)
{
    if (!gPaletteFade.active)
    {
        sTransitionData->counter = 1;
        task->tState++;
    }
    return FALSE;
}

static bool8 Rayquaza_SetBlack(struct Task *task)
{
    BlendPalettes(PALETTES_BG & ~(1 << 15), 8, RGB_BLACK);
    BlendPalettes(PALETTES_OBJECTS | (1 << 15), 0, RGB_BLACK);

    task->tState++;
    return FALSE;
}

static bool8 Rayquaza_TriRing(struct Task *task)
{
    if ((task->tTimer % 3) == 0)
    {
        u16 value = task->tTimer / 3;
        const u16 *palPtr = &sRayquaza_Palette[(value + 0) * 16];
        LoadPalette(palPtr, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    }
    if (++task->tTimer >= 40)
    {
        u16 i;

        sTransitionData->WININ = 0;
        sTransitionData->WINOUT = WINOUT_WIN01_ALL;
        sTransitionData->WIN0H = DISPLAY_WIDTH;
        sTransitionData->WIN0V = DISPLAY_HEIGHT;

        for (i = 0; i < DISPLAY_HEIGHT; i++)
            gScanlineEffectRegBuffers[1][i] = 0;

        SetVBlankCallback(VBlankCB_CircularMask);
        task->tState++;
        task->tGrowSpeed = 1 << 8;
        task->tFlag = FALSE;
        ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG0_ON);
    }

    return FALSE;
}

static void VBlankCB_Rayquaza(void)
{
    void *dmaSrc;

    DmaStop(0);
    VBlankCB_BattleTransition();

    if (sTransitionData->counter == 0)
        dmaSrc = gScanlineEffectRegBuffers[0];
    else if (sTransitionData->counter == 1)
        dmaSrc = gScanlineEffectRegBuffers[1];
    else
        dmaSrc = gScanlineEffectRegBuffers[0];

    DmaSet(0, dmaSrc, &REG_BG0VOFS, B_TRANS_DMA_FLAGS);
}

#undef tTimer
#undef tGrowSpeed
#undef tFlag

//------------------------------
// B_TRANSITION_WHITE_BARS_FADE
//------------------------------

#define sFade            data[0]
#define sFinished        data[1]
#define sDestroyAttempts data[2]
#define sDelay           data[5]
#define sIsMainSprite    data[6]

#define FADE_TARGET (16 << 8)

static void Task_WhiteBarsFade(u8 taskId)
{
    while (sWhiteBarsFade_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 WhiteBarsFade_Init(struct Task *task)
{
    u16 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    sTransitionData->BLDCNT = BLDCNT_TGT1_ALL | BLDCNT_EFFECT_LIGHTEN;
    sTransitionData->BLDY = 0;
    sTransitionData->WININ = WININ_WIN0_BG1 | WININ_WIN0_BG2 | WININ_WIN0_BG3 | WININ_WIN0_OBJ;
    sTransitionData->WINOUT = WINOUT_WIN01_ALL;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        gScanlineEffectRegBuffers[1][i] = 0;
        gScanlineEffectRegBuffers[1][i + DISPLAY_HEIGHT] = DISPLAY_WIDTH;
    }

    EnableInterrupts(INTR_FLAG_HBLANK);
    SetHBlankCallback(HBlankCB_WhiteBarsFade);
    SetVBlankCallback(VBlankCB_WhiteBarsFade);

    task->tState++;
    return FALSE;
}

static bool8 WhiteBarsFade_StartBars(struct Task *task)
{
    s16 i, posY;
    s16 delays[ARRAY_COUNT(sWhiteBarsFade_StartDelays)];
    struct Sprite *sprite;
    memcpy(delays, sWhiteBarsFade_StartDelays, sizeof(sWhiteBarsFade_StartDelays));

    for (i = 0, posY = 0; i < NUM_WHITE_BARS; i++, posY += DISPLAY_HEIGHT / NUM_WHITE_BARS)
    {
        sprite = &gSprites[CreateInvisibleSprite(SpriteCB_WhiteBarFade)];
        sprite->x = DISPLAY_WIDTH;
        sprite->y = posY;
        sprite->sDelay = delays[i];
    }

    // Set on one sprite only. This one will enable the DMA
    // copy in VBlank and wait for the others to destroy.
    sprite->sIsMainSprite++;

    task->tState++;
    return FALSE;
}

static bool8 WhiteBarsFade_WaitBars(struct Task *task)
{
    sTransitionData->VBlank_DMA = 0;
    if (sTransitionData->counter >= NUM_WHITE_BARS)
    {
        BlendPalettes(PALETTES_ALL, 16, RGB_WHITE);
        task->tState++;
    }
    return FALSE;
}

static bool8 WhiteBarsFade_BlendToBlack(struct Task *task)
{
    sTransitionData->VBlank_DMA = 0;

    DmaStop(0);
    SetVBlankCallback(0);
    SetHBlankCallback(0);

    sTransitionData->WIN0H = DISPLAY_WIDTH;
    sTransitionData->BLDY = 0;
    sTransitionData->BLDCNT = 0xFF;
    sTransitionData->WININ = WININ_WIN0_ALL;

    SetVBlankCallback(VBlankCB_WhiteBarsFade_Blend);

    task->tState++;
    return FALSE;
}

static bool8 WhiteBarsFade_End(struct Task *task)
{
   if (++sTransitionData->BLDY > 16)
   {
       FadeScreenBlack();
       DestroyTask(FindTaskIdByFunc(Task_WhiteBarsFade));
   }
   return FALSE;
}

static void VBlankCB_WhiteBarsFade(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    REG_BLDCNT = sTransitionData->BLDCNT;
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 4);
    DmaSet(0, &gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

static void VBlankCB_WhiteBarsFade_Blend(void)
{
    VBlankCB_BattleTransition();
    REG_BLDY = sTransitionData->BLDY;
    REG_BLDCNT = sTransitionData->BLDCNT;
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0H = sTransitionData->WIN0H;
    REG_WIN0V = sTransitionData->WIN0V;
}

static void HBlankCB_WhiteBarsFade(void)
{
    REG_BLDY = gScanlineEffectRegBuffers[1][REG_VCOUNT];
}

static void SpriteCB_WhiteBarFade(struct Sprite *sprite)
{
    if (sprite->sDelay)
    {
        sprite->sDelay--;
        if (sprite->sIsMainSprite)
            sTransitionData->VBlank_DMA = 1;
    }
    else
    {
        u16 i;
        u16 *ptr1 = &gScanlineEffectRegBuffers[0][sprite->y];
        u16 *ptr2 = &gScanlineEffectRegBuffers[0][sprite->y + DISPLAY_HEIGHT];
        for (i = 0; i < DISPLAY_HEIGHT / NUM_WHITE_BARS; i++)
        {
            ptr1[i] = sprite->sFade >> 8;
            ptr2[i] = (u8)sprite->x;
        }
        if (sprite->x == 0 && sprite->sFade == FADE_TARGET)
            sprite->sFinished = TRUE;

        sprite->x -= 16;
        sprite->sFade += FADE_TARGET / 32;

        if (sprite->x < 0)
            sprite->x = 0;
        if (sprite->sFade > FADE_TARGET)
            sprite->sFade = FADE_TARGET;

        if (sprite->sIsMainSprite)
            sTransitionData->VBlank_DMA = 1;

        if (sprite->sFinished)
        {
            // If not the main sprite, destroy self. Otherwise, wait until the
            // others have destroyed themselves, or until enough time has elapsed.
            if (!sprite->sIsMainSprite || (sTransitionData->counter >= NUM_WHITE_BARS - 1 && sprite->sDestroyAttempts++ > 7))
            {
                sTransitionData->counter++;
                DestroySprite(sprite);
            }
        }
    }
}

#undef sFade
#undef sFinished
#undef sDestroyAttempts
#undef sDelay
#undef sIsMainSprite

//---------------------------
// B_TRANSITION_GRID_SQUARES
//---------------------------

#define tDelay       data[1]
#define tShrinkStage data[2]

static void Task_GridSquares(u8 taskId)
{
    while (sGridSquares_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 GridSquares_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuSet(sShrinkingBoxTileset, tileset, 16);
    CpuFill16(0xF0 << 8, tilemap, BG_SCREEN_SIZE);
    LoadPalette(sFieldEffectPal_Pokeball, BG_PLTT_ID(15), sizeof(sFieldEffectPal_Pokeball));

    task->tState++;
    return FALSE;
}

static bool8 GridSquares_Main(struct Task *task)
{
    u16 *tileset;

    if (task->tDelay == 0)
    {
        GetBg0TilemapDst(&tileset);
        task->tDelay = 3;
        task->tShrinkStage++;
        CpuSet(&sShrinkingBoxTileset[task->tShrinkStage * 8], tileset, 16);
        if (task->tShrinkStage > 13)
        {
            task->tState++;
            task->tDelay = 16;
        }
    }

    task->tDelay--;
    return FALSE;
}

static bool8 GridSquares_End(struct Task *task)
{
    if (--task->tDelay == 0)
    {
        FadeScreenBlack();
        DestroyTask(FindTaskIdByFunc(Task_GridSquares));
    }
    return FALSE;
}

#undef tDelay
#undef tShrinkStage

//---------------------------
// B_TRANSITION_ANGLED_WIPES
//---------------------------

#define tWipeId data[1]
#define tDir    data[2]
#define tDelay  data[3]

static void Task_AngledWipes(u8 taskId)
{
    while (sAngledWipes_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 AngledWipes_Init(struct Task *task)
{
    u16 i;

    InitTransitionData();
    ScanlineEffect_Clear();

    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = 0;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[0][i] = DISPLAY_WIDTH;

    CpuSet(gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT);
    SetVBlankCallback(VBlankCB_AngledWipes);

    task->tState++;
    return TRUE;
}

static bool8 AngledWipes_SetWipeData(struct Task *task)
{
    InitBlackWipe(sTransitionData->data,
                  sAngledWipes_MoveData[task->tWipeId][0],
                  sAngledWipes_MoveData[task->tWipeId][1],
                  sAngledWipes_MoveData[task->tWipeId][2],
                  sAngledWipes_MoveData[task->tWipeId][3],
                  1, 1);
    task->tDir = sAngledWipes_MoveData[task->tWipeId][4];
    task->tState++;
    return TRUE;
}

static bool8 AngledWipes_DoWipe(struct Task *task)
{
    s16 i;
    bool8 finished;

    sTransitionData->VBlank_DMA = 0;

    for (i = 0, finished = FALSE; i < 16; i++)
    {
        s16 r3 = gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] >> 8;
        s16 r4 = gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] & 0xFF;
        if (task->tDir == 0)
        {
            // Moving down
            if (r3 < sTransitionData->tWipeCurrX)
                r3 = sTransitionData->tWipeCurrX;
            if (r3 > r4)
                r3 = r4;
        }
        else
        {
            // Moving up
            if (r4 > sTransitionData->tWipeCurrX)
                r4 = sTransitionData->tWipeCurrX;
            if (r4 <= r3)
                r4 = r3;
        }
        gScanlineEffectRegBuffers[0][sTransitionData->tWipeCurrY] = (r4) | (r3 << 8);
        if (finished)
        {
            task->tState++;
            break;
        }
        finished = UpdateBlackWipe(sTransitionData->data, TRUE, TRUE);
    }

    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static bool8 AngledWipes_TryEnd(struct Task *task)
{
    if (++task->tWipeId < NUM_ANGLED_WIPES)
    {
        // Continue with next wipe
        task->tState++;
        task->tDelay = sAngledWipes_EndDelays[task->tWipeId - 1];
        return TRUE;
    }
    else
    {
        // End transition
        DmaStop(0);
        FadeScreenBlack();
        DestroyTask(FindTaskIdByFunc(Task_AngledWipes));
        return FALSE;
    }
}

static bool8 AngledWipes_StartNext(struct Task *task)
{
    if (--task->tDelay == 0)
    {
        // Return to AngledWipes_SetWipeData
        task->tState = 1;
        return TRUE;
    }

    return FALSE;
}

static void VBlankCB_AngledWipes(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    REG_WININ = sTransitionData->WININ;
    REG_WINOUT = sTransitionData->WINOUT;
    REG_WIN0V = sTransitionData->WIN0V;
    REG_WIN0H = gScanlineEffectRegBuffers[1][0];
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_WIN0H, B_TRANS_DMA_FLAGS);
}

#undef tWipeId
#undef tDir
#undef tDelay

//-----------------------------------
// Transition intro
//-----------------------------------

#define tFadeToGrayDelay       data[1]
#define tFadeFromGrayDelay     data[2]
#define tNumFades              data[3]
#define tFadeToGrayIncrement   data[4]
#define tFadeFromGrayIncrement data[5]
#define tDelayTimer            data[6]
#define tBlend                 data[7]
#define tBldCntSaved           data[8]
#define tShadowColor           data[9]

static void CreateIntroTask(s16 fadeToGrayDelay, s16 fadeFromGrayDelay, s16 numFades, s16 fadeToGrayIncrement, s16 fadeFromGrayIncrement)
{
    u8 taskId = CreateTask(Task_BattleTransition_Intro, 3);
    gTasks[taskId].tFadeToGrayDelay = fadeToGrayDelay;
    gTasks[taskId].tFadeFromGrayDelay = fadeFromGrayDelay;
    gTasks[taskId].tNumFades = numFades;
    gTasks[taskId].tFadeToGrayIncrement = fadeToGrayIncrement;
    gTasks[taskId].tFadeFromGrayIncrement = fadeFromGrayIncrement;
    gTasks[taskId].tDelayTimer = fadeToGrayDelay;
}

static bool8 IsIntroTaskDone(void)
{
    if (FindTaskIdByFunc(Task_BattleTransition_Intro) == TASK_NONE)
        return TRUE;
    else
        return FALSE;
}

void Task_BattleTransition_Intro(u8 taskId)
{
    while (sTransitionIntroFuncs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 TransitionIntro_FadeToGray(struct Task *task)
{
    u8 paletteNum = IndexOfSpritePaletteTag(TAG_WEATHER_START);
    u16 index = OBJ_PLTT_ID(paletteNum) + SHADOW_COLOR_INDEX;
    if (task->tDelayTimer == 0 || --task->tDelayTimer == 0)
    {
        task->tDelayTimer = task->tFadeToGrayDelay;
        task->tBlend += task->tFadeToGrayIncrement;
        if (task->tBlend > 16)
            task->tBlend = 16;
        if (paletteNum < 16)
            task->tShadowColor = gPlttBufferFaded[index];
        BlendPalettes(PALETTES_ALL, task->tBlend, RGB(11, 11, 11));
        if (paletteNum < 16)
            gPlttBufferFaded[index] = task->tShadowColor;
    }
    if (task->tBlend >= 16)
    {
        // Fade to gray complete, start fade back
        // Save BLDCNT and turn off targets temporarily
        task->tBldCntSaved = GetGpuReg(REG_OFFSET_BLDCNT);
        SetGpuReg(REG_OFFSET_BLDCNT, task->tBldCntSaved & ~BLDCNT_TGT2_BG_ALL);
        if (paletteNum < 16)
            gPlttBufferFaded[index] = RGB(11, 11, 11);
        task->tState++;
        task->tDelayTimer = task->tFadeFromGrayDelay;
    }
    return FALSE;
}

static bool8 TransitionIntro_FadeFromGray(struct Task *task)
{
    if (task->tDelayTimer == 0 || --task->tDelayTimer == 0)
    {
        u8 paletteNum = IndexOfSpritePaletteTag(TAG_WEATHER_START);
        task->tDelayTimer = task->tFadeFromGrayDelay;
        task->tBlend -= task->tFadeFromGrayIncrement;
        if (task->tBlend < 0)
            task->tBlend = 0;
        BlendPalettes(PALETTES_ALL, task->tBlend, RGB(11, 11, 11));
        // Restore BLDCNT
        SetGpuReg(REG_OFFSET_BLDCNT, task->tBldCntSaved);
        if (paletteNum < 16)
        {
            u16 index = OBJ_PLTT_ID(paletteNum) + SHADOW_COLOR_INDEX;
            gPlttBufferFaded[index] = task->tShadowColor;
        }
    }
    if (task->tBlend == 0)
    {
        if (--task->tNumFades == 0)
        {
            // All fades done, end intro
            DestroyTask(FindTaskIdByFunc(Task_BattleTransition_Intro));
        }
        else
        {
            // Fade from gray complete, start new fade
            task->tDelayTimer = task->tFadeToGrayDelay;
            task->tState = 0;
        }
    }
    return FALSE;
}

#undef tFadeToGrayDelay
#undef tFadeFromGrayDelay
#undef tNumFades
#undef tFadeToGrayIncrement
#undef tFadeFromGrayIncrement
#undef tDelayTimer
#undef tBlend

//-----------------------------------
// General transition functions
//-----------------------------------

static void InitTransitionData(void)
{
    memset(sTransitionData, 0, sizeof(*sTransitionData));
    GetCameraOffsetWithPan(&sTransitionData->cameraX, &sTransitionData->cameraY);
}

static void VBlankCB_BattleTransition(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void GetBg0TilemapDst(u16 **tileset)
{
    u16 charBase = REG_BG0CNT >> 2;
    charBase <<= 14;
    *tileset = (u16 *)(BG_VRAM + charBase);
}

void GetBg0TilesDst(u16 **tilemap, u16 **tileset)
{
    u16 screenBase = REG_BG0CNT >> 8;
    u16 charBase = REG_BG0CNT >> 2;

    screenBase <<= 11;
    charBase <<= 14;

    *tilemap = (u16 *)(BG_VRAM + screenBase);
    *tileset = (u16 *)(BG_VRAM + charBase);
}

static void FadeScreenBlack(void)
{
    BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
}

static void SetSinWave(s16 *array, s16 sinAdd, s16 index, s16 indexIncrementer, s16 amplitude, s16 arrSize)
{
    u8 i;
    for (i = 0; arrSize > 0; arrSize--, i++, index += indexIncrementer)
        array[i] = sinAdd + Sin(index & 0xFF, amplitude);
}

static void SetCircularMask(u16 *buffer, s16 centerX, s16 centerY, s16 radius)
{
    s16 i;

    memset(buffer, 10, DISPLAY_HEIGHT * sizeof(u16));
    for (i = 0; i < 64; i++)
    {
        s16 sinResult, cosResult;
        s16 drawXLeft, drawYBottNext, drawYTopNext, drawX, drawYTop, drawYBott;

        sinResult = Sin(i, radius);
        cosResult = Cos(i, radius);

        drawXLeft = centerX - sinResult;
        drawX = centerX + sinResult;
        drawYTop = centerY - cosResult;
        drawYBott = centerY + cosResult;

        if (drawXLeft < 0)
            drawXLeft = 0;
        if (drawX > DISPLAY_WIDTH)
            drawX = DISPLAY_WIDTH;
        if (drawYTop < 0)
            drawYTop = 0;
        if (drawYBott > DISPLAY_HEIGHT - 1)
            drawYBott = DISPLAY_HEIGHT - 1;

        drawX |= (drawXLeft << 8);
        buffer[drawYTop] = drawX;
        buffer[drawYBott] = drawX;

        cosResult = Cos(i + 1, radius);
        drawYTopNext = centerY - cosResult;
        drawYBottNext = centerY + cosResult;

        if (drawYTopNext < 0)
            drawYTopNext = 0;
        if (drawYBottNext > DISPLAY_HEIGHT - 1)
            drawYBottNext = DISPLAY_HEIGHT - 1;

        while (drawYTop > drawYTopNext)
            buffer[--drawYTop] = drawX;
        while (drawYTop < drawYTopNext)
            buffer[++drawYTop] = drawX;

        while (drawYBott > drawYBottNext)
            buffer[--drawYBott] = drawX;
        while (drawYBott < drawYBottNext)
            buffer[++drawYBott] = drawX;
    }
}

static void InitBlackWipe(s16 *data, s16 startX, s16 startY, s16 endX, s16 endY, s16 xMove, s16 yMove)
{
    tWipeStartX = startX;
    tWipeStartY = startY;
    tWipeCurrX = startX;
    tWipeCurrY = startY;
    tWipeEndX = endX;
    tWipeEndY = endY;
    tWipeXMove = xMove;
    tWipeYMove = yMove;
    tWipeXDist = endX - startX;
    if (tWipeXDist < 0)
    {
        // If end was less than start, reverse direction
        tWipeXDist = -tWipeXDist;
        tWipeXMove = -xMove;
    }
    tWipeYDist = endY - startY;
    if (tWipeYDist < 0)
    {
        // If end was less than start, reverse direction
        tWipeYDist = -tWipeYDist;
        tWipeYMove = -yMove;
    }
    tWipeTemp = 0;
}

static bool8 UpdateBlackWipe(s16 *data, bool8 xExact, bool8 yExact)
{
    u8 numFinished;

    if (tWipeXDist > tWipeYDist)
    {
        // X has further to move, move it first
        tWipeCurrX += tWipeXMove;

        // If it has been far enough since Y's
        // last move then move it too
        tWipeTemp += tWipeYDist;
        if (tWipeTemp > tWipeXDist)
        {
            tWipeCurrY += tWipeYMove;
            tWipeTemp -= tWipeXDist;
        }
    }
    else
    {
        // Y has further to move, move it first
        tWipeCurrY += tWipeYMove;

        // If it has been far enough since X's
        // last move then move it too
        tWipeTemp += tWipeXDist;
        if (tWipeTemp > tWipeYDist)
        {
            tWipeCurrX += tWipeXMove;
            tWipeTemp -= tWipeYDist;
        }
    }

    numFinished = 0;

    // Has X coord reached end?
    if ((tWipeXMove > 0 && tWipeCurrX >= tWipeEndX)
     || (tWipeXMove < 0 && tWipeCurrX <= tWipeEndX))
    {
        numFinished++;
        if (xExact)
            tWipeCurrX = tWipeEndX;
    }

    // Has Y coord reached end?
    if ((tWipeYMove > 0 && tWipeCurrY >= tWipeEndY)
     || (tWipeYMove < 0 && tWipeCurrY <= tWipeEndY))
    {
        numFinished++;
        if (yExact)
            tWipeCurrY = tWipeEndY;
    }

    // Return TRUE if both coords have reached end
    if (numFinished == 2)
        return TRUE;
    else
        return FALSE;
}

//-----------------------------------
// B_TRANSITION_FRONTIER_LOGO_WIGGLE
//-----------------------------------

#define tSinIndex  data[4]
#define tAmplitude data[5]

static bool8 FrontierLogoWiggle_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    InitPatternWeaveTransition(task);
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sFrontierLogo_Tileset, tileset);
    LoadPalette(sFrontierLogo_Palette, BG_PLTT_ID(15), sizeof(sFrontierLogo_Palette));

    task->tState++;
    return FALSE;
}

static bool8 FrontierLogoWiggle_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sFrontierLogo_Tilemap, tilemap);
    SetSinWave((s16*)gScanlineEffectRegBuffers[0], 0, task->tSinIndex, 132, task->tAmplitude, DISPLAY_HEIGHT);

    task->tState++;
    return TRUE;
}

static void Task_FrontierLogoWiggle(u8 taskId)
{
    while (sFrontierLogoWiggle_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

#undef tSinIndex
#undef tAmplitude

//---------------------------------
// B_TRANSITION_FRONTIER_LOGO_WAVE
//---------------------------------

#define tSinVal       data[1]
#define tAmplitudeVal data[2]
#define tTimer        data[3]
#define tStartedFade  data[4]
#define tBlendTarget2 data[5]
#define tBlendTarget1 data[6]
#define tSinDecrement data[7]

static void Task_FrontierLogoWave(u8 taskId)
{
    while (sFrontierLogoWave_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 FrontierLogoWave_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    InitTransitionData();
    ScanlineEffect_Clear();
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
    task->tAmplitudeVal = 32 << 8;
    task->tSinVal = 0x7FFF;
    task->tBlendTarget2 = 0;
    task->tBlendTarget1 = 16;
    task->tSinDecrement = 2560;
    sTransitionData->BLDCNT = BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_ALL;
    sTransitionData->BLDALPHA = BLDALPHA_BLEND(task->tBlendTarget2, task->tBlendTarget1);
    REG_BLDCNT = sTransitionData->BLDCNT;
    REG_BLDALPHA = sTransitionData->BLDALPHA;
    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sFrontierLogo_Tileset, tileset);
    LoadPalette(sFrontierLogo_Palette, BG_PLTT_ID(15), sizeof(sFrontierLogo_Palette));
    sTransitionData->cameraY = 0;
    UpdateShadowColor(RGB_GRAY);

    task->tState++;
    return FALSE;
}

static bool8 FrontierLogoWave_SetGfx(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sFrontierLogo_Tilemap, tilemap);

    task->tState++;
    return TRUE;
}

static bool8 FrontierLogoWave_InitScanline(struct Task *task)
{
    u8 i;

    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[1][i] = sTransitionData->cameraY;

    SetVBlankCallback(VBlankCB_FrontierLogoWave);
    SetHBlankCallback(HBlankCB_FrontierLogoWave);
    EnableInterrupts(INTR_FLAG_HBLANK);

    task->tState++;
    return TRUE;
}

static bool8 FrontierLogoWave_Main(struct Task *task)
{
    u8 i;
    u16 sinVal, amplitude, sinSpread;

    sTransitionData->VBlank_DMA = FALSE;

    amplitude = task->tAmplitudeVal >> 8;
    sinVal = task->tSinVal;
    sinSpread = 384;

    task->tSinVal -= task->tSinDecrement;

    if (task->tTimer >= 70)
    {
        // Decrease amount of logo movement and distortion
        // until it rests normally in the middle of the screen.
        if (task->tAmplitudeVal - 384 >= 0)
            task->tAmplitudeVal -= 384;
        else
            task->tAmplitudeVal = 0;
    }

    if (task->tTimer >= 0 && task->tTimer % 3 == 0)
    {
        // Blend logo into view
        if (task->tBlendTarget2 < 16)
            task->tBlendTarget2++;
        else if (task->tBlendTarget1 > 0)
            task->tBlendTarget1--;

        sTransitionData->BLDALPHA = BLDALPHA_BLEND(task->tBlendTarget2, task->tBlendTarget1);
    }

    // Move logo up and down and distort it
    for (i = 0; i < DISPLAY_HEIGHT; i++, sinVal += sinSpread)
    {
        s16 index = sinVal / 256;
        gScanlineEffectRegBuffers[0][i] = sTransitionData->cameraY + Sin(index & 0xff, amplitude);
    }

    if (++task->tTimer == 101)
    {
        task->tStartedFade++;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }

    if (task->tStartedFade && !gPaletteFade.active)
        DestroyTask(FindTaskIdByFunc(Task_FrontierLogoWave));

    task->tSinDecrement -= 17;
    sTransitionData->VBlank_DMA++;
    return FALSE;
}

static void VBlankCB_FrontierLogoWave(void)
{
    VBlankCB_BattleTransition();
    REG_BLDCNT = sTransitionData->BLDCNT;
    REG_BLDALPHA = sTransitionData->BLDALPHA;

    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
}

static void HBlankCB_FrontierLogoWave(void)
{
    u16 var = gScanlineEffectRegBuffers[1][REG_VCOUNT];
    REG_BG0VOFS = var;
}

#undef tSinVal
#undef tAmplitudeVal
#undef tTimer
#undef tStartedFade
#undef tBlendTarget2
#undef tBlendTarget1
#undef tSinDecrement

//----------------------------------------------------------------------
// B_TRANSITION_FRONTIER_SQUARES, B_TRANSITION_FRONTIER_SQUARES_SCROLL,
// and B_TRANSITION_FRONTIER_SQUARES_SPIRAL
//----------------------------------------------------------------------

#define tPosX             data[2]
#define tPosY             data[3]
#define tRowPos           data[4]
#define tShrinkState      data[5]
#define tShrinkDelayTimer data[6]
#define tShrinkDelay      data[7]

static void Task_FrontierSquares(u8 taskId)
{
    while (sFrontierSquares_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_FrontierSquaresSpiral(u8 taskId)
{
    while (sFrontierSquaresSpiral_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static void Task_FrontierSquaresScroll(u8 taskId)
{
    while (sFrontierSquaresScroll_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

static bool8 FrontierSquares_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sFrontierSquares_FilledBg_Tileset, tileset);

    FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, 32, 32);
    FillBgTilemapBufferRect(0, 1, 0, 0, MARGIN_SIZE, 32, 15);
    FillBgTilemapBufferRect(0, 1, 30 - MARGIN_SIZE, 0, MARGIN_SIZE, 32, 15);
    CopyBgTilemapBufferToVram(0);
    LoadPalette(sFrontierSquares_Palette, BG_PLTT_ID(15), sizeof(sFrontierSquares_Palette));

    task->tPosX = MARGIN_SIZE;
    task->tPosY = 0;
    task->tRowPos = 0;
    task->tShrinkDelay = 10;

    task->tState++;
    return FALSE;
}

static bool8 FrontierSquares_Draw(struct Task *task)
{
    CopyRectToBgTilemapBufferRect(0, sFrontierSquares_Tilemap, 0, 0,
                                  SQUARE_SIZE, SQUARE_SIZE,
                                  task->tPosX, task->tPosY,
                                  SQUARE_SIZE, SQUARE_SIZE,
                                  15, 0, 0);
    CopyBgTilemapBufferToVram(0);

    task->tPosX += SQUARE_SIZE;
    if (++task->tRowPos == NUM_SQUARES_PER_ROW)
    {
        task->tPosX = MARGIN_SIZE;
        task->tPosY += SQUARE_SIZE;
        task->tRowPos = 0;
        if (task->tPosY >= NUM_SQUARES_PER_COL * SQUARE_SIZE)
            task->tState++;
    }

    return FALSE;
}

static bool8 FrontierSquares_Shrink(struct Task *task)
{
    u8 i;
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    if (task->tShrinkDelayTimer++ >= task->tShrinkDelay)
    {
        switch (task->tShrinkState)
        {
        case 0:
            for (i = BG_PLTT_ID(15) + 10; i < BG_PLTT_ID(15) + 15; i++)
            {
                gPlttBufferUnfaded[i] = RGB_BLACK;
                gPlttBufferFaded[i] = RGB_BLACK;
            }
            break;
        case 1:
            BlendPalettes(PALETTES_ALL & ~(1 << 15), 16, RGB_BLACK);
            DecompressDataWithHeaderVram(sFrontierSquares_EmptyBg_Tileset, tileset);
            break;
        case 2:
            DecompressDataWithHeaderVram(sFrontierSquares_Shrink1_Tileset, tileset);
            break;
        case 3:
            DecompressDataWithHeaderVram(sFrontierSquares_Shrink2_Tileset, tileset);
            break;
        default:
            FillBgTilemapBufferRect_Palette0(0, 1, 0, 0, 32, 32);
            CopyBgTilemapBufferToVram(0);
            task->tState++;
            return FALSE;
        }

        task->tShrinkDelayTimer = 0;
        task->tShrinkState++;
    }

    return FALSE;
}

#undef tPosX
#undef tPosY
#undef tRowPos
#undef tShrinkState
#undef tShrinkDelayTimer
#undef tShrinkDelay

#define tSquareNum data[2]
#define tFadeFlag  data[3]

static bool8 FrontierSquaresSpiral_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sFrontierSquares_FilledBg_Tileset, tileset);

    FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, 32, 32);
    FillBgTilemapBufferRect(0, 1, 0, 0, MARGIN_SIZE, 32, 15);
    FillBgTilemapBufferRect(0, 1, 30 - MARGIN_SIZE, 0, MARGIN_SIZE, 32, 15);
    CopyBgTilemapBufferToVram(0);
    LoadPalette(sFrontierSquares_Palette, BG_PLTT_ID(14), sizeof(sFrontierSquares_Palette));
    LoadPalette(sFrontierSquares_Palette, BG_PLTT_ID(15), sizeof(sFrontierSquares_Palette));
    BlendPalette(BG_PLTT_ID(14), 16, 8, RGB_BLACK);

    task->tSquareNum = NUM_SQUARES - 1;
    task->tFadeFlag = 0;

    task->tState++;
    return FALSE;
}

static bool8 FrontierSquaresSpiral_Outward(struct Task *task)
{
    u8 pos = sFrontierSquaresSpiral_Positions[task->tSquareNum];
    u8 x = pos % NUM_SQUARES_PER_ROW;
    u8 y = pos / NUM_SQUARES_PER_ROW;
    CopyRectToBgTilemapBufferRect(0, sFrontierSquares_Tilemap, 0, 0,
                                  SQUARE_SIZE, SQUARE_SIZE,
                                  SQUARE_SIZE * x + MARGIN_SIZE, SQUARE_SIZE * y,
                                  SQUARE_SIZE, SQUARE_SIZE,
                                  15, 0, 0);
    CopyBgTilemapBufferToVram(0);

    if (--task->tSquareNum < 0)
        task->tState++;
    return FALSE;
}

// Now that the overworld is completely covered by the squares,
// set it to black so it's not revealed when the squares are removed.
static bool8 FrontierSquaresSpiral_SetBlack(struct Task *task)
{
    BlendPalette(BG_PLTT_ID(14), 16, 3, RGB_BLACK);
    BlendPalettes(PALETTES_ALL & ~(1 << 15 | 1 << 14), 16, RGB_BLACK);

    task->tSquareNum = 0;
    task->tFadeFlag = 0;

    task->tState++;
    return FALSE;
}

// Spiral inward erasing the squares
static bool8 FrontierSquaresSpiral_Inward(struct Task *task)
{
    // Each square is faded first, then the one that was faded last move is erased.
    if (task->tFadeFlag ^= 1)
    {
        // Shade square
        CopyRectToBgTilemapBufferRect(0, sFrontierSquares_Tilemap, 0, 0,
                                      SQUARE_SIZE, SQUARE_SIZE,
                                      SQUARE_SIZE * (sFrontierSquaresSpiral_Positions[task->tSquareNum] % NUM_SQUARES_PER_ROW) + MARGIN_SIZE,
                                      SQUARE_SIZE * (sFrontierSquaresSpiral_Positions[task->tSquareNum] / NUM_SQUARES_PER_ROW),
                                      SQUARE_SIZE, SQUARE_SIZE,
                                      14, 0, 0);
    }
    else
    {
        if (task->tSquareNum > 0)
        {
            // Erase square
            FillBgTilemapBufferRect(0, 1,
                                    SQUARE_SIZE * (sFrontierSquaresSpiral_Positions[task->tSquareNum - 1] % NUM_SQUARES_PER_ROW) + MARGIN_SIZE,
                                    SQUARE_SIZE * (sFrontierSquaresSpiral_Positions[task->tSquareNum - 1] / NUM_SQUARES_PER_ROW),
                                    SQUARE_SIZE, SQUARE_SIZE,
                                    15);
        }
        task->tSquareNum++;
    }

    if (task->tSquareNum >= NUM_SQUARES)
        task->tState++;

    CopyBgTilemapBufferToVram(0);
    return FALSE;
}

static bool8 FrontierSquares_End(struct Task *task)
{
    FillBgTilemapBufferRect_Palette0(0, 1, 0, 0, 32, 32);
    CopyBgTilemapBufferToVram(0);
    BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
    DestroyTask(FindTaskIdByFunc(task->func));
    return FALSE;
}

#undef tSquareNum
#undef tFadeFlag

#define tScrollXDir       data[0]
#define tScrollYDir       data[1]
#define tScrollUpdateFlag data[2]

#define tSquareNum        data[2]

static void Task_ScrollBg(u8 taskId)
{
    if (!(gTasks[taskId].tScrollUpdateFlag ^= 1))
    {
        SetGpuReg(REG_OFFSET_BG0VOFS, gBattle_BG0_X);
        SetGpuReg(REG_OFFSET_BG0HOFS, gBattle_BG0_Y);
        gBattle_BG0_X += gTasks[taskId].tScrollXDir;
        gBattle_BG0_Y += gTasks[taskId].tScrollYDir;
    }
}

static bool8 FrontierSquaresScroll_Init(struct Task *task)
{
    u8 taskId = 0;
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(sFrontierSquares_FilledBg_Tileset, tileset);
    FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, 32, 32);
    CopyBgTilemapBufferToVram(0);
    LoadPalette(sFrontierSquares_Palette, BG_PLTT_ID(15), sizeof(sFrontierSquares_Palette));

    gBattle_BG0_X = 0;
    gBattle_BG0_Y = 0;
    SetGpuReg(REG_OFFSET_BG0VOFS, gBattle_BG0_X);
    SetGpuReg(REG_OFFSET_BG0HOFS, gBattle_BG0_Y);

    task->tSquareNum = 0;

    // Start scrolling bg in a random direction.
    taskId = CreateTask(Task_ScrollBg, 1);
    switch (Random() % 4)
    {
    case 0: // Down/right
        gTasks[taskId].tScrollXDir = 1;
        gTasks[taskId].tScrollYDir = 1;
        break;
    case 1: // Up/left
        gTasks[taskId].tScrollXDir = -1;
        gTasks[taskId].tScrollYDir = -1;
        break;
    case 2: // Up/right
        gTasks[taskId].tScrollXDir = 1;
        gTasks[taskId].tScrollYDir = -1;
        break;
    default: // Down/left
        gTasks[taskId].tScrollXDir = -1;
        gTasks[taskId].tScrollYDir = 1;
        break;
    }

    task->tState++;
    return FALSE;
}

static bool8 FrontierSquaresScroll_Draw(struct Task *task)
{
    u8 pos = sFrontierSquaresScroll_Positions[task->tSquareNum];
    u8 x = pos / (NUM_SQUARES_PER_ROW + 1); // +1 because during scroll an additional column covers the margin.
    u8 y = pos % (NUM_SQUARES_PER_ROW + 1);

    CopyRectToBgTilemapBufferRect(0, &sFrontierSquares_Tilemap, 0, 0,
                                  SQUARE_SIZE, SQUARE_SIZE,
                                  SQUARE_SIZE * x + MARGIN_SIZE, SQUARE_SIZE * y,
                                  SQUARE_SIZE, SQUARE_SIZE,
                                  15, 0, 0);
    CopyBgTilemapBufferToVram(0);

    if (++task->tSquareNum >= (int)ARRAY_COUNT(sFrontierSquaresScroll_Positions))
        task->tState++;
    return 0;
}

// Now that the overworld is completely covered by the squares,
// set it to black so it's not revealed when the squares are removed.
static bool8 FrontierSquaresScroll_SetBlack(struct Task *task)
{
    BlendPalettes(PALETTES_ALL & ~(1 << 15), 16, RGB_BLACK);

    task->tSquareNum = 0;

    task->tState++;
    return FALSE;
}

static bool8 FrontierSquaresScroll_Erase(struct Task *task)
{
    u8 pos = sFrontierSquaresScroll_Positions[task->tSquareNum];
    u8 x = pos / (NUM_SQUARES_PER_ROW + 1);
    u8 y = pos % (NUM_SQUARES_PER_ROW + 1);

    FillBgTilemapBufferRect(0, 1,
                            SQUARE_SIZE * x + MARGIN_SIZE, SQUARE_SIZE * y,
                            SQUARE_SIZE, SQUARE_SIZE,
                            15);
    CopyBgTilemapBufferToVram(0);

    if (++task->tSquareNum >= (int)ARRAY_COUNT(sFrontierSquaresScroll_Positions))
    {
        DestroyTask(FindTaskIdByFunc(Task_ScrollBg));
        task->tState++;
    }

    return FALSE;
}

static bool8 FrontierSquaresScroll_End(struct Task *task)
{
    gBattle_BG0_X = 0;
    gBattle_BG0_Y = 0;
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BG0HOFS, gBattle_BG0_Y);

    FillBgTilemapBufferRect_Palette0(0, 1, 0, 0, 32, 32);
    CopyBgTilemapBufferToVram(0);
    BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);

    DestroyTask(FindTaskIdByFunc(task->func));
    task->tState++; // Changing value of a destroyed task

    return FALSE;
}

#undef tScrollXDir
#undef tScrollYDir
#undef tScrollUpdateFlag
#undef tSquareNum

//------------------------------------------------------------------------
// Project Grounded: B_TRANSITION_AURORA (Suicune)
// Het scherm wordt donker, er verschijnen noorderlichtgordijnen die glinsteren en van kleur verschuiven
// (groen -> cyaan -> paars), licht dat zachtjes wiegt, en dan oplicht tot wit vlak voor het gevecht.
//------------------------------------------------------------------------
#define AURORA_FRAMES  16
#define tAuroraTimer   data[1]
#define tAuroraDelay   data[8]

static bool8 Aurora_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sAurora_Tileset, tileset);
    CpuCopy16(sAurora_Tilemap, tilemap, sizeof(sAurora_Tilemap));
    LoadPalette(sAurora_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    task->tAuroraTimer = 0;
    task->tState++;
    return FALSE;
}

static void Aurora_LoadFrame(struct Task *task)
{
    u32 frame = (task->tAuroraTimer / 3) % AURORA_FRAMES;
    LoadPalette(&sAurora_Palette[frame * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    SetGpuReg(REG_OFFSET_BG0HOFS, Sin((task->tAuroraTimer * 3) & 0xFF, 6));
}

static bool8 Aurora_Shimmer(struct Task *task)
{
    Aurora_LoadFrame(task);
    if (++task->tAuroraTimer > 84)
        task->tState++;
    return FALSE;
}

static bool8 Aurora_Brighten(struct Task *task)
{
    static u8 sStep;
    if (task->tAuroraTimer == 85)
        sStep = 0;
    Aurora_LoadFrame(task);
    BlendPalette(BG_PLTT_ID(15), 16, min(sStep, 16), RGB_WHITE);
    if ((task->tAuroraTimer & 1) == 0 && sStep < 16)
        sStep++;
    task->tAuroraTimer++;
    if (sStep >= 16)
    {
        // wit vastzetten, zodat het uitfaden van wit naar zwart gaat (en de kleuren niet terugkomen)
        CpuFill16(RGB_WHITE, &gPlttBufferUnfaded[BG_PLTT_ID(15)], PLTT_SIZE_4BPP);
        CpuFill16(RGB_WHITE, &gPlttBufferFaded[BG_PLTT_ID(15)], PLTT_SIZE_4BPP);
        task->tAuroraDelay = 6; // Project Grounded: korter wit vasthouden (was 12)
        task->tState++;
    }
    return FALSE;
}

static const TransitionStateFunc sAurora_Funcs[] =
{
    WeatherTrio_BgFadeBlack,
    WeatherTrio_WaitFade,
    Aurora_Init,
    Aurora_Shimmer,
    Aurora_Brighten,
    FramesCountdown,
    WeatherDuo_FadeOut,
    WeatherDuo_End
};

static void Task_Aurora(u8 taskId)
{
    while (sAurora_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

#undef tAuroraTimer
#undef tAuroraDelay

//------------------------------------------------------------------------
// Project Grounded: B_TRANSITION_DEOXYS
// Het scherm wordt zwart; een sterrenhemel met een draaiende DNA-dubbelhelix (oranje/cyaan) komt op
// en schiet steeds sneller voorbij (warp), tot alles wit oplicht vlak voor het gevecht.
//------------------------------------------------------------------------
#define DEOXYS_FRAMES  8
#define tDeoxysTimer   data[1]
#define tDeoxysSpeed   data[2]
#define tDeoxysScroll  data[3]
#define tDeoxysDelay   data[8]

static bool8 Deoxys_FadeAllBlack(struct Task *task)
{
    // ook de overworld-sprites, anders zweven de speler en NPC's door de ruimte
    BeginNormalPaletteFade(PALETTES_ALL, 1, 0, 16, RGB_BLACK);
    task->tState++;
    return FALSE;
}

static bool8 Deoxys_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    CpuCopy16(sDeoxys_Tileset, tileset, sizeof(sDeoxys_Tileset));
    CpuCopy16(sDeoxys_Tilemap, tilemap, sizeof(sDeoxys_Tilemap));
    LoadPalette(sDeoxys_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    BlendPalette(BG_PLTT_ID(15), 16, 16, RGB_BLACK);
    task->tDeoxysTimer = 0;
    task->tDeoxysSpeed = 16; // in 1/16 pixel per frame
    task->tDeoxysScroll = 0;
    task->tState++;
    return FALSE;
}

static void Deoxys_Update(struct Task *task, u32 fade, u16 color)
{
    u32 frame = (task->tDeoxysTimer / 4) % DEOXYS_FRAMES;
    LoadPalette(&sDeoxys_Palette[frame * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    if (fade)
        BlendPalette(BG_PLTT_ID(15), 16, fade, color);
    task->tDeoxysScroll += task->tDeoxysSpeed;
    SetGpuReg(REG_OFFSET_BG0HOFS, (task->tDeoxysScroll >> 4) & 0xFF);
    SetGpuReg(REG_OFFSET_BG0VOFS, Sin((task->tDeoxysTimer * 4) & 0xFF, 3));
    task->tDeoxysTimer++;
}

static bool8 Deoxys_Warp(struct Task *task)
{
    // eerst invaden uit het zwart, daarna steeds sneller
    u32 fade = task->tDeoxysTimer < 32 ? 16 - task->tDeoxysTimer / 2 : 0;
    if (task->tDeoxysTimer > 30 && task->tDeoxysSpeed < 16 * 12)
        task->tDeoxysSpeed += 3;
    Deoxys_Update(task, fade, RGB_BLACK);
    if (task->tDeoxysTimer > 100)
        task->tState++;
    return FALSE;
}

static bool8 Deoxys_Flash(struct Task *task)
{
    static u8 sStep;
    if (task->tDeoxysTimer == 101)
        sStep = 0;
    Deoxys_Update(task, min(sStep, 16), RGB_WHITE);
    if ((task->tDeoxysTimer & 1) == 0 && sStep < 16)
        sStep++;
    if (sStep >= 16)
    {
        CpuFill16(RGB_WHITE, &gPlttBufferUnfaded[BG_PLTT_ID(15)], PLTT_SIZE_4BPP);
        CpuFill16(RGB_WHITE, &gPlttBufferFaded[BG_PLTT_ID(15)], PLTT_SIZE_4BPP);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        task->tDeoxysDelay = 6; // Project Grounded: korter wit vasthouden (was 12)
        task->tState++;
    }
    return FALSE;
}

static const TransitionStateFunc sDeoxys_Funcs[] =
{
    Deoxys_FadeAllBlack,
    WeatherTrio_WaitFade,
    Deoxys_Init,
    Deoxys_Warp,
    Deoxys_Flash,
    FramesCountdown,
    WeatherDuo_FadeOut,
    WeatherDuo_End
};

static void Task_Deoxys(u8 taskId)
{
    while (sDeoxys_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

#undef tDeoxysTimer
#undef tDeoxysSpeed
#undef tDeoxysScroll
#undef tDeoxysDelay

//------------------------------------------------------------------------
// Project Grounded: B_TRANSITION_BIRCH
// Bruine prut druipt van boven over het beeld (de sprites kleuren mee bruin), daarna fade naar zwart.
// Tiles: zie tools/grounded/birch_transition.py.
//------------------------------------------------------------------------
#define BIRCH_TILE_SOLID   1
#define BIRCH_TILE_EDGE    5
#define BIRCH_EDGE_ROWS    4
#define BIRCH_TILE(t)      ((15 << 12) | (t))

#define tBirchTimer   data[1]
#define tBirchPos     data[2]  // hoe ver de prut gezakt is, in 1/16 pixel
#define tBirchSpeed   data[3]
#define tBirchDelay   data[8]

static u16 Birch_SolidTile(s32 row, s32 col)
{
    // vast patroon per inhoudsrij, zodat de spikkels mee zakken in plaats van te verspringen
    u32 hash = (u32)(row * 7 + col * 13 + row * col * 5) & 31;
    if (hash == 0)
        return BIRCH_TILE(BIRCH_TILE_SOLID + 3); // af en toe een maiskorrel
    return BIRCH_TILE(BIRCH_TILE_SOLID + hash % 3);
}

static void Birch_DrawCurtain(struct Task *task)
{
    u16 *tilemap, *tileset;
    s32 p = task->tBirchPos >> 4;
    s32 q = p / 8, m = p % 8;
    s32 r, c;

    GetBg0TilesDst(&tilemap, &tileset);
    for (r = 0; r < 21; r++)
    {
        s32 contentRow = r - q - (m > 0);
        for (c = 0; c < 32; c++)
        {
            u16 tile;
            if (contentRow >= 0)
                tile = 0;
            else if (contentRow >= -BIRCH_EDGE_ROWS)
                tile = BIRCH_TILE(BIRCH_TILE_EDGE + (contentRow + BIRCH_EDGE_ROWS) * 8 + (c % 8));
            else
                tile = Birch_SolidTile(contentRow, c);
            tilemap[r * 32 + c] = tile;
        }
    }
    SetGpuReg(REG_OFFSET_BG0VOFS, (8 - m) % 8);
}

static bool8 Birch_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    CpuCopy16(sBirch_Tileset, tileset, sizeof(sBirch_Tileset));
    LoadPalette(sBirch_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    // de sprites (speler, Birch) kleuren mee bruin terwijl de prut over het beeld zakt
    BeginNormalPaletteFade(PALETTES_OBJECTS, 3, 0, 16, RGB(13, 8, 3));
    task->tBirchTimer = 0;
    task->tBirchPos = 0;
    task->tBirchSpeed = 8;
    PlaySE(SE_MUD_BALL);
    task->tState++;
    return FALSE;
}

static bool8 Birch_Drip(struct Task *task)
{
    // stroperig: soms bijna stil, dan weer een klodder
    if ((task->tBirchTimer & 15) < 10)
        task->tBirchSpeed += 3;
    else if (task->tBirchSpeed > 12)
        task->tBirchSpeed -= 4;
    task->tBirchPos += task->tBirchSpeed;
    task->tBirchTimer++;
    Birch_DrawCurtain(task);
    if ((task->tBirchPos >> 4) >= DISPLAY_HEIGHT + BIRCH_EDGE_ROWS * 8 + 8)
    {
        u16 *tilemap, *tileset;
        s32 r, c;

        GetBg0TilesDst(&tilemap, &tileset);
        for (r = 0; r < 32; r++)
            for (c = 0; c < 32; c++)
                tilemap[r * 32 + c] = Birch_SolidTile(r, c);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        task->tBirchDelay = 10; // Project Grounded: korter vasthouden (was 20)
        task->tState++;
    }
    return FALSE;
}

static const TransitionStateFunc sBirch_Funcs[] =
{
    Birch_Init,
    Birch_Drip,
    FramesCountdown,
    WeatherDuo_FadeOut,
    WeatherDuo_End
};

static void Task_Birch(u8 taskId)
{
    while (sBirch_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

#undef tBirchTimer
#undef tBirchPos
#undef tBirchSpeed
#undef tBirchDelay

//------------------------------------------------------------------------
// Project Grounded: gedeelde stappen voor Raikou en Entei
//------------------------------------------------------------------------
#define BEASTS_SCENE_PALETTES (PALETTES_ALL & ~(1 << 15)) // alles behalve BG-palet 15 (de transitie zelf)

// alle paletten wit (ook de "unfaded" buffer), zodat de fade hierna van wit naar zwart gaat
static void Beasts_SetAllWhite(void)
{
    CpuFill16(RGB_WHITE, gPlttBufferUnfaded, PLTT_SIZE);
    CpuFill16(RGB_WHITE, gPlttBufferFaded, PLTT_SIZE);
}

static bool8 Beasts_FadeOutAll(struct Task *task)
{
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK); // Project Grounded: snellere fade (was 1)
    task->tState++;
    return FALSE;
}

//------------------------------------------------------------------------
// Project Grounded: B_TRANSITION_RAIKOU
// Het beeld wordt donker en er slaan steeds sneller bliksems in (Thunder) op verschillende plekken, elk met
// een witte flits en een donderklap. De laatste klap maakt alles wit, daarna naar het gevecht.
// Graphics: tools/grounded/beasts_transition.py (RAIKOU_BOLTS schichten rond x=128).
//------------------------------------------------------------------------
#define RAIKOU_BOLTS   3
#define tRaikouTimer   data[1]
#define tRaikouStrike  data[2]
#define tRaikouLast    data[3]
#define tRaikouDelay   data[8]

static const u8 sRaikou_StrikeTimes[] = {14, 46, 72, 92, 106, 116, 123, 128, 132};
static const u8 sRaikou_StrikeX[]     = {64, 176, 112, 32, 204, 148, 84, 216, 120};

static bool8 Raikou_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sRaikou_Tileset, tileset);
    LoadPalette(sRaikou_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    task->tRaikouTimer = 0;
    task->tRaikouStrike = 0;
    task->tRaikouLast = -100;
    task->tState++;
    return FALSE;
}

static bool8 Raikou_Storm(struct Task *task)
{
    u16 *tilemap, *tileset;
    s32 t = task->tRaikouTimer;
    s32 d;

    GetBg0TilesDst(&tilemap, &tileset);
    if (task->tRaikouStrike < ARRAY_COUNT(sRaikou_StrikeTimes) && t == sRaikou_StrikeTimes[task->tRaikouStrike])
    {
        u32 i = task->tRaikouStrike;
        CpuCopy16(&sRaikou_Tilemap[(i % RAIKOU_BOLTS) * 32 * 32], tilemap, BG_SCREEN_SIZE);
        SetGpuReg(REG_OFFSET_BG0HOFS, (128 - sRaikou_StrikeX[i]) & 0x1FF);
        PlaySE(SE_THUNDER);
        task->tRaikouLast = t;
        task->tRaikouStrike++;
    }
    d = t - task->tRaikouLast;

    // de wereld: flits bij een inslag, verder steeds donkerder (blauwzwart)
    if (d == 0)
        BlendPalettes(BEASTS_SCENE_PALETTES, 13, RGB_WHITE);
    else if (d == 1)
        BlendPalettes(BEASTS_SCENE_PALETTES, 7, RGB_WHITE);
    else if (d == 2)
        BlendPalettes(BEASTS_SCENE_PALETTES, 2, RGB_WHITE);
    else
        BlendPalettes(BEASTS_SCENE_PALETTES, min(t / 3, 11), RGB(0, 0, 4));

    // de schicht: even fel, dan uitdoven
    LoadPalette(sRaikou_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    if (d >= 4 && d < 12)
        BlendPalette(BG_PLTT_ID(15), 16, (d - 3) * 2, RGB_BLACK);
    else if (d == 12)
        CpuFill16(0, tilemap, BG_SCREEN_SIZE);

    task->tRaikouTimer++;
    if (task->tRaikouStrike == ARRAY_COUNT(sRaikou_StrikeTimes) && d == 3)
    {
        // laatste klap: alles wit
        PlaySE(SE_THUNDER);
        Beasts_SetAllWhite();
        task->tRaikouDelay = 8; // Project Grounded: korter wit vasthouden (was 16)
        task->tState++;
    }
    return FALSE;
}

static const TransitionStateFunc sRaikou_Funcs[] =
{
    Raikou_Init,
    Raikou_Storm,
    FramesCountdown,
    Beasts_FadeOutAll,
    WeatherDuo_End
};

static void Task_Raikou(u8 taskId)
{
    while (sRaikou_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

#undef tRaikouTimer
#undef tRaikouStrike
#undef tRaikouLast
#undef tRaikouDelay

//------------------------------------------------------------------------
// Project Grounded: B_TRANSITION_ENTEI
// Midden in beeld flakkert een klein steekvlammetje; dat groeit langzaam en dan steeds sneller uit tot vuur
// over het hele scherm, gloeit wit op en gaat dan over in het gevecht.
// Tiles (tools/grounded/beasts_transition.py): 0 leeg, 1-4 vlakvuur, 5-8 randvlammen, 9-32 steekvlam (2x3, 4 frames).
//------------------------------------------------------------------------
#define ENTEI_FRAMES      8
#define ENTEI_FILL        1
#define ENTEI_EDGE        5
#define ENTEI_SMALL       9
#define ENTEI_CENTER_X    120
#define ENTEI_CENTER_Y    80
#define ENTEI_MAX_RADIUS  (160 << 4)
#define tEnteiTimer       data[1]
#define tEnteiRadius      data[2] // in 1/16 pixel
#define tEnteiSpeed       data[3]
#define tEnteiStep        data[4]
#define tEnteiDelay       data[8]

static void Entei_Flicker(struct Task *task)
{
    u32 frame = (task->tEnteiTimer / 3) % ENTEI_FRAMES;
    LoadPalette(&sEntei_Palette[frame * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
}

static bool8 Entei_Init(struct Task *task)
{
    u16 *tilemap, *tileset;

    GetBg0TilesDst(&tilemap, &tileset);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    CpuCopy16(sEntei_Tileset, tileset, sizeof(sEntei_Tileset));
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    task->tEnteiTimer = 0;
    task->tEnteiRadius = 16 << 4;
    task->tEnteiSpeed = 6;
    Entei_Flicker(task);
    PlaySE(SE_M_EMBER);
    task->tState++;
    return FALSE;
}

// klein steekvlammetje in het midden (2x3 tiles), de wereld wordt langzaam donkerrood
static bool8 Entei_Spark(struct Task *task)
{
    u16 *tilemap, *tileset;
    u32 x, y, frame = (task->tEnteiTimer / 5) % 4;

    GetBg0TilesDst(&tilemap, &tileset);
    for (y = 0; y < 3; y++)
        for (x = 0; x < 2; x++)
            tilemap[(8 + y) * 32 + 14 + x] = (ENTEI_SMALL + frame * 6 + y * 2 + x) | (15 << 12);
    Entei_Flicker(task);
    BlendPalettes(BEASTS_SCENE_PALETTES, min(task->tEnteiTimer / 4, 8), RGB(8, 1, 0));
    if (++task->tEnteiTimer > 48)
    {
        PlaySE(SE_M_FLAMETHROWER);
        task->tState++;
    }
    return FALSE;
}

static void Entei_DrawFire(struct Task *task)
{
    u16 *tilemap, *tileset;
    s32 r, c, dx, dy, dist2;
    s32 radius = task->tEnteiRadius >> 4;
    s32 inner = radius - 10;
    u32 phase = task->tEnteiTimer / 4;

    GetBg0TilesDst(&tilemap, &tileset);
    for (r = 0; r < 20; r++)
    {
        dy = r * 8 + 4 - ENTEI_CENTER_Y;
        for (c = 0; c < 30; c++)
        {
            u16 tile = 0;
            dx = c * 8 + 4 - ENTEI_CENTER_X;
            dist2 = dx * dx + dy * dy;
            if (inner > 0 && dist2 < inner * inner)
                tile = ENTEI_FILL + ((r * 3 + c * 5 + phase) & 3);
            else if (dist2 < radius * radius)
                tile = ENTEI_EDGE + ((r + c * 3 + phase) & 3);
            tilemap[r * 32 + c] = tile ? (tile | (15 << 12)) : 0;
        }
    }
}

// het vuur breidt zich uit: eerst langzaam, dan steeds sneller
static bool8 Entei_Spread(struct Task *task)
{
    task->tEnteiSpeed += 1;
    task->tEnteiRadius += task->tEnteiSpeed;
    Entei_DrawFire(task);
    Entei_Flicker(task);
    task->tEnteiTimer++;
    if (task->tEnteiRadius >= ENTEI_MAX_RADIUS)
    {
        task->tEnteiStep = 0;
        task->tState++;
    }
    return FALSE;
}

static bool8 Entei_Brighten(struct Task *task)
{
    Entei_DrawFire(task);
    Entei_Flicker(task);
    BlendPalette(BG_PLTT_ID(15), 16, min(task->tEnteiStep, 16), RGB_WHITE);
    task->tEnteiTimer++;
    if ((task->tEnteiTimer & 1) == 0)
        task->tEnteiStep++;
    if (task->tEnteiStep > 16)
    {
        Beasts_SetAllWhite();
        task->tEnteiDelay = 6; // Project Grounded: korter wit vasthouden (was 12)
        task->tState++;
    }
    return FALSE;
}

static const TransitionStateFunc sEntei_Funcs[] =
{
    Entei_Init,
    Entei_Spark,
    Entei_Spread,
    Entei_Brighten,
    FramesCountdown,
    Beasts_FadeOutAll,
    WeatherDuo_End
};

static void Task_Entei(u8 taskId)
{
    while (sEntei_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

#undef tEnteiTimer
#undef tEnteiRadius
#undef tEnteiSpeed
#undef tEnteiStep
#undef tEnteiDelay

//------------------------------------------------------------------------
// Project Grounded: route-transities (gevechtsovergang per gebied, zie GetGroundedRouteTransition in battle_setup.c)
// Gedeelde runner: tiles + palet (eventueel een kleurcyclus) laden op BG0 met palet 15, elke frame update() tot die
// TRUE geeft, het beeld even vasthouden en dan bevroren naar zwart faden. Tiles: tools/grounded/route_transitions.py.
//------------------------------------------------------------------------
#define tRtTimer  data[1]
#define tRtA      data[2]
#define tRtB      data[3]
#define tRtC      data[4]
#define tRtDelay  data[8]
#define RT_TILE(n) ((n) | (15 << 12))
#define RT_SCENE_PALETTES (PALETTES_ALL & ~(1 << 15))

struct RouteTransition
{
    const void *tiles;
    u32 tilesSize;
    const u16 *palettes;
    u8 numPalettes;
    u8 palSpeed;
    u16 sound;
    void (*init)(struct Task *task);
    bool8 (*update)(struct Task *task);
    void (*finish)(struct Task *task); // opruimen (bijv. een sprite), vlak voor het einde
};

static u16 *RT_Tilemap(void)
{
    u16 *tilemap, *tileset;
    GetBg0TilesDst(&tilemap, &tileset);
    return tilemap;
}

// tekent een blok van w x h tiles (eerste tile 'first')
static void RT_PutBlock(u16 *tilemap, s32 x, s32 y, u32 first, u32 w, u32 h)
{
    u32 i, j;
    for (j = 0; j < h; j++)
        for (i = 0; i < w; i++)
            tilemap[((y + j) & 31) * 32 + ((x + i) & 31)] = RT_TILE(first + j * w + i);
}

static void RT_LoadPalette(const struct RouteTransition *rt, struct Task *task)
{
    u32 frame = rt->numPalettes > 1 ? (task->tRtTimer / rt->palSpeed) % rt->numPalettes : 0;
    LoadPalette(&rt->palettes[frame * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
}

// het huidige (getinte) beeld als basis vastzetten. Daarna blendt een fade naar wit/zwart vanaf dit beeld, in plaats van
// eerst een frame de ongetinte wereld te tonen (BlendPalettes rekent vanaf de "unfaded" paletten).
static void RT_FreezePalettes(void)
{
    CpuCopy16(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
}

static void RouteTransition_Run(u8 taskId, const struct RouteTransition *rt)
{
    struct Task *task = &gTasks[taskId];
    u16 *tilemap, *tileset;

    switch (task->tState)
    {
    case 0:
        GetBg0TilesDst(&tilemap, &tileset);
        CpuFill16(0, tilemap, BG_SCREEN_SIZE);
        if (rt->tilesSize == RT_SMOL)
            DecompressDataWithHeaderVram(rt->tiles, tileset);
        else
            CpuCopy16(rt->tiles, tileset, rt->tilesSize);
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        task->tRtTimer = task->tRtA = task->tRtB = task->tRtC = 0;
        RT_LoadPalette(rt, task);
        if (rt->init)
            rt->init(task);
        if (rt->sound)
            PlaySE(rt->sound);
        task->tState++;
        break;
    case 1:
        RT_LoadPalette(rt, task);
        if (rt->update(task))
        {
            task->tRtDelay = 2; // Project Grounded: kort vasthouden (was 10)
            task->tState++;
        }
        task->tRtTimer++;
        break;
    case 2:
        if (--task->tRtDelay == 0)
        {
            // beeld bevriezen zoals het nu is, dan naar zwart. Een herhalend geluid (wind, zandstorm) stopt hier.
            if (rt->sound)
                m4aSongNumStop(rt->sound);
            CpuCopy16(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK); // Project Grounded: snellere fade (was 1)
            task->tState++;
        }
        break;
    case 3:
        if (!gPaletteFade.active)
        {
            if (rt->finish)
                rt->finish(task);
            DmaStop(0);
            FadeScreenBlack();
            DestroyTask(taskId);
        }
        break;
    }
}

// ---------------- zee / surfen: een golf rolt van rechts naar links over het beeld
// tiles: 1-4 water, 5 schuimrand, 6 schuim, 7 schuim->water, 8 spatdruppels
static const s8 sRTWave_Curl[21] = {0, -1, -2, -3, -3, -3, -2, -2, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0};

static void RTWave_Init(struct Task *task)
{
    task->tRtA = 256; // x-positie van de schuimrand in pixels
    task->tRtB = 1;   // snelheid
}

static bool8 RTWave_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 r, c, front, x;

    if (task->tRtTimer % 3 == 2)
        task->tRtB++;
    task->tRtA -= task->tRtB;
    x = task->tRtA;
    SetGpuReg(REG_OFFSET_BG0HOFS, (-(x & 7)) & 0x1FF);
    for (r = 0; r < 21; r++)
    {
        front = (x >> 3) + sRTWave_Curl[r];
        for (c = -1; c < 31; c++)
        {
            u16 t = 0;
            if (c == front - 1)
                t = ((r + task->tRtTimer / 2) & 1) ? 8 : 0;
            else if (c == front)
                t = 5;
            else if (c == front + 1)
                t = 6;
            else if (c == front + 2)
                t = 7;
            else if (c > front + 2)
                t = 1 + ((r + c * 2 + task->tRtTimer / 4) & 3);
            tilemap[r * 32 + (c & 31)] = t ? RT_TILE(t) : 0;
        }
    }
    return x < -40;
}

static const struct RouteTransition sRT_Wave =
{
    sRouteWave_Tileset, RT_SMOL, sRouteWave_Palette, 4, 4, SE_M_SURF, RTWave_Init, RTWave_Update
};

static void Task_RouteWave(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Wave);
}

// ---------------- strand: vanaf het strand komt er uit de verte een golf aan die over je heen spoelt
// tiles: 1-3 verre zee, 4-5 golfwand, 6 schuimkam (onderrand), 7 schuimkam (boven), 8 schuimspetters
static void RTBeach_Init(struct Task *task)
{
    task->tRtA = 12 << 3; // onderrand van de golf, in 1/8 pixel
    task->tRtB = 4;
}

// onregelmatige schuimkam: per kolom 0 of 1 rij verder naar voren
static const u8 sRTBeach_Jag[32] = {0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0};

static bool8 RTBeach_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 r, c, y, fr, face;

    if (task->tRtA < (176 << 3))
    {
        task->tRtB++;
        task->tRtA += task->tRtB;
    }
    y = task->tRtA >> 3;
    face = 1 + y / 24; // hoe dichterbij, hoe hoger de golfwand
    SetGpuReg(REG_OFFSET_BG0VOFS, (-(y & 7)) & 0x1FF);
    for (c = 0; c < 32; c++)
    {
        fr = (y >> 3) + sRTBeach_Jag[(c + task->tRtTimer / 5) & 31];
        for (r = -1; r < 22; r++)
        {
            u16 t = 0;
            if (r == fr)
                t = 6;
            else if (r == fr - 1)
                t = 7;
            else if (r == fr + 1)
                t = ((task->tRtTimer / 2 + c) & 3) == 0 ? 8 : 0;
            else if (r < fr - 1 && r >= fr - 1 - face)
                t = 4 + ((r + c) & 1);
            else if (r == fr - 2 - face && y > 90)
                t = 7; // schuim boven op de golfwand
            else if (r < fr - 1 - face)
                t = 1 + ((r + c + task->tRtTimer / 6) % 3);
            tilemap[(r & 31) * 32 + c] = t ? RT_TILE(t) : 0;
        }
    }
    if (y >= 176)
    {
        // de golf slaat over je heen: wit opspatten
        BlendPalettes(PALETTES_ALL, min(task->tRtC * 2, 16), RGB_WHITE);
        if (task->tRtC++ >= 8)
            return TRUE;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Beach =
{
    sRouteBeach_Tileset, RT_SMOL, sRouteBeach_Palette, 4, 4, SE_M_SURF, RTBeach_Init, RTBeach_Update
};

static void Task_RouteBeach(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Beach);
}

// ---------------- onder water: steeds meer luchtbellen stijgen van beneden naar boven
// tiles: 1 klein, 2 middel, 3-6 groot (2x2), 7 sliertje
static void RTBubbles_PlaceRow(u16 *tilemap, u32 row, u32 density)
{
    u32 c;
    for (c = 0; c < 32; c++)
    {
        u32 rnd = Random() % 100;
        u16 t = 0;
        if (rnd < density / 2)
            t = 1;
        else if (rnd < density * 3 / 4)
            t = 7;
        else if (rnd < density)
            t = 2;
        tilemap[(row & 31) * 32 + c] = t ? RT_TILE(t) : 0;
    }
}

static void RTBubbles_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    u32 r, i;
    for (r = 0; r < 32; r++)
        RTBubbles_PlaceRow(tilemap, r, 8);
    // een paar grote bellen
    for (i = 0; i < 4; i++)
    {
        u32 x = 2 + (Random() % 26), y = 4 + i * 6;
        tilemap[y * 32 + x] = RT_TILE(3);
        tilemap[y * 32 + x + 1] = RT_TILE(4);
        tilemap[(y + 1) * 32 + x] = RT_TILE(5);
        tilemap[(y + 1) * 32 + x + 1] = RT_TILE(6);
    }
    task->tRtA = 0;  // scroll in 1/16 pixel
    task->tRtB = 16; // snelheid
    task->tRtC = 21; // eerstvolgende rij die onderaan het beeld in komt
}

static bool8 RTBubbles_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;

    if (task->tRtB < 16 * 7)
        task->tRtB += 2;
    task->tRtA += task->tRtB;
    while (task->tRtC < ((task->tRtA >> 4) >> 3) + 21)
    {
        RTBubbles_PlaceRow(tilemap, task->tRtC, min(10 + t, 85));
        task->tRtC++;
    }
    SetGpuReg(REG_OFFSET_BG0VOFS, (task->tRtA >> 4) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, Sin((t * 6) & 0xFF, 3) & 0x1FF);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 6, 11), RGB(4, 12, 24));
    if (t == 0 || t == 30 || t == 55)
        PlaySE(SE_M_BUBBLE);
    if (t > 70)
        BlendPalette(BG_PLTT_ID(15), 16, min((t - 70) * 2, 16), RGB(28, 31, 31));
    return t >= 80;
}

static const struct RouteTransition sRT_Bubbles =
{
    sRouteBubbles_Tileset, RT_SMOL, sRouteBubbles_Palette, 1, 1, 0, RTBubbles_Init, RTBubbles_Update
};

static void Task_RouteBubbles(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Bubbles);
}

// ---------------- Route 135/136: het gaat steeds harder sneeuwen tot het scherm helemaal dichtsneeuwt
// tiles: 1-3 losse vlokken, 4-5 dichte sneeuw, 6 helemaal wit
static bool8 RTSnow_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    u32 i, n = 4 + t / 2;

    SetGpuReg(REG_OFFSET_BG0VOFS, (-(t * 2)) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, (t / 2 + Sin((t * 4) & 0xFF, 4)) & 0x1FF);
    for (i = 0; i < n; i++)
    {
        u16 *cell = &tilemap[Random() % (32 * 32)];
        u32 cur = *cell & 0x3FF;
        if (cur == 0)
            *cell = RT_TILE(1 + Random() % 3);
        else if (cur < 4)
            *cell = RT_TILE(t > 25 ? 4 : cur);
        else if (cur == 4 && t > 45)
            *cell = RT_TILE(5);
    }
    BlendPalettes(RT_SCENE_PALETTES, min(t / 6, 14), RGB_WHITE);
    if (t >= 100)
    {
        for (i = 0; i < 32 * 32; i++)
            tilemap[i] = RT_TILE(6);
        return TRUE;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Snow =
{
    sRouteSnow_Tileset, RT_SMOL, sRouteSnow_Palette, 1, 1, SE_M_GUST, NULL, RTSnow_Update
};

static void Task_RouteSnow(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Snow);
}

// ---------------- Route 113: vulkanische as waait van rechts naar links door het beeld, steeds dichter, tot alles grijs is
// tiles: 1-3 losse asdeeltjes, 4-5 dichte as, 6 helemaal grijs
static bool8 RTAsh_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    u32 i, n = 4 + t / 2;

    SetGpuReg(REG_OFFSET_BG0HOFS, (t * 5) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, (-(t / 2) + Sin((t * 5) & 0xFF, 3)) & 0x1FF);
    for (i = 0; i < n; i++)
    {
        u16 *cell = &tilemap[Random() % (32 * 32)];
        u32 cur = *cell & 0x3FF;
        if (cur == 0)
            *cell = RT_TILE(1 + Random() % 3);
        else if (cur < 4)
            *cell = RT_TILE(t > 25 ? 4 : cur);
        else if (cur == 4 && t > 45)
            *cell = RT_TILE(5);
    }
    BlendPalettes(RT_SCENE_PALETTES, min(t / 6, 13), RGB(13, 13, 13));
    if (t == 30 || t == 60)
        PlaySE(SE_M_GUST);
    if (t >= 95)
    {
        for (i = 0; i < 32 * 32; i++)
            tilemap[i] = RT_TILE(6);
        return TRUE;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Ash =
{
    sRouteAsh_Tileset, RT_SMOL, sRouteAsh_Palette, 1, 1, SE_M_GUST, NULL, RTAsh_Update
};

static void Task_RouteAsh(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Ash);
}

// ---------------- woestijn: zandstorm, laag na laag zand schuift snel van onder naar boven over het beeld
// tiles: 1-2 zandkam, 3-6 zandlagen, 7-8 vliegend zand
static void RTSand_Init(struct Task *task)
{
    task->tRtA = 0; // hoogte van het zand in pixels
    task->tRtB = 4; // snelheid in 1/4 pixel
}

static bool8 RTSand_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    s32 r, c, top, rt;

    if (t > 12)
    {
        task->tRtB += 1;
        task->tRtA += task->tRtB >> 2;
    }
    top = DISPLAY_HEIGHT - task->tRtA;
    rt = top >> 3;
    SetGpuReg(REG_OFFSET_BG0VOFS, (-(top & 7)) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, (t * 4) & 0x1FF);
    for (r = -1; r < 22; r++)
    {
        for (c = 0; c < 32; c++)
        {
            u16 tile = 0;
            if (r == rt)
                tile = 1 + ((c + t / 4) & 1);
            else if (r > rt)
                tile = 3 + (((21 - r) / 2) & 3);
            else if (((c * 5 + r * 3 + t) % 7) == 0)
                tile = 7 + ((c + r) & 1);
            tilemap[(r & 31) * 32 + c] = tile ? RT_TILE(tile) : 0;
        }
    }
    BlendPalettes(RT_SCENE_PALETTES, min(t / 5, 10), RGB(26, 20, 12));
    if (t == 20 || t == 45)
        PlaySE(SE_M_SAND_ATTACK);
    return top < -16;
}

static const struct RouteTransition sRT_Sand =
{
    sRouteSand_Tileset, RT_SMOL, sRouteSand_Palette, 1, 1, SE_M_SANDSTORM, RTSand_Init, RTSand_Update
};

static void Task_RouteSand(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Sand);
}

// ---------------- Cycling Road: je kijkt over je stuur en raast over de weg (strepen bewegen via een kleurcyclus)
static void RTCycling_Init(struct Task *task)
{
    BlendPalette(BG_PLTT_ID(15), 16, 16, RGB_BLACK);
    task->tRtA = 0;  // fase van de strepen
    task->tRtB = 4;  // snelheid
}

static bool8 RTCycling_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    u32 r, c;

    // eerst de wereld kort naar zwart, dan de weg erin faden
    if (t < 8)
    {
        BlendPalettes(RT_SCENE_PALETTES, t * 2 + 2, RGB_BLACK);
        BlendPalette(BG_PLTT_ID(15), 16, 16, RGB_BLACK);
        return FALSE;
    }
    if (t == 8)
    {
        for (r = 0; r < 20; r++)
            for (c = 0; c < 30; c++)
                tilemap[r * 32 + c] = RT_TILE(sRouteCycling_Tilemap[r * 30 + c]);
        PlaySE(SE_BIKE_BELL);
    }
    if (task->tRtB < 40)
        task->tRtB++;
    task->tRtA += task->tRtB;
    LoadPalette(&sRouteCycling_Palette[((task->tRtA >> 4) & 3) * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    SetGpuReg(REG_OFFSET_BG0VOFS, (t & 2) ? 1 : 0); // trillen over de weg
    if (t < 18)
        BlendPalette(BG_PLTT_ID(15), 16, 16 - (t - 8) * 16 / 10, RGB_BLACK);
    if (t >= 78)
    {
        BlendPalette(BG_PLTT_ID(15), 16, min((t - 78) * 2, 16), RGB_WHITE);
        return t >= 86;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Cycling =
{
    sRouteCycling_Tileset, RT_SMOL, sRouteCycling_Palette, 1, 1, 0, RTCycling_Init, RTCycling_Update
};

static void Task_RouteCycling(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Cycling);
}

// ---------------- Fiery Path / Mt. Chimney: hittegolf. Het beeld trilt in opstijgende golven (zoals bij Swirl, via
// HBlank-scroll van de overworld), kleurt oranje en dan verblindend licht, daarna naar zwart.
static void Task_RouteHeat(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    s32 t;

    switch (task->tState)
    {
    case 0:
        InitTransitionData();
        ScanlineEffect_Clear();
        SetSinWave((s16 *)gScanlineEffectRegBuffers[1], sTransitionData->cameraX, 0, 4, 0, DISPLAY_HEIGHT);
        SetVBlankCallback(VBlankCB_Swirl);
        SetHBlankCallback(HBlankCB_Swirl);
        EnableInterrupts(INTR_FLAG_VBLANK | INTR_FLAG_HBLANK);
        task->tRtTimer = 0;
        PlaySE(SE_M_HEAT_WAVE);
        task->tState++;
        break;
    case 1:
    case 2:
        t = task->tRtTimer++;
        sTransitionData->VBlank_DMA = FALSE;
        SetSinWave((s16 *)gScanlineEffectRegBuffers[0], sTransitionData->cameraX, t * 6, 5, min(1 + t / 7, 10), DISPLAY_HEIGHT);
        sTransitionData->VBlank_DMA++;
        if (task->tState == 1)
        {
            if (t < 50)
                BlendPalettes(PALETTES_ALL, min(t / 4, 9), RGB(31, 12, 0));
            else
                BlendPalettes(PALETTES_ALL, min(9 + (t - 50) / 3, 14), RGB(31, 27, 16));
            if (t >= 75)
            {
                CpuCopy16(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
                BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK); // Project Grounded: snellere fade (was 1)
                task->tState++;
            }
        }
        else if (!gPaletteFade.active)
        {
            DmaStop(0);
            FadeScreenBlack();
            DestroyTask(taskId);
        }
        break;
    }
}

// ---------------- Mt. Pyre: een vloek. De wereld wordt grauw en de ongeidentificeerde ghosts uit Lavender Town zweven
// van beneden omhoog door het beeld (de echte sprite uit Red/Blue). tiles: 1-36 ghost (6x6)
static void RTPyre_PutGhost(u16 *tilemap, s32 x, s32 y)
{
    RT_PutBlock(tilemap, x, y, 1, 6, 6);
}

static void RTPyre_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    RTPyre_PutGhost(tilemap, 1, 20);
    RTPyre_PutGhost(tilemap, 23, 21);
    RTPyre_PutGhost(tilemap, 12, 24);
    RTPyre_PutGhost(tilemap, 18, 26);
    RTPyre_PutGhost(tilemap, 6, 26);
}

static bool8 RTPyre_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;

    if (t == 40)
    {
        // tweede golf, in rijen die nu boven het beeld zitten en straks onderaan weer binnenkomen
        RTPyre_PutGhost(tilemap, 4, 2);
        RTPyre_PutGhost(tilemap, 16, 5);
        RTPyre_PutGhost(tilemap, 25, 1);
    }
    SetGpuReg(REG_OFFSET_BG0VOFS, (t * 5 / 2) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, Sin((t * 4) & 0xFF, 6) & 0x1FF);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 4, 13), RGB(5, 5, 6));
    if (t == 30 || t == 60)
        PlaySE(SE_M_NIGHTMARE);
    return t >= 85;
}

static const struct RouteTransition sRT_Pyre =
{
    sRoutePyre_Tileset, RT_SMOL, sRoutePyre_Palette, 1, 1, SE_M_NIGHTMARE, RTPyre_Init, RTPyre_Update
};

static void Task_RoutePyre(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Pyre);
}

// ---------------- Sky Pillar: je schiet zo snel de lucht in dat het beeld het niet bijhoudt: snelheidsstrepen en wolken
// razen naar beneden, de wereld verdwijnt in het blauw en alles wordt wit.
// tiles: 1-2 snelheidsstrepen, 3-6 wolk (2x2), 7 klein wolkje
static void RTSky_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    u32 i;
    for (i = 0; i < 32 * 32; i++)
    {
        u32 rnd = Random() % 100;
        tilemap[i] = rnd < 9 ? RT_TILE(1 + (rnd & 1)) : (rnd < 12 ? RT_TILE(7) : 0);
    }
    for (i = 0; i < 6; i++)
    {
        u32 x = Random() % 30, y = (i * 5 + Random() % 3) & 31;
        tilemap[y * 32 + x] = RT_TILE(3);
        tilemap[y * 32 + x + 1] = RT_TILE(4);
        tilemap[((y + 1) & 31) * 32 + x] = RT_TILE(5);
        tilemap[((y + 1) & 31) * 32 + x + 1] = RT_TILE(6);
    }
    task->tRtA = 0; // scroll in 1/4 pixel
    task->tRtB = 4;
}

static bool8 RTSky_Update(struct Task *task)
{
    s32 t = task->tRtTimer;
    s32 shake = min(t / 12, 4);

    task->tRtB += 2;
    task->tRtA += task->tRtB;
    SetGpuReg(REG_OFFSET_BG0VOFS, (-(task->tRtA >> 2)) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, shake ? ((Random() % (shake * 2 + 1)) - shake) & 0x1FF : 0);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 3, 16), RGB(13, 21, 31));
    if (t == 25)
        PlaySE(SE_M_SKY_UPPERCUT);
    if (t >= 62)
    {
        if (t == 62)
            RT_FreezePalettes();
        BlendPalettes(PALETTES_ALL, min((t - 62) * 2, 16), RGB_WHITE);
        return t >= 70;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Sky =
{
    sRouteSky_Tileset, RT_SMOL, sRouteSky_Palette, 1, 1, SE_M_FLY, RTSky_Init, RTSky_Update
};

static void Task_RouteSky(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Sky);
}

// ---------------- Artisan Cave: grote penseelstreken in alle kleuren schilderen het beeld vol
// tiles per kleur k (0-4): 1+2k penseelstreek, 2+2k spetters
static const s8 sRTPaint_Rows[] = {9, 2, 15, 5, 12, 0, 17, 7, 3, 14, 10, 18};

static bool8 RTPaint_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    u32 k, r, c;

    for (k = 0; k < ARRAY_COUNT(sRTPaint_Rows); k++)
    {
        s32 start = k * 5, p, color = k % 5;
        bool32 right = (k & 1) == 0;
        if (t < start)
            break;
        if (t == start && (k & 1) == 0)
            PlaySE(SE_M_SKETCH);
        p = min((t - start) * 3, 32);
        for (r = sRTPaint_Rows[k]; r < (u32)sRTPaint_Rows[k] + 3 && r < 21; r++)
        {
            for (c = 0; c < (u32)p; c++)
            {
                u32 col = right ? c : 31 - c;
                u16 tile = 1 + color * 2;
                if (c + 1 == (u32)p && p < 32)
                    tile = 2 + color * 2; // natte rand van de streek
                tilemap[r * 32 + col] = RT_TILE(tile);
            }
        }
    }
    return t >= (s32)(ARRAY_COUNT(sRTPaint_Rows) - 1) * 5 + 16;
}

static const struct RouteTransition sRT_Paint =
{
    sRoutePaint_Tileset, RT_SMOL, sRoutePaint_Palette, 1, 1, 0, NULL, RTPaint_Update
};

static void Task_RoutePaint(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Paint);
}

// ---------------- New Mauville: kortsluiting. Het beeld hapert (verschoven banden via HBlank, zoals Swirl), flikkert,
// er springen vonken over, en dan gaat het uit als een oude tv: een witte lijn die krimpt tot een stip.
// tiles: 1 zwart, 2 witte lijn, 3 witte stip, 4-6 vonkbogen, 7 ruis, 8-91 MissingNo (6x14), die een paar keer heel kort in beeld flitst
static void RTShort_Glitch(struct Task *task, s32 t)
{
    u16 *buf = gScanlineEffectRegBuffers[0];
    u32 i, b;
    for (i = 0; i < DISPLAY_HEIGHT; i++)
        buf[i] = sTransitionData->cameraX;
    for (b = 0; b < 2 + t / 12; b++)
    {
        u32 y0 = Random() % DISPLAY_HEIGHT, len = 3 + Random() % 12;
        s32 off = (s32)(Random() % 40) - 20;
        for (i = y0; i < y0 + len && i < DISPLAY_HEIGHT; i++)
            buf[i] = sTransitionData->cameraX + off;
    }
}

// MissingNo flitst een paar keer op steeds een andere plek in beeld: {start, frames, x, y} in tiles
static const u8 sRTShort_MissingNo[][4] = {{5, 3, 3, 2}, {15, 3, 20, 5}, {24, 4, 10, 1}, {33, 3, 1, 6}, {41, 3, 23, 0}, {47, 3, 13, 4}};

static bool32 RTShort_MissingNo(s32 t, u32 *x, u32 *y)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sRTShort_MissingNo); i++)
    {
        if (t >= sRTShort_MissingNo[i][0] && t < sRTShort_MissingNo[i][0] + sRTShort_MissingNo[i][1])
        {
            *x = sRTShort_MissingNo[i][2];
            *y = sRTShort_MissingNo[i][3];
            return TRUE;
        }
    }
    return FALSE;
}

static void Task_RouteShort(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    u16 *tilemap, *tileset;
    s32 t, k;
    u32 i, mx, my;

    switch (task->tState)
    {
    case 0:
        GetBg0TilesDst(&tilemap, &tileset);
        CpuFill16(0, tilemap, BG_SCREEN_SIZE);
        CpuCopy16(sRouteShort_Tileset, tileset, sizeof(sRouteShort_Tileset));
        LoadPalette(sRouteShort_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        InitTransitionData();
        ScanlineEffect_Clear();
        for (i = 0; i < DISPLAY_HEIGHT; i++)
            gScanlineEffectRegBuffers[1][i] = sTransitionData->cameraX;
        SetVBlankCallback(VBlankCB_Swirl);
        SetHBlankCallback(HBlankCB_Swirl);
        EnableInterrupts(INTR_FLAG_VBLANK | INTR_FLAG_HBLANK);
        task->tRtTimer = 0;
        PlaySE(SE_M_THUNDERBOLT);
        task->tState++;
        break;
    case 1:
        t = task->tRtTimer++;
        tilemap = RT_Tilemap();
        sTransitionData->VBlank_DMA = FALSE;
        if (t < 50)
        {
            RTShort_Glitch(task, t);
            // vonken en ruis
            CpuFill16(0, tilemap, BG_SCREEN_SIZE);
            for (i = 0; i < 3 + (u32)t / 4; i++)
                tilemap[(Random() % 20) * 32 + Random() % 30] = RT_TILE(4 + Random() % 4);
            if (RTShort_MissingNo(t, &mx, &my))
            {
                RT_PutBlock(tilemap, mx, my, 8, 6, 14);
                BlendPalettes(PALETTES_ALL & ~(1 << 15), 0, RGB_BLACK);
                break;
            }
            k = Random() % 6;
            if (k == 0)
                BlendPalettes(PALETTES_ALL & ~(1 << 15), 12, RGB_WHITE);
            else if (k == 1)
                BlendPalettes(PALETTES_ALL & ~(1 << 15), 11, RGB_BLACK);
            else
                BlendPalettes(PALETTES_ALL & ~(1 << 15), min(t / 6, 6), RGB(0, 0, 4));
            if (t == 24)
                PlaySE(SE_M_THUNDERBOLT2);
        }
        else
        {
            // stroom eraf: zwart beeld, witte lijn die krimpt tot een stip
            s32 half = 15 - (t - 50) * 2;
            for (i = 0; i < DISPLAY_HEIGHT; i++)
                gScanlineEffectRegBuffers[0][i] = sTransitionData->cameraX;
            for (i = 0; i < 32 * 21; i++)
                tilemap[i] = RT_TILE(1);
            if (t == 50)
                PlaySE(SE_FAINT);
            if (half > 0)
            {
                for (k = 15 - half; k < 15 + half; k++)
                    tilemap[9 * 32 + k] = RT_TILE(2);
            }
            else if (half > -8)
            {
                tilemap[9 * 32 + 14] = RT_TILE(3);
            }
            else
            {
                task->tRtDelay = 3; // Project Grounded: was 8
                task->tState++;
            }
        }
        sTransitionData->VBlank_DMA++;
        break;
    case 2:
        if (--task->tRtDelay == 0)
        {
            CpuFill16(RGB_BLACK, gPlttBufferUnfaded, PLTT_SIZE);
            CpuFill16(RGB_BLACK, gPlttBufferFaded, PLTT_SIZE);
            DmaStop(0);
            FadeScreenBlack();
            DestroyTask(taskId);
        }
        break;
    }
}

// eerst de wereld geleidelijk naar zwart en dan de transitielaag erin faden (voor transities die het hele beeld vullen)
static bool8 RT_FadeInLayer(struct Task *task, s32 t)
{
    if (t < 14)
    {
        BlendPalettes(RT_SCENE_PALETTES, min(t + 3, 16), RGB_BLACK);
        BlendPalette(BG_PLTT_ID(15), 16, 16, RGB_BLACK);
        return TRUE;
    }
    if (t < 30)
        BlendPalette(BG_PLTT_ID(15), 16, 30 - t, RGB_BLACK);
    return FALSE;
}

// ---------------- Safari Zone: van bovenaf zigzag tussen de bomen door, tot je op een open plek uitkomt
// tiles: 1 bosgrond, 2-10 boom (3x3), 11-14 struik (2x2), 15 gras
static s32 RTSafari_PathX(s32 row)
{
    return 13 + Sin((row * 12) & 0xFF, 6);
}

static void RTSafari_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 r, c;
    for (r = 0; r < 32; r++)
        for (c = 0; c < 32; c++)
            tilemap[r * 32 + c] = RT_TILE((Random() % 6) ? 1 : 15);
    for (r = 0; r < 32; r += 3)
    {
        for (c = (r * 5) % 4; c < 32; c += 4 + Random() % 2)
        {
            s32 px = RTSafari_PathX(r);
            if (c + 3 > px - 1 && c < px + 5)
                continue; // het pad vrijhouden
            if (Random() % 5)
                RT_PutBlock(tilemap, c, r, 2, 3, 3);
            else
                RT_PutBlock(tilemap, c, r + 1, 11, 2, 2);
        }
    }
    task->tRtA = 0; // scroll in 1/4 pixel
    task->tRtB = 4;
}

static bool8 RTSafari_Update(struct Task *task)
{
    s32 t = task->tRtTimer, y, row;

    if (RT_FadeInLayer(task, t))
        return FALSE;
    if (task->tRtB < 40)
        task->tRtB++;
    task->tRtA += task->tRtB;
    y = -(task->tRtA >> 2);
    row = ((y + 80) >> 3) & 31;
    SetGpuReg(REG_OFFSET_BG0VOFS, y & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, ((RTSafari_PathX(row) - 13) * 8) & 0x1FF);
    if (t == 16 || t == 50)
        PlaySE(SE_M_RAZOR_WIND);
    if (t >= 80)
    {
        BlendPalette(BG_PLTT_ID(15), 16, min(t - 80, 16), RGB_WHITE);
        return t >= 96;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Safari =
{
    sRouteSafari_Tileset, RT_SMOL, sRouteSafari_Palette, 1, 1, 0, RTSafari_Init, RTSafari_Update
};

static void Task_RouteSafari(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Safari);
}

// ---------------- Meteor Falls: zijwaarts door de grot, laveren tussen stalactieten (boven) en stalagmieten (onder)
// tiles: 1-28 stalactiet (4x7), 29-56 stalagmiet (4x7), 57 rots
static void RTMeteor_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 c;
    for (c = 0; c < 32; c++)
    {
        tilemap[0 * 32 + c] = RT_TILE(57);
        tilemap[20 * 32 + c] = RT_TILE(57);
    }
    for (c = 0; c < 32; c += 5)
    {
        RT_PutBlock(tilemap, c + (Random() % 2), Random() % 2, 1, 4, 7);
        RT_PutBlock(tilemap, c + 2 + (Random() % 2), 13 + (Random() % 2), 29, 4, 7);
    }
    task->tRtA = 0;
    task->tRtB = 8;
}

static bool8 RTMeteor_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    if (task->tRtB < 56)
        task->tRtB++;
    task->tRtA += task->tRtB;
    SetGpuReg(REG_OFFSET_BG0HOFS, (task->tRtA >> 2) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, Sin((t * 5) & 0xFF, 6) & 0x1FF);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 4, 12), RGB(2, 2, 5));
    if (t == 15 || t == 45)
        PlaySE(SE_M_WING_ATTACK);
    if (t >= 70)
    {
        // het donker in (niet wit: in een grot is er geen reden voor een witte flits)
        if (t == 70)
            RT_FreezePalettes();
        BlendPalettes(PALETTES_ALL, min((t - 70) * 2, 16), RGB_BLACK);
        return t >= 78;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Meteor =
{
    sRouteMeteor_Tileset, RT_SMOL, sRouteMeteor_Palette, 1, 1, SE_M_RAZOR_WIND, RTMeteor_Init, RTMeteor_Update
};

static void Task_RouteMeteor(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Meteor);
}

// ---------------- Jagged Pass: POV op de fiets, hobbelend bergaf over een rotsig pad. De rotsen op het pad komen op je af en
// schieten onder je door (vier fases rotsen, per frame is er een zichtbaar; zie tools/grounded/route_transitions.py).
static void RTJagged_Init(struct Task *task)
{
    BlendPalette(BG_PLTT_ID(15), 16, 16, RGB_BLACK);
    task->tRtA = 0; // fase
    task->tRtB = 4; // snelheid
}

static bool8 RTJagged_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    u32 r, c;

    if (RT_FadeInLayer(task, t))
        return FALSE;
    if (t == 14)
    {
        for (r = 0; r < 20; r++)
            for (c = 0; c < 30; c++)
                tilemap[r * 32 + c] = RT_TILE(sRouteJagged_Tilemap[r * 30 + c]);
        PlaySE(SE_FALL);
    }
    if (task->tRtB < 36)
        task->tRtB++;
    task->tRtA += task->tRtB;
    LoadPalette(&sRouteJagged_Palette[((task->tRtA >> 4) & 3) * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    if (t < 30)
        BlendPalette(BG_PLTT_ID(15), 16, 30 - t, RGB_BLACK);
    // hobbelen over de stenen
    SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 3) - 1 + ((t % 9) == 0 ? -2 : 0)) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0HOFS, (Sin((t * 7) & 0xFF, 2)) & 0x1FF);
    if (t == 45)
        PlaySE(SE_M_ROCK_THROW);
    if (t >= 84)
    {
        BlendPalette(BG_PLTT_ID(15), 16, min((t - 84) * 2, 16), RGB_BLACK);
        return t >= 92;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Jagged =
{
    sRouteJagged_Tileset, RT_SMOL, sRouteJagged_Palette, 1, 1, 0, RTJagged_Init, RTJagged_Update
};

static void Task_RouteJagged(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Jagged);
}

// ---------------- regenwoud (Route 119, Fortree, Route 120): je baant je een weg door reuzenbladeren en lianen, in de regen
// tiles: 1-16 blad (4x4), 17-32 blad gespiegeld, 33-34 lianen, 35-36 regen
static void RTRainforest_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 r, c;
    for (r = 0; r < 32; r++)
        for (c = 0; c < 32; c++)
            tilemap[r * 32 + c] = (Random() % 4) ? 0 : RT_TILE(35 + (Random() % 2));
    for (c = 0; c < 32; c += 3)
        for (r = 0; r < 4 + Random() % 6; r++)
            tilemap[r * 32 + c] = RT_TILE(33 + ((r + c) & 1));
    for (r = 0; r < 32; r += 5)
        for (c = (r * 3) % 6; c < 32; c += 7 + Random() % 3)
            RT_PutBlock(tilemap, c, r + (Random() % 2), (Random() & 1) ? 1 : 17, 4, 4);
    task->tRtA = 0;
    task->tRtB = 6;
}

static bool8 RTRainforest_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    if (task->tRtB < 44)
        task->tRtB++;
    task->tRtA += task->tRtB;
    SetGpuReg(REG_OFFSET_BG0HOFS, (task->tRtA >> 2) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, (-(task->tRtA >> 4) + Sin((t * 6) & 0xFF, 3)) & 0x1FF);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 4, 12), RGB(2, 8, 3));
    if (t == 30)
        PlaySE(SE_M_RAZOR_WIND);
    if (t >= 72)
    {
        // het dichte bos in: donker, geen witte flits
        if (t == 72)
            RT_FreezePalettes();
        BlendPalettes(PALETTES_ALL, min((t - 72) * 2, 16), RGB_BLACK);
        return t >= 80;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Rainforest =
{
    sRouteRainforest_Tileset, RT_SMOL, sRouteRainforest_Palette, 1, 1, SE_M_RAIN_DANCE, RTRainforest_Init, RTRainforest_Update
};

static void Task_RouteRainforest(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Rainforest);
}

//------------------------------------------------------------------------
// Project Grounded: unieke transities voor bepaalde wilde Pokemon, trainers en plekken
//------------------------------------------------------------------------
#define tRtSprite data[6]
#define RT_SPRITE_TAG 0x5A11

static const struct OamData sRT_SpriteOam =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const struct SpriteTemplate sRT_SpriteTemplate =
{
    .tileTag = RT_SPRITE_TAG,
    .paletteTag = RT_SPRITE_TAG,
    .oam = &sRT_SpriteOam,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

// een 64x64-sprite die we zelf draaien en schalen (scale: 256 = 1x, max 512 = 2x; angle: volle cirkel = 0x10000)
static void RT_CreateSprite(struct Task *task, const u32 *gfx, const u16 *pal, s16 x, s16 y)
{
    struct SpriteSheet sheet = {gfx, 64 * 64 / 2, RT_SPRITE_TAG};
    struct SpritePalette spal = {pal, RT_SPRITE_TAG};
    u8 id;
    LoadSpriteSheet(&sheet);
    LoadSpritePalette(&spal);
    id = CreateSprite(&sRT_SpriteTemplate, x, y, 0);
    gSprites[id].affineAnimPaused = TRUE;
    task->tRtSprite = id;
}

static void RT_SetSprite(struct Task *task, s16 x, s16 y, s32 scale, u16 angle)
{
    struct Sprite *sprite = &gSprites[task->tRtSprite];
    sprite->x = x;
    sprite->y = y;
    SetOamMatrixRotationScaling(sprite->oam.matrixNum, scale, scale, angle);
}

// alle paletten behalve palet 15 van BG0 en het palet van onze sprite (om de wereld te kleuren zonder de sprite)
static u32 RT_SceneWithoutSprite(void)
{
    return RT_SCENE_PALETTES & ~(1 << (16 + IndexOfSpritePaletteTag(RT_SPRITE_TAG)));
}

static void RT_FinishSprite(struct Task *task)
{
    DestroySpriteAndFreeResources(&gSprites[task->tRtSprite]);
}

// ---------------- Pikachu: meteen een geel scherm, twee rode wangen schuiven erin, dan "Pika!" in het midden
// tiles: 1 geel, 2-37 wang (6x6), 38-117 tekst (16x5)
static bool8 RTPikachu_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, i, x;

    for (i = 0; i < 32 * 21; i++)
        tilemap[i] = RT_TILE(1);
    x = min(t, 14);
    RT_PutBlock(tilemap, -6 + x * 7 / 14, 8, 2, 6, 6);       // linkerwang: van -6 naar 1
    RT_PutBlock(tilemap, 30 - x * 7 / 14, 8, 2, 6, 6);       // rechterwang: van 30 naar 23
    if (t >= 22)
        RT_PutBlock(tilemap, 7, 8, 38, 16, 5);
    if (t == 22)
        PlayCry_Normal(SPECIES_PIKACHU, 0);
    return t >= 66;
}

static const struct RouteTransition sRT_Pikachu =
{
    sPikachu_Tileset, sizeof(sPikachu_Tileset), sPikachu_Palette, 1, 1, SE_M_THUNDER_WAVE, NULL, RTPikachu_Update, NULL
};

static void Task_Pikachu(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Pikachu);
}

// ---------------- Magikarp: je verdrinkt in Magikarp. Grote Magikarp-iconen vullen de achtergrond en daaroverheen
// verschijnen steeds meer spartelende Magikarp-sprites (64x64, front-sprite) die elkaar overlappen.
// BG-tiles: 1-144 icoon frame 1, 145-288 frame 2 (3x vergroot, 12x12). In de tweede helft komen er nog zes reuzen
// bij: affine sprites op bijna 2x (twee gedeelde matrices: normaal en gespiegeld), boven/midden/onder gespreid zodat
// ze niet op dezelfde beeldregels staan (de GBA kan maar een beperkt aantal grote sprites per regel tekenen).
#define MAGIKARP_BG_SLOTS 6
#define MAGIKARP_GIANTS   3
#define MAGIKARP_PILE_START 128
#define MAGIKARP_SPRITES  56
#define MAGIKARP_TAG      0x5A12

static EWRAM_DATA u8 sRTMagikarp_Sprites[MAGIKARP_SPRITES] = {0};

static const struct OamData sRTMagikarp_Oam =
{
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const union AnimCmd sRTMagikarp_Anim[] =
{
    ANIMCMD_FRAME(0, 5),
    ANIMCMD_FRAME(64, 5),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd sRTMagikarp_AnimFlip[] =
{
    ANIMCMD_FRAME(0, 4, .hFlip = TRUE),
    ANIMCMD_FRAME(64, 4, .hFlip = TRUE),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd *const sRTMagikarp_Anims[] = {sRTMagikarp_Anim, sRTMagikarp_AnimFlip};

// spartelen: steeds opnieuw een stukje omhoog springen
static void SpriteCB_RTMagikarp(struct Sprite *sprite)
{
    sprite->data[0] += sprite->data[1];
    sprite->y2 = -Sin(sprite->data[0] & 0x7F, 10);
}

static const struct SpriteTemplate sRTMagikarp_Template =
{
    .tileTag = MAGIKARP_TAG,
    .paletteTag = MAGIKARP_TAG,
    .oam = &sRTMagikarp_Oam,
    .anims = sRTMagikarp_Anims,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_RTMagikarp,
};

static void RTMagikarp_Init(struct Task *task)
{
    struct SpriteSheet sheet = {sMagikarpSprite_Gfx, 64 * 128 / 2, MAGIKARP_TAG};
    struct SpritePalette spal = {sMagikarpSprite_Palette, MAGIKARP_TAG};
    LoadSpriteSheet(&sheet);
    LoadSpritePalette(&spal);
    task->tRtA = 0; // aantal sprites
    task->tRtB = 0; // aantal reuzen
    task->tRtC = 0; // reuzen-matrices aangemaakt
}

static bool8 RTMagikarp_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer;
    u32 k, n;

    // slot: een berg Magikarp (collage zonder een pixel achtergrond) stapelt zich van onder naar boven op
    if (t >= MAGIKARP_PILE_START)
    {
        u16 *tileset;
        u32 r, c, rows = min((t - MAGIKARP_PILE_START) + 1, 20);
        GetBg0TilesDst(&tilemap, &tileset);
        if (t == MAGIKARP_PILE_START)
        {
            CpuFill16(0, tilemap, BG_SCREEN_SIZE);
            DecompressDataWithHeaderVram(sMagikarpPile_Tileset, tileset);
            PlaySE(SE_M_SURF);
        }
        LoadPalette(sMagikarpPile_Palette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
        for (r = 20 - rows; r < 20; r++)
            for (c = 0; c < 30; c++)
                tilemap[r * 32 + c] = RT_TILE(sMagikarpPile_Tilemap[r * 30 + c]);
        return t >= MAGIKARP_PILE_START + 30;
    }

    // achtergrond: reusachtige spartelende iconen, een voor een
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    n = min(t / 12 + 1, MAGIKARP_BG_SLOTS);
    for (k = 0; k < n; k++)
    {
        u32 idx = (k * 5) % MAGIKARP_BG_SLOTS;
        RT_PutBlock(tilemap, (idx % 3) * 10 - (idx / 3) * 3, (idx / 3) * 10 - 2, 1 + (((t / 6 + k) & 1) * 144), 12, 12);
    }
    // reuzen (affine, ~1.8x) bovenop alles
    if (t >= 96 && (t % 9) == 0 && task->tRtB < MAGIKARP_GIANTS && task->tRtA < MAGIKARP_SPRITES)
    {
        u8 id = CreateSprite(&sRTMagikarp_Template, 50 + task->tRtB * 70, 24 + task->tRtB * 56, 0);
        if (id != MAX_SPRITES)
        {
            struct Sprite *sprite = &gSprites[id];
            if (task->tRtC == 0)
            {
                // twee gedeelde matrices: 1.8x, normaal en gespiegeld
                task->tRtC = 1;
                task->data[5] = AllocOamMatrix();
                task->data[7] = AllocOamMatrix();
                SetOamMatrixRotationScaling(task->data[5], 460, 460, 0);
                SetOamMatrixRotationScaling(task->data[7], -460, 460, 0);
            }
            sprite->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
            sprite->oam.matrixNum = (task->tRtB & 1) ? task->data[7] : task->data[5];
            sprite->affineAnimPaused = TRUE;
            CalcCenterToCornerVec(sprite, SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
            sprite->data[0] = Random() & 0x7F;
            sprite->data[1] = 7;
            sRTMagikarp_Sprites[task->tRtA++] = id;
            task->tRtB++;
            PlaySE(SE_M_MEGA_KICK);
        }
    }
    // daaroverheen: steeds meer Magikarp-sprites, steeds sneller
    // steeds meer: eerst af en toe een, dan steeds vaker
    for (k = 0; k < (t < 30 ? (t % 6 == 0) : (t < 60 ? (t % 3 == 0) : (t < 90 ? (t % 2 == 0) : 1))) && task->tRtA < MAGIKARP_SPRITES; k++)
    {
        u8 id = CreateSprite(&sRTMagikarp_Template, 8 + Random() % 224, 8 + Random() % 150, MAGIKARP_SPRITES - task->tRtA);
        if (id == MAX_SPRITES)
            break;
        StartSpriteAnim(&gSprites[id], Random() & 1);
        gSprites[id].subpriority = 2 + MAGIKARP_SPRITES - task->tRtA;
        gSprites[id].animDelayCounter = Random() % 5;
        gSprites[id].data[0] = Random() & 0x7F;
        gSprites[id].data[1] = 6 + Random() % 6;
        sRTMagikarp_Sprites[task->tRtA++] = id;
    }
    if (t % 12 == 0 && t < MAGIKARP_PILE_START)
        PlaySE(t % 24 ? SE_M_DOUBLE_SLAP : SE_M_SURF);
    BlendPalettes(RT_SCENE_PALETTES & ~(1 << (16 + IndexOfSpritePaletteTag(MAGIKARP_TAG))), min(t / 4, 10), RGB(6, 14, 28));
    return FALSE;
}

static void RTMagikarp_Finish(struct Task *task)
{
    u32 k;
    for (k = 0; k < (u32)task->tRtA; k++)
        DestroySprite(&gSprites[sRTMagikarp_Sprites[k]]);
    if (task->tRtC)
    {
        FreeOamMatrix(task->data[5]);
        FreeOamMatrix(task->data[7]);
    }
    FreeSpriteTilesByTag(MAGIKARP_TAG);
    FreeSpritePaletteByTag(MAGIKARP_TAG);
}

static const struct RouteTransition sRT_Magikarp =
{
    sMagikarp_Tileset, RT_SMOL, sMagikarp_Palette, 1, 1, 0, RTMagikarp_Init, RTMagikarp_Update, RTMagikarp_Finish
};

static void Task_Magikarp(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Magikarp);
}

// ---------------- Viagra Boys (Youngster Calvin, "Short shorts, cigarette."): het yin-yang-logo met V en B draait en
// zoomt in op zwart, flits, en draait daarna andersom verder in omgekeerde kleuren (zwart logo op wit). Bron:
// tools/grounded/viagra_boys_transition.py. BG-tile 1 = vlak in kleur 1 (zwart, in de tweede helft wit).
#define VB_TAG    0x5A40
#define VB_FLIP   44
#define VB_END    86

static const u16 sViagraBoys_BgTiles[] = INCBIN_U16("graphics/battle_transitions/viagra_boys_bg.4bpp");
static const u16 sViagraBoys_BgPal[] = INCBIN_U16("graphics/battle_transitions/viagra_boys_bg.gbapal");
static const u32 sViagraBoys_Gfx[] = INCBIN_U32("graphics/battle_transitions/viagra_boys.4bpp");
static const u16 sViagraBoys_Pal[] = INCBIN_U16("graphics/battle_transitions/viagra_boys.gbapal");

static const struct OamData sRTViagraBoys_Oam =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const struct SpriteTemplate sRTViagraBoys_Template =
{
    .tileTag = VB_TAG,
    .paletteTag = VB_TAG,
    .oam = &sRTViagraBoys_Oam,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static void RTViagraBoys_Init(struct Task *task)
{
    struct SpriteSheet sheet = {sViagraBoys_Gfx, sizeof(sViagraBoys_Gfx), VB_TAG};
    struct SpritePalette spal = {sViagraBoys_Pal, VB_TAG};
    u8 id;

    LoadSpriteSheet(&sheet);
    LoadSpritePalette(&spal);
    id = CreateSprite(&sRTViagraBoys_Template, 120, 80, 0);
    task->tRtA = id;
    task->tRtB = AllocOamMatrix();
    if (id != MAX_SPRITES)
    {
        gSprites[id].oam.matrixNum = task->tRtB;
        CalcCenterToCornerVec(&gSprites[id], SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
    }
    PlaySE(SE_M_SWAGGER);
}

static bool8 RTViagraBoys_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, scale, rot;
    u32 i, pal = 16 + IndexOfSpritePaletteTag(VB_TAG);
    u16 black = RGB(2, 2, 2), white = RGB(30, 30, 30);

    for (i = 0; i < 20 * 32; i++)
        tilemap[i] = RT_TILE(1);
    if (t < VB_FLIP)
    {
        // eerst: wit logo op zwart, een hele draai rechtsom terwijl het groeit
        scale = 128 + t * 160 / VB_FLIP;
        rot = -(t * 0x10000 / VB_FLIP);
        LoadPalette(&black, BG_PLTT_ID(15) + 1, PLTT_SIZEOF(1));
        BlendPalettes(RT_SCENE_PALETTES & ~(1 << pal), 16, RGB_BLACK);
    }
    else
    {
        // flits, dan omgekeerd: zwart logo op wit, andersom draaiend en verder groeiend
        u32 k = t - VB_FLIP;
        if (k == 0)
        {
            u16 inv[2] = {black, white};
            LoadPalette(inv, OBJ_PLTT_ID(IndexOfSpritePaletteTag(VB_TAG)) + 1, PLTT_SIZEOF(2));
            PlaySE(SE_M_HEADBUTT);
        }
        scale = 288 + min(k, 30u) * 224 / 30;
        rot = k * 0x10000 / 30;
        LoadPalette(&white, BG_PLTT_ID(15) + 1, PLTT_SIZEOF(1));
        BlendPalettes(RT_SCENE_PALETTES & ~(1 << pal), 16, RGB_WHITE);
        if (k < 2)
            gSprites[task->tRtA].invisible = TRUE;
        else
            gSprites[task->tRtA].invisible = FALSE;
    }
    if (task->tRtA != MAX_SPRITES)
        SetOamMatrixRotationScaling(task->tRtB, scale, scale, rot & 0xFFFF); // 256 = 1x, groter = groter
    return t >= VB_END;
}

static void RTViagraBoys_Finish(struct Task *task)
{
    if (task->tRtA != MAX_SPRITES)
        DestroySprite(&gSprites[task->tRtA]);
    FreeOamMatrix(task->tRtB);
    FreeSpriteTilesByTag(VB_TAG);
    FreeSpritePaletteByTag(VB_TAG);
}

static const struct RouteTransition sRT_ViagraBoys =
{
    sViagraBoys_BgTiles, sizeof(sViagraBoys_BgTiles), sViagraBoys_BgPal, 1, 1, 0, RTViagraBoys_Init, RTViagraBoys_Update, RTViagraBoys_Finish
};

static void Task_ViagraBoys(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_ViagraBoys);
}

// ---------------- Gabby & Ty: een camera wordt op je gericht: zoekerhoeken zoomen in, REC en een knipperende rode stip
// tiles: 1-4 hoek LB, 5-8 RB, 9-12 LO, 13-16 RO (2x2), 17-18 lijnen, 19-22 rode stip (2x2), 23-32 REC (5x2), 33-38 batterij (3x2)
static bool8 RTGabbyTy_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, o = max(1, 8 - t / 2);

    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
    RT_PutBlock(tilemap, o, o, 1, 2, 2);
    RT_PutBlock(tilemap, 28 - o, o, 5, 2, 2);
    RT_PutBlock(tilemap, o, 18 - o, 9, 2, 2);
    RT_PutBlock(tilemap, 28 - o, 18 - o, 13, 2, 2);
    if (t >= 16)
    {
        if ((t / 10) % 2 == 0)
            RT_PutBlock(tilemap, 3, 3, 19, 2, 2);
        RT_PutBlock(tilemap, 5, 3, 23, 5, 2);
        RT_PutBlock(tilemap, 23, 3, 33, 3, 2);
    }
    if (t == 16)
        PlaySE(SE_CLICK);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 8, 4), RGB(12, 12, 12));
    if (t >= 76)
    {
        if (t == 76)
            RT_FreezePalettes();
        BlendPalettes(PALETTES_ALL, min((t - 76) * 4, 16), RGB_WHITE); // flits
        return t >= 80;
    }
    return FALSE;
}

static const struct RouteTransition sRT_GabbyTy =
{
    sGabbyTy_Tileset, RT_SMOL, sGabbyTy_Palette, 1, 1, 0, NULL, RTGabbyTy_Update, NULL
};

static void Task_GabbyTy(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GabbyTy);
}

// ---------------- Koffing/Weezing: het schedel-en-botten-teken op paars, met het weef-effect van de Aqua/Magma-logo's
static bool8 Koffing_Init(struct Task *task)
{
    NewRegi_SetGfx(task, sKoffing_Tileset, RT_SMOL, sKoffing_Tilemap, sKoffing_Palette);
    PlaySE(SE_M_TOXIC);
    return FALSE;
}

static const TransitionStateFunc sKoffing_Funcs[] =
{
    Koffing_Init,
    PatternWeave_Blend1,
    PatternWeave_Blend2,
    PatternWeave_FinishAppear,
    PatternWeave_CircularMask
};

static void Task_Koffing(u8 taskId)
{
    while (sKoffing_Funcs[gTasks[taskId].tState](&gTasks[taskId]));
}

// ---------------- Psyduck: een enorm vraagteken ploft in beeld en gaat dan steeds sneller rondjes draaien
static void RTPsyduck_Init(struct Task *task)
{
    RT_CreateSprite(task, sQuestionSprite_Gfx, sQuestionSprite_Palette, 120, 80);
    RT_SetSprite(task, 120, 80, 16, 0);
    task->tRtA = 0;   // hoek
    task->tRtB = 0;   // draaisnelheid
}

static bool8 RTPsyduck_Update(struct Task *task)
{
    s32 t = task->tRtTimer, scale;

    BlendPalettes(RT_SceneWithoutSprite(), min(t / 3, 9), RGB(31, 26, 8));
    if (t < 10)
        scale = 16 + t * 60;                      // ploft erin, schiet iets door...
    else if (t < 16)
        scale = 616 - (t - 10) * 18;              // ...en veert terug naar 2x
    else
        scale = 512;
    if (t == 2)
        PlaySE(SE_M_CONFUSE_RAY);
    if (t >= 26)
    {
        if (task->tRtB < 0x2400)
            task->tRtB += 0x60;
        task->tRtA += task->tRtB;
        if (t == 26)
            PlaySE(SE_M_TELEPORT);
    }
    RT_SetSprite(task, 120, 80, min(scale, 512), task->tRtA);
    if (t >= 84)
    {
        // geen witte flits: het vraagteken draait het beeld uit
        if (t == 84)
            RT_FreezePalettes();
        BlendPalettes(PALETTES_ALL, min((t - 84) * 2, 16), RGB_BLACK);
        return t >= 92;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Psyduck =
{
    sPikachu_Tileset, 32, sPikachu_Palette, 1, 1, 0, RTPsyduck_Init, RTPsyduck_Update, RT_FinishSprite
};

static void Task_Psyduck(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Psyduck);
}

// ---------------- Joey: zijn Poochyena valt je aan. Hij springt in sprongen op je af, steeds groter, tot hij bijt.
static void RTPoochyena_Init(struct Task *task)
{
    RT_CreateSprite(task, sPoochyenaSprite_Gfx, sPoochyenaSprite_Palette, 120, 70);
    RT_SetSprite(task, 120, 70, 48, 0);
}

static bool8 RTPoochyena_Update(struct Task *task)
{
    s32 t = task->tRtTimer, lunge = t / 14, phase = t % 14, scale, y;

    // elke sprong: snel groter en even omhoog, dan grommend afwachten
    scale = 48 + lunge * 90 + (phase < 5 ? phase * 18 : 90);
    y = 70 + lunge * 4 - (phase < 5 ? Sin((phase * 26) & 0xFF, 10) : 0);
    if (phase == 0 && lunge < 5)
        PlaySE(lunge == 0 ? SE_M_LEER : SE_M_COMET_PUNCH);
    if (t == 1)
        PlayCry_Normal(SPECIES_POOCHYENA, 0);
    BlendPalettes(RT_SceneWithoutSprite(), min(t / 5, 10), RGB(10, 0, 0));
    RT_SetSprite(task, 120 + ((phase > 6) ? (Random() % 3) - 1 : 0), y, min(scale, 512), 0);
    if (t >= 70)
    {
        if (t == 70)
            PlaySE(SE_M_BITE);
        BlendPalettes(PALETTES_ALL, min((t - 70) * 3, 16), RGB(28, 0, 0)); // hap!
        return t >= 76;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Poochyena =
{
    sPikachu_Tileset, 32, sPikachu_Palette, 1, 1, 0, RTPoochyena_Init, RTPoochyena_Update, RT_FinishSprite
};

static void Task_Poochyena(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Poochyena);
}

// ---------------- strand van Route 109 (Slateport): strand met parasols onderin, een strandbal vliegt draaiend op je af en raakt je
// BG-tiles: strand met parasols (30x6), sprite: strandbal
static void RTBeachball_Init(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    u32 r, c;
    for (r = 0; r < 6; r++)
        for (c = 0; c < 30; c++)
            tilemap[(14 + r) * 32 + c] = RT_TILE(sBeachball_Tilemap[r * 30 + c]);
    RT_CreateSprite(task, sBeachballSprite_Gfx, sBeachballSprite_Palette, 210, 20);
    RT_SetSprite(task, 210, 20, 24, 0);
    task->tRtA = 0;
}

static bool8 RTBeachball_Update(struct Task *task)
{
    s32 t = task->tRtTimer, f = min(t, 60), x, y, scale;

    BlendPalettes(RT_SceneWithoutSprite(), min(t / 2, 11), RGB(17, 25, 31)); // felle lucht en zee
    task->tRtA += 0x900;
    // boog van rechtsboven naar het midden, steeds groter
    x = 210 - f * 90 / 60;
    y = 20 + f * 60 / 60 - Sin((f * 2) & 0xFF, 22);
    scale = 24 + f * f * 488 / 3600;
    if (t == 0 || t == 24)
        PlaySE(SE_BALL_BOUNCE_1);
    if (t >= 60)
    {
        // pats! het beeld schudt en wordt wit
        if (t == 60)
        {
            PlaySE(SE_M_MEGA_KICK);
            RT_FreezePalettes();
        }
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 7) - 3) & 0x1FF);
        x += (Random() % 7) - 3;
        BlendPalettes(PALETTES_ALL, min((t - 60) * 3, 16), RGB_WHITE);
    }
    RT_SetSprite(task, x, y, scale, task->tRtA);
    return t >= 68;
}

static const struct RouteTransition sRT_Beachball =
{
    sBeachball_Tileset, RT_SMOL, sBeachball_Palette, 1, 1, 0, RTBeachball_Init, RTBeachball_Update, RT_FinishSprite
};

static void Task_Beachball(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Beachball);
}

// ---------------- Colress: eerst de gewone mugshot-slide, en vanuit het witte scherm grijpen twee draaiende
// tandwielen in elkaar en komen steeds dichterbij (een beetje zoals Gear Grind). De wereld kleurt van wit naar donkerblauw.
#define tRtGear2 data[7]
#define tColressPhase data[15]
#define GEAR_PITCH 27 // afstand van het midden tot waar de tanden in elkaar grijpen, in pixels bij 1x

static void RTColress_Init(struct Task *task)
{
    u8 id;
    RT_CreateSprite(task, sGearSprite_Gfx, sGearSprite_Palette, 120, 80);
    id = CreateSprite(&sRT_SpriteTemplate, 120, 80, 0);
    gSprites[id].affineAnimPaused = TRUE;
    task->tRtGear2 = id;
    task->tRtA = 0;
}

static bool8 RTColress_Update(struct Task *task)
{
    s32 t = task->tRtTimer, f = min(t, 72), scale, d, k;
    struct Sprite *gear2 = &gSprites[task->tRtGear2];

    // wit -> donker staalblauw, aan het eind een witte flits (wereld blijft verborgen)
    k = min(t, 20) * 16 / 20;
    if (t >= 72)
        k = 16 - min((t - 72) * 3, 16);
    BlendPalettes(RT_SceneWithoutSprite(), 16, RGB(31 - k * 29 / 16, 31 - k * 27 / 16, 31 - k * 22 / 16));
    // steeds sneller draaien, steeds groter
    task->tRtA += 0x180 + f * 0x14;
    scale = 40 + f * f * 472 / (72 * 72);
    d = GEAR_PITCH * scale / 256;
    if (t % 12 == 0 && t < 72)
        PlaySE(SE_M_VICEGRIP);
    RT_SetSprite(task, 120 - d, 80, scale, task->tRtA + 0x0CCC);
    gear2->x = 120 + d;
    gear2->y = 80;
    SetOamMatrixRotationScaling(gear2->oam.matrixNum, scale, scale, -task->tRtA);
    if (t >= 72)
    {
        if (t == 72)
            PlaySE(SE_M_HARDEN);
        BlendPalettes(1 << (16 + IndexOfSpritePaletteTag(RT_SPRITE_TAG)), min((t - 72) * 3, 16), RGB_WHITE);
        return t >= 78;
    }
    return FALSE;
}

static void RTColress_Finish(struct Task *task)
{
    struct Sprite *gear2 = &gSprites[task->tRtGear2];
    FreeSpriteOamMatrix(gear2);
    DestroySprite(gear2);
    RT_FinishSprite(task);
}

static const struct RouteTransition sRT_Colress =
{
    sPikachu_Tileset, 32, sPikachu_Palette, 1, 1, 0, RTColress_Init, RTColress_Update, RTColress_Finish
};

static void Task_Colress(u8 taskId)
{
    struct Task *task = &gTasks[taskId];

    if (task->tColressPhase == 0)
    {
        // de mugshot tot en met het witte scherm (Mugshot_GradualWhiteFade); daarna de tandwielen
        while (task->tState < 7 && sMugshot_Funcs[task->tState](task))
            ;
        if (task->tState == 7)
        {
            SetVBlankCallback(NULL);
            DmaStop(0);
            SetHBlankCallback(NULL);
            BlendPalettes(PALETTES_ALL, 16, RGB_WHITE);
            SetGpuReg(REG_OFFSET_BLDCNT, 0);
            SetGpuReg(REG_OFFSET_BLDY, 0);
            ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
            SetVBlankCallback(VBlankCB_BattleTransition);
            // de trainerfoto's van de mugshot liggen nog (wit/onzichtbaar) in beeld; weg ermee
            gSprites[task->data[11]].invisible = TRUE; // tOpponentSpriteAId
            gSprites[task->data[14]].invisible = TRUE; // tPlayerSpriteId
            task->tState = 0;
            task->tColressPhase = 1;
        }
        return;
    }
    RouteTransition_Run(taskId, &sRT_Colress);
}

// ---------------- Zangoose: een reuzenklauw (Crush Claw) haalt diagonaal uit en laat drie striemen achter;
// daarna scheurt de middelste striem open tot een zwarte, gekartelde scheur die het hele beeld opslokt.
// Alles loopt langs de anti-diagonaal: tile (c, r) ligt op striem/scheurrand m als c + r == m.
// tiles: 1 zwart, 2-4 striem, 5-7 scheurrand (zwart rechtsonder), 8-10 scheurrand (zwart linksboven)
#define ZANGOOSE_MID 24

static void RTZangoose_Init(struct Task *task)
{
    RT_CreateSprite(task, sZangooseClaw_Gfx, sZangooseClaw_Palette, 250, -50);
    RT_SetSprite(task, 250, -50, 512, 0);
}

static bool8 RTZangoose_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, f, r, c, s, w, revealed;

    // de klauw zwiept van rechtsboven naar linksonder (x + y blijft 200: door het midden)
    f = min(t, 14);
    if (t == 0)
        PlaySE(SE_M_RAZOR_WIND);
    if (t <= 14)
        RT_SetSprite(task, 250 - f * 300 / 14, -50 + f * 300 / 14, 512, 0);
    else
        gSprites[task->tRtSprite].invisible = TRUE;

    revealed = t * 24 / 14 - 3; // tot en met deze rij zijn de striemen al getekend
    w = (t >= 20) ? (t - 18) : 0;  // halve breedte van de scheur
    if (t == 20)
    {
        PlaySE(SE_M_CUT);
        PlayCry_Normal(SPECIES_ZANGOOSE, 0);
    }
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 30; c++)
        {
            u16 tileNum = 0;
            s = c + r;
            if (w > 0 && s == ZANGOOSE_MID - w)
                tileNum = 5 + ((c * 7 + r) % 3);
            else if (w > 0 && s == ZANGOOSE_MID + w)
                tileNum = 8 + ((c * 5 + r * 3) % 3);
            else if (w > 0 && s > ZANGOOSE_MID - w && s < ZANGOOSE_MID + w)
                tileNum = 1;
            else if (r <= revealed && (s == ZANGOOSE_MID - 3 || s == ZANGOOSE_MID || s == ZANGOOSE_MID + 3))
                tileNum = 2 + (r % 3);
            tilemap[r * 32 + c] = tileNum ? RT_TILE(tileNum) : 0;
        }
    }
    // de wereld kleurt rood en trilt
    if (t >= 12)
        BlendPalettes(RT_SceneWithoutSprite(), min(t - 12, 7), RGB(31, 0, 0));
    if (t >= 20)
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 5) - 2) & 0x1FF);
    return w >= 26;
}

static const struct RouteTransition sRT_Zangoose =
{
    sZangoose_Tileset, RT_SMOL, sZangoose_Palette, 1, 1, 0, RTZangoose_Init, RTZangoose_Update, RT_FinishSprite
};

static void Task_Zangoose(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Zangoose);
}

// ---------------- Seviper: een Poison Fang zo groot als het scherm. De bovenkaak met twee enorme giftanden zakt
// van boven in beeld, de onderkaak komt van onder; dan klappen ze dicht en kleurt alles paars van het gif.
static void RTSeviper_DrawJaw(u16 *tilemap, const u16 *jaw, s32 rows, s32 top)
{
    s32 r, c;
    for (r = 0; r < rows; r++)
    {
        if (top + r < 0 || top + r >= 20)
            continue;
        for (c = 0; c < 30; c++)
            if (jaw[r * 30 + c])
                tilemap[(top + r) * 32 + c] = RT_TILE(jaw[r * 30 + c]);
    }
}

static bool8 RTSeviper_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, upper, lower, i;

    if (t < 24)
    {
        // de bek gaat dreigend open en komt dichterbij
        upper = -20 + t / 2;
        lower = 20 - t / 8;
    }
    else
    {
        // en bijt!
        upper = min(-8 + (t - 24) * 2, 0);
        lower = max(17 - (t - 24), 15);
    }
    for (i = 0; i < 20 * 32; i++)
        tilemap[i] = 0;
    RTSeviper_DrawJaw(tilemap, sSeviper_Lower, 5, lower);
    RTSeviper_DrawJaw(tilemap, sSeviper_Upper, 20, upper);

    if (t == 0)
        PlaySE(SE_M_LEER);
    if (t == 6)
        PlayCry_Normal(SPECIES_SEVIPER, 0);
    if (t < 28)
        BlendPalettes(RT_SceneWithoutSprite(), min(t / 3, 6), RGB(14, 2, 18));
    if (t == 28)
        PlaySE(SE_M_BITE);
    if (t >= 28)
    {
        // gif: het beeld schudt en loopt paars vol
        SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 5) - 2) & 0x1FF);
        BlendPalettes(PALETTES_ALL & ~(1 << 15), min(6 + (t - 28) * 2, 16), RGB(16, 2, 22));
        if (t == 31)
            PlaySE(SE_M_TOXIC);
        return t >= 38;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Seviper =
{
    sSeviper_Tileset, RT_SMOL, sSeviper_Palette, 1, 1, 0, NULL, RTSeviper_Update, NULL
};

static void Task_Seviper(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Seviper);
}

// ---------------- Heatran: de grond rommelt, lavapluimen spuiten een voor een omhoog, en dan loopt het hele beeld
// vol lava (uitbarsting). tiles: 1-2 lava, 3/4 pluimranden, 5-7 kop, 8 druppels, 9 oppervlak van de vloed
#define HEATRAN_PLUMES 5
static const s8 sHeatranPlumeCol[HEATRAN_PLUMES] = {15, 3, 27, 9, 21};
static const u8 sHeatranPlumeStart[HEATRAN_PLUMES] = {4, 10, 15, 20, 24};
#define HEATRAN_FLOOD_START 36

static bool8 RTHeatran_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, i, r, c, h, top, flood;

    for (i = 0; i < 20 * 32; i++)
        tilemap[i] = 0;

    for (i = 0; i < HEATRAN_PLUMES; i++)
    {
        s32 cx = sHeatranPlumeCol[i];
        if (t < sHeatranPlumeStart[i])
            continue;
        if (t == sHeatranPlumeStart[i])
            PlaySE(i % 2 ? SE_M_FLAME_WHEEL : SE_M_EMBER);
        h = min((t - sHeatranPlumeStart[i]) * 3, 22);
        top = 20 - h;
        // pluim van 5 tiles breed: rand, drie keer lava, rand; kop met een koepel erop
        for (r = max(top, 0); r < 20; r++)
        {
            tilemap[r * 32 + ((cx - 2) & 31)] = RT_TILE(3);
            for (c = -1; c <= 1; c++)
                tilemap[r * 32 + ((cx + c) & 31)] = RT_TILE(1 + ((r + c + t / 2) & 1));
            tilemap[r * 32 + ((cx + 2) & 31)] = RT_TILE(4);
        }
        if (top - 1 >= 0)
        {
            tilemap[(top - 1) * 32 + ((cx - 2) & 31)] = RT_TILE(5);
            for (c = -1; c <= 1; c++)
                tilemap[(top - 1) * 32 + ((cx + c) & 31)] = RT_TILE(6);
            tilemap[(top - 1) * 32 + ((cx + 2) & 31)] = RT_TILE(7);
        }
        if (top - 4 >= 0)
        {
            tilemap[(top - 3) * 32 + ((cx - 3 + (t + i) % 3) & 31)] = RT_TILE(8);
            tilemap[(top - 4) * 32 + ((cx + 1 + (t + 2 * i) % 3) & 31)] = RT_TILE(8);
        }
    }

    // de vloed: lava stijgt van onder tot het hele beeld vol is
    flood = (t >= HEATRAN_FLOOD_START) ? (t - HEATRAN_FLOOD_START) * 2 : 0;
    for (r = 20 - min(flood, 21); r < 20; r++)
        for (c = 0; c < 30; c++)
            tilemap[r * 32 + c] = RT_TILE(r == 20 - flood ? 9 : 1 + ((r + c) & 1));

    if (t == 0)
        PlaySE(SE_M_EARTHQUAKE);
    if (t == HEATRAN_FLOOD_START)
        PlaySE(SE_M_EXPLOSION);
    SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 5) - 2) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 3) - 1) & 0x1FF);
    BlendPalettes(RT_SCENE_PALETTES, min(t / 2, 10), RGB(12, 2, 0));
    if (flood >= 22)
    {
        BlendPalettes(PALETTES_ALL, min((flood - 22) * 4, 16), RGB(31, 28, 16));
        return flood >= 30;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Heatran =
{
    sHeatran_Tileset, RT_SMOL, sHeatran_Palette, 4, 3, 0, NULL, RTHeatran_Update, NULL
};

static void Task_Heatran(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Heatran);
}

// ---------------- Shaymin: drie spiraalarmen van bloemen in alle kleuren (Gracidea, rozen, tulpen, zonnebloemen,
// madeliefjes, vergeet-mij-nietjes, viooltjes, lavendel, blaadjes) draaien om het midden van het scherm, de wereld
// wordt donker zodat de bloemen oplichten, en dan bedekt een bloementapijt vanuit het midden het hele beeld.
// Drie paletten: BG 15 (roze/rood/fuchsia), 14 (geel/oranje/zalm), 13 (blauw/paars/lila), elk met een schittering.
// tiles (route_transitions.py, "shaymin"): 1-24 kleine bloemen en blaadjes, 25-48 zes grote bloemen (2x2), 49-63
// tapijt (gras met een bloem). Het beeld wordt eerst in een buffer opgebouwd en dan in een keer gekopieerd (geen scheuren).
#define SHAYMIN_PETALS 210
#define SHAYMIN_CARPET_START 54
#define SHAYMIN_SMALL 24
#define SHAYMIN_BIG 6
#define SHAYMIN_CARPET (1 + SHAYMIN_SMALL + SHAYMIN_BIG * 4)
#define SHAYMIN_CARPET_TILES 15
#define SHAYMIN_SCENE_PALETTES (PALETTES_ALL & ~(7 << 13))

// palet per tile (index 0 = leeg)
static const u8 sShaymin_TilePal[SHAYMIN_CARPET + SHAYMIN_CARPET_TILES] =
{
    0,
    15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13,
    15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13,
    15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13,
};

// cel: bit 0-5 tile, bit 6-7 horizontaal/verticaal spiegelen
static void RTShaymin_Put(u8 *cells, s32 x, s32 y, u8 cell)
{
    if (x >= 0 && x < 30 && y >= 0 && y < 20 && (cells[y * 30 + x] & 0x3F) < SHAYMIN_CARPET) // niet over het tapijt
        cells[y * 30 + x] = cell;
}

static bool8 RTShaymin_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, i, n, r, base, ang, x, y, carpet, dx, dy, b;
    u8 cells[30 * 20];
    const u8 *p;
    u32 f = (t / 4) % 4;

    LoadPalette(&sShaymin_Palette[(4 + f) * 16], BG_PLTT_ID(14), PLTT_SIZE_4BPP);
    LoadPalette(&sShaymin_Palette[(8 + f) * 16], BG_PLTT_ID(13), PLTT_SIZE_4BPP);

    // het bloementapijt: een cirkel vanuit het midden die steeds groter wordt (patroon uit sShaymin_Carpet)
    carpet = (t >= SHAYMIN_CARPET_START) ? (t - SHAYMIN_CARPET_START) * 3 / 2 : -1;
    for (y = 0; y < 20; y++)
    {
        dy = (y * 2 - 19) * 3;
        for (x = 0; x < 30; x++)
        {
            dx = x * 4 - 58;
            cells[y * 30 + x] = (carpet >= 0 && dx * dx + dy * dy <= carpet * carpet * 16) ? sShaymin_Carpet[y * 30 + x] : 0;
        }
    }

    // de wervelwind: drie spiraalarmen die naar buiten draaien; elke zesde is een grote bloem. Per bloem staan straal,
    // hoek en tile vooraf in sShaymin_Petals (geen delingen per frame: anders haalt de GBA het niet in een frame)
    n = min(16 + t * 6, SHAYMIN_PETALS);
    base = (t * 3) % 150;
    for (i = 0, p = sShaymin_Petals; i < n; i++, p += 3)
    {
        r = p[0] + base;
        if (r >= 150)
            r -= 150;
        ang = (p[1] + r + t * 5) & 0xFF;
        x = 15 + (Cos(ang, r) >> 3);
        y = 10 + ((Sin(ang, r) * 171) >> 11);       // r * 2/3, dan /8
        if (p[2] & 0x80)
        {
            b = 1 + SHAYMIN_SMALL + (p[2] & 0x7F) * 4;
            RTShaymin_Put(cells, x, y, b);
            RTShaymin_Put(cells, x + 1, y, b + 1);
            RTShaymin_Put(cells, x, y + 1, b + 2);
            RTShaymin_Put(cells, x + 1, y + 1, b + 3);
        }
        else
        {
            // elke kleine bloem een andere soort; ze tuimelen (spiegelen met de draaihoek)
            RTShaymin_Put(cells, x, y, p[2] | ((ang >> 6) << 6));
        }
    }

    for (y = 0; y < 20; y++)
    {
        for (x = 0; x < 30; x++)
        {
            b = cells[y * 30 + x];
            tilemap[y * 32 + x] = (b & 0x3F) ? ((b & 0x3F) | ((b >> 6) << 10) | (sShaymin_TilePal[b & 0x3F] << 12)) : 0;
        }
    }

    if (t == 0 || t == 30)
        PlaySE(SE_M_PETAL_DANCE);
    // de wereld wordt donkergroen; als het tapijt het beeld vult nog een korte, zachte lichtflits over de bloemen
    BlendPalettes(SHAYMIN_SCENE_PALETTES, min(t / 4, 10), RGB(3, 8, 5));
    if (carpet >= 22)
        BlendPalettes(PALETTES_ALL & ~SHAYMIN_SCENE_PALETTES, max(0, 6 - abs(carpet - 25) * 2), RGB(31, 28, 30));
    return carpet >= 31;
}

static const struct RouteTransition sRT_Shaymin =
{
    sShaymin_Tileset, RT_SMOL, sShaymin_Palette, 4, 4, SE_M_GUST, NULL, RTShaymin_Update, NULL
};

static void Task_Shaymin(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Shaymin);
}

// ---------------- Genesect: CRT-scanlijnen, een rood vizier springt van doel naar doel tot het op het midden vastklikt
// ("LOCKED ON"), dan een Techno Blast-straal die van links het beeld in schiet en het hele scherm vult.
// tiles: 1 scanlijnen, 2 scanbalk, 3-66 vizier (8x8), 67-88 "LOCKED ON" (11x2), 89/90/91 straal boven/kern/onder
#define GENESECT_HOPS 7
static const u8 sGenesectHopX[GENESECT_HOPS] = {2, 19, 4, 18, 8, 14, 11};
static const u8 sGenesectHopY[GENESECT_HOPS] = {1, 10, 11, 2, 4, 8, 6};
#define GENESECT_HOP_START 6
#define GENESECT_LOCK (GENESECT_HOP_START + (GENESECT_HOPS - 1) * 5)
#define GENESECT_BEAM 52

static bool8 RTGenesect_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, i, r, c, w, h;
    bool32 show;

    for (i = 0; i < 20 * 32; i++)
        tilemap[i] = RT_TILE(1);
    if (t < 40)
    {
        r = (t * 2) % 20;
        for (c = 0; c < 32; c++)
        {
            tilemap[r * 32 + c] = RT_TILE(2);
            tilemap[((r + 1) % 20) * 32 + c] = RT_TILE(2);
        }
    }
    if (t == 0)
        PlaySE(SE_PC_LOGIN);

    if (t >= GENESECT_HOP_START)
    {
        i = min((t - GENESECT_HOP_START) / 5, GENESECT_HOPS - 1);
        if (t < GENESECT_LOCK && (t - GENESECT_HOP_START) % 5 == 0)
            PlaySE(SE_SELECT);
        if (t == GENESECT_LOCK)
            PlaySE(SE_M_LOCK_ON);
        show = (t < GENESECT_LOCK || t >= GENESECT_LOCK + 12 || ((t - GENESECT_LOCK) / 3) % 2 == 0);
        if (show)
        {
            RT_PutBlock(tilemap, sGenesectHopX[i], sGenesectHopY[i], 3, 8, 8);
            if (t >= GENESECT_LOCK)
                RT_PutBlock(tilemap, 9, 15, 67, 11, 2);
        }
    }

    if (t >= GENESECT_BEAM)
    {
        if (t == GENESECT_BEAM)
            PlaySE(SE_M_HYPER_BEAM);
        w = min((t - GENESECT_BEAM) * 6 + 2, 32);
        h = (t >= GENESECT_BEAM + 5) ? (t - GENESECT_BEAM - 5) : 0;
        // kern op rij 9-10, groeit naar boven en onder; rand boven (89) en onder (91)
        for (r = 8 - h; r <= 11 + h; r++)
        {
            if (r < 0 || r >= 20)
                continue;
            for (c = 0; c < w; c++)
                tilemap[r * 32 + c] = RT_TILE(r == 8 - h ? 89 : (r == 11 + h ? 91 : 90));
        }
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 5) - 2) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 3) - 1) & 0x1FF);
    }

    BlendPalettes(RT_SCENE_PALETTES, min(t / 2, 9), RGB(10, 0, 3));
    if (t >= GENESECT_BEAM + 15)
    {
        BlendPalettes(PALETTES_ALL, min((t - GENESECT_BEAM - 15) * 4, 16), RGB_WHITE);
        return t >= GENESECT_BEAM + 19;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Genesect =
{
    sGenesect_Tileset, RT_SMOL, sGenesect_Palette, 1, 1, 0, NULL, RTGenesect_Update, NULL
};

static void Task_Genesect(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Genesect);
}

// ---------------- Mewtwo: het lab op Cinnabar Island. Mewtwo zweeft als silhouet in een gloeiende kweektank (belletjes
// stijgen, de consoles tonen een DNA-streng en een hartslag), het dagboek uit de Pokémon Mansion verschijnt regel voor
// regel ("Feb. 6: Mew gave birth. We named the newborn MEWTWO." / "Sept. 1: MEWTWO is far too powerful. We have failed
// to curb its vicious tendencies..."), dan gaan de ogen open, barst het glas in drie stappen en spat de tank uiteen in
// een psychische schokgolf (scherven vliegen weg, daarachter Mewtwo met witte ogen in een paars veld).
// tiles en tilemaps: route_transitions.py ("mewtwo"): 1-3 rand van de golf (buiten/fel/binnen), 4-7 scherven.
// Paletten: 0-2 rustig, 3-5 ontwaakt, 6-8 schokgolf (elk een kleurcyclus van 3 standen).
// Filmisch (Jordi): ±2,5x trager, getimed op Battle! Mewtwo (128 bpm, 1 maat = 112 frames):
// ogen op maat 2 (224), barsten op maat 2 tel 2 / 2,67 / 3,33, de tank spat uiteen op maat 3 (336).
#define MEWTWO_LAB    20
#define MEWTWO_PAGE1  36
#define MEWTWO_PAGE2  128
#define MEWTWO_LINE   38    // frames per regel
#define MEWTWO_EYES   224
#define MEWTWO_CRACK  280   // barst 1, +MEWTWO_CRACK_GAP barst 2, +2x barst 3
#define MEWTWO_CRACK_GAP 19
#define MEWTWO_BURST  336
#define MEWTWO_SHARDS 14

static bool8 RTMewtwo_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, r, c, k, dx, dy, d2, rad, page, line, reveal, ang, dist, x, y;
    const u16 *map = sMewtwo_Lab;
    u16 v;

    if (t >= MEWTWO_CRACK)
        map = &sMewtwo_Crack[min((t - MEWTWO_CRACK) / MEWTWO_CRACK_GAP, 2) * 600];
    rad = (t >= MEWTWO_BURST) ? 12 + (t - MEWTWO_BURST) * 9 : -1;
    page = (t >= MEWTWO_PAGE2) ? 1 : 0;

    // elk vak in een keer zijn eindwaarde geven (niet eerst wissen: dat geeft scheuren)
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 30; c++)
        {
            v = 0;
            if (t >= MEWTWO_LAB)
            {
                v = map[r * 30 + c];
                if (r >= 16 && t >= MEWTWO_PAGE1)
                {
                    line = (r - 16) / 2;
                    reveal = (t - (page ? MEWTWO_PAGE2 : MEWTWO_PAGE1) - line * MEWTWO_LINE) * 2;
                    if (c < reveal)
                        v = sMewtwo_Page[page * 120 + (r - 16) * 30 + c];
                }
            }
            if (rad >= 0)
            {
                dx = c * 8 + 4 - 120;
                dy = r * 8 + 4 - 64;
                d2 = dx * dx + dy * dy;
                if (rad > 16 && d2 < (rad - 16) * (rad - 16))
                    v = sMewtwo_Burst[r * 30 + c];
                else if (rad > 8 && d2 < (rad - 8) * (rad - 8))
                    v = 3;
                else if (d2 < rad * rad)
                    v = 2;
                else if (d2 < (rad + 8) * (rad + 8))
                    v = 1;
            }
            tilemap[r * 32 + c] = v ? RT_TILE(v) : 0;
        }
    }

    // glasscherven vliegen vooruit de schokgolf uit
    if (rad >= 0)
    {
        for (k = 0; k < MEWTWO_SHARDS; k++)
        {
            ang = (k * 256 / MEWTWO_SHARDS + (k * 37) % 11) & 0xFF;
            dist = 30 + (t - MEWTWO_BURST) * (12 + (k % 3) * 3);
            x = 120 + Cos(ang, dist);
            y = 64 + Sin(ang, dist) * 3 / 4;
            if (x < 0 || x >= 240 || y < 0 || y >= 160 || dist < rad + 10)
                continue;
            tilemap[(y / 8) * 32 + x / 8] = RT_TILE(4 + k % 4) | ((k & 1) << 10) | ((k & 2) << 10);
        }
    }

    // paletten: rustig (via de runner), ontwaakt (ogen gloeien, vloeistof flakkert), schokgolf (ringen naar buiten)
    if (t >= MEWTWO_BURST)
        LoadPalette(&sMewtwo_Palette[(6 + (t / 2) % 3) * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    else if (t >= MEWTWO_EYES)
        LoadPalette(&sMewtwo_Palette[(3 + (t / 3) % 3) * 16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    if (t >= MEWTWO_LAB && t < MEWTWO_LAB + 32)
        BlendPalette(BG_PLTT_ID(15), 16, 16 - (t - MEWTWO_LAB) / 2, RGB_BLACK); // het lab komt langzaam uit het donker

    // trillen: licht bij het barsten, harder bij de schokgolf
    if (t >= MEWTWO_BURST)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 5) - 2) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 5) - 2) & 0x1FF);
    }
    else if (t >= MEWTWO_CRACK)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 3) - 1) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    }

    if (t == MEWTWO_LAB)
        PlaySE(SE_M_BUBBLE);
    // (geen cry bij de ogen: die klinkt al bij de start van het gevecht; de muziek geeft hier een aanslag)
    if (t == MEWTWO_CRACK || t == MEWTWO_CRACK + MEWTWO_CRACK_GAP || t == MEWTWO_CRACK + 2 * MEWTWO_CRACK_GAP)
        PlaySE(SE_ICE_CRACK);
    if (t == MEWTWO_BURST)
        PlaySE(SE_ICE_BREAK);
    if (t == MEWTWO_BURST + 3)
        PlaySE(SE_M_PSYBEAM);

    BlendPalettes(RT_SCENE_PALETTES, min(t * 2, 16), RGB_BLACK);
    if (t >= MEWTWO_BURST + 26)
    {
        BlendPalettes(PALETTES_ALL, min((t - MEWTWO_BURST - 26) * 4, 16), RGB(31, 28, 31));
        return t >= MEWTWO_BURST + 30;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Mewtwo =
{
    sMewtwo_Tileset, RT_SMOL, sMewtwo_Palette, 3, 4, 0, NULL, RTMewtwo_Update, NULL
};

static void Task_Mewtwo(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Mewtwo);
}

// ---------------- Giratina: het scherm scheurt open (paarse breuklijnen vanuit het midden, het beeld golft), dan klapt
// de wereld ondersteboven (HBlank-scroll van BG1-3 per beeldlijn, zoals een kaart die omdraait) en sluiten de zes
// schaduwvleugels van de Origin Forme het beeld af, van links en rechts. Tiles: route_transitions.py ("giratina").
#define GIRATINA_FLIP_START 30
#define GIRATINA_FLIP_LEN   26
#define GIRATINA_WING_START (GIRATINA_FLIP_START + GIRATINA_FLIP_LEN)
#define GIRATINA_WING_LEN   28

static void VBlankCB_Giratina(void)
{
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2 * 2);
}

// schrijft tijdens de HBlank van lijn y de scroll van lijn y + 1 (BG1-3 horizontaal en verticaal)
static void HBlankCB_Giratina(void)
{
    u32 y = REG_VCOUNT;
    u16 h, v;

    if (y >= 227)
        y = 0;
    else if (y >= DISPLAY_HEIGHT - 1)
        return;
    else
        y++;
    h = gScanlineEffectRegBuffers[1][y];
    v = gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT + y];
    REG_BG1HOFS = h;
    REG_BG2HOFS = h;
    REG_BG3HOFS = h;
    REG_BG1VOFS = v;
    REG_BG2VOFS = v;
    REG_BG3VOFS = v;
}

static void RTGiratina_Init(struct Task *task)
{
    u32 i;

    InitTransitionData();
    ScanlineEffect_Clear();
    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        gScanlineEffectRegBuffers[0][i] = gScanlineEffectRegBuffers[1][i] = sTransitionData->cameraX;
        gScanlineEffectRegBuffers[0][DISPLAY_HEIGHT + i] = gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT + i] = sTransitionData->cameraY;
    }
    SetVBlankCallback(VBlankCB_Giratina);
    SetHBlankCallback(HBlankCB_Giratina);
    EnableInterrupts(INTR_FLAG_VBLANK | INTR_FLAG_HBLANK);
}

static bool8 RTGiratina_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    u16 *buf = gScanlineEffectRegBuffers[0];
    s32 t = task->tRtTimer, i, r, c, cc, k, amp, half, off, p;

    sTransitionData->VBlank_DMA = FALSE;

    // tilemap in een keer per vak (niet eerst wissen: dat geeft scheuren in beeld omdat het scherm al getekend wordt)
    // scheuren: elk vak verschijnt op zijn eigen moment, vanuit het midden naar buiten. Daarover de zes schaduwvleugels,
    // die van links en rechts het beeld in schuiven (rechts = links 180 graden gedraaid; ze delen nooit een tile)
    off = 30;
    if (t >= GIRATINA_WING_START)
    {
        p = min(t - GIRATINA_WING_START, GIRATINA_WING_LEN);
        off = 30 * (GIRATINA_WING_LEN - p) * (GIRATINA_WING_LEN - p) / (GIRATINA_WING_LEN * GIRATINA_WING_LEN);
    }
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 30; c++)
        {
            u16 v = 0, w;
            if (sGiratina_CrackTime[r * 30 + c] <= t * 3 / 2)
                v = RT_TILE(sGiratina_Crack[r * 30 + c]);
            cc = c + off;
            if (cc < 30 && (w = sGiratina_Wing[r * 30 + cc]) != 0)
                v = RT_TILE(w);
            cc = 29 - c + off;
            if (cc < 30 && (w = sGiratina_Wing[(19 - r) * 30 + cc]) != 0)
                v = RT_TILE(w) | 0x0C00;
            tilemap[r * 32 + c] = v;
        }
    }

    // golvend beeld (horizontaal), dat tijdens het omklappen weer rustig wordt
    amp = (t < GIRATINA_FLIP_START) ? t / 4 : max(0, 7 - (t - GIRATINA_FLIP_START) / 3);
    SetSinWave((s16 *)buf, sTransitionData->cameraX, t * 10, 5, amp, DISPLAY_HEIGHT);

    if (t < GIRATINA_FLIP_START)
    {
        BlendPalettes(RT_SCENE_PALETTES, min(t / 4, 6), RGB(10, 6, 14));
        for (i = 0; i < DISPLAY_HEIGHT; i++)
            buf[DISPLAY_HEIGHT + i] = sTransitionData->cameraY;
    }
    else
    {
        // omklappen om de horizontale middellijn: lijn y toont beeldlijn 80 + (y - 80) / k, k van 1 naar -1
        p = min(t - GIRATINA_FLIP_START, GIRATINA_FLIP_LEN);
        k = Cos((p * 128 / GIRATINA_FLIP_LEN) & 0xFF, 256);
        half = 80 * abs(k) / 256;
        for (i = 0; i < DISPLAY_HEIGHT; i++)
        {
            s32 src = i;
            if (abs(k) >= 6)
                src = (159 + (2 * i - 159) * 256 / k) / 2;
            buf[DISPLAY_HEIGHT + i] = sTransitionData->cameraY + src - i;
        }
        SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(0, DISPLAY_WIDTH));
        SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(80 - half, 80 + half));
        SetGpuReg(REG_OFFSET_WININ, abs(k) >= 6 ? WININ_WIN0_BG_ALL : WININ_WIN0_BG0);
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0);
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
        BlendPalettes(RT_SCENE_PALETTES, min(6 + (t - GIRATINA_FLIP_START) / 4, 11), RGB(7, 0, 11));
        gPlttBufferFaded[0] = RGB_BLACK; // de leegte buiten het omklappende beeld
        if (t == GIRATINA_FLIP_START)
            PlaySE(SE_M_TELEPORT);
        if (t == GIRATINA_FLIP_START + GIRATINA_FLIP_LEN / 2)
            PlayCry_Normal(GetMonData(&gEnemyParty[0], MON_DATA_SPECIES, NULL), 0);
    }

    if (t >= GIRATINA_WING_START)
    {
        SetGpuReg(REG_OFFSET_BG0VOFS, Sin((t * 8) & 0xFF, 2) & 0x1FF);
        if (t == GIRATINA_WING_START)
            PlaySE(SE_M_NIGHTMARE);
        if (t == GIRATINA_WING_START + 10)
            PlaySE(SE_M_WING_ATTACK);
    }
    if (t == 0)
        PlaySE(SE_M_SCREECH);
    if (t == 14)
        PlaySE(SE_M_DETECT);
    sTransitionData->VBlank_DMA++;
    return t >= GIRATINA_WING_START + GIRATINA_WING_LEN + 4;
}

static void RTGiratina_Finish(struct Task *task)
{
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
    SetGpuReg(REG_OFFSET_WININ, 0);
    SetGpuReg(REG_OFFSET_WINOUT, 0);
    SetHBlankCallback(NULL);
}

static const struct RouteTransition sRT_Giratina =
{
    sGiratina_Tileset, RT_SMOL, sGiratina_Palette, 1, 1, 0, RTGiratina_Init, RTGiratina_Update, RTGiratina_Finish
};

static void Task_Giratina(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Giratina);
}

// ---------------- Victini: een grote V komt in vuur van onder het beeld aanvliegen (V-create), met een vlammenspoor
// onder de punt. Hij slaat in (wit-heet, het beeld schudt) en dan vliegt alles in brand.
// tiles (tools/grounded/route_transitions.py): 1-3 vuur, 4-5 vlammentongen, 6 vonken, daarna de V (30x18, sVictini_V)
#define VICTINI_RISE_START  6
#define VICTINI_RISE_LEN    26
#define VICTINI_IMPACT      (VICTINI_RISE_START + VICTINI_RISE_LEN)
#define VICTINI_FLOOD_START (VICTINI_IMPACT + 16)

// het beeld wordt in een buffer opgebouwd en pas de volgende frame (direct na de VBlank) in één keer naar VRAM gekopieerd,
// samen met de scroll; anders zie je halve frames (de V flitst door de vlammen heen)
#define VICTINI_ROWS 21
static EWRAM_DATA u16 sVictini_Map[VICTINI_ROWS * 32] = {0};
static EWRAM_DATA s16 sVictini_Scroll[2] = {0};

static void RTVictini_Fire(u16 *map, s32 r, s32 c, s32 t, bool32 top)
{
    if (r < 0 || r >= VICTINI_ROWS)
        return;
    map[r * 32 + (c & 31)] = RT_TILE(top ? 4 + ((c + t / 3) & 1) : 1 + ((r + c + t / 2) % 3));
}

static bool8 RTVictini_Update(struct Task *task)
{
    u16 *map = sVictini_Map;
    s32 t = task->tRtTimer, i, r, c, p, base, flood, ground;

    if (t > 0)
    {
        CpuCopy16(sVictini_Map, RT_Tilemap(), sizeof(sVictini_Map));
        SetGpuReg(REG_OFFSET_BG0HOFS, sVictini_Scroll[0] & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, sVictini_Scroll[1] & 0x1FF);
    }
    CpuFill16(0, sVictini_Map, sizeof(sVictini_Map));

    // positie van de V in pixels (bovenkant), van onder het beeld naar boven met een uitloop
    if (t < VICTINI_RISE_START)
        p = 176;
    else if (t < VICTINI_IMPACT)
    {
        s32 u = VICTINI_RISE_LEN - (t - VICTINI_RISE_START); // aflopend
        p = 8 + 168 * u * u / (VICTINI_RISE_LEN * VICTINI_RISE_LEN);
    }
    else
        p = 8;
    base = p >> 3;

    // vonken stijgen op over het beeld
    for (i = 0; i < 6; i++)
        map[((19 - ((t / 2 + i * 7) % 20)) * 32) + ((i * 11 + t / 5) % 30)] = RT_TILE(6);

    // vuur aan de onderrand, groeit de eerste frames aan
    ground = min(t / 4, 2);
    for (c = 0; c < 31; c++)
        for (r = 21 - ground; r <= 20; r++)
            RTVictini_Fire(map, r, c, t, r == 21 - ground);

    // vlammenspoor onder de punt zolang hij vliegt
    if (t >= VICTINI_RISE_START && t < VICTINI_IMPACT + 6)
    {
        for (r = max(base + 17, 0); r <= 20; r++)
        {
            for (c = 14; c <= 15; c++)
                RTVictini_Fire(map, r, c, t, FALSE);
            if (((r + t) & 1) == 0)
            {
                map[r * 32 + 13] = RT_TILE(6);
                map[r * 32 + 16] = RT_TILE(6);
            }
        }
    }

    // de V zelf
    for (r = 0; r < 18; r++)
    {
        if (base + r < 0 || base + r >= VICTINI_ROWS)
            continue;
        for (c = 0; c < 30; c++)
            if (sVictini_V[r * 30 + c])
                map[(base + r) * 32 + c] = RT_TILE(sVictini_V[r * 30 + c]);
    }

    // de vloed: alles vliegt in brand
    flood = (t >= VICTINI_FLOOD_START) ? (t - VICTINI_FLOOD_START) * 2 : 0;
    for (r = 21 - min(flood, 22); r <= 20; r++)
        for (c = 0; c < 31; c++)
            RTVictini_Fire(map, r, c, t, r == 21 - flood);

    // scroll voor de volgende frame: fijne verschuiving van de V, en schudden na de inslag
    sVictini_Scroll[0] = 0;
    sVictini_Scroll[1] = -(p & 7);
    if (t >= VICTINI_IMPACT)
    {
        sVictini_Scroll[0] = (Random() % 5) - 2;
        sVictini_Scroll[1] += (Random() % 5) - 2;
    }

    if (t == 0)
        PlaySE(SE_M_FLAME_WHEEL);
    if (t == VICTINI_RISE_START + 10)
        PlayCry_Normal(SPECIES_VICTINI, 0);
    if (t == VICTINI_IMPACT)
        PlaySE(SE_M_SACRED_FIRE);
    if (t == VICTINI_FLOOD_START)
        PlaySE(SE_M_EXPLOSION);

    BlendPalettes(RT_SCENE_PALETTES, min(t / 3, t >= VICTINI_IMPACT ? 12 : 8), RGB(16, 3, 0));
    // inslag: de V wordt even wit-heet
    if (t >= VICTINI_IMPACT && t < VICTINI_IMPACT + 8)
        BlendPalettes(1 << 15, 12 - (t - VICTINI_IMPACT) * 3 / 2, RGB_WHITE);
    if (flood >= 24)
    {
        BlendPalettes(PALETTES_ALL, min((flood - 24) * 4, 16), RGB(31, 30, 20));
        return flood >= 32;
    }
    return FALSE;
}

static const struct RouteTransition sRT_Victini =
{
    sVictini_Tileset, RT_SMOL, sVictini_Palette, 4, 3, 0, NULL, RTVictini_Update, NULL
};

static void Task_Victini(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Victini);
}

// ---------------- Jirachi: een wensster tuimelt fladderend van links naar rechts over het (nachtelijk donker wordende)
// beeld en laat een spoor van fonkelingen achter; dan komt hij terug, duikt draaiend en groeiend naar het midden en het
// hele beeld wordt goudwit. BG-tiles: 1-4 fonkelingen (kleurcyclus = twinkelen), sprite: de ster met wenslabels.
#define JIRACHI_DIVE  44
#define JIRACHI_FLASH 68

static void RTJirachi_Init(struct Task *task)
{
    RT_CreateSprite(task, sJirachiStar_Gfx, sJirachiStar_Palette, -40, 44);
    RT_SetSprite(task, -40, 44, 256, 0);
}

static void RTJirachi_Sparkle(u16 *tilemap, s32 x, s32 y)
{
    s32 c = (x + (Random() % 17) - 8) / 8, r = (y + (Random() % 17) - 8) / 8;
    if (c >= 0 && c < 30 && r >= 0 && r < 20)
        tilemap[r * 32 + c] = RT_TILE(1 + Random() % 4);
}

static bool8 RTJirachi_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    struct Sprite *star = &gSprites[task->tRtSprite];
    s32 t = task->tRtTimer, x, y, scale, flip, d, i;

    if (t < JIRACHI_DIVE)
    {
        // heen: fladderend (op en neer) en tuimelend (om zijn verticale as) van links naar rechts
        task->tRtA += 0x0900;
        x = -40 + t * 7;
        y = 44 + Sin((t * 14) & 0xFF, 22) + t / 2;
        scale = 256;
    }
    else
    {
        // terug: in een boog van rechtsonder naar het midden, steeds sneller draaiend en groter
        d = min(t - JIRACHI_DIVE, 22);
        task->tRtA += 0x0900 + d * 0x180;
        x = 260 - d * 140 / 22;
        y = 120 - d * 40 / 22 - Sin((d * 6) & 0xFF, 34);
        scale = 256 + d * 256 / 22;
    }
    flip = Cos((t * 9) & 0xFF, scale);
    if (flip > -40 && flip < 40)
        flip = (flip < 0) ? -40 : 40;
    star->x = x;
    star->y = y;
    SetOamMatrixRotationScaling(star->oam.matrixNum, flip, scale, task->tRtA);

    // spoor van fonkelingen; bij aankomst in het midden een uitbarsting van fonkelingen over het hele beeld
    if (t < JIRACHI_FLASH)
    {
        RTJirachi_Sparkle(tilemap, x, y);
        if (t & 1)
            RTJirachi_Sparkle(tilemap, x - 10, y + 4);
    }
    if (t >= JIRACHI_DIVE + 22 && t < JIRACHI_FLASH + 4)
        for (i = 0; i < 6; i++)
            RTJirachi_Sparkle(tilemap, Random() % 240, Random() % 160);

    if (t == 0)
        PlaySE(SE_M_MOONLIGHT);
    if (t == JIRACHI_DIVE)
        PlaySE(SE_M_COSMIC_POWER);
    if (t == JIRACHI_DIVE + 22)
        PlaySE(SE_SHINY);

    if (t < JIRACHI_FLASH)
    {
        BlendPalettes(RT_SceneWithoutSprite(), min(t / 3, 11), RGB(1, 2, 9)); // het wordt nacht
    }
    else
    {
        // de wens: alles wordt goudwit
        if (t == JIRACHI_FLASH)
        {
            PlaySE(SE_M_HEAL_BELL);
            RT_FreezePalettes();
        }
        BlendPalettes(PALETTES_ALL, min((t - JIRACHI_FLASH) * 2, 16), RGB(31, 30, 21));
    }
    return t >= JIRACHI_FLASH + 10;
}

static const struct RouteTransition sRT_Jirachi =
{
    sJirachi_Tileset, RT_SMOL, sJirachi_Palette, 4, 4, 0, RTJirachi_Init, RTJirachi_Update, RT_FinishSprite
};

static void Task_Jirachi(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Jirachi);
}

// ---------------- Darkrai: zwarte nachtmerrierook kruipt van boven en van onder dicht, als oogleden die zwaar worden,
// en de wereld zakt weg in paars-zwart. Dan gaat midden in het donker één blauw oog open boven een rode kraag; het oog
// komt op je af en alles wordt zwart. BG-tiles: 1 zwart, 2-4 rookrand onder, 5-7 rookrand boven, 8-9 slierten.
#define DARKRAI_CLOSED 40
#define DARKRAI_EYE    46
#define DARKRAI_LUNGE  70

static void RTDarkrai_Init(struct Task *task)
{
    RT_CreateSprite(task, sDarkraiEye_Gfx, sDarkraiEye_Palette, 120, 80);
    RT_SetSprite(task, 120, 80, 256, 0);
    gSprites[task->tRtSprite].invisible = TRUE;
}

static bool8 RTDarkrai_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    struct Sprite *eye = &gSprites[task->tRtSprite];
    s32 t = task->tRtTimer, r, c, top, bottom, d, open, scale;

    for (r = 0; r < 20; r++)
        for (c = 0; c < 32; c++)
            tilemap[r * 32 + c] = 0;

    // rook van onder en van boven: per kolom een golvende rand die langzaam omhoog/omlaag kruipt
    for (c = 0; c < 30; c++)
    {
        d = min(t, DARKRAI_CLOSED);
        bottom = d * 11 / DARKRAI_CLOSED + Sin((c * 23 + t * 5) & 0xFF, 2) + 1;
        top = d * 11 / DARKRAI_CLOSED + Sin((c * 31 - t * 4 + 64) & 0xFF, 2) + 1;
        for (r = 0; r < 20; r++)
        {
            u16 tileNum = 0;
            if (t >= DARKRAI_CLOSED || r > 20 - bottom || r < top - 1)
                tileNum = 1;
            else if (r == 20 - bottom)
                tileNum = 2 + (c + t / 6) % 3;
            else if (r == top - 1)
                tileNum = 5 + (c + t / 7) % 3;
            else if (r == 20 - bottom - 2 && (c + t / 4) % 5 == 0)
                tileNum = 8;
            else if (r == top + 1 && (c * 3 + t / 5) % 7 == 0)
                tileNum = 9;
            if (tileNum)
                tilemap[r * 32 + c] = RT_TILE(tileNum);
        }
    }
    BlendPalettes(RT_SceneWithoutSprite(), min(t / 3, 13), RGB(3, 0, 6)); // de wereld zakt weg in paars-zwart

    if (t == 0)
        PlaySE(SE_M_HAZE);
    if (t == DARKRAI_EYE)
        PlaySE(SE_M_NIGHTMARE);

    // het oog gaat open (verticaal opschalen), kijkt even, en komt dan op je af
    if (t >= DARKRAI_EYE)
    {
        eye->invisible = FALSE;
        open = min((t - DARKRAI_EYE) * 24, 256);
        scale = (t >= DARKRAI_LUNGE) ? 256 + (t - DARKRAI_LUNGE) * 20 : 256;
        if (scale > 512)
            scale = 512;
        SetOamMatrixRotationScaling(eye->oam.matrixNum, scale, max(open * scale / 256, 12), 0);
        if (t >= DARKRAI_LUNGE)
        {
            if (t == DARKRAI_LUNGE)
            {
                PlaySE(SE_M_FAINT_ATTACK);
                RT_FreezePalettes();
            }
            if (t >= DARKRAI_LUNGE + 8)
                BlendPalettes(PALETTES_ALL, min(t - DARKRAI_LUNGE - 8, 16), RGB_BLACK);
        }
    }
    return t >= DARKRAI_LUNGE + 24;
}

static const struct RouteTransition sRT_Darkrai =
{
    sDarkrai_Tileset, RT_SMOL, sDarkrai_Palette, 4, 5, 0, RTDarkrai_Init, RTDarkrai_Update, RT_FinishSprite
};

static void Task_Darkrai(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Darkrai);
}

// ---------------- Neo Team Plasma (Black 2/White 2): nagemaakt naar de BW2-transitie (2,58 s). Een blauwe P op een donker
// raster; een gloeiende lichtbol komt van rechts en trekt een Z door de P; alles wordt wit; het Plasma-schild verschijnt,
// flitst twee keer en dan schieten bliksems van het schild naar de randen en flakkeren. Tiles en tilemaps (30x20, palet
// 15 al ingevuld): tools/grounded/neo_plasma_transition.py. Tilemap 0 = P, 1-9 = lichtbol, 10 = volledige Z, 11 = schild,
// 12-17 = bliksemvarianten. Palet 0 = normaal, palet 1 = bliksems fel (flakkeren).
#define NP_ZSTART   14     // GIF-frame 1 (na 240 ms)
#define NP_ZFULL    32     // GIF-frame 6: Z af (9 sleutelbeelden van 2 frames)
#define NP_WHITE    47     // GIF-frames 7-9: naar wit
#define NP_SHIELD   58     // GIF-frame 10: schild uit het wit
#define NP_FLASH    86     // GIF-frames 12-13: schild flitst twee keer
#define NP_BOLTS    94     // GIF-frames 14-30: bliksems
#define NP_END      150
#define NP_KEY_Z    10
#define NP_KEY_SHIELD 11
#define NP_KEY_BOLT 12
#define NP_NUM_BOLT 6

static bool8 RTNeoPlasma_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, key, r, white = 0;

    if (t < NP_ZSTART)
        key = 0;
    else if (t < NP_ZFULL)
        key = 1 + (t - NP_ZSTART) / 2;
    else if (t < NP_SHIELD)
        key = NP_KEY_Z;
    else if (t < NP_BOLTS)
        key = NP_KEY_SHIELD;
    else
        key = NP_KEY_BOLT + ((t - NP_BOLTS) / 4) % NP_NUM_BOLT;

    // alleen bij een nieuw beeld de hele tilemap in een keer overschrijven (niet eerst wissen)
    if (task->tRtA != key + 1)
    {
        for (r = 0; r < 20; r++)
            CpuCopy16(&sNeoPlasma_Maps[key * 600 + r * 30], &tilemap[r * 32], 30 * 2);
        task->tRtA = key + 1;
    }

    // de rest van het beeld (overworld, sprites) zwart; het raster dekt het hele scherm
    BlendPalettes(RT_SCENE_PALETTES, 16, RGB_BLACK);
    if (t >= NP_BOLTS && (t & 2))
        LoadPalette(&sNeoPlasma_Palette[16], BG_PLTT_ID(15), PLTT_SIZE_4BPP);

    if (t < 4)
        BlendPalette(BG_PLTT_ID(15), 16, 16 - t * 4, RGB_BLACK);
    else if (t >= NP_WHITE && t < NP_WHITE + 7)
        white = 2 + (t - NP_WHITE) * 2;
    else if (t >= NP_WHITE + 7 && t < NP_SHIELD)
        white = 16;
    else if (t >= NP_SHIELD && t < NP_SHIELD + 4)
        white = 10 - (t - NP_SHIELD) * 3;
    else if (t >= NP_FLASH && t < NP_FLASH + 4)
        white = 9;
    else if (t >= NP_FLASH + 4 && t < NP_BOLTS)
        white = 13;
    else if (t >= NP_BOLTS && t < NP_BOLTS + 4)
        white = 4;
    if (white > 0)
        BlendPalette(BG_PLTT_ID(15), 16, white, RGB_WHITE);

    return t >= NP_END;
}

static const struct RouteTransition sRT_NeoPlasma =
{
    sNeoPlasma_Tileset, RT_SMOL, sNeoPlasma_Palette, 1, 1, 0, NULL, RTNeoPlasma_Update, NULL
};

static void Task_NeoPlasma(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_NeoPlasma);
}

// ---------------- SickBlik (Jordi): eerst de mugshot; vanuit het witte scherm zit je aan tafel bij een yin-yang-hotpot
// (stoom en bubbels via een kleurcyclus). Harde cut naar het bovenaanzicht: de S-scheiding trekt recht tot de band, de rand
// wordt zwart, de ingrediënten zinken en een blokje tofu wordt de knop: de hotpot is een Poké Ball. Het bovenaanzicht
// bestaat uit SB_KEYS sleutelbeelden; hun tiles gaan om en om in twee buffers achter de vaste tiles (nooit in de buffer die
// in beeld is). Paletten 13-15, alles uit tabellen (tools/grounded/sickblik_transition.py).
#define SB_PALS      ((1 << 13) | (1 << 14) | (1 << 15))
#define SB_TABLE_END 84   // frames aan tafel
#define SB_HOLD0     8    // het eerste bovenaanzicht
#define SB_KEY_LEN   3    // frames per sleutelbeeld
#define SB_CYCLE_LEN 5    // frames per stap van de stoom/bubbel-cyclus
#define tSbKey      tRtB
#define tSbCount    tRtC
#define tSbCycle    data[5]
#define tSbCycleT   data[6]
#define tSickBlikPhase data[15]
#define tSbFlash    data[5]

static void SB_ShowMap(const u16 *map)
{
    u16 *tilemap = RT_Tilemap();
    u32 r;
    for (r = 0; r < 20; r++)
        CpuCopy16(&map[r * 30], &tilemap[r * 32], 30 * 2);
}

static u32 *SB_Tileset(void)
{
    u16 *tilemap, *tileset;
    GetBg0TilesDst(&tilemap, &tileset);
    return (u32 *)tileset;
}

// de tiles van de sleutelbeelden zijn per beeld LZ77-gecomprimeerd (±58 i.p.v. 128 KB): een frame wordt het volgende
// beeld uitgepakt in een buffer (SB_UnpackKey), een frame later gaat het naar de vrije VRAM-buffer (SB_UploadKey);
// beide in de dode tijd waarin het getoonde beeld de andere buffer gebruikt
static EWRAM_DATA u8 *sSickBlik_Buffer = NULL;

static void SB_UnpackKey(u32 key)
{
    if (sSickBlik_Buffer != NULL)
        FastLZ77UnCompWram(&sSickBlik_TopDyn[sSickBlik_KeyTiles[key][0]], sSickBlik_Buffer);
}

static void SB_UploadKey(u32 key)
{
    if (sSickBlik_Buffer != NULL)
        CpuCopy32(sSickBlik_Buffer, &SB_Tileset()[(1 + SB_TOP_STATIC + (key & 1) * SB_TOP_DMAX) * 8],
                  sSickBlik_KeyTiles[key][1] * 32);
}

static void RTSickBlik_Init(struct Task *task)
{
    sSickBlik_Buffer = Alloc(SB_TOP_DMAX * TILE_SIZE_4BPP);
    SB_ShowMap(sSickBlik_TableMap);
    task->tSbCycle = 0;
    task->tSbCycleT = 0;
    LoadPalette(sSickBlik_TablePals, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    BlendPalettes(SB_PALS, 16, RGB_WHITE);
}

static bool8 RTSickBlik_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    // de rest van het beeld (overworld, sprites) zwart; de tafel dekt het hele scherm
    BlendPalettes(PALETTES_ALL & ~SB_PALS, 16, RGB_BLACK);
    if (t < SB_TABLE_END)
    {
        // aan tafel: stoom stijgt en de bouillon borrelt (paletcyclus); vanuit het witte scherm infaden
        if (++task->tSbCycleT == SB_CYCLE_LEN)
        {
            task->tSbCycleT = 0;
            if (++task->tSbCycle == SB_CYCLE)
                task->tSbCycle = 0;
        }
        LoadPalette(&sSickBlik_TablePals[task->tSbCycle * 48], BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
        if (t < 8)
            BlendPalettes(SB_PALS, 16 - t * 2, RGB_WHITE);
        if (t == 4)
            PlaySE(SE_M_BUBBLE3);
        return FALSE;
    }
    if (t == SB_TABLE_END)
    {
        // camera-cut: een zwart beeld, daarin worden de tiles van het bovenaanzicht geladen
        BlendPalettes(SB_PALS, 16, RGB_BLACK);
        SB_UnpackKey(0);
        return FALSE;
    }
    if (t == SB_TABLE_END + 1)
    {
        CpuCopy32(sSickBlik_TopStatic, &SB_Tileset()[8], SB_TOP_STATIC * 32);
        SB_UploadKey(0);
        SB_ShowMap(sSickBlik_TopMaps);
        task->tSbKey = 0;
        task->tSbCount = 0;
        LoadPalette(sSickBlik_TopPals, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
        BlendPalettes(SB_PALS, 16, RGB_BLACK);
        return FALSE;
    }
    // bovenaanzicht: de morph. Het volgende sleutelbeeld wordt een frame na de wissel in de vrije buffer geladen.
    task->tSbCount++;
    if (task->tSbCount == 1 && task->tSbKey + 1 < SB_KEYS)
        SB_UnpackKey(task->tSbKey + 1);
    if (task->tSbCount == 2 && task->tSbKey + 1 < SB_KEYS)
        SB_UploadKey(task->tSbKey + 1);
    if (task->tSbCount >= (task->tSbKey == 0 ? SB_HOLD0 : SB_KEY_LEN))
    {
        task->tSbKey++;
        task->tSbCount = 0;
        SB_ShowMap(&sSickBlik_TopMaps[task->tSbKey * 600]);
    }
    LoadPalette(&sSickBlik_TopPals[task->tSbKey * 48], BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    if (task->tSbKey == SB_KEYS - 1)
    {
        PlaySE(SE_BALL_OPEN); // klik: het is een Poké Ball
        return TRUE;
    }
    return FALSE;
}

static void RTSickBlik_Finish(struct Task *task)
{
    TRY_FREE_AND_SET_NULL(sSickBlik_Buffer);
}

static const struct RouteTransition sRT_SickBlik =
{
    (const u16 *)sSickBlik_TableTiles, sizeof(sSickBlik_TableTiles), &sSickBlik_TablePals[32], 1, 1, 0,
    RTSickBlik_Init, RTSickBlik_Update, RTSickBlik_Finish
};

static void Task_SickBlik(u8 taskId)
{
    struct Task *task = &gTasks[taskId];

    if (task->tSickBlikPhase == 0)
    {
        // de mugshot tot de slides klaar zijn; de trage witte fade van de mugshot slaan we over (scheelt ruim een seconde)
        while (task->tState < 6 && sMugshot_Funcs[task->tState](task))
            ;
        if (task->tState == 6)
        {
            task->tSbFlash = 0;
            task->tSickBlikPhase = 1;
        }
        return;
    }
    if (task->tSickBlikPhase == 1)
    {
        // snelle witte flits (4 frames), dan alles van de mugshot opruimen zoals bij Colress
        task->tSbFlash += 4;
        BlendPalettes(PALETTES_ALL, task->tSbFlash, RGB_WHITE);
        if (task->tSbFlash >= 16)
        {
            SetVBlankCallback(NULL);
            DmaStop(0);
            SetHBlankCallback(NULL);
            SetGpuReg(REG_OFFSET_BLDCNT, 0);
            SetGpuReg(REG_OFFSET_BLDY, 0);
            ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
            SetVBlankCallback(VBlankCB_BattleTransition);
            gSprites[task->data[11]].invisible = TRUE; // tOpponentSpriteAId
            gSprites[task->data[14]].invisible = TRUE; // tPlayerSpriteId
            task->tState = 0;
            task->tSickBlikPhase = 2;
        }
        return;
    }
    RouteTransition_Run(taskId, &sRT_SickBlik);
}

#undef tSbKey
#undef tSbCount
#undef tSbCycle
#undef tSbCycleT
#undef tSickBlikPhase
#undef tSbFlash

// ---------------- Team Rocket: zwarte balken schuiven om en om van links en rechts dicht (rode voorrand), rode
// snelheidsstrepen schieten over het zwart, en een grote rode R zoomt draaiend in en stempelt met een klap
// (witte flits, het beeld schudt). Alle grunts en Petrel (zie GetTrainerBattleTransition in battle_setup.c).
// tiles: 1 zwart, 2/3 rode voorrand (balk van links / van rechts), 4 streep-lijf, 5 streep-kop, 6 streep-staart
#define ROCKET_STAMP 18 // frame waarop de R neerkomt

// snelheid per rij (tiles per frame) en een vertraging (frames), zodat de balken niet tegelijk aankomen
static const u8 sRocketBarSpeed[20] = {4, 3, 5, 3, 4, 5, 3, 4, 3, 5, 4, 3, 5, 4, 3, 4, 5, 3, 4, 3};
static const u8 sRocketBarDelay[20] = {0, 1, 0, 2, 1, 0, 2, 1, 0, 1, 2, 0, 1, 0, 2, 1, 0, 2, 0, 1};
// snelheidsstrepen: rij, snelheid in tiles per frame (negatief = naar links), startframe
static const s8 sRocketStreaks[][3] = {
    {2, 3, 8}, {5, -4, 9}, {8, 5, 10}, {11, -3, 11}, {14, 4, 9}, {17, -5, 12},
    {3, -4, 20}, {7, 5, 22}, {12, -5, 21}, {16, 4, 23}, {1, 5, 28}, {18, -4, 27}, {10, 3, 30}, {6, -5, 32},
};
// schaal van de R (256 = 1x, 512 = 2x) en draaiing per frame vanaf het verschijnen
static const u16 sRocketScale[] = {24, 48, 88, 140, 200, 268, 340, 412, 468, 512};
static const s16 sRocketAngle[] = {-0x2400, -0x2000, -0x1A00, -0x1400, -0x0E00, -0x0900, -0x0500, -0x0200, -0x0080, 0};
// schudden na de klap (pixels), steeds minder
static const s8 sRocketShake[] = {5, -5, 4, -4, 4, -3, 3, -2, 2, -1, 1, 0};

static void RTRocket_Init(struct Task *task)
{
    RT_CreateSprite(task, sRocketR_Gfx, sRocketR_Palette, 120, 76);
    gSprites[task->tRtSprite].invisible = TRUE;
}

static bool8 RTRocket_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, r, c, len, n, shake = 0;
    s16 streakHead[20];
    s8 streakDir[20];
    u32 i;

    // snelheidsstrepen (5 tiles: staart, 3x lijf, kop) over het zwart, per rij hoogstens een; pas als de balk dicht is
    for (r = 0; r < 20; r++)
    {
        streakDir[r] = 0;
        streakHead[r] = 0;
    }
    for (i = 0; i < ARRAY_COUNT(sRocketStreaks); i++)
    {
        s32 row = sRocketStreaks[i][0], v = sRocketStreaks[i][1], start = sRocketStreaks[i][2];
        if (t < start || (t - sRocketBarDelay[row]) * sRocketBarSpeed[row] <= 33)
            continue;
        streakHead[row] = (v > 0) ? (t - start) * v : 29 + (t - start) * v;
        streakDir[row] = (v > 0) ? 1 : -1;
    }
    // balken: rij r komt van links (even) of rechts (oneven); len = aantal zwarte tiles. De hele tilemap van 32x32 doet
    // mee, zodat er bij het schudden geen wereld langs de randen piept. Elk vak krijgt in een keer zijn eindwaarde.
    for (r = 0; r < 32; r++)
    {
        s32 rr = (r < 20) ? r : r - 20;
        len = (t - sRocketBarDelay[rr]) * sRocketBarSpeed[rr];
        if (len < 0)
            len = 0;
        for (c = 0; c < 32; c++)
        {
            u16 tileNum = 0;
            n = (r & 1) ? (31 - c) : c; // afstand vanaf de kant waar de balk vandaan komt
            if (n < len - 1 || len > 32)
                tileNum = 1;
            else if (n == len - 1)
                tileNum = (r & 1) ? 3 : 2;
            if (r < 20 && streakDir[r] != 0 && c < 30)
            {
                s32 k = (streakDir[r] > 0) ? streakHead[r] - c : c - streakHead[r];
                if (k >= 0 && k < 5)
                    tileNum = (k == 0) ? 5 : (k == 4 ? 6 : 4);
            }
            tilemap[r * 32 + c] = tileNum ? RT_TILE(tileNum) : 0;
        }
    }
    // 3. de R: verschijnt op frame 9, zoomt draaiend in en stempelt op ROCKET_STAMP
    if (t == 2)
        PlaySE(SE_M_RAZOR_WIND);
    if (t >= ROCKET_STAMP - 9)
    {
        struct Sprite *sprite = &gSprites[task->tRtSprite];
        u32 f = min(t - (ROCKET_STAMP - 9), 9);
        if (t >= ROCKET_STAMP && t - ROCKET_STAMP < (s32)ARRAY_COUNT(sRocketShake))
            shake = sRocketShake[t - ROCKET_STAMP];
        sprite->invisible = FALSE;
        RT_SetSprite(task, 120 + shake, 76 - shake / 2, sRocketScale[f], (u16)sRocketAngle[f]);
        SetGpuReg(REG_OFFSET_BG0HOFS, (-shake) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, (shake / 2) & 0x1FF);
        if (t == ROCKET_STAMP)
        {
            PlaySE(SE_M_MEGA_KICK2);
            SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        }
        // witte flits op de R bij de klap
        if (t >= ROCKET_STAMP && t < ROCKET_STAMP + 6)
            BlendPalettes(1 << (16 + IndexOfSpritePaletteTag(RT_SPRITE_TAG)), 15 - (t - ROCKET_STAMP) * 3, RGB_WHITE);
    }
    return t >= ROCKET_STAMP + 26;
}

static const struct RouteTransition sRT_Rocket =
{
    sRocket_Tileset, RT_SMOL, sRocket_Palette, 1, 1, 0, RTRocket_Init, RTRocket_Update, RT_FinishSprite
};

static void Task_Rocket(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Rocket);
}

// ---------------- Zarude: de jungle groeit van de randen dicht (bladerdek), lianen zwiepen van boven naar beneden, drie
// klauwkrassen scheuren door het blad op de taiko-slagen van "Battle! Zarude" (168 BPM: maat = 86 frames) en op de
// accent in maat 2 doemt Zarude's silhouet op met gloeiende rode ogen die op de achtsten pulseren. Daarna zwart, net voor de koperfanfare.
// tiles (tools/grounded/route_transitions.py): 1-4 bladerdek, 5-7 bladrand, 8-9 liaan, 10 liaantip, 11.. klauwen
#define ZARUDE_CLAW1   15
#define ZARUDE_CLAW2   26
#define ZARUDE_CLAW3   47
#define ZARUDE_REVEAL  72
#define ZARUDE_DARK    118
#define ZARUDE_END     128

static const u8 sZarudeVineCol[] = {3, 9, 16, 22, 27};
static const u8 sZarudeVineStart[] = {4, 10, 18, 7, 24};
static const u8 sZarudeVineLen[] = {9, 13, 7, 11, 14};
static const s8 sZarudeVineBounce[] = {1, 2, 2, 1, 0, -1, -1, 0};
static const u8 sZarudeClawStart[] = {ZARUDE_CLAW1, ZARUDE_CLAW2, ZARUDE_CLAW3};
static const s8 sZarudeShake[] = {4, -4, 3, -3, 2, -1, 1, 0};

static void RTZarude_Init(struct Task *task)
{
    RT_CreateSprite(task, sZarudeSil_Gfx, sZarudeSil_Palette, 120, 84);
    RT_SetSprite(task, 120, 84, 256, 0);
    gSprites[task->tRtSprite].invisible = TRUE;
}

static bool8 RTZarude_Update(struct Task *task)
{
    u16 *tilemap = RT_Tilemap();
    s32 t = task->tRtTimer, r, c, k, threshold, shake = 0;
    const u8 *depth = sZarude_Depth;

    // 1. bladerdek: een vak is dicht als zijn diepte (afstand tot de rand) onder de drempel ligt; de drempel groeit.
    // Per vak alleen een vergelijking (de hele update moet ruim binnen een frame blijven).
    threshold = (t * 54) >> 4; // ±3 s incl. de flits vooraf (blazers op ±5,7 s, na de gevechtsintro)
    for (r = 0; r < 20; r++)
    {
        u16 *row = &tilemap[r * 32];
        for (c = 0; c < 30; c++)
        {
            s32 d = *depth++;
            if (d < threshold - 14)
                row[c] = RT_TILE(1 + ((r * 7 + c * 3) & 3));
            else if (d < threshold)
                row[c] = RT_TILE(5 + ((r + c + (t >> 3)) & 1) + ((r & 2) >> 1));
            else
                row[c] = 0;
        }
    }
    // 2. lianen zwiepen van boven naar beneden (met een kleine stuiter)
    for (k = 0; k < (s32)ARRAY_COUNT(sZarudeVineCol); k++)
    {
        s32 d = t - sZarudeVineStart[k], len;
        if (d <= 0)
            continue;
        if (d < sZarudeVineLen[k])
            len = d;
        else
            len = sZarudeVineLen[k] + sZarudeVineBounce[min(d - sZarudeVineLen[k], (s32)ARRAY_COUNT(sZarudeVineBounce) - 1)];
        for (r = 0; r < len && r < 20; r++)
            tilemap[r * 32 + sZarudeVineCol[k]] = RT_TILE((r == len - 1) ? 10 : 8 + ((r + k) & 1));
    }
    // 3. klauwkrassen: vegen in een paar frames over het beeld en blijven staan
    for (k = 0; k < 3; k++)
    {
        const u16 *claw = &sZarude_Claws[k * 600];
        s32 prog = (t - sZarudeClawStart[k]) * 12;
        if (prog < 0)
            continue;
        for (r = 0; r < 20; r++)
        {
            for (c = 0; c < 30; c++)
            {
                u16 cl = *claw++;
                if (cl != 0 && ((k == 1) ? r + c : r + 29 - c) <= prog)
                    tilemap[r * 32 + c] = RT_TILE(cl);
            }
        }
    }

    // klap bij elke kras: het beeld schudt even
    for (k = 0; k < 3; k++)
    {
        s32 d = t - sZarudeClawStart[k];
        if (d >= 0 && d < (s32)ARRAY_COUNT(sZarudeShake))
            shake = sZarudeShake[d];
        if (d == 0)
            PlaySE(SE_M_RAZOR_WIND);
    }
    SetGpuReg(REG_OFFSET_BG0HOFS, shake & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, (shake / 2) & 0x1FF);

    if (t == 0)
        PlaySE(SE_M_GRASSWHISTLE);
    if (t == sZarudeVineStart[0])
        PlaySE(SE_M_BIND);

    // de wereld wordt jungle-donker
    if (t < ZARUDE_DARK)
        BlendPalettes(RT_SceneWithoutSprite(), min(t >> 3, 10), RGB(1, 6, 2));

    // silhouet: komt in maat 3 op, groeit langzaam; ogen pulseren op de achtsten (11 frames)
    if (t >= ZARUDE_REVEAL)
    {
        struct Sprite *sil = &gSprites[task->tRtSprite];
        s32 d = t - ZARUDE_REVEAL;
        u32 palNum = IndexOfSpritePaletteTag(RT_SPRITE_TAG);
        sil->invisible = FALSE;
        RT_SetSprite(task, 120, 84 - (d >> 2), min(200 + d * 10, 512), 0);
        if (d == 4)
            PlayCry_Normal(SPECIES_ZARUDE, 0);
        if (d < 12)
            BlendPalettes(1 << (16 + palNum), 12 - d, RGB_BLACK); // uit het donker
        // ogen fel/dof
        gPlttBufferFaded[OBJ_PLTT_ID(palNum) + 8] = ((d % 11) < 4) ? RGB(31, 12, 6) : RGB(24, 2, 1);
    }
    if (t == ZARUDE_DARK)
    {
        PlaySE(SE_M_SCREECH);
        RT_FreezePalettes();
    }
    if (t >= ZARUDE_DARK)
        BlendPalettes(PALETTES_ALL, min((t - ZARUDE_DARK) * 2, 16), RGB_BLACK);
    return t >= ZARUDE_END;
}

static const struct RouteTransition sRT_Zarude =
{
    sZarude_Tileset, RT_SMOL, sZarude_Palette, 1, 1, 0, RTZarude_Init, RTZarude_Update, RT_FinishSprite
};

static void Task_Zarude(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Zarude);
}

// ---------------- Loyal Three (Okidogi, Munkidori, Fezandipiti): hun Toxic Chain zoals op de artwork (magenta buis in
// ringen, met als eindstuk de "halve schedel": een ring met twee uitwaaierende tanden). De ketting valt van boven in beeld
// en slingert als een zware ketting uitdempend heen en weer rond de nek (links buiten beeld), terwijl hij wat op en neer
// deint; het beeld wordt donker-paars, dan de gewone fade. Drie vooraf getekende standen; het restje draaihoek per
// scanline als BG0HOFS (HBlank) en als één BG0VOFS. De standwissel en de scroll gaan samen in de VBlank (geen scheuren).
// Alles per frame staat vooraf in route_poisonchain_anim.bin (route_transitions.py).
#define POISONCHAIN_FRAMES ((s32)(sizeof(sPoisonChain_Anim) / (3 * 2)))
#define POISONCHAIN_PIVOT_Y 126
#define tPcPending data[0] // sTransitionData: stand die in de volgende VBlank getekend wordt
#define tPcShown   data[1] // sTransitionData: stand die nu in de tilemap staat

static void VBlankCB_PoisonChain(void)
{
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
    {
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2 * 2);
        sTransitionData->VBlank_DMA = FALSE;
    }
    if (sTransitionData->tPcPending != sTransitionData->tPcShown)
    {
        // nieuwe stand: alleen de vakken die verschillen, elk in een keer zijn eindwaarde
        u16 *tilemap = RT_Tilemap();
        const u16 *map = &sPoisonChain_Map[sTransitionData->tPcPending * 600];
        const u16 *prev = (sTransitionData->tPcShown >= 0) ? &sPoisonChain_Map[sTransitionData->tPcShown * 600] : NULL;
        u32 r, c;
        for (r = 0; r < 20; r++)
        {
            for (c = 0; c < 30; c++, map++)
            {
                if (prev != NULL && *map == *prev++)
                    continue;
                tilemap[r * 32 + c] = *map ? RT_TILE(*map) : 0;
            }
        }
        sTransitionData->tPcShown = sTransitionData->tPcPending;
    }
}

static void HBlankCB_PoisonChain(void)
{
    u32 y = REG_VCOUNT;

    if (y >= 227)
        y = 0;
    else if (y >= DISPLAY_HEIGHT - 1)
        return;
    else
        y++;
    REG_BG0HOFS = gScanlineEffectRegBuffers[1][y];
    REG_BG0VOFS = gScanlineEffectRegBuffers[1][DISPLAY_HEIGHT + y];
}

// scrollwaarden van frame t in buffer 0: per scanline HOFS = restje draaihoek (Q12) * (beeldlijn - draaipunt)
static void PoisonChain_SetScroll(s32 t)
{
    const s16 *anim = (const s16 *)&sPoisonChain_Anim[t * 3];
    s32 rest = anim[1], vofs = anim[2], y;
    u16 *buf = gScanlineEffectRegBuffers[0];

    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        buf[y] = ((rest * (y + vofs - POISONCHAIN_PIVOT_Y)) >> 12) & 0x1FF;
        buf[DISPLAY_HEIGHT + y] = vofs & 0x1FF;
    }
    sTransitionData->tPcPending = anim[0];
}

static void RTPoisonChain_Init(struct Task *task)
{
    InitTransitionData();
    ScanlineEffect_Clear();
    sTransitionData->tPcShown = -1;
    PoisonChain_SetScroll(0);
    CpuCopy16(gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2 * 2);
    SetVBlankCallback(VBlankCB_PoisonChain);
    SetHBlankCallback(HBlankCB_PoisonChain);
    EnableInterrupts(INTR_FLAG_VBLANK | INTR_FLAG_HBLANK);
}

static bool8 RTPoisonChain_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    if (t < POISONCHAIN_FRAMES)
    {
        PoisonChain_SetScroll(t);
        sTransitionData->VBlank_DMA = TRUE;
    }
    if (t == 0)
        PlaySE(SE_M_BIND);
    else if (t == 62)
        PlaySE(SE_M_TOXIC);
    BlendPalettes(RT_SCENE_PALETTES, min(t >> 1, 14), RGB(2, 0, 4));
    return t >= POISONCHAIN_FRAMES;
}

static void RTPoisonChain_Finish(struct Task *task)
{
    SetHBlankCallback(NULL);
    SetVBlankCallback(VBlankCB_BattleTransition);
}

#undef tPcPending
#undef tPcShown

static const struct RouteTransition sRT_PoisonChain =
{
    sPoisonChain_Tileset, RT_SMOL, sPoisonChain_Palette, 1, 1, 0, RTPoisonChain_Init, RTPoisonChain_Update, RTPoisonChain_Finish
};

static void Task_PoisonChain(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_PoisonChain);
}

// ---------------- Dave (Freed From Desire): penalty vanuit de schutter. Het veld gaat open als een tv-beeld, de bal
// wipt op de riff, wordt op een riffnoot getrapt en zit op de volgende strak in de winkelhaak (paal-tik, net bolt),
// dan GOAL! groot in beeld (pop-in, schudden, knipperen) en op de klap van tel 5 naar het gevecht.
// Tiles/tilemaps/bal/baan: tools/grounded/dave_transition.py. Tilemaps zijn 32x22 (rij 21 = rij 0 voor boven het beeld).
// Muziek (128 BPM, gMPlayInfo_BGM.clock 24 per tel): riffnoten op klok 0/24/42/60/84 = muziekframe 0/28/50/71/99,
// klappen op klok 24/72/120 = muziekframe 28/85/141 (gemeten in mGBA).
// De transitie begint DAVE_MUSIC_OFS frames na de muziek (gemeten met gMPlayInfo_BGM.clock).
#define DAVE_MUSIC_OFS 19                 // gemeten: rij 9/10 verschijnt op muziekframe 19
#define DAVE_T(m)      ((m) - DAVE_MUSIC_OFS)
#define DAVE_REVEAL    10                 // beeld gaat open vanuit het midden
#define DAVE_HOP       DAVE_T(50)         // riffnoot 3: de bal wipt even op
#define DAVE_KICK      DAVE_T(71)         // riffnoot 4: trap
#define DAVE_FLIGHT    28
#define DAVE_HIT       (DAVE_KICK + DAVE_FLIGHT) // riffnoot 5 (muziekframe 99): in de winkelhaak
#define DAVE_GOAL      (DAVE_HIT + 3)
#define DAVE_END       (DAVE_T(141) - 3)  // klap op tel 5: de fade naar het gevecht begint (na 2 frames vasthouden)
#define DAVE_KEY_NET   1
#define DAVE_KEY_GOAL  5

static const s8 sDaveHop[] = {2, 4, 5, 6, 6, 5, 4, 2};
static const s8 sDaveHitShake[] = {2, -2, 2, -1, 1, -1, 1, 0};
static const s8 sDaveGoalShake[] = {4, -4, 3, -3, 3, -2, 2, -2, 1, -1, 1, 0};
// na de inslag: het net neemt de bal mee naar achteren (dx, dy, schaal) en laat hem in de hoek hangen
static const s8 sDaveNetBall[][3] = {{-1, -1, -2}, {-2, -1, -4}, {-2, 0, -5}, {-1, 1, -4}, {0, 1, -3}, {0, 2, -2}, {0, 2, -1}, {0, 3, 0}};

static void RTDave_DrawKey(struct Task *task, u32 key)
{
    u16 *tilemap = RT_Tilemap();
    if (task->tRtB == (s16)key)
        return;
    task->tRtB = key;
    CpuCopy16(&sDave_Maps[key * 32 * 22], tilemap, 32 * 21 * 2);
    CpuCopy16(&sDave_Maps[key * 32 * 22 + 21 * 32], &tilemap[31 * 32], 32 * 2);
}

static void RTDave_Init(struct Task *task)
{
    RT_CreateSprite(task, sDaveBall_Gfx, sDaveBall_Palette, sDave_Ball[0], sDave_Ball[1]);
    RT_SetSprite(task, sDave_Ball[0], sDave_Ball[1], sDave_Ball[2], 0);
    gSprites[task->tRtSprite].invisible = TRUE;
    task->tRtA = 0;  // draaihoek van de bal
    task->tRtB = -1; // getekende tilemap
}

// de penalty zelf (ongewijzigd); t = 0 is het begin van de penalty (na de tribune, zie RTDaveFull_Update)
static bool8 RTDave_Penalty(struct Task *task, s32 t)
{
    u16 *tilemap = RT_Tilemap();
    s32 x, y, scale, shake = 0, key = 0;

    // 1. beeld gaat open vanuit het midden (elke rij in één keer zijn eindwaarde)
    if (t < DAVE_REVEAL)
    {
        s32 r, k = t + 1;
        for (r = 10 - k; r < 10 + k; r++)
            CpuCopy16(&sDave_Maps[r * 32], &tilemap[r * 32], 32 * 2);
        if (t == DAVE_REVEAL - 1)
        {
            RTDave_DrawKey(task, 0);
            gSprites[task->tRtSprite].invisible = FALSE;
        }
        return FALSE;
    }

    // 2. de bal
    x = sDave_Ball[0];
    y = sDave_Ball[1];
    scale = sDave_Ball[2];
    if (t >= DAVE_HOP && t < DAVE_HOP + (s32)ARRAY_COUNT(sDaveHop))
        y -= sDaveHop[t - DAVE_HOP];
    if (t == DAVE_KICK)
        PlaySE(SE_M_MEGA_KICK);
    if (t >= DAVE_KICK && t <= DAVE_HIT)
    {
        const s16 *b = &sDave_Ball[(t - DAVE_KICK) * 3];
        x = b[0];
        y = b[1];
        scale = b[2];
        task->tRtA -= 0x1500;
    }
    else if (t > DAVE_HIT)
    {
        u32 i = min(t - DAVE_HIT - 1, (s32)ARRAY_COUNT(sDaveNetBall) - 1);
        const s16 *b = &sDave_Ball[DAVE_FLIGHT * 3];
        x = b[0] + sDaveNetBall[i][0];
        y = b[1] + sDaveNetBall[i][1];
        scale = b[2] + sDaveNetBall[i][2];
        if (t < DAVE_HIT + 8)
            task->tRtA -= 0x0600;
    }

    // 3. net en GOAL!
    if (t == DAVE_HIT)
        PlaySE(SE_BALL_BOUNCE_1); // tik tegen de binnenkant van paal en lat
    if (t >= DAVE_HIT && t < DAVE_HIT + 2)
        key = DAVE_KEY_NET;
    else if (t >= DAVE_HIT + 2 && t < DAVE_HIT + 5)
        key = DAVE_KEY_NET + 1;
    else if (t >= DAVE_HIT + 5 && t < DAVE_HIT + 8)
        key = DAVE_KEY_NET + 2;
    else if (t >= DAVE_HIT + 8 && t < DAVE_HIT + 11)
        key = DAVE_KEY_NET + 3;
    if (t >= DAVE_HIT && t - DAVE_HIT < (s32)ARRAY_COUNT(sDaveHitShake))
        shake = sDaveHitShake[t - DAVE_HIT];
    if (t >= DAVE_GOAL)
    {
        if (t < DAVE_GOAL + 2)
            key = DAVE_KEY_GOAL;
        else if (t < DAVE_GOAL + 5)
            key = DAVE_KEY_GOAL + 1;
        else
            key = DAVE_KEY_GOAL + 2;
        if (t == DAVE_GOAL)
            PlaySE(SE_M_MEGA_KICK2);
        if (t - DAVE_GOAL < (s32)ARRAY_COUNT(sDaveGoalShake))
            shake = sDaveGoalShake[t - DAVE_GOAL];
        if (t >= DAVE_GOAL + 8 && ((t - DAVE_GOAL) & 4))
            LoadPalette(&sDave_Palette[16], BG_PLTT_ID(15), PLTT_SIZE_4BPP); // GOAL! knippert
    }
    RTDave_DrawKey(task, key);
    SetGpuReg(REG_OFFSET_BG0HOFS, shake & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, (shake / 2) & 0x1FF);
    RT_SetSprite(task, x - shake, y - shake / 2, scale, task->tRtA);
    return t >= DAVE_END;
}

// sRT_Dave en Task_Dave staan na de filmspeler (de tribune vooraf is een film)

//------------------------------------------------------------------------
// Project Grounded: filmtransities (Steven, Wally, Rayquaza). Een film is per gameframe een tilemap (LZ77), een
// paletset (BG 13-15) en eventueel een laadactie: de tiles (LZ77) die het nieuwe beeld nog mist, met per run de plek in
// VRAM. De encoder kiest alleen plekken die het getoonde beeld niet gebruikt, en elke nieuwe tilemap gaat naar het
// schermblok dat niet getoond wordt (31 of 27); BG0CNT wisselt pas in de VBlank. Zo is het beeld nooit half beschreven
// en wordt een stilstaande achtergrond maar één keer geladen. Gemaakt met tools/grounded/film.py (+
// steven_transition.py, wally_transition.py, rayquaza_transition.py).
//------------------------------------------------------------------------
#define FILM_BLANK      0xFFFF
#define FILM_SCREEN_B   27          // tweede schermblok (tiles 704-767 van charblock 2; de film gebruikt 1-702)
#define FILM_TILE_BUF   (351 * TILE_SIZE_4BPP)
#define FILM_MAP_BUF    (32 * 20 * 2)
#define FILM_MAP_DELTA  0x80000000  // mapofs: XOR met de vorige tilemap
#define FILM_SCENE_PALETTES (PALETTES_ALL & ~(7 << 13))
#define tFilmMap    data[11]
#define tFilmScreen data[12]
#define tFilmCnt    data[13]

struct Film
{
    const u32 *tiles;   // LZ77-blokken per laadactie
    const u32 *loads;   // per laadactie: u32 offset in tiles, u32 aantal runs | eerste run << 16
    const u32 *runs;    // per run: doeltile | aantal << 16
    const u32 *maps;    // LZ77-tilemaps (32x20)
    const u32 *mapOfs;  // per tilemap de offset in maps
    const u32 *seq;     // per gameframe 2 x u32: tilemap | laadactie << 16, paletset
    const u16 *pals;    // paletsets van 3 x 16 kleuren
    u16 numFrames;
};

static EWRAM_DATA u8 *sFilmBuffer = NULL;
static const u16 sFilm_EmptyTile[16] = {0};

static u16 *Film_Screen(struct Task *task, u32 which)
{
    u32 base = which ? FILM_SCREEN_B : ((u16)task->tFilmCnt >> 8) & 0x1F;
    return (u16 *)(BG_VRAM + base * BG_SCREEN_SIZE);
}

static void Film_Init(struct Task *task)
{
    sFilmBuffer = Alloc(FILM_TILE_BUF + FILM_MAP_BUF);
    task->tFilmMap = -1;    // = FILM_BLANK: beide schermen zijn leeg
    task->tFilmScreen = 0;
    task->tFilmCnt = GetGpuReg(REG_OFFSET_BG0CNT);
    CpuFill16(0, Film_Screen(task, 1), BG_SCREEN_SIZE);
}

static void Film_Finish(struct Task *task)
{
    SetGpuReg(REG_OFFSET_BG0CNT, (u16)task->tFilmCnt);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    TRY_FREE_AND_SET_NULL(sFilmBuffer);
}

// toont gameframe t van de film; TRUE als de film af is
static bool8 Film_Update(struct Task *task, const struct Film *film)
{
    s32 t = task->tRtTimer;
    u32 e, map, load, pal, next, i, n, r, run;
    u16 *screen, *tilemap, *tileset;
    const u8 *src;

    if (t >= film->numFrames)
    {
        // RT_LoadPalette heeft net paletset 0 teruggezet: het laatste beeld houdt zijn eigen paletten (anders flitsen
        // er bij het uitfaden losse tiles in de oude kleuren door het witte eindbeeld)
        pal = film->seq[(film->numFrames - 1) * 2 + 1] & 0xFF;
        LoadPalette(&film->pals[pal * 48], BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
        return TRUE;
    }
    e = film->seq[t * 2];
    map = e & 0xFFFF;
    load = e >> 16;
    pal = film->seq[t * 2 + 1] & 0xFF;
    LoadPalette(&film->pals[pal * 48], BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    // de wereld eronder wordt zwart (ook de sprites); daarna dekt de film hem af. Alleen tijdens het uitfaden: BlendPalettes
    // over 29 paletten kost ±60 beeldlijnen per frame
    if (t <= 8)
        BlendPalettes(FILM_SCENE_PALETTES, min(t * 2, 16), RGB_BLACK);

    if (sFilmBuffer == NULL)
        return FALSE;
    if (load != FILM_BLANK)
    {
        // de ontbrekende tiles, in plekken die het getoonde beeld niet gebruikt
        GetBg0TilesDst(&tilemap, &tileset);
        FastLZ77UnCompWram(&film->tiles[film->loads[load * 2] / 4], sFilmBuffer);
        n = film->loads[load * 2 + 1] & 0xFFFF;
        r = film->loads[load * 2 + 1] >> 16;
        src = sFilmBuffer;
        for (i = 0; i < n; i++)
        {
            run = film->runs[r + i];
            CpuCopy32(src, (u8 *)tileset + (run & 0xFFFF) * TILE_SIZE_4BPP, (run >> 16) * TILE_SIZE_4BPP);
            src += (run >> 16) * TILE_SIZE_4BPP;
        }
    }
    if (map == (u16)task->tFilmMap)
        return FALSE;
    next = task->tFilmScreen ^ 1;
    screen = Film_Screen(task, next);
    if (map == FILM_BLANK)
    {
        CpuFill16(0, screen, BG_SCREEN_SIZE);
    }
    else
    {
        if (film->mapOfs[map] & FILM_MAP_DELTA)
        {
            // verschil met de vorige tilemap, die nog in de buffer staat (tools/grounded/film_delta.py)
            u32 *dst = (u32 *)(sFilmBuffer + FILM_TILE_BUF);
            FastLZ77UnCompWram(&film->maps[(film->mapOfs[map] & ~FILM_MAP_DELTA) / 4], sFilmBuffer);
            for (i = 0; i < FILM_MAP_BUF / 4; i++)
                dst[i] ^= ((u32 *)sFilmBuffer)[i];
        }
        else
        {
            FastLZ77UnCompWram(&film->maps[film->mapOfs[map] / 4], sFilmBuffer + FILM_TILE_BUF);
        }
        CpuFastCopy(sFilmBuffer + FILM_TILE_BUF, screen, FILM_MAP_BUF);
        // rij 20 = rij 19 en rij 31 = rij 0, voor verticaal trillen
        CpuFastCopy(&screen[19 * 32], &screen[20 * 32], 64);
        CpuFastCopy(&screen[0], &screen[31 * 32], 64);
    }
    SetGpuReg(REG_OFFSET_BG0CNT, ((u16)task->tFilmCnt & ~(0x1F << 8)) | ((next ? FILM_SCREEN_B : (((u16)task->tFilmCnt >> 8) & 0x1F)) << 8));
    task->tFilmScreen = next;
    task->tFilmMap = map;
    return FALSE;
}

#define FILM(name) \
    { s##name##_Tiles, s##name##_Loads, s##name##_Runs, s##name##_Maps, s##name##_MapOfs, s##name##_Seq, s##name##_Pal, \
      ARRAY_COUNT(s##name##_Seq) / 2 }

// ---------------- Steven: zijn verzamelkast met edelstenen op donker fluweel ("ROCK", "ALSO ROCK", "THE ROCK"). De
// middelste steen gaat gloeien, de camera zoomt in op de facetten en in de acht kite-facetten verschijnen een voor een
// de badges, eerst in de blauwe tint van de steen; dan lichten ze een voor een op in hun echte kleur, elk met een klap
// (wit facet, de badge springt groot op, het beeld schokt) en een noot hoger. Dan barst de steen en spat hij uiteen.
// Vervangt de mugshot (zie battle_setup.c).
static const u32 sFilmSteven_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_steven_tiles.bin");
static const u32 sFilmSteven_Loads[] = INCBIN_U32("graphics/battle_transitions/film_steven_loads.bin");
static const u32 sFilmSteven_Runs[] = INCBIN_U32("graphics/battle_transitions/film_steven_runs.bin");
static const u32 sFilmSteven_Maps[] = INCBIN_U32("graphics/battle_transitions/film_steven_maps.bin");
static const u32 sFilmSteven_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_steven_mapofs.bin");
static const u32 sFilmSteven_Seq[] = INCBIN_U32("graphics/battle_transitions/film_steven_seq.bin");
static const u16 sFilmSteven_Pal[] = INCBIN_U16("graphics/battle_transitions/film_steven_pal.bin");
static const struct Film sFilm_Steven = FILM(FilmSteven);

// tijden: zie steven_transition.py
#define STEVEN_GLOW     56
#define STEVEN_ZOOM     96
#define STEVEN_BADGE    146
#define STEVEN_BADGE_GAP 4
#define STEVEN_LIGHT    182
#define STEVEN_LIGHT_GAP 8
#define STEVEN_CRACK    256
#define STEVEN_SHATTER  274

static const u16 sStevenBadgeNotes[8] =
{
    SE_NOTE_C, SE_NOTE_D, SE_NOTE_E, SE_NOTE_F, SE_NOTE_G, SE_NOTE_A, SE_NOTE_B, SE_NOTE_C_HIGH
};

static bool8 RTSteven_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    if (t == STEVEN_GLOW)
        PlaySE(SE_SHINY);
    if (t == STEVEN_ZOOM)
        PlaySE(SE_M_HARDEN);
    if (t >= STEVEN_BADGE && t < STEVEN_BADGE + 8 * STEVEN_BADGE_GAP && (t - STEVEN_BADGE) % STEVEN_BADGE_GAP == 0)
        PlaySE(SE_BALL_TRAY_BALL);
    if (t >= STEVEN_LIGHT && t < STEVEN_LIGHT + 8 * STEVEN_LIGHT_GAP && (t - STEVEN_LIGHT) % STEVEN_LIGHT_GAP == 0)
        PlaySE(sStevenBadgeNotes[(t - STEVEN_LIGHT) / STEVEN_LIGHT_GAP]);
    if (t == STEVEN_CRACK || t == STEVEN_CRACK + 6 || t == STEVEN_CRACK + 12)
        PlaySE(SE_ICE_CRACK);
    if (t == STEVEN_SHATTER)
        PlaySE(SE_ICE_BREAK);
    if (t >= STEVEN_CRACK && t < STEVEN_SHATTER + 14)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 3) - 1) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 3) - 1) & 0x1FF);
    }
    else if (t >= STEVEN_LIGHT && t < STEVEN_LIGHT + 8 * STEVEN_LIGHT_GAP && (t - STEVEN_LIGHT) % STEVEN_LIGHT_GAP < 4)
    {
        // de klap van een badge: het beeld schokt 4 frames
        static const s8 sKick[4][2] = {{0, -1}, {2, 1}, {-2, 0}, {1, 0}};
        const s8 *kick = sKick[(t - STEVEN_LIGHT) % STEVEN_LIGHT_GAP];
        SetGpuReg(REG_OFFSET_BG0HOFS, kick[0] & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, kick[1] & 0x1FF);
    }
    else
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    }
    return Film_Update(task, &sFilm_Steven);
}

static const struct RouteTransition sRT_Steven =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmSteven_Pal, 1, 1, 0, Film_Init, RTSteven_Update, Film_Finish
};

static void Task_Steven(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Steven);
}

// ---------------- Wally (Victory Road): een oude VHS-band. Blauw scherm met PLAY en het etiket, Route 102 (Wally vangt
// Ralts met de geleende Zigzagoon), doorspoelen door zijn groei (Mauville, zijn rondje in Meteor Falls, Kirlia wordt
// Gallade), dan een snelle zoom op zijn vastberaden gezicht, PAUSE, sneeuw. De sporingsband en het trillen doet de
// HBlank: per gameframe staat in film_wally_fx.bin de y van de band (255 = geen) en de sterkte | vlaggen.
static const u32 sFilmWally_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_wally_tiles.bin");
static const u32 sFilmWally_Loads[] = INCBIN_U32("graphics/battle_transitions/film_wally_loads.bin");
static const u32 sFilmWally_Runs[] = INCBIN_U32("graphics/battle_transitions/film_wally_runs.bin");
static const u32 sFilmWally_Maps[] = INCBIN_U32("graphics/battle_transitions/film_wally_maps.bin");
static const u32 sFilmWally_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_wally_mapofs.bin");
static const u32 sFilmWally_Seq[] = INCBIN_U32("graphics/battle_transitions/film_wally_seq.bin");
static const u16 sFilmWally_Pal[] = INCBIN_U16("graphics/battle_transitions/film_wally_pal.bin");
static const u8 sFilmWally_Fx[] = INCBIN_U8("graphics/battle_transitions/film_wally_fx.bin");
static const struct Film sFilm_Wally = FILM(FilmWally);

#define WALLY_FX_SHAKE  0x40
#define WALLY_FX_WOBBLE 0x80
#define WALLY_BAND_H    10
// tijden: zie wally_transition.py
#define WALLY_PLAY      8
#define WALLY_THROW     104
#define WALLY_CATCH     124
#define WALLY_WOBBLE    146     // drie keer wiebelen: +0, +8, +16
#define WALLY_CLICK     166
#define WALLY_FF        226
#define WALLY_ZOOM      428
#define WALLY_PAUSE     442
#define WALLY_SNOW      476

// de HOFS per beeldlijn gaat met HBlank-DMA (geen interrupt per lijn: dat kostte ±30 beeldlijnen rekentijd per frame)
static void VBlankCB_WallyVhs(void)
{
    VBlankCB_BattleTransition();
    DmaStop(0);
    if (sTransitionData->VBlank_DMA)
    {
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
        sTransitionData->VBlank_DMA = FALSE;
    }
    REG_BG0HOFS = gScanlineEffectRegBuffers[1][0];
    DmaSet(0, &gScanlineEffectRegBuffers[1][1], &REG_BG0HOFS,
           ((DMA_ENABLE | DMA_START_HBLANK | DMA_REPEAT | DMA_SRC_INC | DMA_DEST_RELOAD | DMA_16BIT) << 16) | 1);
}

static void RTWallyVhs_Init(struct Task *task)
{
    u32 i;

    Film_Init(task);
    InitTransitionData();
    ScanlineEffect_Clear();
    for (i = 0; i < DISPLAY_HEIGHT; i++)
        gScanlineEffectRegBuffers[0][i] = gScanlineEffectRegBuffers[1][i] = 0;
    SetVBlankCallback(VBlankCB_WallyVhs);
}

static void RTWallyVhs_Finish(struct Task *task)
{
    DmaStop(0);
    SetVBlankCallback(VBlankCB_BattleTransition);
    Film_Finish(task);
}

static bool8 RTWallyVhs_Update(struct Task *task)
{
    s32 t = task->tRtTimer, y, band = 255, amp = 0, flags = 0, wob;
    u16 *buf = gScanlineEffectRegBuffers[0];

    if (t < (s32)ARRAY_COUNT(sFilmWally_Fx) / 2)
    {
        band = sFilmWally_Fx[t * 2];
        amp = sFilmWally_Fx[t * 2 + 1] & 0x3F;
        flags = sFilmWally_Fx[t * 2 + 1] & 0xC0;
    }
    // per beeldlijn een horizontale verschuiving: de sporingsband scheurt, bij doorspoelen golft alles, en altijd
    // een paar lijnen die een pixel verspringen (de band is oud)
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 h = 0;
        if (band != 255 && y >= band && y < band + WALLY_BAND_H)
            h = (Random() % (2 * amp + 1)) - amp;
        if (flags & WALLY_FX_WOBBLE)
        {
            wob = Sin(((y * 6 + t * 13) & 0xFF), 2);
            h += wob;
        }
        buf[y] = h & 0x1FF;
    }
    for (y = 0; y < 3; y++)
        buf[Random() % DISPLAY_HEIGHT] = ((Random() & 1) ? 1 : 0x1FF);
    sTransitionData->VBlank_DMA = TRUE;
    // PAUSE: het stilstaande beeld trilt een lijn op en neer
    SetGpuReg(REG_OFFSET_BG0VOFS, (flags & WALLY_FX_SHAKE) ? ((t / 2) & 1) : 0);

    if (t == WALLY_PLAY)
        PlaySE(SE_PC_ON);
    if (t == WALLY_THROW)
        PlaySE(SE_BALL_THROW);
    if (t == WALLY_CATCH)
        PlaySE(SE_BALL_OPEN);
    if (t == WALLY_WOBBLE || t == WALLY_WOBBLE + 8 || t == WALLY_WOBBLE + 16)
        PlaySE(SE_BALL_BOUNCE_1);
    if (t == WALLY_CLICK)
        PlaySE(SE_RG_BALL_CLICK);
    if (t >= WALLY_FF && t < WALLY_ZOOM && (t - WALLY_FF) % 18 == 0)
        PlaySE(SE_DEX_SCROLL);
    if (t == WALLY_PAUSE)
        PlaySE(SE_CLICK);
    if (t == WALLY_SNOW)
        PlaySE(SE_PC_OFF);
    return Film_Update(task, &sFilm_Wally);
}

static const struct RouteTransition sRT_WallyVhs =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmWally_Pal, 1, 1, 0, RTWallyVhs_Init, RTWallyVhs_Update, RTWallyVhs_Finish
};

static void Task_WallyVhs(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_WallyVhs);
}

// ---------------- Rayquaza (Sky Pillar, ook de shiny en de Delta Episode): je kijkt omhoog langs de pilaar, door de
// wolken; een groene streep cirkelt steeds sneller om de top tot hij een ring is, en daaruit breekt Rayquaza's silhouet
// recht op de camera af (kop eerst, gele markeringen gloeien). Vervangt B_TRANSITION_RAYQUAZA (die blijft bestaan).
static const u32 sFilmRayquaza_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_rayquaza_tiles.bin");
static const u32 sFilmRayquaza_Loads[] = INCBIN_U32("graphics/battle_transitions/film_rayquaza_loads.bin");
static const u32 sFilmRayquaza_Runs[] = INCBIN_U32("graphics/battle_transitions/film_rayquaza_runs.bin");
static const u32 sFilmRayquaza_Maps[] = INCBIN_U32("graphics/battle_transitions/film_rayquaza_maps.bin");
static const u32 sFilmRayquaza_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_rayquaza_mapofs.bin");
static const u32 sFilmRayquaza_Seq[] = INCBIN_U32("graphics/battle_transitions/film_rayquaza_seq.bin");
static const u16 sFilmRayquaza_Pal[] = INCBIN_U16("graphics/battle_transitions/film_rayquaza_pal.bin");
static const struct Film sFilm_Rayquaza = FILM(FilmRayquaza);

// tijden: zie rayquaza_transition.py
#define RAYQUAZA_STREAK 22
#define RAYQUAZA_RING   100
#define RAYQUAZA_FLASH  116
#define RAYQUAZA_PAN    142
#define RAYQUAZA_S3     194
#define RAYQUAZA_S4     244

static bool8 RTRayquazaPillar_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    if (t == 2)
        PlaySE(SE_M_GUST);
    if (t == RAYQUAZA_STREAK + 30)
        PlaySE(SE_M_GUST2);
    if (t == RAYQUAZA_RING - 12)
        PlaySE(SE_M_TWISTER);
    if (t == RAYQUAZA_FLASH - 4)
        PlaySE(SE_M_DRAGON_RAGE);
    // Rayquaza duikt door het gat in de wolken
    if (t == RAYQUAZA_PAN + 12)
        PlaySE(SE_M_FLY);
    // de aanval: zoals in de cutscene om de 8 frames SE_INTRO_BLAST, dan schiet hij naar voren
    if (t >= RAYQUAZA_S3 && t < RAYQUAZA_S3 + 24 && ((t - RAYQUAZA_S3) & 7) == 0)
        PlaySE(SE_INTRO_BLAST);
    if (t == RAYQUAZA_S3 + 24)
        PlaySE(SE_M_HYPER_BEAM);
    return Film_Update(task, &sFilm_Rayquaza);
}

static const struct RouteTransition sRT_RayquazaPillar =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmRayquaza_Pal, 1, 1, 0, Film_Init, RTRayquazaPillar_Update, Film_Finish
};

static void Task_RayquazaPillar(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_RayquazaPillar);
}

// ---------------- gedeelde hulpjes voor de filmtransities hieronder: geluid op vaste frames en trillen
struct FilmSfx
{
    u16 frame;
    u16 se;
};

static void Film_PlaySfx(s32 t, const struct FilmSfx *sfx, u32 n)
{
    u32 i;
    for (i = 0; i < n; i++)
    {
        if (sfx[i].frame == t)
            PlaySE(sfx[i].se);
    }
}

// trillen (amp px) tussen t0 en t1, anders stil
static void Film_Shake(s32 t, s32 t0, s32 t1, u32 amp)
{
    if (t >= t0 && t < t1)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, ((s32)(Random() % (2 * amp + 1)) - (s32)amp) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, ((s32)(Random() % (2 * amp + 1)) - (s32)amp) & 0x1FF);
    }
    else
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    }
}


// ---------------- Dave (Freed From Desire), deel 1: de tribune. Een wave loopt rond, op de laatste noot van de eerste
// riff gaat het spandoek DP PENNINGS omhoog, op de klap een close-up, op de eerste noot van de tweede riff flitsen de
// camera's. Dan de penalty (RTDave_Penalty, ongewijzigd) op de tweede riff: die begint DAVE_STADIUM frames later
// (klok 192 = 225 muziekframes), dus alle penaltytijden blijven op de maat. Film: tools/grounded/dave_stadium.py.
static const u32 sFilmDaveStadium_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_dave_stadium_tiles.bin");
static const u32 sFilmDaveStadium_Loads[] = INCBIN_U32("graphics/battle_transitions/film_dave_stadium_loads.bin");
static const u32 sFilmDaveStadium_Runs[] = INCBIN_U32("graphics/battle_transitions/film_dave_stadium_runs.bin");
static const u32 sFilmDaveStadium_Maps[] = INCBIN_U32("graphics/battle_transitions/film_dave_stadium_maps.bin");
static const u32 sFilmDaveStadium_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_dave_stadium_mapofs.bin");
static const u32 sFilmDaveStadium_Seq[] = INCBIN_U32("graphics/battle_transitions/film_dave_stadium_seq.bin");
static const u16 sFilmDaveStadium_Pal[] = INCBIN_U16("graphics/battle_transitions/film_dave_stadium_pal.bin");
static const struct Film sFilm_DaveStadium = FILM(FilmDaveStadium);

#define DAVE_STADIUM    225     // lengte van de tribunefilm = één keer de riff (2 maten)
#define DAVE_SWITCH     (DAVE_STADIUM - 5) // de film is hier al zwart: penalty-tiles laden

static const struct FilmSfx sDaveStadiumSfx[] =
{
    {10, SE_APPLAUSE},
    {122, SE_APPLAUSE},
};

static void RTDaveFull_Init(struct Task *task)
{
    RTDave_Init(task);
    Film_Init(task);
}

static bool8 RTDaveFull_Update(struct Task *task)
{
    s32 t = task->tRtTimer;
    u16 *tilemap, *tileset;

    if (t < DAVE_SWITCH)
    {
        Film_PlaySfx(t, sDaveStadiumSfx, ARRAY_COUNT(sDaveStadiumSfx));
        Film_Shake(t, 206, 212, 2);
        Film_Update(task, &sFilm_DaveStadium);
        return FALSE;
    }
    if (t == DAVE_SWITCH)
    {
        // beide filmschermen leeg, het oorspronkelijke scherm terug, de penalty-tiles en het balpalet (de film heeft
        // de sprites zwart geblend) opnieuw laden
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        CpuFill16(0, Film_Screen(task, 0), BG_SCREEN_SIZE);
        CpuFill16(0, Film_Screen(task, 1), BG_SCREEN_SIZE);
        SetGpuReg(REG_OFFSET_BG0CNT, (u16)task->tFilmCnt);
        GetBg0TilesDst(&tilemap, &tileset);
        DecompressDataWithHeaderVram(sDave_Tileset, tileset);
        LoadPalette(sDaveBall_Palette, OBJ_PLTT_ID(IndexOfSpritePaletteTag(RT_SPRITE_TAG)), PLTT_SIZE_4BPP);
        TRY_FREE_AND_SET_NULL(sFilmBuffer);
        return FALSE;
    }
    if (t < DAVE_STADIUM)
        return FALSE;
    return RTDave_Penalty(task, t - DAVE_STADIUM);
}

static void RTDaveFull_Finish(struct Task *task)
{
    RT_FinishSprite(task);
    Film_Finish(task);
}

static const struct RouteTransition sRT_Dave =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sDave_Palette, 1, 1, 0, RTDaveFull_Init, RTDaveFull_Update, RTDaveFull_Finish
};

static void Task_Dave(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Dave);
}

// ---------------- Mimi (Mimikyu, Mimic Circle Route 119; ook in het Battle Stadium): een donkere kinderkamer met een
// poppenkast ("THE PIKACHU SHOW"). Het doek gaat open, de Pikachu-pop draait langzaam zijn kop opzij tot het nekje
// knakt (busted), het licht flikkert en gaat uit, en onder het doek gaan twee ogen open. Film: mimi_transition.py.
static const u32 sFilmMimi_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_mimi_tiles.bin");
static const u32 sFilmMimi_Loads[] = INCBIN_U32("graphics/battle_transitions/film_mimi_loads.bin");
static const u32 sFilmMimi_Runs[] = INCBIN_U32("graphics/battle_transitions/film_mimi_runs.bin");
static const u32 sFilmMimi_Maps[] = INCBIN_U32("graphics/battle_transitions/film_mimi_maps.bin");
static const u32 sFilmMimi_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_mimi_mapofs.bin");
static const u32 sFilmMimi_Seq[] = INCBIN_U32("graphics/battle_transitions/film_mimi_seq.bin");
static const u16 sFilmMimi_Pal[] = INCBIN_U16("graphics/battle_transitions/film_mimi_pal.bin");
static const struct Film sFilm_Mimi = FILM(FilmMimi);

// tijden: zie mimi_transition.py
#define MIMI_SNAP 150

static const struct FilmSfx sMimiSfx[] =
{
    {30, SE_CONTEST_CURTAIN_RISE},
    {80, SE_ROTATING_GATE},
    {108, SE_ROTATING_GATE},
    {132, SE_ROTATING_GATE},
    {MIMI_SNAP, SE_ICE_CRACK},
    {166, SE_M_THUNDER_WAVE},
    {192, SE_SWITCH},
    {201, SE_M_LEER},
};

static bool8 RTMimi_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    Film_PlaySfx(t, sMimiSfx, ARRAY_COUNT(sMimiSfx));
    Film_Shake(t, MIMI_SNAP, MIMI_SNAP + 8, 2);
    return Film_Update(task, &sFilm_Mimi);
}

static const struct RouteTransition sRT_Mimi =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmMimi_Pal, 1, 1, 0, Film_Init, RTMimi_Update, Film_Finish
};

static void Task_Mimi(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Mimi);
}

// ---------------- Keccles (Kecleon, een droge, echt wijze denker; ook in het Battle Stadium): een verlaten lab vol
// schoolborden. De camera zoekt (handheld): het lege lab, de aantekeningen (waarneming, camouflage, geduld), THE PLAN
// met jouw gezicht omcirkeld. Een rode zigzag hangt in de lucht, een oog gaat open in het krijt, de camouflage golft weg
// en Keccles staat er. Het krijt schrijft "WE SEE WHAT WE EXPECT." Film: keccles_transition.py.
static const u32 sFilmKeccles_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_keccles_tiles.bin");
static const u32 sFilmKeccles_Loads[] = INCBIN_U32("graphics/battle_transitions/film_keccles_loads.bin");
static const u32 sFilmKeccles_Runs[] = INCBIN_U32("graphics/battle_transitions/film_keccles_runs.bin");
static const u32 sFilmKeccles_Maps[] = INCBIN_U32("graphics/battle_transitions/film_keccles_maps.bin");
static const u32 sFilmKeccles_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_keccles_mapofs.bin");
static const u32 sFilmKeccles_Seq[] = INCBIN_U32("graphics/battle_transitions/film_keccles_seq.bin");
static const u16 sFilmKeccles_Pal[] = INCBIN_U16("graphics/battle_transitions/film_keccles_pal.bin");
static const struct Film sFilm_Keccles = FILM(FilmKeccles);

// tijden: zie keccles_transition.py
#define KECCLES_SHOT3 98

static const struct FilmSfx sKecclesSfx[] =
{
    {54, SE_M_LOCK_ON},
    {KECCLES_SHOT3, SE_M_LOCK_ON},
    {126, SE_M_LEER},
    {148, SE_M_TELEPORT},
    {194, SE_M_SKETCH},     // T_QUOTE: het krijt schrijft (twee regels)
    {205, SE_M_SKETCH},
};

// handheld: een langzaam zwalkende camera (in pixels, per 4 frames een stap)
static const s8 sKecclesWobbleX[16] = {0, 1, 1, 2, 2, 1, 1, 0, 0, -1, -1, -2, -2, -1, -1, 0};
static const s8 sKecclesWobbleY[16] = {0, 0, 1, 1, 1, 1, 0, 0, -1, -1, -1, 0, 0, 1, 0, 0};

static bool8 RTKeccles_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    Film_PlaySfx(t, sKecclesSfx, ARRAY_COUNT(sKecclesSfx));
    if (t < KECCLES_SHOT3)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, sKecclesWobbleX[(t >> 2) & 15] & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, sKecclesWobbleY[((t >> 2) + 5) & 15] & 0x1FF);
    }
    else
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    }
    return Film_Update(task, &sFilm_Keccles);
}

static const struct RouteTransition sRT_Keccles =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmKeccles_Pal, 1, 1, 0, Film_Init, RTKeccles_Update, Film_Finish
};

static void Task_Keccles(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Keccles);
}

// ---------------- Burglar (Simon, het inbreker-event; ook in het Battle Stadium): bewakingscamera CAM 03, de Burglar
// uit Red/Blue sluipt door de woonkamer, draait zich naar de camera, digitale zoom (2X, 4X), REC knippert, alarm. Film:
// burglar_transition.py.
static const u32 sFilmBurglar_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_burglar_tiles.bin");
static const u32 sFilmBurglar_Loads[] = INCBIN_U32("graphics/battle_transitions/film_burglar_loads.bin");
static const u32 sFilmBurglar_Runs[] = INCBIN_U32("graphics/battle_transitions/film_burglar_runs.bin");
static const u32 sFilmBurglar_Maps[] = INCBIN_U32("graphics/battle_transitions/film_burglar_maps.bin");
static const u32 sFilmBurglar_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_burglar_mapofs.bin");
static const u32 sFilmBurglar_Seq[] = INCBIN_U32("graphics/battle_transitions/film_burglar_seq.bin");
static const u16 sFilmBurglar_Pal[] = INCBIN_U16("graphics/battle_transitions/film_burglar_pal.bin");
static const struct Film sFilm_Burglar = FILM(FilmBurglar);

// tijden: zie burglar_transition.py
#define BURGLAR_ALARM 182

static const struct FilmSfx sBurglarSfx[] =
{
    {8, SE_PC_ON},
    {106, SE_PIN},
    {124, SE_M_LOCK_ON},
    {142, SE_M_LOCK_ON},
    {BURGLAR_ALARM, SE_M_SCREECH},
    {BURGLAR_ALARM + 16, SE_M_SCREECH},
};

static bool8 RTBurglar_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    Film_PlaySfx(t, sBurglarSfx, ARRAY_COUNT(sBurglarSfx));
    Film_Shake(t, BURGLAR_ALARM, BURGLAR_ALARM + 36, 1);
    return Film_Update(task, &sFilm_Burglar);
}

static const struct RouteTransition sRT_Burglar =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmBurglar_Pal, 1, 1, 0, Film_Init, RTBurglar_Update, Film_Finish
};

static void Task_Burglar(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Burglar);
}

// ---------------- Kyogre/Groudon (Marine Cave / Terra Cave): een oude muurschildering van hun strijd (Groudon met de
// bergen, Kyogre met de golven, braille "DONT WAKE THEM"). Er lopen barsten door vanuit de borst van degene die je wekt;
// door de barsten stroomt water of lava tot het beeld vol is, en daarin gaan de gloeiende Primal-markeringen aan.
// Vervangt B_TRANSITION_KYOGRE/GROUDON (die blijven bestaan). Zie primal_mural_transition.py.
static const u32 sFilmMuralKyogre_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_mural_kyogre_tiles.bin");
static const u32 sFilmMuralKyogre_Loads[] = INCBIN_U32("graphics/battle_transitions/film_mural_kyogre_loads.bin");
static const u32 sFilmMuralKyogre_Runs[] = INCBIN_U32("graphics/battle_transitions/film_mural_kyogre_runs.bin");
static const u32 sFilmMuralKyogre_Maps[] = INCBIN_U32("graphics/battle_transitions/film_mural_kyogre_maps.bin");
static const u32 sFilmMuralKyogre_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_mural_kyogre_mapofs.bin");
static const u32 sFilmMuralKyogre_Seq[] = INCBIN_U32("graphics/battle_transitions/film_mural_kyogre_seq.bin");
static const u16 sFilmMuralKyogre_Pal[] = INCBIN_U16("graphics/battle_transitions/film_mural_kyogre_pal.bin");
static const struct Film sFilm_MuralKyogre = FILM(FilmMuralKyogre);
static const u32 sFilmMuralGroudon_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_mural_groudon_tiles.bin");
static const u32 sFilmMuralGroudon_Loads[] = INCBIN_U32("graphics/battle_transitions/film_mural_groudon_loads.bin");
static const u32 sFilmMuralGroudon_Runs[] = INCBIN_U32("graphics/battle_transitions/film_mural_groudon_runs.bin");
static const u32 sFilmMuralGroudon_Maps[] = INCBIN_U32("graphics/battle_transitions/film_mural_groudon_maps.bin");
static const u32 sFilmMuralGroudon_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_mural_groudon_mapofs.bin");
static const u32 sFilmMuralGroudon_Seq[] = INCBIN_U32("graphics/battle_transitions/film_mural_groudon_seq.bin");
static const u16 sFilmMuralGroudon_Pal[] = INCBIN_U16("graphics/battle_transitions/film_mural_groudon_pal.bin");
static const struct Film sFilm_MuralGroudon = FILM(FilmMuralGroudon);

#define MURAL_CRACK 40
#define MURAL_LEAK  78
#define MURAL_POOL  92
#define MURAL_MARK  176

static bool8 RTMural_Update(struct Task *task, const struct Film *film, bool32 lava)
{
    s32 t = task->tRtTimer;

    if (t == MURAL_CRACK || t == MURAL_CRACK + 8 || t == MURAL_CRACK + 18)
        PlaySE(SE_ICE_CRACK);
    if (t == MURAL_CRACK + 28)
        PlaySE(SE_M_ROCK_THROW);
    if (t == MURAL_LEAK)
        PlaySE(lava ? SE_M_EMBER : SE_M_BUBBLE);
    if (t == MURAL_POOL)
        PlaySE(lava ? SE_M_HEAT_WAVE : SE_M_WATERFALL);
    if (t == MURAL_POOL + 44)
        PlaySE(lava ? SE_M_FLAMETHROWER : SE_M_SURF);
    if (t == MURAL_MARK + 20)
        PlaySE(SE_M_DETECT);
    // de muur trilt terwijl hij barst
    if (t >= MURAL_CRACK && t < MURAL_CRACK + 30 && (t & 1))
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % 3) - 1) & 0x1FF);
        SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % 3) - 1) & 0x1FF);
    }
    else if (t == MURAL_CRACK + 30 || !(t & 1))
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    }
    return Film_Update(task, film);
}

static bool8 RTKyogreMural_Update(struct Task *task)
{
    return RTMural_Update(task, &sFilm_MuralKyogre, FALSE);
}

static bool8 RTGroudonMural_Update(struct Task *task)
{
    return RTMural_Update(task, &sFilm_MuralGroudon, TRUE);
}

static const struct RouteTransition sRT_KyogreMural =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmMuralKyogre_Pal, 1, 1, 0, Film_Init, RTKyogreMural_Update, Film_Finish
};

static const struct RouteTransition sRT_GroudonMural =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmMuralGroudon_Pal, 1, 1, 0, Film_Init, RTGroudonMural_Update, Film_Finish
};

static void Task_KyogreMural(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_KyogreMural);
}

static void Task_GroudonMural(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GroudonMural);
}

// ---------------- Ogerpon (Fortree Jungle, einde van de quest): een maskerkraam op een nachtfestival. Vier maskers
// (uit de echte Ogerpon-sprites), één lege haak ("STOLEN"), het Teal-masker "NOT FOR SALE". De lantaarns gaan uit, de
// camera zoomt in, de ogen van het masker gaan branden en Ogerpon springt in een wolk bladeren. Zie ogerpon_transition.py.
static const u32 sFilmOgerpon_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_ogerpon_tiles.bin");
static const u32 sFilmOgerpon_Loads[] = INCBIN_U32("graphics/battle_transitions/film_ogerpon_loads.bin");
static const u32 sFilmOgerpon_Runs[] = INCBIN_U32("graphics/battle_transitions/film_ogerpon_runs.bin");
static const u32 sFilmOgerpon_Maps[] = INCBIN_U32("graphics/battle_transitions/film_ogerpon_maps.bin");
static const u32 sFilmOgerpon_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_ogerpon_mapofs.bin");
static const u32 sFilmOgerpon_Seq[] = INCBIN_U32("graphics/battle_transitions/film_ogerpon_seq.bin");
static const u16 sFilmOgerpon_Pal[] = INCBIN_U16("graphics/battle_transitions/film_ogerpon_pal.bin");
static const struct Film sFilm_Ogerpon = FILM(FilmOgerpon);

#define OGERPON_OUT   30
#define OGERPON_ZOOM  50
#define OGERPON_EYES  122
#define OGERPON_LEAP  164

static bool8 RTOgerpon_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    // lantaarns gaan uit (om de 4 frames een)
    if (t >= OGERPON_OUT && t < OGERPON_OUT + 24 && ((t - OGERPON_OUT) & 7) == 0)
        PlaySE(SE_M_MINIMIZE);
    if (t == OGERPON_ZOOM)
        PlaySE(SE_M_SWAGGER);
    if (t == OGERPON_EYES)
        PlaySE(SE_M_LEER);
    if (t == OGERPON_LEAP)
        PlaySE(SE_M_RAZOR_WIND);
    if (t == OGERPON_LEAP + 16)
        PlaySE(SE_M_GIGA_DRAIN);
    return Film_Update(task, &sFilm_Ogerpon);
}

static const struct RouteTransition sRT_Ogerpon =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmOgerpon_Pal, 1, 1, 0, Film_Init, RTOgerpon_Update, Film_Finish
};

static void Task_Ogerpon(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Ogerpon);
}

// ---------------- Archie + Maxie (werkstraf, Weather Institute): het prikbord van de pauzeruimte. Een druppel koffie
// op het rooster; de vlek wordt Groudon, dan Kyogre. Het rooster scheurt: links brand, rechts doorweekt. Eronder:
// "VOLUNTEER OF THE MONTH" met allebei erop, "(DISPUTED)". Zie service_transition.py.
static const u32 sFilmService_Tiles[] = INCBIN_U32("graphics/battle_transitions/film_service_tiles.bin");
static const u32 sFilmService_Loads[] = INCBIN_U32("graphics/battle_transitions/film_service_loads.bin");
static const u32 sFilmService_Runs[] = INCBIN_U32("graphics/battle_transitions/film_service_runs.bin");
static const u32 sFilmService_Maps[] = INCBIN_U32("graphics/battle_transitions/film_service_maps.bin");
static const u32 sFilmService_MapOfs[] = INCBIN_U32("graphics/battle_transitions/film_service_mapofs.bin");
static const u32 sFilmService_Seq[] = INCBIN_U32("graphics/battle_transitions/film_service_seq.bin");
static const u16 sFilmService_Pal[] = INCBIN_U16("graphics/battle_transitions/film_service_pal.bin");
static const struct Film sFilm_Service = FILM(FilmService);

#define SERVICE_SPLAT 38
#define SERVICE_MORPH 84
#define SERVICE_TEAR  124
#define SERVICE_SPLIT 140

static bool8 RTWeatherService_Update(struct Task *task)
{
    s32 t = task->tRtTimer;

    if (t == SERVICE_SPLAT)
        PlaySE(SE_M_BUBBLE3);
    if (t == SERVICE_MORPH)
        PlaySE(SE_M_BUBBLE);
    if (t == SERVICE_TEAR)
        PlaySE(SE_M_CUT);
    if (t == SERVICE_SPLIT)
        PlaySE(SE_M_FLAME_WHEEL);
    if (t == SERVICE_SPLIT + 14)
        PlaySE(SE_M_WATERFALL);
    return Film_Update(task, &sFilm_Service);
}

static const struct RouteTransition sRT_WeatherService =
{
    sFilm_EmptyTile, sizeof(sFilm_EmptyTile), sFilmService_Pal, 1, 1, 0, Film_Init, RTWeatherService_Update, Film_Finish
};

static void Task_WeatherService(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_WeatherService);
}

// Project Grounded: gymleider-intro's (Roxanne, Brawly, Wattson, Flannery)
#include "data/gym_intros_a.h"

// ---------------- Tapu Koko/Lele/Bulu/Fini: lichte intro (geen film). Het gesloten schild verschijnt op een donkere
// achtergrond in de kleur van de Tapu, met een motief uit het schildpatroon dat via een paletcyclus beweegt
// (tools/grounded/tapu_transition.py). Het patroon licht op op de beat, bouwt op, en op de eerste grote drumslag
// (met de chant) van MUS_GROUNDED_VS_TAPU gaat het schild open: licht, flits, gevecht.
// Alles hangt aan TAPU_HIT_FRAME: het aantal VBlanks vanaf de start van de transitie (= start van de muziek, die
// CreateBattleStartTask een frame eerder start) tot die drumslag, dus HIT_SECONDS * 60 uit tools/grounded/tapu_theme.py.
// Er wordt op echte VBlanks geteld (gMain.vblankCounter1), zodat vertraagde frames de sync met de muziek niet breken.
#define TAPU_HIT_FRAME 333 // = HIT_SECONDS_GBA (5,542 s) * 60 (tapu_theme.py v3: chant, dan de eerste grote slag); de transitie eindigt precies hier
#define TAPU_BEAT      21  // 174 bpm = 20,7 frames per tel; beat-afstand voor het oplichten (geteld terug vanaf de drumslag)
#define TAPU_BUILD     48  // opbouw: snellere pulsen, trillen, alles lichter
#define TAPU_OPEN      10  // het schild gaat open in de laatste TAPU_OPEN frames
#define TAPU_LATENCY   2   // gemeten: muziekstart -> transitiestart 1 frame, transitie-einde -> CB2_InitBattle 1 frame

enum { TAPU_KOKO, TAPU_LELE, TAPU_BULU, TAPU_FINI };

struct TapuIntro
{
    const u32 *tiles;
    const u32 *map;
    const u16 *shell; // [0] = lichttile, daarna w x h
    const u16 *pal;
    u8 w, h, cycleSpeed;
    u16 dark, motif, glow;
};

static const u32 sTapuKoko_Tiles[] = INCBIN_U32("graphics/battle_transitions/tapu_koko.4bpp.smol");
static const u32 sTapuKoko_Map[] = INCBIN_U32("graphics/battle_transitions/tapu_koko.bin.smolTM");
static const u16 sTapuKoko_Shell[] = INCBIN_U16("graphics/battle_transitions/tapu_koko_shell.bin");
static const u16 sTapuKoko_Pal[] = INCBIN_U16("graphics/battle_transitions/tapu_koko.gbapal");
static const u32 sTapuLele_Tiles[] = INCBIN_U32("graphics/battle_transitions/tapu_lele.4bpp.smol");
static const u32 sTapuLele_Map[] = INCBIN_U32("graphics/battle_transitions/tapu_lele.bin.smolTM");
static const u16 sTapuLele_Shell[] = INCBIN_U16("graphics/battle_transitions/tapu_lele_shell.bin");
static const u16 sTapuLele_Pal[] = INCBIN_U16("graphics/battle_transitions/tapu_lele.gbapal");
static const u32 sTapuBulu_Tiles[] = INCBIN_U32("graphics/battle_transitions/tapu_bulu.4bpp.smol");
static const u32 sTapuBulu_Map[] = INCBIN_U32("graphics/battle_transitions/tapu_bulu.bin.smolTM");
static const u16 sTapuBulu_Shell[] = INCBIN_U16("graphics/battle_transitions/tapu_bulu_shell.bin");
static const u16 sTapuBulu_Pal[] = INCBIN_U16("graphics/battle_transitions/tapu_bulu.gbapal");
static const u32 sTapuFini_Tiles[] = INCBIN_U32("graphics/battle_transitions/tapu_fini.4bpp.smol");
static const u32 sTapuFini_Map[] = INCBIN_U32("graphics/battle_transitions/tapu_fini.bin.smolTM");
static const u16 sTapuFini_Shell[] = INCBIN_U16("graphics/battle_transitions/tapu_fini_shell.bin");
static const u16 sTapuFini_Pal[] = INCBIN_U16("graphics/battle_transitions/tapu_fini.gbapal");

static const struct TapuIntro sTapuIntros[] =
{
    [TAPU_KOKO] = {sTapuKoko_Tiles, sTapuKoko_Map, sTapuKoko_Shell, sTapuKoko_Pal, 12, 18, 2,
                   RGB(3, 3, 0), RGB(31, 27, 4), RGB(31, 31, 18)},
    [TAPU_LELE] = {sTapuLele_Tiles, sTapuLele_Map, sTapuLele_Shell, sTapuLele_Pal, 12, 18, 4,
                   RGB(5, 1, 4), RGB(31, 12, 22), RGB(31, 26, 31)},
    [TAPU_BULU] = {sTapuBulu_Tiles, sTapuBulu_Map, sTapuBulu_Shell, sTapuBulu_Pal, 18, 16, 5,
                   RGB(1, 4, 1), RGB(18, 28, 4), RGB(31, 31, 16)},
    [TAPU_FINI] = {sTapuFini_Tiles, sTapuFini_Map, sTapuFini_Shell, sTapuFini_Pal, 14, 17, 4,
                   RGB(1, 2, 7), RGB(16, 19, 31), RGB(24, 31, 31)},
};

// helderheid van de 8 fasen van het motief (fase 0 = de lichtgolf, daarachter een staart)
static const u8 sTapuCycle[8] = {16, 4, 3, 3, 3, 4, 6, 10};
// schild open: verschuiving per helft in tiles, en de flits naar wit
static const u8 sTapuOpenStep[TAPU_OPEN] = {0, 0, 1, 1, 2, 3, 4, 6, 9, 13};
static const u8 sTapuOpenFlash[TAPU_OPEN] = {2, 4, 5, 6, 8, 9, 11, 13, 15, 16};

#define tTapuState  data[0]
#define tTapuTimer  data[1]
#define tTapuPulse  data[2]
#define tTapuId     data[3]
#define tTapuHidden data[4]
#define tTapuPos    data[5] // verticale positie (Bulu valt, Fini stijgt) in 1/16 px
#define tTapuVel    data[6]
#define tTapuSin    data[7]
#define tTapuLast   data[8] // laatst geziene 'r' (frames tot de drumslag), voor beats bij vertraagde frames
#define tTapuLanded data[9]

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

static void VBlankCB_Tapu(void)
{
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sTransitionData->VBlank_DMA)
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    DmaSet(0, gScanlineEffectRegBuffers[1], &REG_BG0HOFS, B_TRANS_DMA_FLAGS);
}

// schild tekenen met de helften 'step' tiles uit elkaar, de spleet vol licht (over het hele scherm)
static void Tapu_DrawOpen(const struct TapuIntro *ti, s32 step)
{
    u16 *tilemap = RT_Tilemap();
    s32 x0 = 15 - ti->w / 2, y0 = (20 - ti->h) / 2, half = ti->w / 2;
    s32 r, c;
    u16 light = ti->shell[0];

    for (r = 0; r < 20; r++)
    {
        s32 sr = r - y0;
        for (c = 15 - step; c < 15 + step; c++)
            if (c >= 0 && c < 30)
                tilemap[r * 32 + c] = light;
        if (sr < 0 || sr >= ti->h)
            continue;
        for (c = 0; c < half; c++)
        {
            s32 xl = x0 + c - step, xr = 15 + c + step;
            u16 el = ti->shell[1 + sr * ti->w + c], er = ti->shell[1 + sr * ti->w + half + c];
            if (xl >= 0 && el)
                tilemap[r * 32 + xl] = el;
            if (xr < 30 && er)
                tilemap[r * 32 + xr] = er;
        }
    }
}

static void Tapu_Finish(u8 taskId)
{
    SetVBlankCallback(NULL);
    DmaStop(0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG1_ON | DISPCNT_BG2_ON | DISPCNT_BG3_ON | DISPCNT_OBJ_ON);
    FadeScreenBlack();
    DestroyTask(taskId);
}

static void Tapu_Update(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    const struct TapuIntro *ti = &sTapuIntros[task->tTapuId];
    s32 t = task->tTapuTimer, r = TAPU_HIT_FRAME - TAPU_LATENCY - Tapu_Elapsed();
    s32 i, level, bgLevel, glow, flash = 0, shake = 0, wave = 0, cyc;
    u16 *tilemap, *tileset;
    u16 *pal14 = &gPlttBufferFaded[BG_PLTT_ID(14)], *pal15 = &gPlttBufferFaded[BG_PLTT_ID(15)];
    s16 *hofs = (s16 *)gScanlineEffectRegBuffers[0];

    if (task->tTapuState == 0)
    {
        InitTransitionData();
        ScanlineEffect_Clear();
        GetBg0TilesDst(&tilemap, &tileset);
        CpuFill16(0, tilemap, BG_SCREEN_SIZE);
        DecompressDataWithHeaderVram(ti->tiles, tileset);
        for (i = 0; i < 16; i++)
            pal14[i] = pal15[i] = ti->dark;
        CpuCopy16(pal14, &gPlttBufferUnfaded[BG_PLTT_ID(14)], PLTT_SIZE_4BPP * 2);
        for (i = 0; i < DISPLAY_HEIGHT; i++)
            gScanlineEffectRegBuffers[0][i] = gScanlineEffectRegBuffers[1][i] = 0;
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        // de wereld (BG 0-13 en alle sprites) zakt weg in de donkere kleur van de Tapu
        BeginNormalPaletteFade(PALETTES_ALL & ~((1 << 14) | (1 << 15)), 0, 0, 16, ti->dark);
        task->tTapuPos = (task->tTapuId == TAPU_BULU) ? (96 << 4) : (task->tTapuId == TAPU_FINI) ? -(96 << 4) : 0;
        task->tTapuVel = 0;
        task->tTapuLast = r;
        SetVBlankCallback(VBlankCB_Tapu);
        task->tTapuState++;
        return;
    }

    if (r <= 0)
    {
        Tapu_Finish(taskId);
        return;
    }

    // eerst zakt de wereld weg; pas dan het beeld tekenen en de tijdlijn starten. Daarna blijven alleen BG0 en de
    // achtergrondkleur over (dan kan de flits via de achtergrondkleur)
    if (!task->tTapuHidden)
    {
        if (gPaletteFade.active)
            return;
        ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG1_ON | DISPCNT_BG2_ON | DISPCNT_BG3_ON | DISPCNT_OBJ_ON);
        DecompressDataWithHeaderVram(ti->map, RT_Tilemap());
        task->tTapuHidden = TRUE;
    }

    // verschijnen (frames 8-56): elke Tapu op zijn eigen manier
    level = (t - 8) * 16 / 40;
    level = max(0, min(level, 16));
    bgLevel = max(0, min((t - 40) * 16 / 30, 16));
    switch (task->tTapuId)
    {
    case TAPU_KOKO: // elektrisch: het silhouet flitst aan, scanlijnen springen
        if (t >= 8 && t < 56 && (Random() & 3) == 0)
            level = 16;
        if (t < 56)
            wave = (56 - t) / 4;
        break;
    case TAPU_LELE: // psychisch: weefgolf zoals de Regi's, die uitdooft
        wave = max(0, 40 - t) / 2;
        break;
    case TAPU_BULU: // zwaar: valt van boven, dreun, nadreunen
        if (t >= 8 && !task->tTapuLanded)
        {
            task->tTapuVel += 20;
            task->tTapuPos -= task->tTapuVel;
            if (task->tTapuPos <= 0)
            {
                task->tTapuPos = 3 << 4; // terugvering, zakt hieronder weer weg
                task->tTapuLanded = TRUE;
                task->tTapuPulse = 16;
            }
        }
        break;
    case TAPU_FINI: // water: stijgt op uit de diepte, golvend
        if (t >= 8 && task->tTapuPos < 0)
            task->tTapuPos = -(((96 << 4) * (56 - t) / 48) * (56 - t) / 48);
        if (t >= 56)
            task->tTapuPos = 0;
        wave = 2 + max(0, 56 - t) / 6;
        break;
    }

    // beats: teruggeteld vanaf de drumslag; in de opbouw steeds sneller
    if (t > 56)
    {
        s32 beat = r > TAPU_BUILD ? TAPU_BEAT : r > TAPU_BUILD / 2 ? 12 : 6;
        for (i = task->tTapuLast - 1; i >= r; i--)
        {
            if (i > TAPU_OPEN && (i % beat) == 0)
            {
                task->tTapuPulse = 16;
                if (task->tTapuId == TAPU_BULU && r > TAPU_BUILD)
                    task->tTapuPos = 2 << 4; // dreun
                break;
            }
        }
    }
    task->tTapuLast = r;

    glow = task->tTapuPulse;
    if (r < TAPU_BUILD)
    {
        s32 b = (TAPU_BUILD - r) * 10 / TAPU_BUILD;
        glow = max(glow, b);
        shake = (TAPU_BUILD - r) / 12;
    }
    if (r <= TAPU_OPEN)
    {
        Tapu_DrawOpen(ti, sTapuOpenStep[TAPU_OPEN - r]);
        flash = sTapuOpenFlash[TAPU_OPEN - r];
        shake = 0;
    }

    // palet 15: het schild (vanuit donker), het patroon (11-13) licht op, alles naar wit bij de flits
    for (i = 1; i < 16; i++)
    {
        u16 c = Tapu_Blend(ti->dark, ti->pal[i], level);
        if (i >= 11 && i <= 13)
            c = Tapu_Blend(c, ti->glow, glow);
        else if (i == 15)
            c = ti->glow;
        else
            c = Tapu_Blend(c, RGB_WHITE, glow / 5);
        pal15[i] = Tapu_Blend(c, RGB_WHITE, flash);
    }
    // palet 14: het motief, een lichtgolf die rondloopt; op de beat licht alles op
    cyc = t / ti->cycleSpeed;
    for (i = 1; i <= 8; i++)
    {
        s32 k = sTapuCycle[(i - 1 - cyc) & 7] + glow / 2;
        if (task->tTapuId == TAPU_KOKO && task->tTapuPulse >= 14)
            k = 16; // bliksemflits
        k = min(k, 16) * bgLevel / 16;
        pal14[i] = Tapu_Blend(Tapu_Blend(ti->dark, ti->motif, k), RGB_WHITE, flash);
    }
    gPlttBufferFaded[0] = Tapu_Blend(ti->dark, RGB_WHITE, flash); // achtergrondkleur
    if (task->tTapuPulse > 0)
        task->tTapuPulse -= 2;

    // per beeldlijn horizontaal (golf / sprongen) en verticaal (vallen, stijgen, trillen)
    sTransitionData->VBlank_DMA = FALSE;
    if (task->tTapuId == TAPU_KOKO)
    {
        for (i = 0; i < DISPLAY_HEIGHT; i += 4)
        {
            s32 o = wave ? (s32)(Random() % (2 * wave + 1)) - wave : 0;
            if (task->tTapuPulse >= 12 && (Random() & 1))
                o += (Random() & 3) - 1;
            hofs[i] = hofs[i + 1] = hofs[i + 2] = hofs[i + 3] = o;
        }
    }
    else
    {
        s32 amp = wave + (task->tTapuId == TAPU_LELE ? task->tTapuPulse / 5 : task->tTapuId == TAPU_FINI ? task->tTapuPulse / 6 : 0);
        task->tTapuSin += (task->tTapuId == TAPU_FINI) ? 3 : 8;
        SetSinWave(hofs, 0, task->tTapuSin, task->tTapuId == TAPU_FINI ? 3 : 6, amp, DISPLAY_HEIGHT);
    }
    if (shake)
    {
        s32 o = (t & 1) ? shake : -shake;
        for (i = 0; i < DISPLAY_HEIGHT; i++)
            hofs[i] += o;
    }
    sTransitionData->VBlank_DMA = TRUE;

    {
        s32 vofs = task->tTapuPos >> 4;
        if (task->tTapuId == TAPU_BULU && task->tTapuLanded && task->tTapuPos > 0)
            task->tTapuPos = max(0, task->tTapuPos - 6);
        SetGpuReg(REG_OFFSET_BG0VOFS, vofs & 0x1FF);
    }
    task->tTapuTimer++;
}

// de taakfunctie blijft per Tapu dezelfde (Transition_WaitForMain zoekt erop)
static void Tapu_Run(u8 taskId, s16 which)
{
    gTasks[taskId].tTapuId = which;
    Tapu_Update(taskId);
}

static void Task_TapuKoko(u8 taskId) { Tapu_Run(taskId, TAPU_KOKO); }
static void Task_TapuLele(u8 taskId) { Tapu_Run(taskId, TAPU_LELE); }
static void Task_TapuBulu(u8 taskId) { Tapu_Run(taskId, TAPU_BULU); }
static void Task_TapuFini(u8 taskId) { Tapu_Run(taskId, TAPU_FINI); }

#undef tTapuState
#undef tTapuTimer
#undef tTapuPulse
#undef tTapuId
#undef tTapuHidden
#undef tTapuPos
#undef tTapuVel
#undef tTapuSin
#undef tTapuLast
#undef tTapuLanded
// Project Grounded: gymleider-intro's deel B (Norman, Winona, Tate & Liza, Wallace)
#include "data/gym_intros_b.h"
// Project Grounded: legendary-intro's (Lugia, Ho-Oh, Volcanion, Hoopa, Forces of Nature)
#include "data/legend_intros.h"
#include "data/legend_intros2.h"
#include "data/wario_intro.h"
#include "data/boo_intro.h"
#include "data/shyguy_intro.h"
#include "data/legend_intros_dp.h"
// Project Grounded: goedkope legendary-intro's (Calyrex, Celebi, meren-trio, Meloetta, ...)
#include "data/legend_intros_cheap2.h"
#include "data/legend_intros_cheap1.h" // Project Grounded: goedkope legendary-intro's (Swords, UB's, paradoxen, Eternatus, Marshadow, Terapagos, Pecharunt)
// Project Grounded: trainerklasse-intro's (met de gedeelde runner) en de rivaal-intro's
#include "data/class_intros.h"
#include "data/rival_intros.h"
