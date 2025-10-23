Sub GjeneroPrezantimin()
    '================================================================================
    ' GJENERUESI AUTOMATIK I PREZANTIMIT POWERPOINT
    ' NIVELI DOKTORATURE - ANALIZA FINANCIARE
    ' Universiteti i Prishtines - Republika e Kosoves
    '================================================================================
    
    Dim pptApp As PowerPoint.Application
    Dim pptPres As PowerPoint.Presentation
    Dim pptSlide As PowerPoint.Slide
    Dim pptShape As PowerPoint.Shape
    Dim slideIndex As Integer
    
    ' Krijo PowerPoint application
    Set pptApp = New PowerPoint.Application
    pptApp.Visible = True
    
    ' Krijo prezantim te ri
    Set pptPres = pptApp.Presentations.Add
    
    MsgBox "Duke filluar gjenerimin e prezantimit..." & vbCrLf & _
           "Ky proces do te marre 30-60 sekonda.", vbInformation, "Gjenerues Prezantimi"
    
    '================================================================================
    ' SLIDE 1: TITULL
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(1, ppLayoutTitle)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "ANALIZA FINANCIARE" & vbCrLf & "NIVEL DOKTORATURE"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 48
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(46, 134, 171)
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = "Universiteti i Prishtines" & vbCrLf & _
                                                  "Republika e Kosoves" & vbCrLf & vbCrLf & _
                                                  "56,298 Rows | 22 Assets | 8 Modele Stokastike" & vbCrLf & _
                                                  "Tetor 2025"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 20
    
    '================================================================================
    ' SLIDE 2: PERSH

KRIMI I PROJEKTIT
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(2, ppLayoutText)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "PERSH KRIMI I PROJEKTIT"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 40
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = _
        "• QELLIMI: Analiza e tregut financiar me modele stokastike te avancuara" & vbCrLf & vbCrLf & _
        "• SCOPE: 22 Assets (Stocks, Crypto, Forex, Commodities, Indices)" & vbCrLf & vbCrLf & _
        "• PERIUDHA: 2015-2024 (10 vjet te dhenat)" & vbCrLf & vbCrLf & _
        "• MADHESIA: 56,298 rows (2,559 dite tregtimi)" & vbCrLf & vbCrLf & _
        "• METODA: 8 modele matemat ikore te sofistikuara"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 20
    
    '================================================================================
    ' SLIDE 3: MODELET STOKASTIKE
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(3, ppLayoutText)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "8 MODELET STOKASTIKE TE APLIKUARA"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = _
        "1. GEOMETRIC BROWNIAN MOTION (GBM)" & vbCrLf & _
        "   → Modeli Baseline Black-Scholes" & vbCrLf & vbCrLf & _
        "2. HESTON STOCHASTIC VOLATILITY" & vbCrLf & _
        "   → Volatilitet me mean reversion" & vbCrLf & vbCrLf & _
        "3. JUMP DIFFUSION MODEL (Merton 1976)" & vbCrLf & _
        "   → Kaptimi i event-eve ekstreme" & vbCrLf & vbCrLf & _
        "4. GARCH(1,1) EFFECTS" & vbCrLf & _
        "   → Volatility clustering & fat tails"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 18
    
    '================================================================================
    ' SLIDE 4: MODELET (vazhdim)
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(4, ppLayoutText)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "MODELET STOKASTIKE (vazhdim)"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = _
        "5. REGIME SWITCHING (Markov Chain)" & vbCrLf & _
        "   → Bull/Bear/Sideways markets" & vbCrLf & vbCrLf & _
        "6. LEVY PROCESSES" & vbCrLf & _
        "   → Heavy tails (Student-t distribution)" & vbCrLf & vbCrLf & _
        "7. MARKET CRASH SIMULATION" & vbCrLf & _
        "   → Eventi historik (2015, 2018, 2020, 2022)" & vbCrLf & vbCrLf & _
        "8. CORRELATION DYNAMICS" & vbCrLf & _
        "   → Cholesky decomposition"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 18
    
    '================================================================================
    ' SLIDE 5: ASSET-ET
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(5, ppLayoutText)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "22 ASSET-ET E ANALIZUARA"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 38
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = _
        "STOCKS (8): AAPL, GOOGL, MSFT, AMZN, NVDA, TSLA, META, NFLX" & vbCrLf & vbCrLf & _
        "CRYPTO (5): BTC, ETH, SOL, ADA, DOT" & vbCrLf & vbCrLf & _
        "FOREX (3): EUR/USD, GBP/USD, USD/JPY" & vbCrLf & vbCrLf & _
        "COMMODITIES (4): Gold, Silver, Oil, Natural Gas" & vbCrLf & vbCrLf & _
        "INDICES (2): S&P500, NASDAQ"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 20
    
    '================================================================================
    ' SLIDE 6-10: VIZUALIZIMET (do te shtohen manualisht ose automatikisht)
    '================================================================================
    
    ' SLIDE 6: Serite Kohore
    Set pptSlide = pptPres.Slides.Add(6, ppLayoutTitleOnly)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "SERITE KOHORE - 22 ASSETS"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    ' Ketu shto imazhin: 01_serite_kohore_all_assets.png
    
    ' SLIDE 7: Matrica Korrelacionit
    Set pptSlide = pptPres.Slides.Add(7, ppLayoutTitleOnly)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "MATRICA E KORRELACIONIT"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    ' Ketu shto imazhin: 02_matrica_korrelacionit.png
    
    ' SLIDE 8: Shperndarja Returns
    Set pptSlide = pptPres.Slides.Add(8, ppLayoutTitleOnly)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "SHPERNDARJA E RETURNS"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    ' Ketu shto imazhin: 03_shperndarja_returns.png
    
    ' SLIDE 9: Volatiliteti
    Set pptSlide = pptPres.Slides.Add(9, ppLayoutTitleOnly)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "KRAHASIMI I VOLATILITETIT"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    ' Ketu shto imazhin: 04_volatiliteti_krahasim.png
    
    ' SLIDE 10: Analiza Volumit
    Set pptSlide = pptPres.Slides.Add(10, ppLayoutTitleOnly)
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 36
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "ANALIZA E VOLUMIT"
    ' Ketu shto imazhin: 05_analiza_volumit.png
    
    '================================================================================
    ' SLIDE 11: REZULTATET KYCE
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(11, ppLayoutText)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "REZULTATET KYCE"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 40
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = _
        "✓ 56,298 ROWS te gjeneruar me sukses" & vbCrLf & vbCrLf & _
        "✓ 22 ASSETS nga 5 kategori te ndryshmett" & vbCrLf & vbCrLf & _
        "✓ 8 MODELE STOKASTIKE te aplikuara" & vbCrLf & vbCrLf & _
        "✓ 10 VJET te dhena (2015-2024)" & vbCrLf & vbCrLf & _
        "✓ VIZUALIZIME PROFESIONALE (300 DPI)" & vbCrLf & vbCrLf & _
        "✓ NIVEL DOKTORATURE - Kerkime Avancuara"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 22
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Bold = msoTrue
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Color.RGB = RGB(0, 128, 0)
    
    '================================================================================
    ' SLIDE 12: KONKLUZIONE
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(12, ppLayoutText)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "KONKLUZIONE"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 40
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = _
        "• Dataset-i i gjeneruar eshte ne NIVEL DOKTORATURE" & vbCrLf & vbCrLf & _
        "• Modelet stokastike japin realitze financiar" & vbCrLf & vbCrLf & _
        "• Vizualizimet jane PROFESIONALE dhe te detajuara" & vbCrLf & vbCrLf & _
        "• Te dhenat mund te perdoren per:" & vbCrLf & _
        "  - Analiza PySpark" & vbCrLf & _
        "  - Machine Learning Models" & vbCrLf & _
        "  - Risk Management" & vbCrLf & _
        "  - Portfolio Optimization" & vbCrLf & vbCrLf & _
        "• Kerkimi eshte i gatshem per publikim shkencor"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 18
    
    '================================================================================
    ' SLIDE 13: FALEMINDERIT
    '================================================================================
    Set pptSlide = pptPres.Slides.Add(13, ppLayoutTitle)
    pptSlide.Shapes.Title.TextFrame.TextRange.Text = "FALEMINDERIT!"
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Size = 60
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Bold = msoTrue
    pptSlide.Shapes.Title.TextFrame.TextRange.Font.Color.RGB = RGB(46, 134, 171)
    
    pptSlide.Shapes(2).TextFrame.TextRange.Text = "Universiteti i Prishtines" & vbCrLf & _
                                                  "Republika e Kosoves" & vbCrLf & vbCrLf & _
                                                  "Analiza Financiare - Nivel Doktorature" & vbCrLf & _
                                                  "Tetor 2025"
    pptSlide.Shapes(2).TextFrame.TextRange.Font.Size = 24
    
    '================================================================================
    ' PERFUNDIMI
    '================================================================================
    
    ' Ruaj prezantimin
    Dim savePath As String
    savePath = ThisWorkbook.Path & "\PREZANTIMI_DOKTORATURE_" & Format(Now, "YYYYMMDD_HHMMSS") & ".pptx"
    pptPres.SaveAs savePath
    
    MsgBox "PREZANTIMI U GJENERUA ME SUKSES!" & vbCrLf & vbCrLf & _
           "13 SLIDE te krijuara" & vbCrLf & _
           "Lokacioni: " & savePath & vbCrLf & vbCrLf & _
           "HAPI TJETER:" & vbCrLf & _
           "Shto imazhet nga folder-i 'vizualizime_doktorature' ne slides 6-10", _
           vbInformation, "Gjenerues Prezantimi - SUKSES"
    
    ' Pastrimi
    Set pptShape = Nothing
    Set pptSlide = Nothing
    Set pptPres = Nothing
    Set pptApp = Nothing
    
End Sub

'================================================================================
' UDHEZIME PER PERDORIM:
'================================================================================
' 1. Hap Microsoft Excel ose PowerPoint
' 2. Shtyp ALT + F11 per te hapur VBA Editor
' 3. Insert > Module
' 4. Kopjo dhe ngjit kete kod
' 5. Shtyp F5 ose Run > Run Sub/UserForm
' 6. Prit 30-60 sekonda
' 7. Prezantimi do te hapet automatikisht!
' 8. Shto imazhet manualisht ne slides 6-10 nga folder-i "vizualizime_doktorature"
'
' NOTES:
' - Duhet te kesh Microsoft PowerPoint te instaluar
' - Duhet te aktivizosh "Microsoft PowerPoint Object Library" ne Tools > References
' - Folder-i "vizualizime_doktorature" duhet te jete ne te njejtin vend me Excel/PowerPoint file
'================================================================================
