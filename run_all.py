"""
SKRIPTI I PLOTË PËR EKZEKUTIM - RUN ALL
========================================

Ky skript ekzekuton të gjithë pipeline-in e projektit doktoral:
1. Kontrollon instalimin e dependency-ve
2. Gjeneron dataset-in financiar
3. Ekzekuton analizën e plotë
4. Raporton rezultatet

Përdorimi:
  python run_all.py
"""

import subprocess
import sys
import os

def print_header(text):
    """Printon header të formatuar"""
    print("\n" + "="*80)
    print(text)
    print("="*80 + "\n")

def check_dependencies():
    """Kontrollon nëse të gjitha libraritë janë të instaluara"""
    print_header("HAPI 1: KONTROLLIMI I DEPENDENCY-VE")
    
    required_packages = [
        'pyspark',
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} është i instaluar")
        except ImportError:
            print(f"✗ {package} mungon")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Libraritë e mëposhtme mungojnë: {', '.join(missing_packages)}")
        print("\nPo i instalojmë automatikisht...")
        
        for package in missing_packages:
            print(f"\nDuke instaluar {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} u instalua me sukses")
            except subprocess.CalledProcessError:
                print(f"✗ Gabim gjatë instalimit të {package}")
                return False
    
    print("\n✓✓✓ Të gjitha dependency-të janë gati!")
    return True

def generate_dataset():
    """Gjeneron dataset-in financiar"""
    print_header("HAPI 2: GJENERIMI I DATASET-IT FINANCIAR")
    
    if os.path.exists('data_kaggle/financial_data.csv'):
        print("⚠️  Dataset-i ekziston tashmë.")
        response = input("Dëshironi ta ri-gjeneroni? (y/n): ")
        if response.lower() != 'y':
            print("✓ Duke përdorur dataset-in ekzistues")
            return True
    
    print("Duke gjeneruar dataset-in e ri...")
    try:
        subprocess.check_call([sys.executable, "generate_dataset.py"])
        print("\n✓✓✓ Dataset-i u gjenerua me sukses!")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Gabim gjatë gjenerimit të dataset-it")
        return False
    except FileNotFoundError:
        print("\n✗ File 'generate_dataset.py' nuk u gjet")
        return False

def run_analysis():
    """Ekzekuton analizën kryesore"""
    print_header("HAPI 3: EKZEKUTIMI I ANALIZËS SË AVANCUAR")
    
    print("Duke filluar analizën financiare të avancuar...")
    print("Kjo mund të marrë disa minuta...\n")
    
    try:
        subprocess.check_call([sys.executable, "analiza_financiare_advanced.py"])
        print("\n✓✓✓ Analiza u përfundua me sukses!")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Gabim gjatë ekzekutimit të analizës")
        return False
    except FileNotFoundError:
        print("\n✗ File 'analiza_financiare_advanced.py' nuk u gjet")
        return False

def show_results():
    """Shfaq rezultatet e gjeneruara"""
    print_header("REZULTATET")
    
    print("📁 OUTPUTET CSV:")
    csv_dir = 'rezultatet_doktorature'
    if os.path.exists(csv_dir):
        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
        for i, f in enumerate(csv_files, 1):
            file_path = os.path.join(csv_dir, f)
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"  {i}. {f} ({size:.1f} KB)")
    else:
        print("  ⚠️  Direktoria 'rezultatet_doktorature' nuk u krijua")
    
    print("\n📊 VIZUALIZIMET:")
    viz_dir = 'vizualizime_doktorature'
    if os.path.exists(viz_dir):
        png_files = [f for f in os.listdir(viz_dir) if f.endswith('.png')]
        for i, f in enumerate(png_files, 1):
            file_path = os.path.join(viz_dir, f)
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"  {i}. {f} ({size:.1f} KB)")
    else:
        print("  ⚠️  Direktoria 'vizualizime_doktorature' nuk u krijua")

def main():
    """Funksioni kryesor"""
    print("="*80)
    print("PROJEKTI DOKTORATURË: ANALIZA E AVANCUAR FINANCIARE")
    print("Universiteti i Prishtinës, Republika e Kosovës")
    print("="*80)
    
    # Hapi 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Instalimi i dependency-ve dështoi. Ju lutem instaloni manualisht:")
        print("   python -m pip install pyspark pandas matplotlib seaborn numpy")
        return
    
    # Hapi 2: Generate dataset
    if not generate_dataset():
        print("\n❌ Gjenerimi i dataset-it dështoi.")
        print("Ju lutem shkarkoni një dataset financiar CSV dhe vendoseni në:")
        print("   data_kaggle/financial_data.csv")
        return
    
    # Hapi 3: Run analysis
    if not run_analysis():
        print("\n❌ Analiza dështoi. Kontrolloni mesazhet e gabimit më lart.")
        return
    
    # Hapi 4: Show results
    show_results()
    
    # Success message
    print_header("✓✓✓ PROJEKTI U EKZEKUTUA ME SUKSES ✓✓✓")
    print("Të gjitha rezultatet janë gati!")
    print("\nHapat e ardhshëm:")
    print("  1. Shikoni CSV files në: rezultatet_doktorature/")
    print("  2. Shikoni figurat në: vizualizime_doktorature/")
    print("  3. Lexoni dokumentimin në: README_SHQIP.md")
    print("\n" + "="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Procesi u ndërpre nga përdoruesi.")
    except Exception as e:
        print(f"\n❌ Gabim i papritur: {str(e)}")
        import traceback
        traceback.print_exc()
