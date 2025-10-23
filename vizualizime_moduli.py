"""
═══════════════════════════════════════════════════════════════════════════════
MODUL PËR VIZUALIZIME TË AVANCUARA - 12+ FIGURA PROFESIONALE
═══════════════════════════════════════════════════════════════════════════════

Krijon vizualizime të sofistikuara për analizë doktorale:
1. Time Series Comprehensive
2. Returns Distribution (3D)
3. Volatility Analysis
4. Correlation Heatmap
5. Portfolio Performance
6. Volume Analysis  
7. Candlestick Charts
8. Statistical Distributions
9. 3D Surface Plot
10. Risk-Return Scatter
11. Cumulative Returns
12. Drawdown Analysis

Plus vizualizime extra me Plotly për interaktivitet
═══════════════════════════════════════════════════════════════════════════════
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime
from matplotlib.patches import Rectangle
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

# Konfigurimi global
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['figure.figsize'] = (16, 10)

class VizualizimeDoktorale:
    """Klasa për krijimin e vizualizimeve profesionale"""
    
    def __init__(self, output_dir='vizualizime_doktorature'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Direktoria e vizualizimeve: {output_dir}")
    
    def viz_01_time_series_comprehensive(self, df_pandas):
        """FIGURA 1: Time Series me Moving Averages dhe Returns"""
        fig = plt.figure(figsize=(20, 14))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.25)
        
        # Sort by date
        df = df_pandas.sort_values('Date')
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Plot 1: Price dhe Moving Averages
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(df['Date'], df['Close'], label='Çmimi Aktual', linewidth=2, alpha=0.7, color='#1f77b4')
        ax1.plot(df['Date'], df['MA_7d'], label='MA 7-ditore', linewidth=2, color='#ff7f0e')
        ax1.plot(df['Date'], df['MA_30d'], label='MA 30-ditore', linewidth=2, color='#2ca02c')
        ax1.plot(df['Date'], df['MA_90d'], label='MA 90-ditore', linewidth=2, color='#d62728')
        ax1.set_title('TIME SERIES: Çmimi dhe Mesataret Lëvizëse', fontsize=18, fontweight='bold', pad=20)
        ax1.set_xlabel('Data', fontsize=14)
        ax1.set_ylabel('Çmimi ($)', fontsize=14)
        ax1.legend(fontsize=12, loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Daily Returns
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(df['Date'], df['Daily_Return'], linewidth=1, alpha=0.6, color='darkblue')
        ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)
        ax2.fill_between(df['Date'], df['Daily_Return'], 0, where=(df['Daily_Return'] > 0), 
                         alpha=0.3, color='green', label='Pozitiv')
        ax2.fill_between(df['Date'], df['Daily_Return'], 0, where=(df['Daily_Return'] < 0), 
                         alpha=0.3, color='red', label='Negativ')
        ax2.set_title('Rendimentet Ditore (%)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Data', fontsize=12)
        ax2.set_ylabel('Rendimenti (%)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Returns Histogram
        ax3 = fig.add_subplot(gs[1, 1])
        returns_clean = df['Daily_Return'].dropna()
        n, bins, patches = ax3.hist(returns_clean, bins=100, edgecolor='black', alpha=0.7, color='steelblue')
        ax3.axvline(returns_clean.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {returns_clean.mean():.4f}%')
        ax3.axvline(returns_clean.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {returns_clean.median():.4f}%')
        ax3.set_title('Shpërndarja e Rendimenteve Ditore', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Rendimenti Ditor (%)', fontsize=12)
        ax3.set_ylabel('Frekuenca', fontsize=12)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Volume
        ax4 = fig.add_subplot(gs[2, :])
        ax4.bar(df['Date'], df['Volume'], alpha=0.6, color='steelblue', width=2)
        ax4.set_title('Volumet e Tregtimit', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Data', fontsize=12)
        ax4.set_ylabel('Volume', fontsize=12)
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('ANALIZA E SERIVE KOHORE - COMPREHENSIVE VIEW', 
                     fontsize=22, fontweight='bold', y=0.995)
        
        output_path = os.path.join(self.output_dir, '01_time_series_comprehensive.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 1: {output_path}")
    
    def viz_02_returns_distribution_3d(self, df_pandas):
        """FIGURA 2: Returns Distribution në 3D"""
        fig = plt.figure(figsize=(20, 12))
        
        # Prepare data
        df = df_pandas.dropna(subset=['Daily_Return', 'Weekly_Return', 'Monthly_Return'])
        
        # Create 3D scatter
        ax = fig.add_subplot(121, projection='3d')
        scatter = ax.scatter(df['Daily_Return'], df['Weekly_Return'], df['Monthly_Return'],
                            c=df['Volume'], cmap='viridis', s=10, alpha=0.6)
        ax.set_xlabel('Daily Return (%)', fontsize=12)
        ax.set_ylabel('Weekly Return (%)', fontsize=12)
        ax.set_zlabel('Monthly Return (%)', fontsize=12)
        ax.set_title('3D: Rendimentet (Daily, Weekly, Monthly)', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax, label='Volume', shrink=0.5)
        
        # 2D Heatmap
        ax2 = fig.add_subplot(122)
        returns_data = df[['Daily_Return', 'Weekly_Return', 'Monthly_Return']].corr()
        sns.heatmap(returns_data, annot=True, fmt='.4f', cmap='coolwarm', center=0,
                    square=True, linewidths=2, cbar_kws={"shrink": 0.8}, ax=ax2,
                    vmin=-1, vmax=1)
        ax2.set_title('Correlation Matrix: Rendimentet', fontsize=14, fontweight='bold')
        
        plt.suptitle('ANALIZA E RENDIMENTEVE - 3D DHE CORRELATION', 
                     fontsize=20, fontweight='bold')
        
        output_path = os.path.join(self.output_dir, '02_returns_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 2: {output_path}")
    
    def viz_03_volatility_analysis(self, df_pandas):
        """FIGURA 3: Volatility Analysis (Historical dhe Rolling)"""
        fig, axes = plt.subplots(3, 1, figsize=(20, 14))
        
        df = df_pandas.sort_values('Date')
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Rolling Volatility
        ax1 = axes[0]
        ax1.plot(df['Date'], df['Rolling_Volatility_30d'], linewidth=2, color='darkred', label='Rolling Volatility (30d)')
        ax1.fill_between(df['Date'], df['Rolling_Volatility_30d'], alpha=0.3, color='red')
        ax1.set_title('ROLLING VOLATILITY (30-ditore)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Volatiliteti (%)', fontsize=12)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Volatility vs Returns
        ax2 = axes[1]
        scatter = ax2.scatter(df['Daily_Return'], df['Rolling_Volatility_30d'], 
                             c=df['Volume'], cmap='plasma', s=20, alpha=0.6)
        ax2.set_title('VOLATILITY vs RETURNS', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Daily Return (%)', fontsize=12)
        ax2.set_ylabel('Rolling Volatility (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label='Volume')
        
        # Distribution of Volatility
        ax3 = axes[2]
        vol_clean = df['Rolling_Volatility_30d'].dropna()
        ax3.hist(vol_clean, bins=50, edgecolor='black', alpha=0.7, color='darkred')
        ax3.axvline(vol_clean.mean(), color='blue', linestyle='--', linewidth=2, 
                   label=f'Mean: {vol_clean.mean():.4f}%')
        ax3.axvline(vol_clean.median(), color='green', linestyle='--', linewidth=2,
                   label=f'Median: {vol_clean.median():.4f}%')
        ax3.set_title('SHPËRNDARJA E VOLATILITETIT', fontsize=16, fontweight='bold')
        ax3.set_xlabel('Volatiliteti (%)', fontsize=12)
        ax3.set_ylabel('Frekuenca', fontsize=12)
        ax3.legend(fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        plt.suptitle('ANALIZA E VOLATILITETIT - RISK MEASUREMENT', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '03_volatility_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 3: {output_path}")
    
    def viz_04_correlation_heatmap(self, df_pandas):
        """FIGURA 4: Correlation Heatmap për të gjitha features"""
        fig, ax = plt.subplots(figsize=(16, 14))
        
        # Select numeric columns
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 
                       'Daily_Return', 'Weekly_Return', 'Monthly_Return',
                       'MA_7d', 'MA_30d', 'MA_90d', 'Rolling_Volatility_30d']
        
        available_cols = [col for col in numeric_cols if col in df_pandas.columns]
        correlation_matrix = df_pandas[available_cols].corr()
        
        # Create heatmap
        sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='RdYlGn', center=0,
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax,
                    vmin=-1, vmax=1, annot_kws={'size': 9})
        
        ax.set_title('CORRELATION MATRIX - TË GJITHA FEATURES', 
                    fontsize=18, fontweight='bold', pad=20)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, '04_correlation_heatmap.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 4: {output_path}")
    
    def viz_05_portfolio_performance(self, df_pandas):
        """FIGURA 5: Portfolio Performance Over Time"""
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        
        df = df_pandas.sort_values('Date')
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Cumulative Returns
        df['Cumulative_Return'] = (1 + df['Daily_Return']/100).cumprod() - 1
        
        ax1 = axes[0, 0]
        ax1.plot(df['Date'], df['Cumulative_Return'] * 100, linewidth=2, color='green')
        ax1.fill_between(df['Date'], df['Cumulative_Return'] * 100, alpha=0.3, color='green')
        ax1.set_title('CUMULATIVE RETURNS', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Return (%)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Drawdown
        df['Running_Max'] = df['Close'].expanding().max()
        df['Drawdown'] = (df['Close'] - df['Running_Max']) / df['Running_Max'] * 100
        
        ax2 = axes[0, 1]
        ax2.fill_between(df['Date'], df['Drawdown'], alpha=0.5, color='red')
        ax2.set_title('DRAWDOWN ANALYSIS', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Drawdown (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Monthly Returns Heatmap (by year and month)
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        monthly_returns = df.groupby(['Year', 'Month'])['Daily_Return'].mean().unstack()
        
        ax3 = axes[1, :]
        sns.heatmap(monthly_returns, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
                    ax=ax3, cbar_kws={"label": "Avg Daily Return (%)"})
        ax3.set_title('MONTHLY RETURNS HEATMAP', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Muaji', fontsize=12)
        ax3.set_ylabel('Viti', fontsize=12)
        
        plt.suptitle('PORTFOLIO PERFORMANCE ANALYSIS', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '05_portfolio_performance.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 5: {output_path}")
    
    def viz_06_volume_analysis(self, df_pandas):
        """FIGURA 6: Volume Analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        
        df = df_pandas.sort_values('Date')
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Volume over time
        ax1 = axes[0, :]
        ax1.bar(df['Date'], df['Volume'], alpha=0.7, color='steelblue', width=1)
        ax1.set_title('TRADING VOLUME OVER TIME', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Volume', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Volume vs Price Change
        df['Price_Change'] = df['Close'].pct_change() * 100
        
        ax2 = axes[1, 0]
        scatter = ax2.scatter(df['Price_Change'], df['Volume'], alpha=0.5, s=20)
        ax2.set_title('VOLUME vs PRICE CHANGE', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Price Change (%)', fontsize=12)
        ax2.set_ylabel('Volume', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Volume Distribution
        ax3 = axes[1, 1]
        ax3.hist(df['Volume'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax3.axvline(df['Volume'].mean(), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {df["Volume"].mean():,.0f}')
        ax3.set_title('VOLUME DISTRIBUTION', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Volume', fontsize=12)
        ax3.set_ylabel('Frekuenca', fontsize=12)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        plt.suptitle('ANALIZA E VOLUMIT TË TREGTIMIT', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '06_volume_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 6: {output_path}")
    
    def viz_07_candlestick_analysis(self, df_pandas):
        """FIGURA 7: Candlestick Charts (OHLC)"""
        fig, axes = plt.subplots(2, 1, figsize=(20, 12))
        
        df = df_pandas.sort_values('Date').tail(100).copy()  # Last 100 days
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date_num'] = mdates.date2num(df['Date'])
        
        # Candlestick chart
        ax1 = axes[0]
        
        for idx, row in df.iterrows():
            color = 'green' if row['Close'] >= row['Open'] else 'red'
            # Body
            ax1.add_patch(Rectangle((row['Date_num'] - 0.3, min(row['Open'], row['Close'])),
                                    0.6, abs(row['Close'] - row['Open']),
                                    facecolor=color, edgecolor='black', alpha=0.8))
            # Wick
            ax1.plot([row['Date_num'], row['Date_num']], 
                    [row['Low'], row['High']], 
                    color='black', linewidth=1)
        
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        ax1.set_title('CANDLESTICK CHART (100 ditët e fundit)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Çmimi ($)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # OHLC Line Chart
        ax2 = axes[1]
        ax2.plot(df['Date'], df['High'], label='High', linewidth=2, color='green', alpha=0.7)
        ax2.plot(df['Date'], df['Low'], label='Low', linewidth=2, color='red', alpha=0.7)
        ax2.plot(df['Date'], df['Open'], label='Open', linewidth=1.5, color='blue', alpha=0.7, linestyle='--')
        ax2.plot(df['Date'], df['Close'], label='Close', linewidth=2, color='black')
        ax2.fill_between(df['Date'], df['High'], df['Low'], alpha=0.2, color='gray')
        ax2.set_title('OHLC LINE CHART', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Çmimi ($)', fontsize=12)
        ax2.set_xlabel('Data', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        plt.suptitle('CANDLESTICK DHE OHLC ANALYSIS', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '07_candlestick_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 7: {output_path}")
    
    def viz_08_statistical_distributions(self, df_pandas):
        """FIGURA 8: Statistical Distributions (Box Plots, Violin Plots)"""
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        
        # Box plots
        columns_to_plot = [
            ('Close', 'Çmimi Mbylljes'),
            ('Daily_Return', 'Rendimenti Ditor'),
            ('Rolling_Volatility_30d', 'Volatiliteti 30d')
        ]
        
        for idx, (col, title) in enumerate(columns_to_plot):
            if col in df_pandas.columns:
                # Box plot
                ax1 = axes[0, idx]
                data_clean = df_pandas[col].dropna()
                bp = ax1.boxplot([data_clean], labels=[title], patch_artist=True)
                bp['boxes'][0].set_facecolor('lightblue')
                ax1.set_title(f'BOX PLOT: {title}', fontsize=12, fontweight='bold')
                ax1.grid(True, alpha=0.3)
                
                # Violin plot
                ax2 = axes[1, idx]
                parts = ax2.violinplot([data_clean], positions=[1], showmeans=True, showmedians=True)
                ax2.set_title(f'VIOLIN PLOT: {title}', fontsize=12, fontweight='bold')
                ax2.set_xticks([1])
                ax2.set_xticklabels([title])
                ax2.grid(True, alpha=0.3)
        
        plt.suptitle('STATISTICAL DISTRIBUTIONS - BOX & VIOLIN PLOTS', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '08_statistical_distributions.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 8: {output_path}")
    
    def viz_09_3d_surface_plot(self, df_pandas):
        """FIGURA 9: 3D Surface Plot (Price vs Volume vs Time)"""
        fig = plt.figure(figsize=(20, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        df = df_pandas.sort_values('Date').tail(200).copy()  # Last 200 days
        df['Date'] = pd.to_datetime(df['Date'])
        df['Days'] = (df['Date'] - df['Date'].min()).dt.days
        
        # Create meshgrid
        x = df['Days'].values
        y = df['Volume'].values
        z = df['Close'].values
        
        # Scatter plot
        scatter = ax.scatter(x, y, z, c=df['Daily_Return'], cmap='RdYlGn', 
                            s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel('Ditë (nga fillimi)', fontsize=12)
        ax.set_ylabel('Volume', fontsize=12)
        ax.set_zlabel('Çmimi ($)', fontsize=12)
        ax.set_title('3D SURFACE: Çmimi vs Volume vs Koha', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('Daily Return (%)', fontsize=12)
        
        # Rotate for better view
        ax.view_init(elev=20, azim=45)
        
        output_path = os.path.join(self.output_dir, '09_3d_surface_plot.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 9: {output_path}")
    
    def viz_10_risk_return_scatter(self, df_pandas):
        """FIGURA 10: Risk-Return Scatter Plot"""
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        
        df = df_pandas.copy()
        df['Year'] = pd.to_datetime(df['Date']).dt.year
        
        # Calculate annual metrics
        annual_stats = df.groupby('Year').agg({
            'Daily_Return': ['mean', 'std'],
            'Close': 'last'
        }).reset_index()
        
        annual_stats.columns = ['Year', 'Avg_Return', 'Volatility', 'End_Price']
        annual_stats['Sharpe_Ratio'] = annual_stats['Avg_Return'] / annual_stats['Volatility']
        
        # Risk-Return Scatter
        ax1 = axes[0]
        scatter = ax1.scatter(annual_stats['Volatility'], annual_stats['Avg_Return'],
                             s=annual_stats['End_Price'], c=annual_stats['Year'],
                             cmap='viridis', alpha=0.6, edgecolors='black', linewidth=2)
        
        for idx, row in annual_stats.iterrows():
            ax1.annotate(int(row['Year']), 
                        (row['Volatility'], row['Avg_Return']),
                        fontsize=10, ha='center')
        
        ax1.set_xlabel('Risk (Volatility %)', fontsize=14)
        ax1.set_ylabel('Return (Avg Daily %)', fontsize=14)
        ax1.set_title('RISK-RETURN ANALYSIS (Vjetore)', fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='red', linestyle='--', linewidth=1)
        ax1.axvline(x=0, color='red', linestyle='--', linewidth=1)
        
        plt.colorbar(scatter, ax=ax1, label='Viti')
        
        # Sharpe Ratio bar chart
        ax2 = axes[1]
        colors = ['green' if x > 0 else 'red' for x in annual_stats['Sharpe_Ratio']]
        ax2.bar(annual_stats['Year'].astype(str), annual_stats['Sharpe_Ratio'],
                color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_title('SHARPE RATIO (Vjetore)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Viti', fontsize=14)
        ax2.set_ylabel('Sharpe Ratio', fontsize=14)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=2)
        ax2.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)
        
        plt.suptitle('RISK-RETURN DHE SHARPE RATIO ANALYSIS', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '10_risk_return_scatter.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 10: {output_path}")
    
    def viz_11_cumulative_returns(self, df_pandas):
        """FIGURA 11: Cumulative Returns Analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        
        df = df_pandas.sort_values('Date').copy()
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Cumulative returns
        df['Cum_Return_Daily'] = (1 + df['Daily_Return']/100).cumprod()
        df['Cum_Return_Weekly'] = (1 + df['Weekly_Return']/100).fillna(0).cumprod()
        df['Cum_Return_Monthly'] = (1 + df['Monthly_Return']/100).fillna(0).cumprod()
        
        # Plot 1: All cumulative returns
        ax1 = axes[0, 0]
        ax1.plot(df['Date'], df['Cum_Return_Daily'], label='Daily', linewidth=2)
        ax1.plot(df['Date'], df['Cum_Return_Weekly'], label='Weekly', linewidth=2)
        ax1.plot(df['Date'], df['Cum_Return_Monthly'], label='Monthly', linewidth=2)
        ax1.set_title('CUMULATIVE RETURNS (Normalized)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Cumulative Factor', fontsize=12)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Log returns
        ax2 = axes[0, 1]
        ax2.plot(df['Date'], np.log(df['Cum_Return_Daily']), linewidth=2, color='darkgreen')
        ax2.set_title('LOG CUMULATIVE RETURNS', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Log(Cumulative Return)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Year-over-Year comparison
        df['Year'] = df['Date'].dt.year
        yearly_returns = df.groupby('Year')['Daily_Return'].sum()
        
        ax3 = axes[1, 0]
        colors = ['green' if x > 0 else 'red' for x in yearly_returns]
        ax3.bar(yearly_returns.index.astype(str), yearly_returns.values,
                color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_title('YEAR-OVER-YEAR RETURNS', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Total Return (%)', fontsize=12)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=2)
        ax3.grid(True, alpha=0.3, axis='y')
        plt.sca(ax3)
        plt.xticks(rotation=45)
        
        # Plot 4: Rolling 1-Year returns
        ax4 = axes[1, 1]
        df['Rolling_1Y_Return'] = df['Daily_Return'].rolling(window=252).sum()
        ax4.plot(df['Date'], df['Rolling_1Y_Return'], linewidth=2, color='purple')
        ax4.axhline(y=0, color='red', linestyle='--', linewidth=2)
        ax4.fill_between(df['Date'], df['Rolling_1Y_Return'], 0,
                        where=(df['Rolling_1Y_Return'] > 0), alpha=0.3, color='green')
        ax4.fill_between(df['Date'], df['Rolling_1Y_Return'], 0,
                        where=(df['Rolling_1Y_Return'] < 0), alpha=0.3, color='red')
        ax4.set_title('ROLLING 1-YEAR RETURNS', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Return (%)', fontsize=12)
        ax4.set_xlabel('Data', fontsize=12)
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('CUMULATIVE RETURNS ANALYSIS', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '11_cumulative_returns.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 11: {output_path}")
    
    def viz_12_drawdown_analysis(self, df_pandas):
        """FIGURA 12: Drawdown Analysis"""
        fig, axes = plt.subplots(3, 1, figsize=(20, 14))
        
        df = df_pandas.sort_values('Date').copy()
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Calculate drawdown
        df['Running_Max'] = df['Close'].expanding().max()
        df['Drawdown'] = (df['Close'] - df['Running_Max']) / df['Running_Max'] * 100
        df['Drawdown_Duration'] = (df['Drawdown'] < 0).astype(int)
        
        # Plot 1: Price dhe Running Max
        ax1 = axes[0]
        ax1.plot(df['Date'], df['Close'], label='Çmimi Aktual', linewidth=2, color='blue')
        ax1.plot(df['Date'], df['Running_Max'], label='All-Time High', linewidth=2, 
                color='green', linestyle='--', alpha=0.7)
        ax1.fill_between(df['Date'], df['Close'], df['Running_Max'], alpha=0.2, color='red')
        ax1.set_title('ÇMIMI DHE ALL-TIME HIGH', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Çmimi ($)', fontsize=12)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Drawdown
        ax2 = axes[1]
        ax2.fill_between(df['Date'], df['Drawdown'], 0, alpha=0.5, color='red')
        ax2.plot(df['Date'], df['Drawdown'], linewidth=1, color='darkred')
        ax2.set_title('DRAWDOWN (%)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Drawdown (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Annotate max drawdown
        max_dd_idx = df['Drawdown'].idxmin()
        max_dd_value = df.loc[max_dd_idx, 'Drawdown']
        max_dd_date = df.loc[max_dd_idx, 'Date']
        ax2.annotate(f'Max DD: {max_dd_value:.2f}%',
                    xy=(max_dd_date, max_dd_value),
                    xytext=(max_dd_date, max_dd_value - 5),
                    arrowprops=dict(arrowstyle='->', color='black', lw=2),
                    fontsize=12, fontweight='bold')
        
        # Plot 3: Underwater chart
        ax3 = axes[2]
        ax3.bar(df['Date'], df['Drawdown'], color='red', alpha=0.6, width=2)
        ax3.set_title('UNDERWATER CHART', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_xlabel('Data', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        plt.suptitle('DRAWDOWN ANALYSIS - RISK ASSESSMENT', 
                     fontsize=20, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, '12_drawdown_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Figura 12: {output_path}")
    
    def generate_all_visualizations(self, df_pandas):
        """Gjeneron të gjitha 12+ vizualizimet"""
        print("\n" + "="*80)
        print("GJENERIMI I 12+ VIZUALIZIMEVE TË AVANCUARA")
        print("="*80 + "\n")
        
        try:
            self.viz_01_time_series_comprehensive(df_pandas)
            self.viz_02_returns_distribution_3d(df_pandas)
            self.viz_03_volatility_analysis(df_pandas)
            self.viz_04_correlation_heatmap(df_pandas)
            self.viz_05_portfolio_performance(df_pandas)
            self.viz_06_volume_analysis(df_pandas)
            self.viz_07_candlestick_analysis(df_pandas)
            self.viz_08_statistical_distributions(df_pandas)
            self.viz_09_3d_surface_plot(df_pandas)
            self.viz_10_risk_return_scatter(df_pandas)
            self.viz_11_cumulative_returns(df_pandas)
            self.viz_12_drawdown_analysis(df_pandas)
            
            print("\n" + "="*80)
            print("✓✓✓ TË GJITHA 12 VIZUALIZIMET U KRIJUAN ME SUKSES ✓✓✓")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ GABIM gjatë gjenerimit të vizualizimeve: {str(e)}")
            import traceback
            traceback.print_exc()
