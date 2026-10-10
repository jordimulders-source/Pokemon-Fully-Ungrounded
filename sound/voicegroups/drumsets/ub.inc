@ Project Grounded: drumkit voor ub_theme.py (Battle! Ultra Beast). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 synthsnare, 39 clap, 40 crash, 41 tom laag, 42 tom hoog.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group ub_drumset, 36
	voice_directsound 62, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 160
	voice_directsound 62, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170
	voice_directsound 66, 64, DirectSoundWaveData_unknown_synth_snare, 255, 226, 0, 120
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 170
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 50, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 150
	voice_directsound 58, 76, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 150
