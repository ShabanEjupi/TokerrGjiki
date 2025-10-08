# Tokerrgjik - Assets Folder

This folder contains game assets like icons, images, and graphics.

## Required Assets

### Icons
- `icon.png` (512x512) - App icon for Android/iOS
- `icon.ico` (256x256) - Windows EXE icon
- `presplash.png` (1920x1080) - Android splash screen

### Images (Optional)
- Background images
- Button graphics
- Achievement badges
- Logo variants

## Creating Icons

### From existing image:
```bash
# Install Pillow if not already installed
pip install pillow

# Convert to proper sizes
python -c "from PIL import Image; img = Image.open('your_image.png'); img.resize((512, 512)).save('icon.png')"
```

### Online Tools:
- [favicon.io](https://favicon.io/) - Free icon generator
- [app-icon.co](https://www.appicon.co/) - iOS/Android icons
- [convertio.co](https://convertio.co/png-ico/) - PNG to ICO converter

## Current Status

⚠️ **Placeholder assets** - Replace with your own:
1. Create a 512x512 PNG logo/icon
2. Name it `icon.png` and place here
3. Convert to ICO for Windows: `icon.ico`
4. Create splash screen: `presplash.png` (1920x1080)

## Asset Guidelines

- **Icon**: Simple, recognizable at small sizes
- **Colors**: Match app theme (turquoise/gold)
- **Style**: Modern, minimalist
- **Format**: PNG with transparency (except ICO)

---

*This is a placeholder file. Add your assets here.*
