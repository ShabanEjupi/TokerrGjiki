# 🚀 Deployment Guide - Publishing to App Stores

Complete guide to publishing Tokerrgjik on all major platforms.

---

## 📱 Google Play Store (Android)

### Prerequisites
- Google Play Console account ($25 one-time fee)
- Signed APK/AAB
- App assets (screenshots, icons, descriptions)

### Step 1: Create Signed APK

```bash
# Generate keystore (first time only)
keytool -genkey -v -keystore tokerrgjik.keystore \
    -alias tokerrgjik \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000

# Build release APK
buildozer android release

# Sign the APK
jarsigner -verbose \
    -sigalg SHA256withRSA \
    -digestalg SHA-256 \
    -keystore tokerrgjik.keystore \
    bin/tokerrgjik-11.0-arm64-v8a-release-unsigned.apk \
    tokerrgjik

# Zipalign
zipalign -v 4 \
    bin/tokerrgjik-11.0-arm64-v8a-release-unsigned.apk \
    bin/tokerrgjik-release.apk
```

### Step 2: Prepare Store Listing

**Required Assets:**
- App icon (512x512 PNG)
- Feature graphic (1024x500 PNG)
- Screenshots (min 2, max 8)
  - Phone: 320-3840px on long side
  - Tablet: 1280-7680px on long side
- Short description (80 chars)
- Full description (4000 chars)

**Sample Description:**
```
TOKERRGJIK - Traditional Albanian Board Game

Play the classic Nine Men's Morris strategy game with a modern twist!

🎮 FEATURES:
• Smart AI opponent (4 difficulty levels)
• Local multiplayer (2 players)
• Beautiful modern interface
• Albanian & English support
• Offline play - no internet needed
• Track your statistics and achievements

🇦🇱 Preserve Albanian traditional games!

Perfect for strategy game lovers and cultural enthusiasts.
```

### Step 3: Upload to Play Console

1. Create new app in Play Console
2. Fill in app details
3. Upload APK/AAB
4. Set pricing (Free)
5. Select countries/regions
6. Content rating questionnaire
7. Privacy policy (required)
8. Submit for review

**Review Time:** 1-7 days

---

## 🍎 Apple App Store (iOS)

### Prerequisites
- Apple Developer account ($99/year)
- macOS with Xcode
- Signed IPA
- App Store Connect account

### Step 1: Build iOS Version

```bash
# On macOS
./build_ios.sh

# Opens Xcode project
# Configure:
# 1. Bundle Identifier: com.shabanejupi.tokerrgjik
# 2. Version: 11.0
# 3. Build: 1
# 4. Team: Your developer team
```

### Step 2: Archive and Upload

**In Xcode:**
1. Product → Archive
2. Window → Organizer
3. Select archive
4. Distribute App
5. App Store Connect
6. Upload

### Step 3: App Store Connect Setup

**Required Info:**
- Name: Tokerrgjik
- Subtitle (30 chars): Albanian Strategy Game
- Description (4000 chars)
- Keywords (100 chars): "board game, strategy, Albanian, traditional, nine mens morris"
- Support URL
- Privacy policy URL

**Required Assets:**
- App icon (1024x1024 PNG, no alpha)
- Screenshots:
  - iPhone 6.5" (3 required)
  - iPhone 5.5" (3 required)
  - iPad Pro 12.9" (3 required)
- App preview video (optional)

### Step 4: Submit for Review

1. Complete all info
2. Add build
3. Set release (manual/automatic)
4. Submit for review

**Review Time:** 24-48 hours typically

---

## 💻 Microsoft Store (Windows)

### Prerequisites
- Microsoft Partner Center account ($19 one-time)
- Windows 10+ SDK
- Signed MSIX package

### Step 1: Create MSIX Package

```powershell
# Install Windows SDK
# Convert EXE to MSIX using MSIX Packaging Tool

# Or use command line
makeappx pack /d dist /p Tokerrgjik.msix
```

### Step 2: Sign Package

```powershell
signtool sign /f YourCertificate.pfx /p Password Tokerrgjik.msix
```

### Step 3: Submit to Store

1. Create app submission
2. Upload MSIX
3. Fill store listing
4. Set pricing
5. Submit

**Review Time:** 1-3 days

---

## 🌐 Web Deployment

### Option 1: GitHub Pages (Free)

```bash
# Build web version
./build_web.sh

# Create gh-pages branch
git checkout -b gh-pages
git add build/web/*
git commit -m "Deploy web version"
git push origin gh-pages

# Enable in repo settings
# Site will be at: https://yourusername.github.io/tokerrgjik
```

### Option 2: Netlify (Free)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd build/web
netlify deploy --prod
```

### Option 3: Vercel (Free)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd build/web
vercel --prod
```

### Option 4: itch.io (Game Platform)

1. Create itch.io account
2. Upload `build/web` folder as HTML5 game
3. Set to "playable in browser"
4. Publish

---

## 📦 Distribution Checklist

### Before Publishing

- [ ] Test on real devices
- [ ] Check all features work
- [ ] Test on different screen sizes
- [ ] Verify sound effects
- [ ] Test offline functionality
- [ ] Check translations
- [ ] Verify privacy compliance
- [ ] Create privacy policy
- [ ] Prepare marketing materials

### Marketing Assets

**Screenshots to Capture:**
1. Main menu
2. Game in progress
3. Victory screen
4. Statistics screen
5. AI difficulty selection

**Description Keywords:**
- Traditional Albanian game
- Nine Men's Morris
- Strategy board game
- Offline game
- Cultural preservation
- Mind game
- Puzzle strategy

---

## 🎯 Post-Launch Strategy

### Week 1: Launch
- Announce on social media
- Contact Albanian gaming communities
- Submit to app review sites
- Monitor reviews and ratings

### Week 2-4: Growth
- Respond to all reviews
- Fix reported bugs (update)
- Add requested features
- A/B test screenshots

### Month 2+: Optimization
- ASO (App Store Optimization)
- User acquisition campaigns
- Content marketing
- Influencer outreach

---

## 💰 Monetization Options

### Option 1: Free with Ads
```python
# Add AdMob (Android) or AdMob/AdColony (iOS)
# Show interstitial after each game
# Banner ads on menu screens
```

### Option 2: Freemium
- Free base game
- Premium features:
  - Remove ads ($1.99)
  - Extra AI personalities ($0.99)
  - Themes pack ($0.99)
  - Statistics export ($0.99)

### Option 3: Paid App
- One-time purchase: $2.99-$4.99
- Premium experience
- No ads ever

### Option 4: Donations
- Free app
- Optional tip jar
- PayPal/Ko-fi integration

---

## 📊 Analytics Setup

### Google Analytics (Free)

```python
# Add to main.py
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    # Initialize Firebase Analytics

# Track events
analytics.track('game_start', {
    'difficulty': difficulty,
    'mode': 'vs_ai'
})
```

### Track These Events:
- Game started
- Game completed
- Difficulty changed
- Achievement unlocked
- Settings changed
- Crashes/errors

---

## 🔄 Update Strategy

### Version Numbering
- **Major.Minor.Patch** (e.g., 11.0.1)
- Major: Big features
- Minor: New features
- Patch: Bug fixes

### Update Frequency
- **Bug fixes:** Within 24-48 hours
- **Minor updates:** Monthly
- **Major updates:** Quarterly

### Update Checklist
- [ ] Increment version number
- [ ] Update changelog
- [ ] Test thoroughly
- [ ] Build all platforms
- [ ] Submit updates
- [ ] Announce on social media

---

## 📝 Legal Requirements

### Privacy Policy (Required)
Include:
- What data is collected
- How data is used
- Data retention
- User rights
- Contact information

**Template:** [Privacy Policy Generator](https://www.freeprivacypolicy.com/)

### Terms of Service
Include:
- Usage rules
- Intellectual property
- Disclaimers
- Liability
- Governing law

---

## 🎨 Branding Guidelines

### App Name Variants
- Primary: **Tokerrgjik**
- Subtitle: **Albanian Strategy Game**
- Hashtags: #Tokerrgjik #AlbanianGames #BoardGame

### Visual Identity
- Primary color: Turquoise (#1ABC9C)
- Accent color: Gold (#F1C40F)
- Logo: Albanian flag + game board element

### Social Media
- Facebook: @TokerrgjikGame
- Instagram: @tokerrgjik
- Twitter: @Tokerrgjik
- YouTube: Tokerrgjik Official

---

## 📈 Success Metrics

### Key Performance Indicators (KPIs)

**Downloads:**
- Target: 1,000 in first month
- Target: 10,000 in first year

**Ratings:**
- Target: 4.0+ stars
- Target: 100+ reviews

**Retention:**
- Day 1: 40%+
- Day 7: 20%+
- Day 30: 10%+

**Revenue (if monetized):**
- Target: $500 in first year
- Target: $2,000 in second year

---

## 🌍 Localization

### Priority Languages
1. ✅ Albanian (Shqip)
2. ✅ English
3. 🔄 German (large Albanian diaspora)
4. 🔄 Italian (large Albanian diaspora)
5. 🔄 Greek (neighboring country)
6. 🔄 Turkish (historical connection)

### Translation Services
- Google Translate (free, basic)
- Professional translators
- Community translations

---

## 🆘 Support Strategy

### Support Channels
1. Email: support@tokerrgjik.com
2. In-app feedback form
3. Social media DMs
4. GitHub issues

### FAQ Document
Create FAQ.md with:
- How to play
- How to change difficulty
- How to undo moves
- How to view statistics
- Troubleshooting

---

## 🎉 Launch Checklist

### Pre-Launch (2 weeks before)
- [ ] All platforms tested
- [ ] Marketing materials ready
- [ ] Social media accounts created
- [ ] Landing page live
- [ ] Press kit prepared

### Launch Day
- [ ] Submit to all stores
- [ ] Announce on social media
- [ ] Send to press
- [ ] Monitor for issues
- [ ] Respond to early reviews

### Post-Launch (1 week after)
- [ ] Collect feedback
- [ ] Fix critical bugs
- [ ] Plan first update
- [ ] Thank early adopters
- [ ] Analyze metrics

---

## 📞 Resources

### Developer Accounts
- [Google Play Console](https://play.google.com/console)
- [Apple Developer](https://developer.apple.com/)
- [Microsoft Partner Center](https://partner.microsoft.com/)

### Tools
- [App Store Screenshot Generator](https://www.appscreenshot.com/)
- [Privacy Policy Generator](https://www.freeprivacypolicy.com/)
- [ASO Tools](https://appradar.com/)

### Communities
- Reddit: r/androiddev, r/iOSProgramming
- Discord: Kivy community
- Stack Overflow: [kivy] tag

---

**🚀 Ready to launch? Good luck! 🎉**

*Remember: Success comes from iteration and user feedback!*
