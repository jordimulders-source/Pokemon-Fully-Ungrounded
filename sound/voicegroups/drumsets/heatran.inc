@ Project Grounded: stoner-drumkit voor Battle! Heatran (heatran_theme.py), FluidR3 Power-kit (heatran_samples.py):
@ 36 kick, 37 snare, 38 open hihat, 39 ride, 40 floor tom, 41 middentom, 42 crash, 43 china,
@ 44 sidestick, 45 ride hoger (bel), 46 halfopen hihat (kort, open-hihatsample afgekapt).
voice_group heatran_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_kick, 255, 0, 255, 0
	voice_directsound_no_resample 60, 62, DirectSoundWaveData_heatran_snare, 255, 0, 255, 0
	voice_directsound_no_resample 60, 80, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, 215
	voice_directsound_no_resample 60, 44, DirectSoundWaveData_heatran_ride, 255, 0, 255, 215
	voice_directsound 60, 40, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, 0
	voice_directsound 65, 76, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, 0
	voice_directsound_no_resample 60, 36, DirectSoundWaveData_heatran_crash, 255, 0, 255, 225
	voice_directsound_no_resample 60, 92, DirectSoundWaveData_heatran_china, 255, 0, 255, 220
	voice_directsound_no_resample 60, 56, DirectSoundWaveData_heatran_side_stick, 255, 0, 255, 0
	voice_directsound 66, 40, DirectSoundWaveData_heatran_ride, 255, 0, 255, 200
	voice_directsound_no_resample 60, 70, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, 0

