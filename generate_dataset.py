"""
Gjenerues i Dataset-it Financiar për Analizë Doktorale
Dataset i sofistikuar që përfaqëson të dhëna reale të tregut financiar
"""

def generate_financial_dataset():
    """
    Krijon një dataset financiar të detajuar me modele reale të tregut
    """
    import math
    import random
    from datetime import datetime, timedelta
    import os
    
    print("="*80)
    print("GJENERIMI I DATASET-IT FINANCIAR PËR ANALIZË DOKTORALE")
    print("="*80)
    
    # Parametrat
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 10, 22)
    
    # Krijimi i datave (vetëm ditë pune)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        # Përjashto fundjavat (Saturday=5, Sunday=6)
        if current_date.weekday() < 5:
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    print(f"✓ {len(dates)} ditë tregtare të gjeneruara")
    
    # Parametrat e tregut
    initial_price = 2000.00
    annual_drift = 0.08  # 8% rritje vjetore
    annual_volatility = 0.25  # 25% volatilitet vjetor
    
    # Konvertimi në parametra ditore
    daily_drift = annual_drift / 252
    daily_volatility = annual_volatility / math.sqrt(252)
    
    # Parametrat e volumit
    base_volume = 3_500_000_000
    
    # Seed për riprodhueshmëri
    random.seed(42)
    
    # Gjenerimi i çmimeve me Geometric Brownian Motion
    prices = [initial_price]
    
    for i in range(1, len(dates)):
        # Random walk me drift dhe volatilitet
        random_shock = random.gauss(0, 1)
        daily_return = daily_drift + daily_volatility * random_shock
        
        # Çmimi i ri
        new_price = prices[-1] * math.exp(daily_return)
        prices.append(new_price)
    
    print(f"✓ Çmimet u gjeneruan me Geometric Brownian Motion")
    
    # Krijimi i file CSV
    os.makedirs('data_kaggle', exist_ok=True)
    csv_path = 'data_kaggle/financial_data.csv'
    
    with open(csv_path, 'w', encoding='utf-8') as f:
        # Header
        f.write('Date,Open,High,Low,Close,Volume\n')
        
        # Të dhënat
        for i, date in enumerate(dates):
            close_price = prices[i]
            
            # Gjenerimi i Open (çmimi i hapjes)
            open_variation = random.gauss(0, daily_volatility * 0.3)
            open_price = close_price * (1 + open_variation)
            
            # Gjenerimi i High dhe Low
            high_low_range = abs(random.gauss(0, daily_volatility * 0.5))
            high_price = max(open_price, close_price) * (1 + high_low_range)
            low_price = min(open_price, close_price) * (1 - high_low_range)
            
            # Gjenerimi i Volume (më i lartë në ditë me volatilitet të lartë)
            if i > 0:
                price_change = abs((close_price - prices[i-1]) / prices[i-1])
                volume_multiplier = 1 + price_change * 10
            else:
                volume_multiplier = 1
            
            volume = int(base_volume * volume_multiplier * (1 + random.gauss(0, 0.3)))
            volume = max(volume, 1_000_000)  # Minimum volume
            
            # Shkruaj në CSV
            f.write(f"{date.strftime('%Y-%m-%d')},{open_price:.2f},{high_price:.2f},"
                   f"{low_price:.2f},{close_price:.2f},{volume}\n")
    
    print(f"✓ Dataset-i u ruajt në: {csv_path}")
    print(f"✓ Çmimi fillimisht: ${prices[0]:,.2f}")
    print(f"✓ Çmimi në fund: ${prices[-1]:,.2f}")
    
    total_return = ((prices[-1] - prices[0]) / prices[0]) * 100
    print(f"✓ Return total: {total_return:.2f}%")
    
    # Llogaritja e statistikave
    returns = []
    for i in range(1, len(prices)):
        ret = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(ret)
    
    avg_return = sum(returns) / len(returns)
    
    # Devijimi standard
    variance = sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance)
    
    print(f"✓ Rendimenti ditor mesatar: {avg_return:.4f}%")
    print(f"✓ Volatiliteti ditor: {std_dev:.4f}%")
    print(f"✓ Volatiliteti vjetor: {std_dev * math.sqrt(252):.2f}%")
    
    print("\n" + "="*80)
    print("✓✓✓ DATASET-I U KRIJUA ME SUKSES ✓✓✓")
    print("="*80)
    print("\nTani mund të ekzekutoni:")
    print("  python analiza_financiare_advanced.py")
    print("="*80)
    
    return csv_path

if __name__ == "__main__":
    generate_financial_dataset()
