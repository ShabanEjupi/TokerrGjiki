# Tokerrgjik - Sounds Folder

This folder contains game sound effects.

## Required Sound Files

Place these WAV files in this folder:

1. **place.wav** - Piece placement sound (short click)
2. **move.wav** - Piece movement sound (slide)
3. **remove.wav** - Piece removal sound (pop/break)
4. **mill.wav** - Mill formation sound (success chime)
5. **win.wav** - Victory sound (celebration)
6. **lose.wav** - Defeat sound (sad tone)
7. **click.wav** - UI button click
8. **error.wav** - Invalid move sound (buzz)

## Sound Guidelines

- **Format**: WAV (16-bit, 44.1kHz recommended)
- **Length**: 0.1-2 seconds (short and crisp)
- **Volume**: Normalized to -3dB to prevent clipping
- **Style**: Matching game theme (modern, pleasant)

## Free Sound Resources

- [freesound.org](https://freesound.org/) - Creative Commons sounds
- [zapsplat.com](https://www.zapsplat.com/) - Free sound effects
- [soundbible.com](http://soundbible.com/) - Public domain sounds
- [mixkit.co](https://mixkit.co/free-sound-effects/) - Free game sounds

## Creating Your Own

Use free tools:
- **Audacity** - Free audio editor
- **LMMS** - Music production
- **Bfxr** - 8-bit sound generator

## Example Search Terms

- "button click"
- "game pop"
- "success chime"
- "error buzz"
- "victory fanfare"
- "piece placement"

## Converting to WAV

```bash
# Using ffmpeg
ffmpeg -i input.mp3 -acodec pcm_s16le -ar 44100 output.wav
```

## Current Status

⚠️ **No sounds included** - Game works without sounds but:
- Enhanced experience with audio feedback
- Professional polish
- Better user engagement

---

*Add your sound files here to enable audio!*
