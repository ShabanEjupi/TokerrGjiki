# ================================================================================
# EKZEKUTUES POWERSHELL - PROJEKTI DOKTORAL
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "PROJEKTI DOKTORATURE - ANALIZA FINANCIARE E AVANCUAR" -ForegroundColor Yellow
Write-Host "Universiteti i Prishtines, Republika e Kosoves" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Funksioni per te gjetur Python
function Find-Python {
    $pythonPaths = @(
        "py",
        "python",
        "python3",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python310\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
    )
    
    foreach ($pythonPath in $pythonPaths) {
        try {
            $null = & $pythonPath --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                return $pythonPath
            }
        } catch {
            continue
        }
    }
    
    return $null
}

# Kerko Python
Write-Host "[1/5] Duke kerkuar Python..." -ForegroundColor Cyan
$python = Find-Python

if ($null -eq $python) {
    Write-Host ""
    Write-Host "[GABIM] Python nuk u gjet!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Shkarkoni Python nga: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Gjate instalimit zgjidhni: 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Shtypni Enter per te mbyllur"
    exit 1
}

Write-Host "[OK] Python u gjet: $python" -ForegroundColor Green

# Instalo librariite
Write-Host ""
Write-Host "[2/5] Duke instaluar/verifikuar librariite..." -ForegroundColor Cyan
& $python -m pip install --upgrade pip --quiet 2>$null
& $python -m pip install pyspark pandas matplotlib seaborn numpy openpyxl python-pptx Pillow --quiet 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Librariite jane gati" -ForegroundColor Green
} else {
    Write-Host "[INFO] Duke instaluar librariite..." -ForegroundColor Yellow
    & $python -m pip install pyspark pandas matplotlib seaborn numpy openpyxl python-pptx Pillow
}

# Gjenerimi i dataset-it
Write-Host ""
Write-Host "[3/5] Duke gjeneruar dataset-in financiar te sofistikuar..." -ForegroundColor Cyan
& $python gjenerues_dataset_financiar.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[GABIM] Gjenerimi i dataset-it deshtoi" -ForegroundColor Red
    Read-Host "Shtypni Enter per te mbyllur"
    exit 1
}

# Ekzekutimi i analizes
Write-Host ""
Write-Host "[4/5] Duke ekzekutuar analizen e avancuar financiare..." -ForegroundColor Cyan
& $python analiza_financiare_advanced.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[GABIM] Analiza deshtoi" -ForegroundColor Red
    Read-Host "Shtypni Enter per te mbyllur"
    exit 1
}

# Gjenerimi i PowerPoint
Write-Host ""
Write-Host "[5/5] Duke gjeneruar prezantimin PowerPoint..." -ForegroundColor Cyan
& $python gjenerues_powerpoint.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[KUJDES] Gjenerimi i PowerPoint deshtoi, por analiza u krye me sukses" -ForegroundColor Yellow
}

# Sukses
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "PROJEKTI U EKZEKUTUA ME SUKSES!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Rezultatet:" -ForegroundColor Yellow
Write-Host "  - rezultatet_doktorature/     5 CSV files me analiza" -ForegroundColor White
Write-Host "  - vizualizime_doktorature/    12+ figura profesionale" -ForegroundColor White
Write-Host "  - prezantimi_powerpoint/      Prezantimi PowerPoint automatik" -ForegroundColor White
Write-Host ""
Read-Host "Shtypni Enter per te mbyllur"
