@ Project Grounded: drumkit voor regio_theme.py (spookachtig). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 doodsklok, 39 pauk, 40 crash.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_spooky_drumset, 36
	voice_directsound 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 56, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 160
	voice_directsound 50, 64, DirectSoundWaveData_sc88pro_tubular_bell, 255, 165, 90, 200
	voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 180
	voice_directsound 56, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 165
