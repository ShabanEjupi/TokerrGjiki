# 🚀 Dashboard Financiar në Kohë Reale

## 📊 Përshkrim

Një dashboard interaktiv dhe kompleks për vizualizimin e të dhënave financiare në gjuhën shqipe. Dashboard-i përmban grafikë, diagrame, forma, vija, dhe vizualizime të ndryshme të të dhënave të tregut financiar.

## ✨ Karakteristikat Kryesore

### 📈 Vizualizime të Shumëllojshme
- **Grafikë Çmimesh**: Grafikë linjash interaktivë për çdo aset
- **Candlestick Charts**: Grafikë japonezë për analizë të detajuar
- **Tregues Teknikë**: RSI, Bollinger Bands, Moving Averages, Momentum, Volatilitet
- **Analiza e Volumit**: Grafikë volumi dhe harta termike
- **Parashikime ML**: Vizualizime të parashikimeve të Machine Learning
- **Portfolio Visualization**: Diagrame pie për alokimin e portofolit

### 🎯 Karakteristika të Veçanta
- ✅ **100% në Gjuhën Shqipe** - Të gjitha tekstet, etiketat, dhe mesazhet
- ✅ **6 Skeda Interaktive**: Përmbledhje, Grafikë, Portofoli, Parashikime, Tregues Teknikë, Volumi
- ✅ **14 Asete Financiare**: Aksione teknologjike, komoditete, dhe indekse
- ✅ **Përditësime Automatike**: Të dhënat përditësohen automatikisht çdo 10 sekonda
- ✅ **Design Modern**: Gradiente, animacione, dhe efekte CSS të avancuara
- ✅ **Responsive**: Funksionon në desktop, tablet, dhe mobile

### 🤖 Machine Learning
- **4 Modele të ML**: Random Forest, Gradient Boosting, Regresioni Logjistik, SVM
- **Analiza e Regjimit të Tregut**: Bull Market, Bear Market, Stable Market, High Volatility
- **Niveli i Konfidencës**: Për çdo parashikim individual

## 🛠️ Instalimi

### Kërkesat
```bash
Python 3.8+
Flask
Pandas
NumPy
Plotly
```

### Instalimi i Paketave
```bash
pip install flask pandas numpy plotly
```

## 🚀 Si të Filloni

### Hapi 1: Sigurohuni që të dhënat janë në vend
Struktura e folderëve:
```
WebInfo_Projects/
├── dashboard_app.py
├── templates/
│   └── dashboard.html
├── static/
│   └── js/
│       └── dashboard.js
├── data/
│   ├── advanced_labels.csv
│   ├── processed_features.csv
│   ├── realtime_prices.csv
│   └── latest_predictions.json
```

### Hapi 2: Nise aplikacionin
```bash
python dashboard_app.py
```

### Hapi 3: Hap në browser
Shko në: **http://localhost:5000**

## 📱 Si të Përdorni Dashboard-in

### Skeda "Përmbledhje" (📊)
- Shfaq të gjitha asetet me çmimet e fundit
- Kliko mbi çdo aset për të parë detajet
- Ngjyrat tregojnë: 🟢 Rritje, 🔴 Rënie, ⚪ Stabil

### Skeda "Grafikët" (📈)
- **Zgjidh Asetin**: Dropdown në krye
- **Zgjidh Kohën**: 6O, 12O, 24O, 48O (orë)
- Grafikë interaktivë me zoom dhe pan
- Candlestick chart për analizë detajuar

### Skeda "Portofoli" (💼)
- Shfaq alokimin e rekomanduar
- Metrikat: Kthimi i Pritshëm, Raporti Sharpe, Volatiliteti
- Diagram pie për diversifikimin
- Arsyet për çdo alokim

### Skeda "Parashikimet" (🎯)
- Parashikimet e ML për çdo aset
- 📈 RRITJE / 📉 RËNIE / ➡️ STABIL
- Niveli i konfidencës (%)
- Regjimi i tregut (Bull/Bear/Stable/Volatile)
- Rezultatet e modeleve individuale

### Skeda "Treguesit Teknikë" (🔧)
- **RSI (Relative Strength Index)**: Tregon mbiblerje/mbështyerje
- **Bollinger Bands**: 3 breza për volatilitetin
- **Mesatare Lëvizëse**: MA 5, 14, 20, 50
- **Momentumi**: Forca e lëvizjes së çmimit
- **Volatiliteti**: Shkalla e luhatjeve

### Skeda "Volumi" (📦)
- Volumi krahasuar me çmimin
- Statistika: Mesatar, Maksimal, Trendi
- Harta termike për të gjitha asetet

## 🎨 Përmbajtja e Vizualizimeve

### Grafikë dhe Forma
- ✅ **Line Charts** - Linja të lëmuara për çmimet
- ✅ **Bar Charts** - Volumi dhe konfidenca
- ✅ **Candlestick Charts** - Grafikë japonezë
- ✅ **Pie Charts** - Alokimi i portofolit
- ✅ **Heatmaps** - Harta termike e volumit
- ✅ **Multi-line Charts** - Tregues teknikë
- ✅ **Area Charts** - Volatiliteti me fill
- ✅ **Dual-axis Charts** - Volumi + Çmimi

### Elemente CSS të Avancuara
- 🎨 **Gradient Backgrounds** - Sfonde me gradiente
- 🎨 **Box Shadows** - Hijet 3D për kartat
- 🎨 **Animations** - Pulse, spin, hover effects
- 🎨 **Glassmorphism** - Efekt transparent modern
- 🎨 **Responsive Grid** - Grid layout adaptiv
- 🎨 **Custom Scrollbars** - Scrollbar të personalizuar
- 🎨 **Loading Spinners** - Animacione ngarkimi

## 📊 Të Dhënat

### Asetet e Disponueshme
1. **AAPL** - Apple Inc.
2. **GOOGL** - Alphabet (Google)
3. **MSFT** - Microsoft Corp.
4. **AMZN** - Amazon.com Inc.
5. **NVDA** - NVIDIA Corp.
6. **TSLA** - Tesla Inc.
7. **META** - Meta Platforms
8. **NFLX** - Netflix Inc.
9. **GC=F** - Ari (Gold Futures)
10. **SI=F** - Argjendi (Silver Futures)
11. **CL=F** - Nafta (Crude Oil)
12. **NG=F** - Gazi Natyror (Natural Gas)
13. **^GSPC** - S&P 500
14. **^IXIC** - NASDAQ Composite

### Treguesit Teknikë të Përfshirë
- **RSI** - Relative Strength Index (14 periudha)
- **Bollinger Bands** - Breza (20 periudha, 2 devijime)
- **Moving Averages** - MA 5, 14, 20, 50
- **Momentum** - 7 dhe 14 periudha
- **Volatility** - 14 dhe 20 periudha
- **Volume** - Volumi i transaksioneve

## 🔧 API Endpoints

### GET /
Faqja kryesore e dashboard-it

### GET /api/live-prices
Kthen çmimet e fundit për të gjitha asetet
```json
{
  "AAPL": {
    "name": "Apple Inc.",
    "price": 178.5,
    "high": 180.1,
    "low": 176.2,
    "volume": 14383257,
    "timestamp": "2025-05-21 18:37:13"
  }
}
```

### GET /api/chart/<asset>?hours=24
Kthen të dhënat për grafikun e një aseti

### GET /api/technical/<asset>
Kthen treguesit teknikë për një aset

### GET /api/volume/<asset>
Kthen të dhënat e volumit për një aset

### GET /api/volume-heatmap
Kthen heatmap të volumit për të gjitha asetet

### GET /api/predictions
Kthen parashikimet e ML për të gjitha asetet

### GET /api/portfolio
Kthen rekomandimin e portofolit

### GET /api/assets
Kthen listën e të gjitha aseteve

### GET /api/candlestick/<asset>
Kthen të dhënat për grafikun candlestick

## 🎯 Teknologjitë e Përdorura

### Backend
- **Flask** - Web framework
- **Pandas** - Përpunimi i të dhënave
- **NumPy** - Operacione matematikore
- **JSON** - Formati i të dhënave

### Frontend
- **HTML5** - Struktura
- **CSS3** - Styling (gradients, animations, flexbox, grid)
- **JavaScript (ES6+)** - Logjika interaktive
- **jQuery** - AJAX dhe DOM manipulation
- **Plotly.js** - Grafikë interaktivë

### Design
- **Color Scheme**: Dark mode me akcentë neon
- **Typography**: Segoe UI, sans-serif
- **Layout**: CSS Grid dhe Flexbox
- **Animations**: Keyframes dhe transitions

## 🌟 Karakteristika të Veçanta CSS

### Gradiente dhe Ngjyra
```css
Background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%)
Accent Colors: #00ff88 (green), #667eea (purple), #ff3366 (red)
```

### Animacione
- **Pulse**: Për status dot
- **Spin**: Për loading spinner
- **Hover Effects**: Transform translateY(-5px)

### Shadows dhe Effects
- Box shadows: 0 8px 16px rgba(0, 0, 0, 0.3)
- Hover shadows: 0 12px 24px rgba(102, 126, 234, 0.3)

## 🐛 Troubleshooting

### Problem: Të dhënat nuk ngarkohen
**Zgjidhje**: Kontrollo që skedarët CSV dhe JSON janë në folderin `data/`

### Problem: Grafikët nuk shfaqen
**Zgjidhje**: Sigurohu që Plotly.js dhe jQuery janë ngarkuar

### Problem: Port 5000 është në përdorim
**Zgjidhje**: Ndrysho portin në `dashboard_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: Gabime në console
**Zgjidhje**: Hap Developer Tools (F12) dhe kontrollo console-n për detaje

## 📝 Personalizimi

### Ndrysho Ngjyrat
Modifiko variablat në `dashboard.html` seksionin `<style>`:
```css
/* Ngjyrat kryesore */
--color-primary: #667eea;
--color-success: #00ff88;
--color-danger: #ff3366;
--color-background: #0a0e27;
```

### Shto Asete të Reja
Modifiko `ASSET_NAMES` në `dashboard_app.py`:
```python
ASSET_NAMES = {
    'AAPL': 'Apple Inc.',
    'YOURNEW': 'Emri i Asetit të Ri',
}
```

### Ndrysho Intervalin e Përditësimit
Modifiko në `dashboard.js`:
```javascript
updateInterval = setInterval(function() {
    updatePrices();
}, 10000); // 10 sekonda
```

## 📚 Dokumentacioni i Plotë

### Struktura e Projektit
```
WebInfo_Projects/
│
├── dashboard_app.py          # Backend Flask aplikacioni
├── README.md                 # Ky skedar
│
├── templates/
│   └── dashboard.html        # Frontend HTML
│
├── static/
│   ├── css/
│   └── js/
│       └── dashboard.js      # Frontend JavaScript
│
├── data/
│   ├── advanced_labels.csv   # Të dhëna me tregues teknikë
│   ├── processed_features.csv # Të dhëna të përpunuara
│   ├── realtime_prices.csv    # Çmimet në kohë reale
│   └── latest_predictions.json # Parashikimet e ML
│
└── requirements.txt          # Varësitë Python
```

## 🤝 Kontributi

Nëse dëshironi të kontribuoni:
1. Fork the repository
2. Krijo një branch të ri
3. Bëj ndryshimet tuaja
4. Dërgo pull request

## 📄 Liçensa

MIT License - Përdorni lirisht!

## 👨‍💻 Autori

Dashboard Financiar në Gjuhën Shqipe
Krijuar me ❤️ për komunitetin shqiptar

## 🎉 Faleminderit!

Për çdo pyetje apo problem, mos hezitoni të kontaktoni!

---

**Mirë se vini në Dashboard-in Financiar! 🚀📊💼**
