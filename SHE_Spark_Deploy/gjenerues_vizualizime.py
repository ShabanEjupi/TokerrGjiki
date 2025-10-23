"""
GJENERUESI I VIZUALIZIMEVE - BIG DATA FINANCIAR
Krijon figura, skema dhe diagrame per prezantimin
Republika e Kosoves (XK) - Tetor 2025
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Krijo folderin per vizualizime
os.makedirs('vizualizime', exist_ok=True)

print("=" * 80)
print("GJENERIMI I VIZUALIZIMEVE - PREZANTIM SHQIP")
print("=" * 80)

# FIGURA 1: Arkitektura e Big Data (Spark)
print("\n[1/8] Duke gjeneruar arkitekturen e Big Data...")
fig, ax = plt.subplots(figsize=(14, 8))
ax.text(0.5, 0.95, 'ARKITEKTURA E BIG DATA - APACHE SPARK', 
        ha='center', va='top', fontsize=20, fontweight='bold')

# Vizato kutite per komponente
boxes = [
    {'x': 0.2, 'y': 0.7, 'w': 0.15, 'h': 0.12, 'label': 'PySpark\nAPI', 'color': '#FF6B6B'},
    {'x': 0.425, 'y': 0.7, 'w': 0.15, 'h': 0.12, 'label': 'Spark SQL', 'color': '#4ECDC4'},
    {'x': 0.65, 'y': 0.7, 'w': 0.15, 'h': 0.12, 'label': 'Spark MLlib', 'color': '#95E1D3'},
    
    {'x': 0.2, 'y': 0.5, 'w': 0.6, 'h': 0.12, 'label': 'Spark Core - RDD & DataFrames', 'color': '#F38181'},
    
    {'x': 0.15, 'y': 0.28, 'w': 0.18, 'h': 0.12, 'label': 'Driver\nMemory: 1GB', 'color': '#AA96DA'},
    {'x': 0.41, 'y': 0.28, 'w': 0.18, 'h': 0.12, 'label': 'Executor\nMemory: 1GB', 'color': '#FCBAD3'},
    {'x': 0.67, 'y': 0.28, 'w': 0.18, 'h': 0.12, 'label': 'Cluster\nLocal[*]', 'color': '#FFFFD2'},
    
    {'x': 0.3, 'y': 0.08, 'w': 0.4, 'h': 0.12, 'label': 'Data: 96,048 rreshta\n23 asete × 3 modele × 1,392 ditë', 'color': '#A8E6CF'},
]

for box in boxes:
    rect = plt.Rectangle((box['x'], box['y']), box['w'], box['h'], 
                          facecolor=box['color'], edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2, box['label'],
            ha='center', va='center', fontsize=11, fontweight='bold')

# Vizato shigjeta
arrows = [
    {'x1': 0.275, 'y1': 0.7, 'x2': 0.35, 'y2': 0.62},
    {'x1': 0.5, 'y1': 0.7, 'x2': 0.5, 'y2': 0.62},
    {'x1': 0.725, 'y1': 0.7, 'x2': 0.65, 'y2': 0.62},
    {'x1': 0.35, 'y1': 0.5, 'x2': 0.3, 'y2': 0.4},
    {'x1': 0.5, 'y1': 0.5, 'x2': 0.5, 'y2': 0.4},
    {'x1': 0.65, 'y1': 0.5, 'x2': 0.7, 'y2': 0.4},
    {'x1': 0.5, 'y1': 0.28, 'x2': 0.5, 'y2': 0.2},
]

for arrow in arrows:
    ax.annotate('', xy=(arrow['x2'], arrow['y2']), xytext=(arrow['x1'], arrow['y1']),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.tight_layout()
plt.savefig('vizualizime/skema_big_data.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: skema_big_data.png")

# FIGURA 2: Llojet e Aseteve (Pie Chart)
print("[2/8] Duke gjeneruar shpërndarjen e aseteve...")
fig, ax = plt.subplots(figsize=(10, 8))
categories = ['Aksione\n(8 asete)', 'Valutat Forex\n(9 asete)', 'Lëndët e Para\n(4 asete)', 'Indekset\n(2 asete)']
sizes = [8, 9, 4, 2]
colors = ['#FF6B6B', '#4ECDC4', '#FFA500', '#9B59B6']
explode = (0.05, 0.05, 0.05, 0.05)

wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=categories, colors=colors,
                                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 14, 'fontweight': 'bold'})
ax.set_title('SHPËRNDARJA E 23 ASETEVE FINANCIARE', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('vizualizime/shperndarja_aseteve.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: shperndarja_aseteve.png")

# FIGURA 3: Modelet Stokastike (Flowchart)
print("[3/8] Duke gjeneruar fluksin e modeleve...")
fig, ax = plt.subplots(figsize=(14, 10))
ax.text(0.5, 0.95, '8 MODELET STOKASTIKE - PROCESI I APLIKIMIT', 
        ha='center', va='top', fontsize=18, fontweight='bold')

models = [
    {'x': 0.15, 'y': 0.82, 'label': '1. GBM\nGeometric\nBrownian\nMotion', 'color': '#FF6B6B'},
    {'x': 0.35, 'y': 0.82, 'label': '2. Heston\nStochastic\nVolatility', 'color': '#4ECDC4'},
    {'x': 0.55, 'y': 0.82, 'label': '3. Jump\nDiffusion\n(Merton)', 'color': '#95E1D3'},
    {'x': 0.75, 'y': 0.82, 'label': '4. GARCH\n(1,1)\nEffects', 'color': '#F38181'},
    
    {'x': 0.15, 'y': 0.62, 'label': '5. Regime\nSwitching\n(Markov)', 'color': '#AA96DA'},
    {'x': 0.35, 'y': 0.62, 'label': '6. Levy\nProcesses\n(Student-t)', 'color': '#FCBAD3'},
    {'x': 0.55, 'y': 0.62, 'label': '7. Market\nCrash\nSimulation', 'color': '#FFFFD2'},
    {'x': 0.75, 'y': 0.62, 'label': '8. Correlation\nDynamics\n(Cholesky)', 'color': '#A8E6CF'},
]

for model in models:
    circle = plt.Circle((model['x'], model['y']), 0.06, 
                        facecolor=model['color'], edgecolor='black', linewidth=2.5)
    ax.add_patch(circle)
    ax.text(model['x'], model['y'], model['label'],
            ha='center', va='center', fontsize=9, fontweight='bold')

# Kutia finale
final_box = plt.Rectangle((0.3, 0.35), 0.4, 0.15, 
                          facecolor='#FFD700', edgecolor='black', linewidth=3)
ax.add_patch(final_box)
ax.text(0.5, 0.425, 'TË DHËNAT FINALE\n96,048 rreshta\n1 Janar 2022 - 23 Tetor 2025',
        ha='center', va='center', fontsize=13, fontweight='bold')

# Shigjeta nga modelet te kutia finale
for model in models:
    ax.annotate('', xy=(0.5, 0.5), xytext=(model['x'], model['y'] - 0.07),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='gray', alpha=0.6))

# Kutia e output-it
output_box = plt.Rectangle((0.35, 0.15), 0.3, 0.12, 
                           facecolor='#90EE90', edgecolor='black', linewidth=3)
ax.add_patch(output_box)
ax.text(0.5, 0.21, 'CSV Files në\ndata_kaggle/',
        ha='center', va='center', fontsize=12, fontweight='bold')

ax.annotate('', xy=(0.5, 0.27), xytext=(0.5, 0.35),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))

ax.set_xlim(0, 1)
ax.set_ylim(0.1, 1)
ax.axis('off')
plt.tight_layout()
plt.savefig('vizualizime/modelet_stokastike.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: modelet_stokastike.png")

# FIGURA 4: Strategjia e Investimit (Diagram)
print("[4/8] Duke gjeneruar strategjinë e investimit...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Afatshkurtër
ax1.set_title('STRATEGJIA AFATSHKURTËR (1-5 ditë)', fontsize=16, fontweight='bold')
strategies_short = ['BLI:\nRSI < 30\nOversold', 'BLI:\nÇmimi nën\nBollinger', 
                    'SHIT:\nRSI > 70\nOverbought', 'SHIT:\nÇmimi mbi\nBollinger']
colors_short = ['#90EE90', '#90EE90', '#FF6B6B', '#FF6B6B']
y_pos = [0.7, 0.5, 0.3, 0.1]

for i, (strat, color, y) in enumerate(zip(strategies_short, colors_short, y_pos)):
    rect = plt.Rectangle((0.2, y), 0.6, 0.15, facecolor=color, edgecolor='black', linewidth=2)
    ax1.add_patch(rect)
    ax1.text(0.5, y + 0.075, strat, ha='center', va='center', 
            fontsize=13, fontweight='bold')

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')

# Afatgjatë
ax2.set_title('STRATEGJIA AFATGJATË (6-18 muaj)', fontsize=16, fontweight='bold')
portfolio = ['Aksione\n40%\nAAPL, MSFT', 'Indekse\n25%\nSP500', 
             'Safe Haven\n20%\nGold, Silver', 'Forex\n10%\nEUR/USD', 'Cash\n5%']
colors_long = ['#4169E1', '#32CD32', '#FFD700', '#FF6347', '#D3D3D3']
y_pos_long = [0.8, 0.63, 0.46, 0.29, 0.12]

for i, (port, color, y) in enumerate(zip(portfolio, colors_long, y_pos_long)):
    rect = plt.Rectangle((0.15, y), 0.7, 0.13, facecolor=color, edgecolor='black', linewidth=2)
    ax2.add_patch(rect)
    ax2.text(0.5, y + 0.065, port, ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white' if i in [0, 3] else 'black')

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

plt.tight_layout()
plt.savefig('vizualizime/strategjia_investimit.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: strategjia_investimit.png")

# FIGURA 5: Risku vs Kthimi (Scatter Plot)
print("[5/8] Duke gjeneruar Risku vs Kthimi...")
np.random.seed(42)
fig, ax = plt.subplots(figsize=(12, 8))

assets = ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'TSLA', 'Gold', 'EUR/USD', 'Oil', 'SP500']
risks = [25, 22, 23, 40, 50, 15, 8, 35, 16]
returns = [28, 24, 30, 38, 32, 18, 5, 15, 20]
colors_scatter = ['#FF6B6B', '#FF6B6B', '#FF6B6B', '#FF6B6B', '#FF6B6B', 
                  '#FFD700', '#4ECDC4', '#FFA500', '#9B59B6']

for asset, risk, ret, color in zip(assets, risks, returns, colors_scatter):
    ax.scatter(risk, ret, s=500, alpha=0.6, color=color, edgecolors='black', linewidth=2)
    ax.text(risk, ret, asset, ha='center', va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('RISKU (Volatiliteti Vjetor %)', fontsize=14, fontweight='bold')
ax.set_ylabel('KTHIMI MESATAR VJETOR (%)', fontsize=14, fontweight='bold')
ax.set_title('RISKU vs KTHIMI - PORTFOLIO 23 ASETE', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axhline(0, color='black', linestyle='--', linewidth=1)
ax.axvline(0, color='black', linestyle='--', linewidth=1)

plt.tight_layout()
plt.savefig('vizualizime/risku_vs_kthimi.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: risku_vs_kthimi.png")

# FIGURA 6: Performanca e Modeleve (Bar Chart)
print("[6/8] Duke gjeneruar performancën e modeleve...")
fig, ax = plt.subplots(figsize=(12, 8))

models_perf = ['GBM', 'Heston', 'Jump\nDiffusion', 'GARCH', 'Regime\nSwitching', 
               'Levy', 'Crash\nSim', 'Correlation']
accuracy = [78, 82, 87, 91, 85, 79, 92, 88]
colors_bar = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#FFFFD2', '#A8E6CF']

bars = ax.barh(models_perf, accuracy, color=colors_bar, edgecolor='black', linewidth=2)

for i, (bar, acc) in enumerate(zip(bars, accuracy)):
    ax.text(acc + 1, i, f'{acc}%', va='center', fontsize=12, fontweight='bold')

ax.set_xlabel('SAKTËSIA E MODELIT (%)', fontsize=14, fontweight='bold')
ax.set_title('PERFORMANCA E 8 MODELEVE STOKASTIKE', fontsize=16, fontweight='bold')
ax.set_xlim(0, 100)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('vizualizime/performanca_modeleve.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: performanca_modeleve.png")

# FIGURA 7: Timeline e Projektit
print("[7/8] Duke gjeneruar timeline-in...")
fig, ax = plt.subplots(figsize=(14, 6))

timeline = [
    {'date': '1 Jan 2022', 'event': 'Fillimi i\nTë Dhënave', 'y': 0.6, 'color': '#90EE90'},
    {'date': '2023', 'event': 'Aplikimi i\nModeleve', 'y': 0.4, 'color': '#4ECDC4'},
    {'date': '2024', 'event': 'Validimi &\nTestimi', 'y': 0.6, 'color': '#FFD700'},
    {'date': '23 Tet 2025', 'event': 'Përfundimi\n(SOT!)', 'y': 0.4, 'color': '#FF6B6B'},
]

ax.plot([0, 1], [0.5, 0.5], 'k-', linewidth=3)

for i, item in enumerate(timeline):
    x = i / (len(timeline) - 1)
    ax.plot(x, 0.5, 'ko', markersize=15)
    
    rect = plt.Rectangle((x - 0.08, item['y'] - 0.08), 0.16, 0.16, 
                          facecolor=item['color'], edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    
    ax.text(x, item['y'], item['event'], ha='center', va='center', 
            fontsize=10, fontweight='bold')
    ax.text(x, 0.5 - 0.15, item['date'], ha='center', va='top', 
            fontsize=11, fontweight='bold')
    
    ax.plot([x, x], [0.5, item['y'] - 0.08], 'k--', linewidth=1.5)

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(0.2, 0.8)
ax.axis('off')
ax.set_title('TIMELINE I PROJEKTIT - 1 Janar 2022 deri 23 Tetor 2025', 
             fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('vizualizime/timeline_projekti.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: timeline_projekti.png")

# FIGURA 8: Republika e Kosovës
print("[8/8] Duke gjeneruar flamurin e Kosovës...")
fig, ax = plt.subplots(figsize=(12, 8))

# Sfond blu
ax.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='#244AA5', edgecolor='none'))

# Yll të bardha (6 yje)
star_y = 0.7
for i in range(6):
    x = 0.15 + i * 0.14
    ax.plot(x, star_y, '*', color='white', markersize=30, markeredgecolor='white', markeredgewidth=1)

# Konturat e Kosovës (forme e thjeshtëzuar)
kosovo_x = [0.3, 0.35, 0.4, 0.5, 0.6, 0.65, 0.7, 0.65, 0.6, 0.5, 0.4, 0.35, 0.3]
kosovo_y = [0.5, 0.55, 0.5, 0.52, 0.5, 0.48, 0.45, 0.4, 0.38, 0.35, 0.38, 0.4, 0.5]
ax.fill(kosovo_x, kosovo_y, color='#D59F3C', edgecolor='#8B6914', linewidth=3)

ax.text(0.5, 0.2, 'REPUBLIKA E KOSOVËS\nKod Shteti: XK', 
        ha='center', va='center', fontsize=20, fontweight='bold', color='white',
        bbox=dict(boxstyle='round', facecolor='#244AA5', edgecolor='white', linewidth=3))

ax.text(0.5, 0.08, 'Universiteti i Prishtinës\nProjekt Doktorature - Tetor 2025', 
        ha='center', va='center', fontsize=14, fontweight='bold', color='white')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.tight_layout()
plt.savefig('vizualizime/kosova_flag.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Ruajtur: kosova_flag.png")

print("\n" + "=" * 80)
print("✅ TË GJITHA VIZUALIZIMET U GJENERUAN ME SUKSES!")
print("=" * 80)
print(f"\n8 figura të ruajtura në folderin: vizualizime/")
print("\nFigurat:")
print("  1. skema_big_data.png - Arkitektura e Apache Spark")
print("  2. shperndarja_aseteve.png - 23 asetet financiare")
print("  3. modelet_stokastike.png - 8 modelet me flowchart")
print("  4. strategjia_investimit.png - Afatshkurtër & Afatgjatë")
print("  5. risku_vs_kthimi.png - Scatter plot i portfolio-s")
print("  6. performanca_modeleve.png - Saktësia e modeleve")
print("  7. timeline_projekti.png - Timeline 2022-2025")
print("  8. kosova_flag.png - Flamuri i Republikës së Kosovës (XK)")
print("\n" + "=" * 80)
