#include "global.h"
#include "graphics.h"
#include "palette.h"
#include "util.h"
#include "battle_transition.h"
#include "task.h"
#include "battle_transition.h"
#include "fieldmap.h"

static EWRAM_DATA struct {
    const u16 *src;
    u16 *dest;
    u16 size;
} sTilesetDMA3TransferBuffer[20] = {0};

static u8 sTilesetDMA3TransferBufferSize;
static u16 sPrimaryTilesetAnimCounter;
static u16 sPrimaryTilesetAnimCounterMax;
static u16 sSecondaryTilesetAnimCounter;
static u16 sSecondaryTilesetAnimCounterMax;
static void (*sPrimaryTilesetAnimCallback)(u16);
static void (*sSecondaryTilesetAnimCallback)(u16);

static void _InitPrimaryTilesetAnimation(void);
static void _InitSecondaryTilesetAnimation(void);
static void TilesetAnim_General(u16);
static void TilesetAnim_Building(u16);
static void TilesetAnim_Rustboro(u16);
static void TilesetAnim_Dewford(u16);
static void TilesetAnim_Slateport(u16);
static void TilesetAnim_Mauville(u16);
static void TilesetAnim_Lavaridge(u16);
static void TilesetAnim_EverGrande(u16);
static void TilesetAnim_Pacifidlog(u16);
static void TilesetAnim_Sootopolis(u16);
static void TilesetAnim_BattleFrontierOutsideWest(u16);
static void TilesetAnim_BattleFrontierOutsideEast(u16);
static void TilesetAnim_Underwater(u16);
static void TilesetAnim_SootopolisGym(u16);
static void TilesetAnim_Cave(u16);
static void TilesetAnim_EliteFour(u16);
static void TilesetAnim_MauvilleGym(u16);
static void TilesetAnim_BikeShop(u16);
static void TilesetAnim_BattlePyramid(u16);
static void TilesetAnim_BattleDome(u16);
static void QueueAnimTiles_General_Flower(u16);
static void QueueAnimTiles_General_Water(u16);
static void QueueAnimTiles_General_SandWaterEdge(u16);
static void QueueAnimTiles_General_Waterfall(u16);
static void QueueAnimTiles_General_LandWaterEdge(u16);
static void QueueAnimTiles_Building_TVTurnedOn(u16);
static void QueueAnimTiles_Rustboro_WindyWater(u16, u8);
static void QueueAnimTiles_Rustboro_Fountain(u16);
static void QueueAnimTiles_Dewford_Flag(u16);
static void QueueAnimTiles_Slateport_Balloons(u16);
static void QueueAnimTiles_Mauville_Flowers(u16, u8);
static void QueueAnimTiles_BikeShop_BlinkingLights(u16);
static void QueueAnimTiles_BattlePyramid_Torch(u16);
static void QueueAnimTiles_BattlePyramid_StatueShadow(u16);
static void BlendAnimPalette_BattleDome_FloorLights(u16);
static void BlendAnimPalette_BattleDome_FloorLightsNoBlend(u16);
static void QueueAnimTiles_Lavaridge_Steam(u8);
static void QueueAnimTiles_Lavaridge_Lava(u16);
static void QueueAnimTiles_EverGrande_Flowers(u16, u8);
static void QueueAnimTiles_Pacifidlog_LogBridges(u8);
static void QueueAnimTiles_Pacifidlog_WaterCurrents(u8);
static void QueueAnimTiles_Sootopolis_StormyWater(u16);
static void QueueAnimTiles_Underwater_Seaweed(u8);
static void QueueAnimTiles_Cave_Lava(u16);
static void QueueAnimTiles_BattleFrontierOutsideWest_Flag(u16);
static void QueueAnimTiles_BattleFrontierOutsideEast_Flag(u16);
static void QueueAnimTiles_MauvilleGym_ElectricGates(u16);
static void QueueAnimTiles_SootopolisGym_Waterfalls(u16);
static void QueueAnimTiles_EliteFour_GroundLights(u16);
static void QueueAnimTiles_EliteFour_WallLights(u16);

const u16 gTilesetAnims_General_Flower_Frame1[] = INCBIN_U16("data/tilesets/primary/general/anim/flower/1.4bpp");
const u16 gTilesetAnims_General_Flower_Frame0[] = INCBIN_U16("data/tilesets/primary/general/anim/flower/0.4bpp");
const u16 gTilesetAnims_General_Flower_Frame2[] = INCBIN_U16("data/tilesets/primary/general/anim/flower/2.4bpp");

const u16 *const gTilesetAnims_General_Flower[] = {
    gTilesetAnims_General_Flower_Frame0,
    gTilesetAnims_General_Flower_Frame1,
    gTilesetAnims_General_Flower_Frame0,
    gTilesetAnims_General_Flower_Frame2
};

const u16 gTilesetAnims_General_Water_Frame0[] = INCBIN_U16("data/tilesets/primary/general/anim/water/0.4bpp");
const u16 gTilesetAnims_General_Water_Frame1[] = INCBIN_U16("data/tilesets/primary/general/anim/water/1.4bpp");
const u16 gTilesetAnims_General_Water_Frame2[] = INCBIN_U16("data/tilesets/primary/general/anim/water/2.4bpp");
const u16 gTilesetAnims_General_Water_Frame3[] = INCBIN_U16("data/tilesets/primary/general/anim/water/3.4bpp");
const u16 gTilesetAnims_General_Water_Frame4[] = INCBIN_U16("data/tilesets/primary/general/anim/water/4.4bpp");
const u16 gTilesetAnims_General_Water_Frame5[] = INCBIN_U16("data/tilesets/primary/general/anim/water/5.4bpp");
const u16 gTilesetAnims_General_Water_Frame6[] = INCBIN_U16("data/tilesets/primary/general/anim/water/6.4bpp");
const u16 gTilesetAnims_General_Water_Frame7[] = INCBIN_U16("data/tilesets/primary/general/anim/water/7.4bpp");

const u16 *const gTilesetAnims_General_Water[] = {
    gTilesetAnims_General_Water_Frame0,
    gTilesetAnims_General_Water_Frame1,
    gTilesetAnims_General_Water_Frame2,
    gTilesetAnims_General_Water_Frame3,
    gTilesetAnims_General_Water_Frame4,
    gTilesetAnims_General_Water_Frame5,
    gTilesetAnims_General_Water_Frame6,
    gTilesetAnims_General_Water_Frame7
};

const u16 gTilesetAnims_General_SandWaterEdge_Frame0[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/0.4bpp");
const u16 gTilesetAnims_General_SandWaterEdge_Frame1[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/1.4bpp");
const u16 gTilesetAnims_General_SandWaterEdge_Frame2[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/2.4bpp");
const u16 gTilesetAnims_General_SandWaterEdge_Frame3[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/3.4bpp");
const u16 gTilesetAnims_General_SandWaterEdge_Frame4[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/4.4bpp");
const u16 gTilesetAnims_General_SandWaterEdge_Frame5[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/5.4bpp");
const u16 gTilesetAnims_General_SandWaterEdge_Frame6[] = INCBIN_U16("data/tilesets/primary/general/anim/sand_water_edge/6.4bpp");

const u16 *const gTilesetAnims_General_SandWaterEdge[] = {
    gTilesetAnims_General_SandWaterEdge_Frame0,
    gTilesetAnims_General_SandWaterEdge_Frame1,
    gTilesetAnims_General_SandWaterEdge_Frame2,
    gTilesetAnims_General_SandWaterEdge_Frame3,
    gTilesetAnims_General_SandWaterEdge_Frame4,
    gTilesetAnims_General_SandWaterEdge_Frame5,
    gTilesetAnims_General_SandWaterEdge_Frame6,
    gTilesetAnims_General_SandWaterEdge_Frame0
};

const u16 gTilesetAnims_General_Waterfall_Frame0[] = INCBIN_U16("data/tilesets/primary/general/anim/waterfall/0.4bpp");
const u16 gTilesetAnims_General_Waterfall_Frame1[] = INCBIN_U16("data/tilesets/primary/general/anim/waterfall/1.4bpp");
const u16 gTilesetAnims_General_Waterfall_Frame2[] = INCBIN_U16("data/tilesets/primary/general/anim/waterfall/2.4bpp");
const u16 gTilesetAnims_General_Waterfall_Frame3[] = INCBIN_U16("data/tilesets/primary/general/anim/waterfall/3.4bpp");

const u16 *const gTilesetAnims_General_Waterfall[] = {
    gTilesetAnims_General_Waterfall_Frame0,
    gTilesetAnims_General_Waterfall_Frame1,
    gTilesetAnims_General_Waterfall_Frame2,
    gTilesetAnims_General_Waterfall_Frame3
};

const u16 gTilesetAnims_General_LandWaterEdge_Frame0[] = INCBIN_U16("data/tilesets/primary/general/anim/land_water_edge/0.4bpp");
const u16 gTilesetAnims_General_LandWaterEdge_Frame1[] = INCBIN_U16("data/tilesets/primary/general/anim/land_water_edge/1.4bpp");
const u16 gTilesetAnims_General_LandWaterEdge_Frame2[] = INCBIN_U16("data/tilesets/primary/general/anim/land_water_edge/2.4bpp");
const u16 gTilesetAnims_General_LandWaterEdge_Frame3[] = INCBIN_U16("data/tilesets/primary/general/anim/land_water_edge/3.4bpp");

const u16 *const gTilesetAnims_General_LandWaterEdge[] = {
    gTilesetAnims_General_LandWaterEdge_Frame0,
    gTilesetAnims_General_LandWaterEdge_Frame1,
    gTilesetAnims_General_LandWaterEdge_Frame2,
    gTilesetAnims_General_LandWaterEdge_Frame3
};

const u16 gTilesetAnims_Lavaridge_Steam_Frame0[] = INCBIN_U16("data/tilesets/secondary/lavaridge/anim/steam/0.4bpp");
const u16 gTilesetAnims_Lavaridge_Steam_Frame1[] = INCBIN_U16("data/tilesets/secondary/lavaridge/anim/steam/1.4bpp");
const u16 gTilesetAnims_Lavaridge_Steam_Frame2[] = INCBIN_U16("data/tilesets/secondary/lavaridge/anim/steam/2.4bpp");
const u16 gTilesetAnims_Lavaridge_Steam_Frame3[] = INCBIN_U16("data/tilesets/secondary/lavaridge/anim/steam/3.4bpp");

const u16 *const gTilesetAnims_Lavaridge_Steam[] = {
    gTilesetAnims_Lavaridge_Steam_Frame0,
    gTilesetAnims_Lavaridge_Steam_Frame1,
    gTilesetAnims_Lavaridge_Steam_Frame2,
    gTilesetAnims_Lavaridge_Steam_Frame3
};

const u16 gTilesetAnims_Pacifidlog_LogBridges_Frame0[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/log_bridges/0.4bpp");
const u16 gTilesetAnims_Pacifidlog_LogBridges_Frame1[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/log_bridges/1.4bpp");
const u16 gTilesetAnims_Pacifidlog_LogBridges_Frame2[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/log_bridges/2.4bpp");

const u16 *const gTilesetAnims_Pacifidlog_LogBridges[] = {
    gTilesetAnims_Pacifidlog_LogBridges_Frame0,
    gTilesetAnims_Pacifidlog_LogBridges_Frame1,
    gTilesetAnims_Pacifidlog_LogBridges_Frame2,
    gTilesetAnims_Pacifidlog_LogBridges_Frame1
};

const u16 gTilesetAnims_Underwater_Seaweed_Frame0[] = INCBIN_U16("data/tilesets/secondary/underwater/anim/seaweed/0.4bpp");
const u16 gTilesetAnims_Underwater_Seaweed_Frame1[] = INCBIN_U16("data/tilesets/secondary/underwater/anim/seaweed/1.4bpp");
const u16 gTilesetAnims_Underwater_Seaweed_Frame2[] = INCBIN_U16("data/tilesets/secondary/underwater/anim/seaweed/2.4bpp");
const u16 gTilesetAnims_Underwater_Seaweed_Frame3[] = INCBIN_U16("data/tilesets/secondary/underwater/anim/seaweed/3.4bpp");

const u16 *const gTilesetAnims_Underwater_Seaweed[] = {
    gTilesetAnims_Underwater_Seaweed_Frame0,
    gTilesetAnims_Underwater_Seaweed_Frame1,
    gTilesetAnims_Underwater_Seaweed_Frame2,
    gTilesetAnims_Underwater_Seaweed_Frame3
};

const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame0[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/0.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame1[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/1.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame2[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/2.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame3[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/3.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame4[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/4.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame5[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/5.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame6[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/6.4bpp");
const u16 gTilesetAnims_Pacifidlog_WaterCurrents_Frame7[] = INCBIN_U16("data/tilesets/secondary/pacifidlog/anim/water_currents/7.4bpp");

const u16 *const gTilesetAnims_Pacifidlog_WaterCurrents[] = {
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame0,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame1,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame2,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame3,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame4,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame5,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame6,
    gTilesetAnims_Pacifidlog_WaterCurrents_Frame7
};

const u16 gTilesetAnims_Mauville_Flower1_Frame0[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_1/0.4bpp");
const u16 gTilesetAnims_Mauville_Flower1_Frame1[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_1/1.4bpp");
const u16 gTilesetAnims_Mauville_Flower1_Frame2[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_1/2.4bpp");
const u16 gTilesetAnims_Mauville_Flower1_Frame3[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_1/3.4bpp");
const u16 gTilesetAnims_Mauville_Flower1_Frame4[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_1/4.4bpp");
const u16 gTilesetAnims_Mauville_Flower2_Frame0[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_2/0.4bpp");
const u16 gTilesetAnims_Mauville_Flower2_Frame1[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_2/1.4bpp");
const u16 gTilesetAnims_Mauville_Flower2_Frame2[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_2/2.4bpp");
const u16 gTilesetAnims_Mauville_Flower2_Frame3[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_2/3.4bpp");
const u16 gTilesetAnims_Mauville_Flower2_Frame4[] = INCBIN_U16("data/tilesets/secondary/mauville/anim/flower_2/4.4bpp");

u16 *const gTilesetAnims_Mauville_Flower1_VDests[] = {
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 96)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 100)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 104)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 108)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 112)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 116)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 120)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 124))
};

u16 *const gTilesetAnims_Mauville_Flower2_VDests[] = {
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 128)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 132)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 136)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 140)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 144)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 148)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 152)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 156))
};

const u16 *const gTilesetAnims_Mauville_Flower1[] = {
    gTilesetAnims_Mauville_Flower1_Frame0,
    gTilesetAnims_Mauville_Flower1_Frame0,
    gTilesetAnims_Mauville_Flower1_Frame1,
    gTilesetAnims_Mauville_Flower1_Frame2,
    gTilesetAnims_Mauville_Flower1_Frame3,
    gTilesetAnims_Mauville_Flower1_Frame3,
    gTilesetAnims_Mauville_Flower1_Frame3,
    gTilesetAnims_Mauville_Flower1_Frame3,
    gTilesetAnims_Mauville_Flower1_Frame3,
    gTilesetAnims_Mauville_Flower1_Frame3,
    gTilesetAnims_Mauville_Flower1_Frame2,
    gTilesetAnims_Mauville_Flower1_Frame1
};

const u16 *const gTilesetAnims_Mauville_Flower2[] = {
    gTilesetAnims_Mauville_Flower2_Frame0,
    gTilesetAnims_Mauville_Flower2_Frame0,
    gTilesetAnims_Mauville_Flower2_Frame1,
    gTilesetAnims_Mauville_Flower2_Frame2,
    gTilesetAnims_Mauville_Flower2_Frame3,
    gTilesetAnims_Mauville_Flower2_Frame3,
    gTilesetAnims_Mauville_Flower2_Frame3,
    gTilesetAnims_Mauville_Flower2_Frame3,
    gTilesetAnims_Mauville_Flower2_Frame3,
    gTilesetAnims_Mauville_Flower2_Frame3,
    gTilesetAnims_Mauville_Flower2_Frame2,
    gTilesetAnims_Mauville_Flower2_Frame1
};

const u16 *const gTilesetAnims_Mauville_Flower1_B[] = {
    gTilesetAnims_Mauville_Flower1_Frame0,
    gTilesetAnims_Mauville_Flower1_Frame0,
    gTilesetAnims_Mauville_Flower1_Frame4,
    gTilesetAnims_Mauville_Flower1_Frame4
};

const u16 *const gTilesetAnims_Mauville_Flower2_B[] = {
    gTilesetAnims_Mauville_Flower2_Frame0,
    gTilesetAnims_Mauville_Flower2_Frame0,
    gTilesetAnims_Mauville_Flower2_Frame4,
    gTilesetAnims_Mauville_Flower2_Frame4
};

const u16 gTilesetAnims_Rustboro_WindyWater_Frame0[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/0.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame1[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/1.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame2[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/2.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame3[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/3.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame4[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/4.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame5[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/5.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame6[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/6.4bpp");
const u16 gTilesetAnims_Rustboro_WindyWater_Frame7[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/windy_water/7.4bpp");

u16 *const gTilesetAnims_Rustboro_WindyWater_VDests[] = {
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 128)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 132)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 136)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 140)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 144)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 148)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 152)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 156))
};

const u16 *const gTilesetAnims_Rustboro_WindyWater[] = {
    gTilesetAnims_Rustboro_WindyWater_Frame0,
    gTilesetAnims_Rustboro_WindyWater_Frame1,
    gTilesetAnims_Rustboro_WindyWater_Frame2,
    gTilesetAnims_Rustboro_WindyWater_Frame3,
    gTilesetAnims_Rustboro_WindyWater_Frame4,
    gTilesetAnims_Rustboro_WindyWater_Frame5,
    gTilesetAnims_Rustboro_WindyWater_Frame6,
    gTilesetAnims_Rustboro_WindyWater_Frame7
};

const u16 gTilesetAnims_Rustboro_Fountain_Frame0[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/fountain/0.4bpp");
const u16 gTilesetAnims_Rustboro_Fountain_Frame1[] = INCBIN_U16("data/tilesets/secondary/rustboro/anim/fountain/1.4bpp");

const u16 *const gTilesetAnims_Rustboro_Fountain[] = {
    gTilesetAnims_Rustboro_Fountain_Frame0,
    gTilesetAnims_Rustboro_Fountain_Frame1
};

const u16 gTilesetAnims_Lavaridge_Cave_Lava_Frame0[] = INCBIN_U16("data/tilesets/secondary/cave/anim/lava/0.4bpp");
const u16 gTilesetAnims_Lavaridge_Cave_Lava_Frame1[] = INCBIN_U16("data/tilesets/secondary/cave/anim/lava/1.4bpp");
const u16 gTilesetAnims_Lavaridge_Cave_Lava_Frame2[] = INCBIN_U16("data/tilesets/secondary/cave/anim/lava/2.4bpp");
const u16 gTilesetAnims_Lavaridge_Cave_Lava_Frame3[] = INCBIN_U16("data/tilesets/secondary/cave/anim/lava/3.4bpp");

const u16 *const gTilesetAnims_Lavaridge_Cave_Lava[] = {
    gTilesetAnims_Lavaridge_Cave_Lava_Frame0,
    gTilesetAnims_Lavaridge_Cave_Lava_Frame1,
    gTilesetAnims_Lavaridge_Cave_Lava_Frame2,
    gTilesetAnims_Lavaridge_Cave_Lava_Frame3
};

const u16 gTilesetAnims_EverGrande_Flowers_Frame0[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/0.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame1[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/1.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame2[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/2.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame3[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/3.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame4[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/4.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame5[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/5.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame6[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/6.4bpp");
const u16 gTilesetAnims_EverGrande_Flowers_Frame7[] = INCBIN_U16("data/tilesets/secondary/ever_grande/anim/flowers/7.4bpp");

u16 *const gTilesetAnims_EverGrande_VDests[] = {
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 224)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 228)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 232)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 236)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 240)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 244)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 248)),
    (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 252))
};

const u16 *const gTilesetAnims_EverGrande_Flowers[] = {
    gTilesetAnims_EverGrande_Flowers_Frame0,
    gTilesetAnims_EverGrande_Flowers_Frame1,
    gTilesetAnims_EverGrande_Flowers_Frame2,
    gTilesetAnims_EverGrande_Flowers_Frame3,
    gTilesetAnims_EverGrande_Flowers_Frame4,
    gTilesetAnims_EverGrande_Flowers_Frame5,
    gTilesetAnims_EverGrande_Flowers_Frame6,
    gTilesetAnims_EverGrande_Flowers_Frame7
};

const u16 gTilesetAnims_Dewford_Flag_Frame0[] = INCBIN_U16("data/tilesets/secondary/dewford/anim/flag/0.4bpp");
const u16 gTilesetAnims_Dewford_Flag_Frame1[] = INCBIN_U16("data/tilesets/secondary/dewford/anim/flag/1.4bpp");
const u16 gTilesetAnims_Dewford_Flag_Frame2[] = INCBIN_U16("data/tilesets/secondary/dewford/anim/flag/2.4bpp");
const u16 gTilesetAnims_Dewford_Flag_Frame3[] = INCBIN_U16("data/tilesets/secondary/dewford/anim/flag/3.4bpp");

const u16 *const gTilesetAnims_Dewford_Flag[] = {
    gTilesetAnims_Dewford_Flag_Frame0,
    gTilesetAnims_Dewford_Flag_Frame1,
    gTilesetAnims_Dewford_Flag_Frame2,
    gTilesetAnims_Dewford_Flag_Frame3
};

const u16 gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame0[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_west/anim/flag/0.4bpp");
const u16 gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame1[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_west/anim/flag/1.4bpp");
const u16 gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame2[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_west/anim/flag/2.4bpp");
const u16 gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame3[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_west/anim/flag/3.4bpp");

const u16 *const gTilesetAnims_BattleFrontierOutsideWest_Flag[] = {
    gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame0,
    gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame1,
    gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame2,
    gTilesetAnims_BattleFrontierOutsideWest_Flag_Frame3
};

const u16 gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame0[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_east/anim/flag/0.4bpp");
const u16 gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame1[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_east/anim/flag/1.4bpp");
const u16 gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame2[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_east/anim/flag/2.4bpp");
const u16 gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame3[] = INCBIN_U16("data/tilesets/secondary/battle_frontier_outside_east/anim/flag/3.4bpp");

const u16 *const gTilesetAnims_BattleFrontierOutsideEast_Flag[] = {
    gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame0,
    gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame1,
    gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame2,
    gTilesetAnims_BattleFrontierOutsideEast_Flag_Frame3
};

const u16 gTilesetAnims_Slateport_Balloons_Frame0[] = INCBIN_U16("data/tilesets/secondary/slateport/anim/balloons/0.4bpp");
const u16 gTilesetAnims_Slateport_Balloons_Frame1[] = INCBIN_U16("data/tilesets/secondary/slateport/anim/balloons/1.4bpp");
const u16 gTilesetAnims_Slateport_Balloons_Frame2[] = INCBIN_U16("data/tilesets/secondary/slateport/anim/balloons/2.4bpp");
const u16 gTilesetAnims_Slateport_Balloons_Frame3[] = INCBIN_U16("data/tilesets/secondary/slateport/anim/balloons/3.4bpp");

const u16 *const gTilesetAnims_Slateport_Balloons[] = {
    gTilesetAnims_Slateport_Balloons_Frame0,
    gTilesetAnims_Slateport_Balloons_Frame1,
    gTilesetAnims_Slateport_Balloons_Frame2,
    gTilesetAnims_Slateport_Balloons_Frame3
};

const u16 gTilesetAnims_Building_TvTurnedOn_Frame0[] = INCBIN_U16("data/tilesets/primary/building/anim/tv_turned_on/0.4bpp");
const u16 gTilesetAnims_Building_TvTurnedOn_Frame1[] = INCBIN_U16("data/tilesets/primary/building/anim/tv_turned_on/1.4bpp");

const u16 *const gTilesetAnims_Building_TvTurnedOn[] = {
    gTilesetAnims_Building_TvTurnedOn_Frame0,
    gTilesetAnims_Building_TvTurnedOn_Frame1
};

const u16 gTilesetAnims_SootopolisGym_SideWaterfall_Frame0[] = INCBIN_U16("data/tilesets/secondary/sootopolis_gym/anim/side_waterfall/0.4bpp");
const u16 gTilesetAnims_SootopolisGym_SideWaterfall_Frame1[] = INCBIN_U16("data/tilesets/secondary/sootopolis_gym/anim/side_waterfall/1.4bpp");
const u16 gTilesetAnims_SootopolisGym_SideWaterfall_Frame2[] = INCBIN_U16("data/tilesets/secondary/sootopolis_gym/anim/side_waterfall/2.4bpp");
const u16 gTilesetAnims_SootopolisGym_FrontWaterfall_Frame0[] = INCBIN_U16("data/tilesets/secondary/sootopolis_gym/anim/front_waterfall/0.4bpp");
const u16 gTilesetAnims_SootopolisGym_FrontWaterfall_Frame1[] = INCBIN_U16("data/tilesets/secondary/sootopolis_gym/anim/front_waterfall/1.4bpp");
const u16 gTilesetAnims_SootopolisGym_FrontWaterfall_Frame2[] = INCBIN_U16("data/tilesets/secondary/sootopolis_gym/anim/front_waterfall/2.4bpp");

const u16 *const gTilesetAnims_SootopolisGym_SideWaterfall[] = {
    gTilesetAnims_SootopolisGym_SideWaterfall_Frame0,
    gTilesetAnims_SootopolisGym_SideWaterfall_Frame1,
    gTilesetAnims_SootopolisGym_SideWaterfall_Frame2
};

const u16 *const gTilesetAnims_SootopolisGym_FrontWaterfall[] = {
    gTilesetAnims_SootopolisGym_FrontWaterfall_Frame0,
    gTilesetAnims_SootopolisGym_FrontWaterfall_Frame1,
    gTilesetAnims_SootopolisGym_FrontWaterfall_Frame2
};

const u16 gTilesetAnims_EliteFour_FloorLight_Frame0[] = INCBIN_U16("data/tilesets/secondary/elite_four/anim/floor_light/0.4bpp");
const u16 gTilesetAnims_EliteFour_FloorLight_Frame1[] = INCBIN_U16("data/tilesets/secondary/elite_four/anim/floor_light/1.4bpp");
const u16 gTilesetAnims_EliteFour_WallLights_Frame0[] = INCBIN_U16("data/tilesets/secondary/elite_four/anim/wall_lights/0.4bpp");
const u16 gTilesetAnims_EliteFour_WallLights_Frame1[] = INCBIN_U16("data/tilesets/secondary/elite_four/anim/wall_lights/1.4bpp");
const u16 gTilesetAnims_EliteFour_WallLights_Frame2[] = INCBIN_U16("data/tilesets/secondary/elite_four/anim/wall_lights/2.4bpp");
const u16 gTilesetAnims_EliteFour_WallLights_Frame3[] = INCBIN_U16("data/tilesets/secondary/elite_four/anim/wall_lights/3.4bpp");

const u16 *const gTilesetAnims_EliteFour_WallLights[] = {
    gTilesetAnims_EliteFour_WallLights_Frame0,
    gTilesetAnims_EliteFour_WallLights_Frame1,
    gTilesetAnims_EliteFour_WallLights_Frame2,
    gTilesetAnims_EliteFour_WallLights_Frame3
};

const u16 *const gTilesetAnims_EliteFour_FloorLight[] = {
    gTilesetAnims_EliteFour_FloorLight_Frame0,
    gTilesetAnims_EliteFour_FloorLight_Frame1
};

const u16 gTilesetAnims_MauvilleGym_ElectricGates_Frame0[] = INCBIN_U16("data/tilesets/secondary/mauville_gym/anim/electric_gates/0.4bpp");
const u16 gTilesetAnims_MauvilleGym_ElectricGates_Frame1[] = INCBIN_U16("data/tilesets/secondary/mauville_gym/anim/electric_gates/1.4bpp");

const u16 *const gTilesetAnims_MauvilleGym_ElectricGates[] = {
    gTilesetAnims_MauvilleGym_ElectricGates_Frame0,
    gTilesetAnims_MauvilleGym_ElectricGates_Frame1
};

const u16 gTilesetAnims_BikeShop_BlinkingLights_Frame0[] = INCBIN_U16("data/tilesets/secondary/bike_shop/anim/blinking_lights/0.4bpp");
const u16 gTilesetAnims_BikeShop_BlinkingLights_Frame1[] = INCBIN_U16("data/tilesets/secondary/bike_shop/anim/blinking_lights/1.4bpp");

const u16 *const gTilesetAnims_BikeShop_BlinkingLights[] = {
    gTilesetAnims_BikeShop_BlinkingLights_Frame0,
    gTilesetAnims_BikeShop_BlinkingLights_Frame1
};

const u16 gTilesetAnims_Sootopolis_StormyWater_Frame0[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/0_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/0_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame1[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/1_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/1_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame2[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/2_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/2_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame3[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/3_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/3_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame4[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/4_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/4_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame5[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/5_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/5_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame6[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/6_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/6_groudon.4bpp");
const u16 gTilesetAnims_Sootopolis_StormyWater_Frame7[] = INCBIN_U16("data/tilesets/secondary/sootopolis/anim/stormy_water/7_kyogre.4bpp", "data/tilesets/secondary/sootopolis/anim/stormy_water/7_groudon.4bpp");


// Project Grounded: draaikolken van het Keldeo-eiland (tools/grounded/maptools/swords_isle.py)
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame0[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/0.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame1[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/1.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame2[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/2.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame3[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/3.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame4[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/4.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame5[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/5.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame6[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/6.4bpp");
const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame7[] = INCBIN_U16("data/tilesets/secondary/uncharted_isle/anim/whirlpool/7.4bpp");
const u16 *const gTilesetAnims_UnchartedIsle_Whirlpool[] = {
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame0,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame1,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame2,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame3,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame4,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame5,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame6,
    gTilesetAnims_UnchartedIsle_Whirlpool_Frame7,
};

// Project Grounded: vuur in het brandende National Park (national_park_tiles.py)
const u16 gTilesetAnims_ParkBurnt_Fire_Frame0[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/0.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame1[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/1.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame2[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/2.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame3[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/3.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame4[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/4.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame5[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/5.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame6[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/6.4bpp");
const u16 gTilesetAnims_ParkBurnt_Fire_Frame7[] = INCBIN_U16("data/tilesets/secondary/park_burnt_rustboro/anim/fire/7.4bpp");
const u16 *const gTilesetAnims_ParkBurnt_Fire[] = {
    gTilesetAnims_ParkBurnt_Fire_Frame0,
    gTilesetAnims_ParkBurnt_Fire_Frame1,
    gTilesetAnims_ParkBurnt_Fire_Frame2,
    gTilesetAnims_ParkBurnt_Fire_Frame3,
    gTilesetAnims_ParkBurnt_Fire_Frame4,
    gTilesetAnims_ParkBurnt_Fire_Frame5,
    gTilesetAnims_ParkBurnt_Fire_Frame6,
    gTilesetAnims_ParkBurnt_Fire_Frame7,
};

const u16 *const gTilesetAnims_Sootopolis_StormyWater[] = {
    gTilesetAnims_Sootopolis_StormyWater_Frame0,
    gTilesetAnims_Sootopolis_StormyWater_Frame1,
    gTilesetAnims_Sootopolis_StormyWater_Frame2,
    gTilesetAnims_Sootopolis_StormyWater_Frame3,
    gTilesetAnims_Sootopolis_StormyWater_Frame4,
    gTilesetAnims_Sootopolis_StormyWater_Frame5,
    gTilesetAnims_Sootopolis_StormyWater_Frame6,
    gTilesetAnims_Sootopolis_StormyWater_Frame7
};

const u16 gTilesetAnims_BattlePyramid_Torch_Frame0[] = INCBIN_U16("data/tilesets/secondary/battle_pyramid/anim/torch/0.4bpp");
const u16 gTilesetAnims_BattlePyramid_Torch_Frame1[] = INCBIN_U16("data/tilesets/secondary/battle_pyramid/anim/torch/1.4bpp");
const u16 gTilesetAnims_BattlePyramid_Torch_Frame2[] = INCBIN_U16("data/tilesets/secondary/battle_pyramid/anim/torch/2.4bpp");

const u16 gTilesetAnims_BattlePyramid_StatueShadow_Frame0[] = INCBIN_U16("data/tilesets/secondary/battle_pyramid/anim/statue_shadow/0.4bpp");
const u16 gTilesetAnims_BattlePyramid_StatueShadow_Frame1[] = INCBIN_U16("data/tilesets/secondary/battle_pyramid/anim/statue_shadow/1.4bpp");
const u16 gTilesetAnims_BattlePyramid_StatueShadow_Frame2[] = INCBIN_U16("data/tilesets/secondary/battle_pyramid/anim/statue_shadow/2.4bpp");



const u16 *const gTilesetAnims_BattlePyramid_Torch[] = {
    gTilesetAnims_BattlePyramid_Torch_Frame0,
    gTilesetAnims_BattlePyramid_Torch_Frame1,
    gTilesetAnims_BattlePyramid_Torch_Frame2
};

const u16 *const gTilesetAnims_BattlePyramid_StatueShadow[] = {
    gTilesetAnims_BattlePyramid_StatueShadow_Frame0,
    gTilesetAnims_BattlePyramid_StatueShadow_Frame1,
    gTilesetAnims_BattlePyramid_StatueShadow_Frame2
};

static const u16 *const sTilesetAnims_BattleDomeFloorLightPals[] = {
    gTilesetAnims_BattleDomePals0_0,
    gTilesetAnims_BattleDomePals0_1,
    gTilesetAnims_BattleDomePals0_2,
    gTilesetAnims_BattleDomePals0_3,
};

static void ResetTilesetAnimBuffer(void)
{
    sTilesetDMA3TransferBufferSize = 0;
    CpuFill32(0, sTilesetDMA3TransferBuffer, sizeof sTilesetDMA3TransferBuffer);
}

static void AppendTilesetAnimToBuffer(const u16 *src, u16 *dest, u16 size)
{
    if (sTilesetDMA3TransferBufferSize < 20)
    {
        sTilesetDMA3TransferBuffer[sTilesetDMA3TransferBufferSize].src = src;
        sTilesetDMA3TransferBuffer[sTilesetDMA3TransferBufferSize].dest = dest;
        sTilesetDMA3TransferBuffer[sTilesetDMA3TransferBufferSize].size = size;
        sTilesetDMA3TransferBufferSize ++;
    }
}

void TransferTilesetAnimsBuffer(void)
{
    int i;

    for (i = 0; i < sTilesetDMA3TransferBufferSize; i ++)
        DmaCopy16(3, sTilesetDMA3TransferBuffer[i].src, sTilesetDMA3TransferBuffer[i].dest, sTilesetDMA3TransferBuffer[i].size);

    sTilesetDMA3TransferBufferSize = 0;
}

void InitTilesetAnimations(void)
{
    ResetTilesetAnimBuffer();
    _InitPrimaryTilesetAnimation();
    _InitSecondaryTilesetAnimation();
}

void InitSecondaryTilesetAnimation(void)
{
    _InitSecondaryTilesetAnimation();
}

void UpdateTilesetAnimations(void)
{
    ResetTilesetAnimBuffer();
    if (++sPrimaryTilesetAnimCounter >= sPrimaryTilesetAnimCounterMax)
        sPrimaryTilesetAnimCounter = 0;
    if (++sSecondaryTilesetAnimCounter >= sSecondaryTilesetAnimCounterMax)
        sSecondaryTilesetAnimCounter = 0;

    if (sPrimaryTilesetAnimCallback)
        sPrimaryTilesetAnimCallback(sPrimaryTilesetAnimCounter);
    if (sSecondaryTilesetAnimCallback)
        sSecondaryTilesetAnimCallback(sSecondaryTilesetAnimCounter);
}

static void _InitPrimaryTilesetAnimation(void)
{
    sPrimaryTilesetAnimCounter = 0;
    sPrimaryTilesetAnimCounterMax = 0;
    sPrimaryTilesetAnimCallback = NULL;
    if (gMapHeader.mapLayout->primaryTileset && gMapHeader.mapLayout->primaryTileset->callback)
        gMapHeader.mapLayout->primaryTileset->callback();
}

static void _InitSecondaryTilesetAnimation(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 0;
    sSecondaryTilesetAnimCallback = NULL;
    if (gMapHeader.mapLayout->secondaryTileset && gMapHeader.mapLayout->secondaryTileset->callback)
        gMapHeader.mapLayout->secondaryTileset->callback();
}

void InitTilesetAnim_General(void)
{
    sPrimaryTilesetAnimCounter = 0;
    sPrimaryTilesetAnimCounterMax = 256;
    sPrimaryTilesetAnimCallback = TilesetAnim_General;
}

void InitTilesetAnim_Building(void)
{
    sPrimaryTilesetAnimCounter = 0;
    sPrimaryTilesetAnimCounterMax = 256;
    sPrimaryTilesetAnimCallback = TilesetAnim_Building;
}

static void TilesetAnim_General(u16 timer)
{
    if (timer % 16 == 0)
        QueueAnimTiles_General_Flower(timer / 16);
    if (timer % 16 == 1)
        QueueAnimTiles_General_Water(timer / 16);
    if (timer % 16 == 2)
        QueueAnimTiles_General_SandWaterEdge(timer / 16);
    if (timer % 16 == 3)
        QueueAnimTiles_General_Waterfall(timer / 16);
    if (timer % 16 == 4)
        QueueAnimTiles_General_LandWaterEdge(timer / 16);
}

static void TilesetAnim_Building(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_Building_TVTurnedOn(timer / 8);
}

static void QueueAnimTiles_General_Flower(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_General_Flower);
    AppendTilesetAnimToBuffer(gTilesetAnims_General_Flower[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(508)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_General_Water(u16 timer)
{
    u8 i = timer % ARRAY_COUNT(gTilesetAnims_General_Water);
    AppendTilesetAnimToBuffer(gTilesetAnims_General_Water[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(432)), 30 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_General_SandWaterEdge(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_General_SandWaterEdge);
    AppendTilesetAnimToBuffer(gTilesetAnims_General_SandWaterEdge[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(464)), 10 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_General_Waterfall(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_General_Waterfall);
    AppendTilesetAnimToBuffer(gTilesetAnims_General_Waterfall[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(496)), 6 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_Petalburg(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = NULL;
}

void InitTilesetAnim_Rustboro(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Rustboro;
}

void InitTilesetAnim_Dewford(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Dewford;
}

void InitTilesetAnim_Slateport(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Slateport;
}

void InitTilesetAnim_Mauville(void)
{
    sSecondaryTilesetAnimCounter = sPrimaryTilesetAnimCounter;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Mauville;
}

void InitTilesetAnim_Lavaridge(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Lavaridge;
}

void InitTilesetAnim_Fallarbor(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = NULL;
}

void InitTilesetAnim_Fortree(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = NULL;
}

void InitTilesetAnim_Lilycove(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = NULL;
}

void InitTilesetAnim_Mossdeep(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = NULL;
}

void InitTilesetAnim_EverGrande(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_EverGrande;
}

void InitTilesetAnim_Pacifidlog(void)
{
    sSecondaryTilesetAnimCounter = sPrimaryTilesetAnimCounter;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Pacifidlog;
}

void InitTilesetAnim_Sootopolis(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Sootopolis;
}

void InitTilesetAnim_BattleFrontierOutsideWest(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_BattleFrontierOutsideWest;
}

void InitTilesetAnim_BattleFrontierOutsideEast(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_BattleFrontierOutsideEast;
}

void InitTilesetAnim_Underwater(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 128;
    sSecondaryTilesetAnimCallback = TilesetAnim_Underwater;
}

void InitTilesetAnim_SootopolisGym(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 240;
    sSecondaryTilesetAnimCallback = TilesetAnim_SootopolisGym;
}

void InitTilesetAnim_Cave(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_Cave;
}

void InitTilesetAnim_EliteFour(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 128;
    sSecondaryTilesetAnimCallback = TilesetAnim_EliteFour;
}

void InitTilesetAnim_MauvilleGym(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_MauvilleGym;
}

void InitTilesetAnim_BikeShop(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_BikeShop;
}

void InitTilesetAnim_BattlePyramid(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_BattlePyramid;
}

void InitTilesetAnim_BattleDome(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_BattleDome;
}

static void TilesetAnim_Rustboro(u16 timer)
{
    if (timer % 8 == 0)
    {
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 0);
        QueueAnimTiles_Rustboro_Fountain(timer / 8);
    }
    if (timer % 8 == 1)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 1);
    if (timer % 8 == 2)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 2);
    if (timer % 8 == 3)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 3);
    if (timer % 8 == 4)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 4);
    if (timer % 8 == 5)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 5);
    if (timer % 8 == 6)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 6);
    if (timer % 8 == 7)
        QueueAnimTiles_Rustboro_WindyWater(timer / 8, 7);
}

static void TilesetAnim_Dewford(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_Dewford_Flag(timer / 8);
}

static void TilesetAnim_Slateport(u16 timer)
{
    if (timer % 16 == 0)
        QueueAnimTiles_Slateport_Balloons(timer / 16);
}

static void TilesetAnim_Mauville(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 0);
    if (timer % 8 == 1)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 1);
    if (timer % 8 == 2)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 2);
    if (timer % 8 == 3)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 3);
    if (timer % 8 == 4)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 4);
    if (timer % 8 == 5)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 5);
    if (timer % 8 == 6)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 6);
    if (timer % 8 == 7)
        QueueAnimTiles_Mauville_Flowers(timer / 8, 7);
}

static void TilesetAnim_Lavaridge(u16 timer)
{
    if (timer % 16 == 0)
        QueueAnimTiles_Lavaridge_Steam(timer / 16);
    if (timer % 16 == 1)
        QueueAnimTiles_Lavaridge_Lava(timer / 16);
}

static void TilesetAnim_EverGrande(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 0);
    if (timer % 8 == 1)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 1);
    if (timer % 8 == 2)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 2);
    if (timer % 8 == 3)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 3);
    if (timer % 8 == 4)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 4);
    if (timer % 8 == 5)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 5);
    if (timer % 8 == 6)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 6);
    if (timer % 8 == 7)
        QueueAnimTiles_EverGrande_Flowers(timer / 8, 7);
}

static void TilesetAnim_Pacifidlog(u16 timer)
{
    if (timer % 16 == 0)
        QueueAnimTiles_Pacifidlog_LogBridges(timer / 16);
    if (timer % 16 == 1)
        QueueAnimTiles_Pacifidlog_WaterCurrents(timer / 16);
}

static void TilesetAnim_Sootopolis(u16 timer)
{
    if (timer % 16 == 0)
        QueueAnimTiles_Sootopolis_StormyWater(timer / 16);
}

static void TilesetAnim_Underwater(u16 timer)
{
    if (timer % 16 == 0)
        QueueAnimTiles_Underwater_Seaweed(timer / 16);
}

static void TilesetAnim_Cave(u16 timer)
{
    if (timer % 16 == 1)
        QueueAnimTiles_Cave_Lava(timer / 16);
}

static void TilesetAnim_BattleFrontierOutsideWest(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_BattleFrontierOutsideWest_Flag(timer / 8);
}

static void TilesetAnim_BattleFrontierOutsideEast(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_BattleFrontierOutsideEast_Flag(timer / 8);
}

static void QueueAnimTiles_General_LandWaterEdge(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_General_LandWaterEdge);
    AppendTilesetAnimToBuffer(gTilesetAnims_General_LandWaterEdge[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(480)), 10 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Lavaridge_Steam(u8 timer)
{
    u8 i = timer % ARRAY_COUNT(gTilesetAnims_Lavaridge_Steam);
    AppendTilesetAnimToBuffer(gTilesetAnims_Lavaridge_Steam[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 288)), 4 * TILE_SIZE_4BPP);

    i = (timer + 2) % (int)ARRAY_COUNT(gTilesetAnims_Lavaridge_Steam);
    AppendTilesetAnimToBuffer(gTilesetAnims_Lavaridge_Steam[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 292)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Pacifidlog_LogBridges(u8 timer)
{
    u8 i = timer % ARRAY_COUNT(gTilesetAnims_Pacifidlog_LogBridges);
    AppendTilesetAnimToBuffer(gTilesetAnims_Pacifidlog_LogBridges[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 464)), 30 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Underwater_Seaweed(u8 timer)
{
    u8 i = timer % ARRAY_COUNT(gTilesetAnims_Underwater_Seaweed);
    AppendTilesetAnimToBuffer(gTilesetAnims_Underwater_Seaweed[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 496)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Pacifidlog_WaterCurrents(u8 timer)
{
    u8 i = timer % ARRAY_COUNT(gTilesetAnims_Pacifidlog_WaterCurrents);
    AppendTilesetAnimToBuffer(gTilesetAnims_Pacifidlog_WaterCurrents[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 496)), 8 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Mauville_Flowers(u16 timer_div, u8 timer_mod)
{
    timer_div -= timer_mod;
    if (timer_div < min(ARRAY_COUNT(gTilesetAnims_Mauville_Flower1), ARRAY_COUNT(gTilesetAnims_Mauville_Flower2)))
    {
        timer_div %= min(ARRAY_COUNT(gTilesetAnims_Mauville_Flower1), ARRAY_COUNT(gTilesetAnims_Mauville_Flower2));
        AppendTilesetAnimToBuffer(gTilesetAnims_Mauville_Flower1[timer_div], gTilesetAnims_Mauville_Flower1_VDests[timer_mod], 4 * TILE_SIZE_4BPP);
        AppendTilesetAnimToBuffer(gTilesetAnims_Mauville_Flower2[timer_div], gTilesetAnims_Mauville_Flower2_VDests[timer_mod], 4 * TILE_SIZE_4BPP);
    }
    else
    {
        timer_div %= min(ARRAY_COUNT(gTilesetAnims_Mauville_Flower1_B), ARRAY_COUNT(gTilesetAnims_Mauville_Flower2_B));
        AppendTilesetAnimToBuffer(gTilesetAnims_Mauville_Flower1_B[timer_div], gTilesetAnims_Mauville_Flower1_VDests[timer_mod], 4 * TILE_SIZE_4BPP);
        AppendTilesetAnimToBuffer(gTilesetAnims_Mauville_Flower2_B[timer_div], gTilesetAnims_Mauville_Flower2_VDests[timer_mod], 4 * TILE_SIZE_4BPP);
    }
}

static void QueueAnimTiles_Rustboro_WindyWater(u16 timer_div, u8 timer_mod)
{
    timer_div -= timer_mod;
    timer_div %= ARRAY_COUNT(gTilesetAnims_Rustboro_WindyWater);
    if (gTilesetAnims_Rustboro_WindyWater[timer_div])
        AppendTilesetAnimToBuffer(gTilesetAnims_Rustboro_WindyWater[timer_div], gTilesetAnims_Rustboro_WindyWater_VDests[timer_mod], 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Rustboro_Fountain(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Rustboro_Fountain);
    AppendTilesetAnimToBuffer(gTilesetAnims_Rustboro_Fountain[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 448)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Lavaridge_Lava(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Lavaridge_Cave_Lava);
    AppendTilesetAnimToBuffer(gTilesetAnims_Lavaridge_Cave_Lava[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 160)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_EverGrande_Flowers(u16 timer_div, u8 timer_mod)
{
    timer_div -= timer_mod;
    timer_div %= ARRAY_COUNT(gTilesetAnims_EverGrande_Flowers);

    AppendTilesetAnimToBuffer(gTilesetAnims_EverGrande_Flowers[timer_div], gTilesetAnims_EverGrande_VDests[timer_mod], 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Cave_Lava(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Lavaridge_Cave_Lava);
    AppendTilesetAnimToBuffer(gTilesetAnims_Lavaridge_Cave_Lava[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 416)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Dewford_Flag(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Dewford_Flag);
    AppendTilesetAnimToBuffer(gTilesetAnims_Dewford_Flag[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 170)), 6 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_BattleFrontierOutsideWest_Flag(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_BattleFrontierOutsideWest_Flag);
    AppendTilesetAnimToBuffer(gTilesetAnims_BattleFrontierOutsideWest_Flag[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 218)), 6 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_BattleFrontierOutsideEast_Flag(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_BattleFrontierOutsideEast_Flag);
    AppendTilesetAnimToBuffer(gTilesetAnims_BattleFrontierOutsideEast_Flag[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 218)), 6 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Slateport_Balloons(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Slateport_Balloons);
    AppendTilesetAnimToBuffer(gTilesetAnims_Slateport_Balloons[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 224)), 4 * TILE_SIZE_4BPP);
}

static void TilesetAnim_MauvilleGym(u16 timer)
{
    if (timer % 2 == 0)
        QueueAnimTiles_MauvilleGym_ElectricGates(timer / 2);
}

static void TilesetAnim_SootopolisGym(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_SootopolisGym_Waterfalls(timer / 8);
}

static void TilesetAnim_EliteFour(u16 timer)
{
    if (timer % 64 == 1)
        QueueAnimTiles_EliteFour_GroundLights(timer / 64);
    if (timer % 8 == 1)
        QueueAnimTiles_EliteFour_WallLights(timer / 8);
}

static void TilesetAnim_BikeShop(u16 timer)
{
    if (timer % 4 == 0)
        QueueAnimTiles_BikeShop_BlinkingLights(timer / 4);
}

static void TilesetAnim_BattlePyramid(u16 timer)
{
    if (timer % 8 == 0)
    {
        QueueAnimTiles_BattlePyramid_Torch(timer / 8);
        QueueAnimTiles_BattlePyramid_StatueShadow(timer / 8);
    }
}

static void TilesetAnim_BattleDome(u16 timer)
{
    if (timer % 4 == 0)
        BlendAnimPalette_BattleDome_FloorLights(timer / 4);
}

static void TilesetAnim_BattleDome2(u16 timer)
{
    if (timer % 4 == 0)
        BlendAnimPalette_BattleDome_FloorLightsNoBlend(timer / 4);
}

static void QueueAnimTiles_Building_TVTurnedOn(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Building_TvTurnedOn);
    AppendTilesetAnimToBuffer(gTilesetAnims_Building_TvTurnedOn[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(496)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_SootopolisGym_Waterfalls(u16 timer)
{
    u16 i = timer % min(ARRAY_COUNT(gTilesetAnims_SootopolisGym_SideWaterfall), ARRAY_COUNT(gTilesetAnims_SootopolisGym_FrontWaterfall));
    AppendTilesetAnimToBuffer(gTilesetAnims_SootopolisGym_SideWaterfall[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 496)), 12 * TILE_SIZE_4BPP);
    AppendTilesetAnimToBuffer(gTilesetAnims_SootopolisGym_FrontWaterfall[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 464)), 20 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_EliteFour_WallLights(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_EliteFour_WallLights);
    AppendTilesetAnimToBuffer(gTilesetAnims_EliteFour_WallLights[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 504)), 1 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_EliteFour_GroundLights(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_EliteFour_FloorLight);
    AppendTilesetAnimToBuffer(gTilesetAnims_EliteFour_FloorLight[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 480)), 4 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_MauvilleGym_ElectricGates(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_MauvilleGym_ElectricGates);
    AppendTilesetAnimToBuffer(gTilesetAnims_MauvilleGym_ElectricGates[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 144)), 16 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_BikeShop_BlinkingLights(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_BikeShop_BlinkingLights);
    AppendTilesetAnimToBuffer(gTilesetAnims_BikeShop_BlinkingLights[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 496)), 9 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_Sootopolis_StormyWater(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_Sootopolis_StormyWater);
    AppendTilesetAnimToBuffer(gTilesetAnims_Sootopolis_StormyWater[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 240)), 96 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_BattlePyramid_Torch(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_BattlePyramid_Torch);
    AppendTilesetAnimToBuffer(gTilesetAnims_BattlePyramid_Torch[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 151)), 8 * TILE_SIZE_4BPP);
}

static void QueueAnimTiles_BattlePyramid_StatueShadow(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_BattlePyramid_StatueShadow);
    AppendTilesetAnimToBuffer(gTilesetAnims_BattlePyramid_StatueShadow[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 135)), 8 * TILE_SIZE_4BPP);
}

static void BlendAnimPalette_BattleDome_FloorLights(u16 timer)
{
    CpuCopy16(sTilesetAnims_BattleDomeFloorLightPals[timer % ARRAY_COUNT(sTilesetAnims_BattleDomeFloorLightPals)], &gPlttBufferUnfaded[BG_PLTT_ID(8)], PLTT_SIZE_4BPP);
    BlendPalette(BG_PLTT_ID(8), 16, gPaletteFade.y, gPaletteFade.blendColor & 0x7FFF);
    if ((u8)FindTaskIdByFunc(Task_BattleTransition_Intro) != TASK_NONE)
    {
        sSecondaryTilesetAnimCallback = TilesetAnim_BattleDome2;
        sSecondaryTilesetAnimCounterMax = 32;
    }
}

static void BlendAnimPalette_BattleDome_FloorLightsNoBlend(u16 timer)
{
    CpuCopy16(sTilesetAnims_BattleDomeFloorLightPals[timer % ARRAY_COUNT(sTilesetAnims_BattleDomeFloorLightPals)], &gPlttBufferUnfaded[BG_PLTT_ID(8)], PLTT_SIZE_4BPP);
    if ((u8)FindTaskIdByFunc(Task_BattleTransition_Intro) == TASK_NONE)
    {
        BlendPalette(BG_PLTT_ID(8), 16, gPaletteFade.y, gPaletteFade.blendColor & 0x7FFF);
        if (!--sSecondaryTilesetAnimCounterMax)
            sSecondaryTilesetAnimCallback = NULL;
    }
}

// Project Grounded: draaikolken van het Keldeo-eiland; tiles 16-31 van de secondary, elke 8 frames een stap
static void QueueAnimTiles_UnchartedIsle_Whirlpool(u16 timer)
{
    u16 i = timer % ARRAY_COUNT(gTilesetAnims_UnchartedIsle_Whirlpool);
    AppendTilesetAnimToBuffer(gTilesetAnims_UnchartedIsle_Whirlpool[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 16)), 16 * TILE_SIZE_4BPP);
}

static void TilesetAnim_UnchartedIsle(u16 timer)
{
    if (timer % 8 == 0)
        QueueAnimTiles_UnchartedIsle_Whirlpool(timer / 8);
}

void InitTilesetAnim_UnchartedIsle(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UnchartedIsle;
}

// Project Grounded: brandend National Park (tools/grounded/maptools/national_park_tiles.py): Rustboro (fontein) +
// vuur in tiles 320-375 van de secondary, elke 8 frames een stap
static void TilesetAnim_ParkBurnt(u16 timer)
{
    TilesetAnim_Rustboro(timer);
    if (timer % 8 == 1)
        AppendTilesetAnimToBuffer(gTilesetAnims_ParkBurnt_Fire[(timer / 8) % ARRAY_COUNT(gTilesetAnims_ParkBurnt_Fire)],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 320)), 56 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_ParkBurnt(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_ParkBurnt;
}

// ultra_worlds_a { (tools/grounded/maptools/ultra_worlds_a.py: eigen tilesets van zes Ultra Beast-werelden)
#include "constants/rgb.h"

// paletcyclus: kleuren first..first+n-1 van BG-palet pal schuiven elke stap een plek op (lava, water, leds)
static void UltraWorld_CyclePal(u8 pal, u8 first, u8 n, const u16 *cols, u16 step)
{
    u32 i;
    for (i = 0; i < n; i++)
        gPlttBufferUnfaded[BG_PLTT_ID(pal) + first + i] = cols[(i + step) % n];
    if ((u8)FindTaskIdByFunc(Task_BattleTransition_Intro) == TASK_NONE)
        BlendPalette(BG_PLTT_ID(pal) + first, n, gPaletteFade.y, gPaletteFade.blendColor & 0x7FFF);
}
const u16 gTilesetAnims_UltraWorldNihilego_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/0.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/1.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/2.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/3.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/4.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/5.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/6.4bpp");
const u16 gTilesetAnims_UltraWorldNihilego_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_world_nihilego/anim/7.4bpp");
const u16 *const gTilesetAnims_UltraWorldNihilego[] = {
    gTilesetAnims_UltraWorldNihilego_Frame0,
    gTilesetAnims_UltraWorldNihilego_Frame1,
    gTilesetAnims_UltraWorldNihilego_Frame2,
    gTilesetAnims_UltraWorldNihilego_Frame3,
    gTilesetAnims_UltraWorldNihilego_Frame4,
    gTilesetAnims_UltraWorldNihilego_Frame5,
    gTilesetAnims_UltraWorldNihilego_Frame6,
    gTilesetAnims_UltraWorldNihilego_Frame7,
};

static void TilesetAnim_UltraWorldNihilego(u16 timer)
{
    if (timer % 8 == 0)
        AppendTilesetAnimToBuffer(gTilesetAnims_UltraWorldNihilego[(timer / 8) % 8], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY)), 52 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraWorldNihilego(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 256;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraWorldNihilego;
}

const u16 gTilesetAnims_UltraWorldPheromosa_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/0.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/1.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/2.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/3.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/4.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/5.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/6.4bpp");
const u16 gTilesetAnims_UltraWorldPheromosa_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_world_pheromosa/anim/7.4bpp");
const u16 *const gTilesetAnims_UltraWorldPheromosa[] = {
    gTilesetAnims_UltraWorldPheromosa_Frame0,
    gTilesetAnims_UltraWorldPheromosa_Frame1,
    gTilesetAnims_UltraWorldPheromosa_Frame2,
    gTilesetAnims_UltraWorldPheromosa_Frame3,
    gTilesetAnims_UltraWorldPheromosa_Frame4,
    gTilesetAnims_UltraWorldPheromosa_Frame5,
    gTilesetAnims_UltraWorldPheromosa_Frame6,
    gTilesetAnims_UltraWorldPheromosa_Frame7,
};

static const u16 sUltraWorldPheromosa_Cycle0[] = {RGB(24, 5, 0), RGB(30, 12, 1), RGB(31, 20, 3), RGB(31, 28, 12)};
static const u16 sUltraWorldPheromosa_Cycle1[] = {RGB(4, 11, 21), RGB(6, 16, 26), RGB(11, 21, 29), RGB(19, 26, 31)};
static void TilesetAnim_UltraWorldPheromosa(u16 timer)
{
    if (timer % 6 == 0)
        AppendTilesetAnimToBuffer(gTilesetAnims_UltraWorldPheromosa[(timer / 6) % 8], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY)), 112 * TILE_SIZE_4BPP);
    if (timer % 8 == 0)
        UltraWorld_CyclePal(11, 12, 4, sUltraWorldPheromosa_Cycle0, timer / 8);
    if (timer % 8 == 0)
        UltraWorld_CyclePal(12, 12, 4, sUltraWorldPheromosa_Cycle1, timer / 8);
}

void InitTilesetAnim_UltraWorldPheromosa(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 256;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraWorldPheromosa;
}

const u16 gTilesetAnims_UltraWorldXurkitree_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/0.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/1.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/2.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/3.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/4.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/5.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/6.4bpp");
const u16 gTilesetAnims_UltraWorldXurkitree_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_world_xurkitree/anim/7.4bpp");
const u16 *const gTilesetAnims_UltraWorldXurkitree[] = {
    gTilesetAnims_UltraWorldXurkitree_Frame0,
    gTilesetAnims_UltraWorldXurkitree_Frame1,
    gTilesetAnims_UltraWorldXurkitree_Frame2,
    gTilesetAnims_UltraWorldXurkitree_Frame3,
    gTilesetAnims_UltraWorldXurkitree_Frame4,
    gTilesetAnims_UltraWorldXurkitree_Frame5,
    gTilesetAnims_UltraWorldXurkitree_Frame6,
    gTilesetAnims_UltraWorldXurkitree_Frame7,
};

static const u16 sUltraWorldXurkitree_Cycle0[] = {RGB(31, 30, 15), RGB(13, 12, 6), RGB(12, 11, 7), RGB(11, 12, 6)};
static const u16 sUltraWorldXurkitree_Cycle1[] = {RGB(3, 9, 14), RGB(6, 18, 26), RGB(17, 28, 31), RGB(5, 13, 21)};
static void TilesetAnim_UltraWorldXurkitree(u16 timer)
{
    if (timer % 4 == 0)
        AppendTilesetAnimToBuffer(gTilesetAnims_UltraWorldXurkitree[(timer / 4) % 8], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY)), 48 * TILE_SIZE_4BPP);
    if (timer % 8 == 0)
        UltraWorld_CyclePal(11, 12, 4, sUltraWorldXurkitree_Cycle0, timer / 8);
    if (timer % 8 == 0)
        UltraWorld_CyclePal(12, 12, 4, sUltraWorldXurkitree_Cycle1, timer / 8);
}

void InitTilesetAnim_UltraWorldXurkitree(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 256;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraWorldXurkitree;
}

const u16 gTilesetAnims_UltraWorldKartana_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/0.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/1.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/2.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/3.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/4.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/5.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/6.4bpp");
const u16 gTilesetAnims_UltraWorldKartana_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_world_kartana/anim/7.4bpp");
const u16 *const gTilesetAnims_UltraWorldKartana[] = {
    gTilesetAnims_UltraWorldKartana_Frame0,
    gTilesetAnims_UltraWorldKartana_Frame1,
    gTilesetAnims_UltraWorldKartana_Frame2,
    gTilesetAnims_UltraWorldKartana_Frame3,
    gTilesetAnims_UltraWorldKartana_Frame4,
    gTilesetAnims_UltraWorldKartana_Frame5,
    gTilesetAnims_UltraWorldKartana_Frame6,
    gTilesetAnims_UltraWorldKartana_Frame7,
};

static void TilesetAnim_UltraWorldKartana(u16 timer)
{
    if (timer % 6 == 0)
        AppendTilesetAnimToBuffer(gTilesetAnims_UltraWorldKartana[(timer / 6) % 8], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY)), 77 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraWorldKartana(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 256;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraWorldKartana;
}
// } ultra_worlds_a
// ultra_worlds_b { (tools/grounded/maptools/ultra_worlds_b.py: animaties van de Ultra Space-werelden)
static const u16 sTilesetAnims_UltraBStakataka_Eyes0_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes0/0.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes0_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes0/1.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes0_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes0/2.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes0_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes0/3.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes0_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes0/4.4bpp");
static const u16 *const sTilesetAnims_UltraBStakataka_Eyes0[] = {
    sTilesetAnims_UltraBStakataka_Eyes0_Frame0,
    sTilesetAnims_UltraBStakataka_Eyes0_Frame1,
    sTilesetAnims_UltraBStakataka_Eyes0_Frame2,
    sTilesetAnims_UltraBStakataka_Eyes0_Frame3,
    sTilesetAnims_UltraBStakataka_Eyes0_Frame4,
};
static const u8 sTilesetAnimSeq_UltraBStakataka_Eyes0[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3, 4, 3};
static const u16 sTilesetAnims_UltraBStakataka_Eyes1_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes1/0.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes1_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes1/1.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes1_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes1/2.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes1_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes1/3.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes1_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes1/4.4bpp");
static const u16 *const sTilesetAnims_UltraBStakataka_Eyes1[] = {
    sTilesetAnims_UltraBStakataka_Eyes1_Frame0,
    sTilesetAnims_UltraBStakataka_Eyes1_Frame1,
    sTilesetAnims_UltraBStakataka_Eyes1_Frame2,
    sTilesetAnims_UltraBStakataka_Eyes1_Frame3,
    sTilesetAnims_UltraBStakataka_Eyes1_Frame4,
};
static const u8 sTilesetAnimSeq_UltraBStakataka_Eyes1[] = {0, 0, 0, 0, 3, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 1, 1, 0, 0, 0};
static const u16 sTilesetAnims_UltraBStakataka_Eyes2_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes2/0.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes2_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes2/1.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes2_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes2/2.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes2_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes2/3.4bpp");
static const u16 sTilesetAnims_UltraBStakataka_Eyes2_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_stakataka/anim/eyes2/4.4bpp");
static const u16 *const sTilesetAnims_UltraBStakataka_Eyes2[] = {
    sTilesetAnims_UltraBStakataka_Eyes2_Frame0,
    sTilesetAnims_UltraBStakataka_Eyes2_Frame1,
    sTilesetAnims_UltraBStakataka_Eyes2_Frame2,
    sTilesetAnims_UltraBStakataka_Eyes2_Frame3,
    sTilesetAnims_UltraBStakataka_Eyes2_Frame4,
};
static const u8 sTilesetAnimSeq_UltraBStakataka_Eyes2[] = {0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 3, 0, 2, 2};
static void TilesetAnim_UltraBStakataka(u16 timer)
{
    if (timer % 8 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBStakataka_Eyes0[sTilesetAnimSeq_UltraBStakataka_Eyes0[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBStakataka_Eyes0)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 0)), 36 * TILE_SIZE_4BPP);
    if (timer % 8 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBStakataka_Eyes1[sTilesetAnimSeq_UltraBStakataka_Eyes1[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBStakataka_Eyes1)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 36)), 36 * TILE_SIZE_4BPP);
    if (timer % 8 == 2)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBStakataka_Eyes2[sTilesetAnimSeq_UltraBStakataka_Eyes2[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBStakataka_Eyes2)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 72)), 36 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraBStakataka(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraBStakataka;
}

static const u16 sTilesetAnims_UltraBNecrozma_Spark0_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark0/0.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark0_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark0/1.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark0_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark0/2.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark0_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark0/3.4bpp");
static const u16 *const sTilesetAnims_UltraBNecrozma_Spark0[] = {
    sTilesetAnims_UltraBNecrozma_Spark0_Frame0,
    sTilesetAnims_UltraBNecrozma_Spark0_Frame1,
    sTilesetAnims_UltraBNecrozma_Spark0_Frame2,
    sTilesetAnims_UltraBNecrozma_Spark0_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBNecrozma_Spark0[] = {0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBNecrozma_Spark1_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark1/0.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark1_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark1/1.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark1_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark1/2.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark1_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark1/3.4bpp");
static const u16 *const sTilesetAnims_UltraBNecrozma_Spark1[] = {
    sTilesetAnims_UltraBNecrozma_Spark1_Frame0,
    sTilesetAnims_UltraBNecrozma_Spark1_Frame1,
    sTilesetAnims_UltraBNecrozma_Spark1_Frame2,
    sTilesetAnims_UltraBNecrozma_Spark1_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBNecrozma_Spark1[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBNecrozma_Spark2_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark2/0.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark2_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark2/1.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark2_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark2/2.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark2_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark2/3.4bpp");
static const u16 *const sTilesetAnims_UltraBNecrozma_Spark2[] = {
    sTilesetAnims_UltraBNecrozma_Spark2_Frame0,
    sTilesetAnims_UltraBNecrozma_Spark2_Frame1,
    sTilesetAnims_UltraBNecrozma_Spark2_Frame2,
    sTilesetAnims_UltraBNecrozma_Spark2_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBNecrozma_Spark2[] = {0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBNecrozma_Spark3_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark3/0.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark3_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark3/1.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark3_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark3/2.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark3_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark3/3.4bpp");
static const u16 *const sTilesetAnims_UltraBNecrozma_Spark3[] = {
    sTilesetAnims_UltraBNecrozma_Spark3_Frame0,
    sTilesetAnims_UltraBNecrozma_Spark3_Frame1,
    sTilesetAnims_UltraBNecrozma_Spark3_Frame2,
    sTilesetAnims_UltraBNecrozma_Spark3_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBNecrozma_Spark3[] = {0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBNecrozma_Spark4_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark4/0.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark4_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark4/1.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark4_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark4/2.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark4_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark4/3.4bpp");
static const u16 *const sTilesetAnims_UltraBNecrozma_Spark4[] = {
    sTilesetAnims_UltraBNecrozma_Spark4_Frame0,
    sTilesetAnims_UltraBNecrozma_Spark4_Frame1,
    sTilesetAnims_UltraBNecrozma_Spark4_Frame2,
    sTilesetAnims_UltraBNecrozma_Spark4_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBNecrozma_Spark4[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBNecrozma_Spark5_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark5/0.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark5_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark5/1.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark5_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark5/2.4bpp");
static const u16 sTilesetAnims_UltraBNecrozma_Spark5_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_necrozma/anim/spark5/3.4bpp");
static const u16 *const sTilesetAnims_UltraBNecrozma_Spark5[] = {
    sTilesetAnims_UltraBNecrozma_Spark5_Frame0,
    sTilesetAnims_UltraBNecrozma_Spark5_Frame1,
    sTilesetAnims_UltraBNecrozma_Spark5_Frame2,
    sTilesetAnims_UltraBNecrozma_Spark5_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBNecrozma_Spark5[] = {0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static void TilesetAnim_UltraBNecrozma(u16 timer)
{
    if (timer % 6 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBNecrozma_Spark0[sTilesetAnimSeq_UltraBNecrozma_Spark0[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBNecrozma_Spark0)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 0)), 28 * TILE_SIZE_4BPP);
    if (timer % 6 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBNecrozma_Spark1[sTilesetAnimSeq_UltraBNecrozma_Spark1[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBNecrozma_Spark1)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 28)), 28 * TILE_SIZE_4BPP);
    if (timer % 6 == 2)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBNecrozma_Spark2[sTilesetAnimSeq_UltraBNecrozma_Spark2[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBNecrozma_Spark2)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 56)), 28 * TILE_SIZE_4BPP);
    if (timer % 6 == 3)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBNecrozma_Spark3[sTilesetAnimSeq_UltraBNecrozma_Spark3[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBNecrozma_Spark3)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 84)), 16 * TILE_SIZE_4BPP);
    if (timer % 6 == 4)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBNecrozma_Spark4[sTilesetAnimSeq_UltraBNecrozma_Spark4[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBNecrozma_Spark4)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 100)), 12 * TILE_SIZE_4BPP);
    if (timer % 6 == 5)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBNecrozma_Spark5[sTilesetAnimSeq_UltraBNecrozma_Spark5[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBNecrozma_Spark5)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 112)), 12 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraBNecrozma(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraBNecrozma;
}

static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/0.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/1.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/2.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/3.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/4.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/5.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/6.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire0_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire0/7.4bpp");
static const u16 *const sTilesetAnims_UltraBGuzzlord_Fire0[] = {
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame0,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame1,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame2,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame3,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame4,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame5,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame6,
    sTilesetAnims_UltraBGuzzlord_Fire0_Frame7,
};
static const u8 sTilesetAnimSeq_UltraBGuzzlord_Fire0[] = {0, 1, 2, 3, 4, 5, 6, 7};
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/0.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/1.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/2.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/3.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/4.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/5.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/6.4bpp");
static const u16 sTilesetAnims_UltraBGuzzlord_Fire1_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_b_guzzlord/anim/fire1/7.4bpp");
static const u16 *const sTilesetAnims_UltraBGuzzlord_Fire1[] = {
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame0,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame1,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame2,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame3,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame4,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame5,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame6,
    sTilesetAnims_UltraBGuzzlord_Fire1_Frame7,
};
static const u8 sTilesetAnimSeq_UltraBGuzzlord_Fire1[] = {0, 1, 2, 3, 4, 5, 6, 7};
static void TilesetAnim_UltraBGuzzlord(u16 timer)
{
    if (timer % 8 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBGuzzlord_Fire0[sTilesetAnimSeq_UltraBGuzzlord_Fire0[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBGuzzlord_Fire0)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 0)), 12 * TILE_SIZE_4BPP);
    if (timer % 8 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBGuzzlord_Fire1[sTilesetAnimSeq_UltraBGuzzlord_Fire1[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBGuzzlord_Fire1)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 12)), 8 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraBGuzzlord(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraBGuzzlord;
}

static const u16 sTilesetAnims_UltraBBlacephalon_Bulbs_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/bulbs/0.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Bulbs_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/bulbs/1.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Bulbs_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/bulbs/2.4bpp");
static const u16 *const sTilesetAnims_UltraBBlacephalon_Bulbs[] = {
    sTilesetAnims_UltraBBlacephalon_Bulbs_Frame0,
    sTilesetAnims_UltraBBlacephalon_Bulbs_Frame1,
    sTilesetAnims_UltraBBlacephalon_Bulbs_Frame2,
};
static const u8 sTilesetAnimSeq_UltraBBlacephalon_Bulbs[] = {0, 1, 2};
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/0.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/1.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/2.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/3.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/4.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/5.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/6.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Hoop_Frame7[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/hoop/7.4bpp");
static const u16 *const sTilesetAnims_UltraBBlacephalon_Hoop[] = {
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame0,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame1,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame2,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame3,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame4,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame5,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame6,
    sTilesetAnims_UltraBBlacephalon_Hoop_Frame7,
};
static const u8 sTilesetAnimSeq_UltraBBlacephalon_Hoop[] = {0, 1, 2, 3, 4, 5, 6, 7};
static const u16 sTilesetAnims_UltraBBlacephalon_Balloons_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/balloons/0.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Balloons_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/balloons/1.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Balloons_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/balloons/2.4bpp");
static const u16 sTilesetAnims_UltraBBlacephalon_Balloons_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_blacephalon/anim/balloons/3.4bpp");
static const u16 *const sTilesetAnims_UltraBBlacephalon_Balloons[] = {
    sTilesetAnims_UltraBBlacephalon_Balloons_Frame0,
    sTilesetAnims_UltraBBlacephalon_Balloons_Frame1,
    sTilesetAnims_UltraBBlacephalon_Balloons_Frame2,
    sTilesetAnims_UltraBBlacephalon_Balloons_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBBlacephalon_Balloons[] = {0, 1, 2, 3};
static void TilesetAnim_UltraBBlacephalon(u16 timer)
{
    if (timer % 10 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBBlacephalon_Bulbs[sTilesetAnimSeq_UltraBBlacephalon_Bulbs[(timer / 10) % ARRAY_COUNT(sTilesetAnimSeq_UltraBBlacephalon_Bulbs)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 0)), 12 * TILE_SIZE_4BPP);
    if (timer % 8 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBBlacephalon_Hoop[sTilesetAnimSeq_UltraBBlacephalon_Hoop[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBBlacephalon_Hoop)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 12)), 8 * TILE_SIZE_4BPP);
    if (timer % 16 == 2)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBBlacephalon_Balloons[sTilesetAnimSeq_UltraBBlacephalon_Balloons[(timer / 16) % ARRAY_COUNT(sTilesetAnimSeq_UltraBBlacephalon_Balloons)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 20)), 16 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraBBlacephalon(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraBBlacephalon;
}

static const u16 sTilesetAnims_UltraBPoipole_Eye_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/eye/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Eye_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/eye/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Eye_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/eye/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Eye_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/eye/3.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Eye_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/eye/4.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Eye[] = {
    sTilesetAnims_UltraBPoipole_Eye_Frame0,
    sTilesetAnims_UltraBPoipole_Eye_Frame1,
    sTilesetAnims_UltraBPoipole_Eye_Frame2,
    sTilesetAnims_UltraBPoipole_Eye_Frame3,
    sTilesetAnims_UltraBPoipole_Eye_Frame4,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Eye[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Meteor0_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor0/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor0_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor0/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor0_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor0/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor0_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor0/3.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Meteor0[] = {
    sTilesetAnims_UltraBPoipole_Meteor0_Frame0,
    sTilesetAnims_UltraBPoipole_Meteor0_Frame1,
    sTilesetAnims_UltraBPoipole_Meteor0_Frame2,
    sTilesetAnims_UltraBPoipole_Meteor0_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Meteor0[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Meteor1_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor1/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor1_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor1/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor1_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor1/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor1_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor1/3.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Meteor1[] = {
    sTilesetAnims_UltraBPoipole_Meteor1_Frame0,
    sTilesetAnims_UltraBPoipole_Meteor1_Frame1,
    sTilesetAnims_UltraBPoipole_Meteor1_Frame2,
    sTilesetAnims_UltraBPoipole_Meteor1_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Meteor1[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Meteor2_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor2/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor2_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor2/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor2_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor2/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor2_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor2/3.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Meteor2[] = {
    sTilesetAnims_UltraBPoipole_Meteor2_Frame0,
    sTilesetAnims_UltraBPoipole_Meteor2_Frame1,
    sTilesetAnims_UltraBPoipole_Meteor2_Frame2,
    sTilesetAnims_UltraBPoipole_Meteor2_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Meteor2[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Meteor3_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor3/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor3_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor3/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor3_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor3/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Meteor3_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/meteor3/3.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Meteor3[] = {
    sTilesetAnims_UltraBPoipole_Meteor3_Frame0,
    sTilesetAnims_UltraBPoipole_Meteor3_Frame1,
    sTilesetAnims_UltraBPoipole_Meteor3_Frame2,
    sTilesetAnims_UltraBPoipole_Meteor3_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Meteor3[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Bubbles_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/bubbles/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Bubbles_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/bubbles/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Bubbles_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/bubbles/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Bubbles_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/bubbles/3.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Bubbles_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/bubbles/4.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Bubbles[] = {
    sTilesetAnims_UltraBPoipole_Bubbles_Frame0,
    sTilesetAnims_UltraBPoipole_Bubbles_Frame1,
    sTilesetAnims_UltraBPoipole_Bubbles_Frame2,
    sTilesetAnims_UltraBPoipole_Bubbles_Frame3,
    sTilesetAnims_UltraBPoipole_Bubbles_Frame4,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Bubbles[] = {0, 1, 2, 3, 4, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/3.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/4.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/5.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Geyser_Frame6[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/geyser/6.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Geyser[] = {
    sTilesetAnims_UltraBPoipole_Geyser_Frame0,
    sTilesetAnims_UltraBPoipole_Geyser_Frame1,
    sTilesetAnims_UltraBPoipole_Geyser_Frame2,
    sTilesetAnims_UltraBPoipole_Geyser_Frame3,
    sTilesetAnims_UltraBPoipole_Geyser_Frame4,
    sTilesetAnims_UltraBPoipole_Geyser_Frame5,
    sTilesetAnims_UltraBPoipole_Geyser_Frame6,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Geyser[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 6, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Plasma_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/plasma/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Plasma_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/plasma/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Plasma_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/plasma/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Plasma_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/plasma/3.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Plasma_Frame4[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/plasma/4.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Plasma_Frame5[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/plasma/5.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Plasma[] = {
    sTilesetAnims_UltraBPoipole_Plasma_Frame0,
    sTilesetAnims_UltraBPoipole_Plasma_Frame1,
    sTilesetAnims_UltraBPoipole_Plasma_Frame2,
    sTilesetAnims_UltraBPoipole_Plasma_Frame3,
    sTilesetAnims_UltraBPoipole_Plasma_Frame4,
    sTilesetAnims_UltraBPoipole_Plasma_Frame5,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Plasma[] = {0, 1, 2, 3, 4, 5, 1, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Arc_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/arc/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Arc_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/arc/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Arc_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/arc/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Arc_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/arc/3.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Arc[] = {
    sTilesetAnims_UltraBPoipole_Arc_Frame0,
    sTilesetAnims_UltraBPoipole_Arc_Frame1,
    sTilesetAnims_UltraBPoipole_Arc_Frame2,
    sTilesetAnims_UltraBPoipole_Arc_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Arc[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 3, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0};
static const u16 sTilesetAnims_UltraBPoipole_Ufo_Frame0[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/ufo/0.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Ufo_Frame1[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/ufo/1.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Ufo_Frame2[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/ufo/2.4bpp");
static const u16 sTilesetAnims_UltraBPoipole_Ufo_Frame3[] = INCBIN_U16("data/tilesets/secondary/ultra_b_poipole/anim/ufo/3.4bpp");
static const u16 *const sTilesetAnims_UltraBPoipole_Ufo[] = {
    sTilesetAnims_UltraBPoipole_Ufo_Frame0,
    sTilesetAnims_UltraBPoipole_Ufo_Frame1,
    sTilesetAnims_UltraBPoipole_Ufo_Frame2,
    sTilesetAnims_UltraBPoipole_Ufo_Frame3,
};
static const u8 sTilesetAnimSeq_UltraBPoipole_Ufo[] = {0, 1, 2, 3};
static void TilesetAnim_UltraBPoipole(u16 timer)
{
    if (timer % 10 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Eye[sTilesetAnimSeq_UltraBPoipole_Eye[(timer / 10) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Eye)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 0)), 84 * TILE_SIZE_4BPP);
    if (timer % 3 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Meteor0[sTilesetAnimSeq_UltraBPoipole_Meteor0[(timer / 3) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Meteor0)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 84)), 12 * TILE_SIZE_4BPP);
    if (timer % 3 == 2)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Meteor1[sTilesetAnimSeq_UltraBPoipole_Meteor1[(timer / 3) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Meteor1)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 96)), 12 * TILE_SIZE_4BPP);
    if (timer % 3 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Meteor2[sTilesetAnimSeq_UltraBPoipole_Meteor2[(timer / 3) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Meteor2)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 108)), 12 * TILE_SIZE_4BPP);
    if (timer % 3 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Meteor3[sTilesetAnimSeq_UltraBPoipole_Meteor3[(timer / 3) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Meteor3)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 120)), 12 * TILE_SIZE_4BPP);
    if (timer % 8 == 5)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Bubbles[sTilesetAnimSeq_UltraBPoipole_Bubbles[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Bubbles)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 132)), 16 * TILE_SIZE_4BPP);
    if (timer % 6 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Geyser[sTilesetAnimSeq_UltraBPoipole_Geyser[(timer / 6) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Geyser)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 148)), 8 * TILE_SIZE_4BPP);
    if (timer % 7 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Plasma[sTilesetAnimSeq_UltraBPoipole_Plasma[(timer / 7) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Plasma)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 156)), 12 * TILE_SIZE_4BPP);
    if (timer % 4 == 0)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Arc[sTilesetAnimSeq_UltraBPoipole_Arc[(timer / 4) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Arc)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 168)), 20 * TILE_SIZE_4BPP);
    if (timer % 8 == 1)
        AppendTilesetAnimToBuffer(sTilesetAnims_UltraBPoipole_Ufo[sTilesetAnimSeq_UltraBPoipole_Ufo[(timer / 8) % ARRAY_COUNT(sTilesetAnimSeq_UltraBPoipole_Ufo)]],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 188)), 16 * TILE_SIZE_4BPP);
}

void InitTilesetAnim_UltraBPoipole(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraBPoipole;
}

// } ultra_worlds_b
