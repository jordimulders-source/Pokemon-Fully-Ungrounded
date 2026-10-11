# Project Grounded: eigen muzieksamples die als DPCM (4 bit, ±halve grootte) in de ROM gaan.
# De HQ-mixer (src/m4a_hq_mixer.s) speelt ze af (MODE_COMP). Lijst = bestandsnamen zonder .wav in grounded/.
# Jordi 10 okt (A/B Mitch): "ik hoor geen verschil". Niet gecomprimeerd: drums (aanzet), aria/koor/stem van Area Zero, < 4 KB.
# Area Zero v10: az_bells_0 (wolk m5-7) en az_bells_8 (intro m1-4) niet: zachte knippen, DPCM-ruis maar 8-14 dB eronder
# (nultest gecomprimeerd - ongecomprimeerd; de luide knippen 22-24 dB, ruis onder het signaal in elke band).
COMPRESSED_SAMPLES := \
	ashfrost_recorder ashfrost_sleigh ashfrost_warm_pad az_bells_1 az_bells_2 \
	az_bells_3 az_bells_4 az_bells_5 az_bells_6 az_bells_7 az_bells_9 az_bells_10 az_bells_11 az_bells_12 az_crystal vsaz_0 vsaz_1 vsaz_2 vsaz_3 vsaz_4 vsaz_5 vsaz_6 vsaz_7 vsaz_8 vsaz_9 bg_bari bg_brush_slap bg_brush_tap \
	bg_mtpt bg_stab bg_upright bg_vibes darkrai_brass_dim darkrai_brass_low \
	darkrai_brass_tt darkrai_celesta darkrai_cry_rev darkrai_drone darkrai_lullaby_rev darkrai_music_box \
	darkrai_rev_box darkrai_rev_cluster darkrai_scream genesect_anvil genesect_bass genesect_bass_dark \
	genesect_cannon genesect_ohit genesect_pipe genesect_press genesect_stab gym2_braam \
	gym2_brush_swirl gym2_brush_tap gym2_cello gym2_flugel gym2_nb_5 gym2_nb_dom \
	gym2_nb_maj gym2_nb_min gym2_nb_sus gym2_np_5 gym2_np_dom gym2_np_maj \
	gym2_np_min gym2_np_sus gym2_pop_brass gym2_pop_pluck gym2_pop_stab gym2_pop_stab5 \
	gym2_rh_dom gym2_rh_maj gym2_rh_min gym2_rh_sus gym2_rhodes gym2_side_stick \
	gym2_tl_lead gym2_tl_pad_maj gym2_tl_pad_min gym2_upright gym2_vibes gym2_w_reese \
	gym2_w_saw_dark gym_fla_down_five gym_fla_down_maj gym_fla_gba_nylon gym_fla_pclara gym_fla_psorda \
	gym_fla_rasg_five gym_fla_rasg_maj gym_fla_up_five gym_fla_up_maj gym_rox_clean_60 gym_rox_clean_72 \
	gym_rox_open gym_rox_pbass gym_wat_hoover gym_wat_saw_60 gym_wat_saw_72 gym_wat_saw_84 \
	heatran_st_lead_60 heatran_st_lead_67 heatran_st_pw_36 heatran_st_pw_37 heatran_st_pw_39 heatran_st_pw_41 \
	heatran_st_pw_42 heatran_st_pw_43 heatran_st_pw_44 heatran_st_pw_46 heatran_st_pw_48 hooh_kiai \
	hooh_koto_57 hooh_koto_64 hooh_koto_71 hooh_koto_78 hooh_nagado hooh_odaiko \
	hooh_shaku_62 hooh_shaku_69 hooh_shaku_76 hooh_shami_52 hooh_shami_59 hooh_shami_66 \
	hooh_shami_73 hooh_sho hoopa_bendir hoopa_dum hoopa_mizmar_57 hoopa_mizmar_64 \
	hoopa_mizmar_71 hoopa_oud_50 hoopa_oud_57 hoopa_oud_64 hoopa_oud_71 hoopa_zill \
	jirachi_celesta jirachi_chimes jirachi_music_box jirachi_sawbass jirachi_supersaw_bright jirachi_supersaw_dark \
	jirachi_supersaw_mid jirachi_vox kc_bongo_hi kc_bongo_lo kc_claves kc_cowbell \
	kc_cuatro kc_guiro_long kc_guitar_57 kc_guitar_69 kc_timbale_hi kc_timbale_lo \
	kc_trombone_55 kc_trombone_67 magikarp_bassoon magikarp_boing magikarp_cry magikarp_cry_rev \
	magikarp_vibraslap magikarp_woodblock mitch5_reese_raw_dark mitch5_wob_c2 mitch5_wob_db2 mitch5_wob_eb2 \
	mitch5_wob_f1 mitch7_pluck mitch7_reese_raw mitch7a_lead_55 mitch7a_lead_61 mitch7a_lead_67 \
	mitch7b_lead_55 mitch7b_lead_61 mitch7b_lead_67 mitch7c_lead_55 mitch7c_lead_61 mitch7c_lead_67 \
	mitch_pad_maj mitch_pad_min rayquaza_choir rayquaza_gangsa rayquaza_gong rayquaza_gongbass \
	rayquaza_jegogan rayquaza_reyong ruinous_call ruinous_impact ruinous_lo58 ruinous_ostbar \
	ruinous_ostbar2      \
	      \
	      \
	                                ruinous_st21 ruinous_st23 ruinous_st25 ruinous_st27 ruinous_st29 ruinous_st31 ruinous_st33 ruinous_st35 ruinous_st37 ruinous_st39 ruinous_st41 ruinous_st43 ruinous_st45 ruinous_st47 ruinous_st49 ruinous_st51 ruinous_st53 ruinous_st55 ruinous_st57 ruinous_st59 ruinous_st61 ruinous_st63 ruinous_st65           ruinous_taiko ruinous_wide14 ruinous_wide18 \
	sb_bass_harm sb_br_a13 sb_br_am9 sb_br_b7alt sb_br_cmaj9 sb_br_d13 \
	sb_br_em9 sb_br_fmaj7s11 sb_br_gmu sb_clav sb_gtr_mute sb_horns \
	sb_horns_hi sb_jazz_oct sb_jazz_oct_hi sb_mute_tpt sb_mute_tpt_hi sb_rh_am9 \
	sb_rh_b7alt sb_rh_cmaj9 sb_rh_cmu sb_rh_d13 sb_rh_fmaj7s11 sb_rh_fsm7b5 \
	sb_rh_gmu sb_rhodes_13 sb_rhodes_m9 sb_side_stick sb_slap_pop sb_slap_thumb \
	sb_talkbox shaymin_celesta shaymin_clarinet shaymin_flute shaymin_harp shaymin_nylon \
	shaymin_upright tapu_brass tapu_brass_hi tapu_impact tapu_lead tapu_odaiko \
	tapu_taiko tapu_vox_a tapu_vox_hu ub_swell victini_power regio_steeldrum \
	yi_dcb99354f_1929

COMPRESSED_SAMPLE_BINS := $(patsubst %,sound/direct_sound_samples/grounded/%.bin,$(COMPRESSED_SAMPLES))
$(COMPRESSED_SAMPLE_BINS): sound/%.bin: sound/%.wav sound/compressed_samples.mk
	$(WAV2AGB) -b -c $< $@
