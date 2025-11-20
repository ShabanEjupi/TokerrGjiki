#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ML MODEL EVALUATOR - Comprehensive Performance Analysis
================================================================================
Evaluates trained ML models with detailed metrics and visualizations:
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix
- ROC Curve & AUC
- Feature Importance
- Cross-Validation Scores
- Model Comparison Charts
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Scikit-learn metrics
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, 
    roc_curve, roc_auc_score, auc,
    precision_recall_curve, average_precision_score
)
from sklearn.model_selection import cross_val_score, cross_validate

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

FEATURE_COLUMNS = [
    'return', 'ma_5', 'ma_14', 'ma_20', 'ma_50',
    'volatility_14', 'volatility_20',
    'momentum_7', 'momentum_14',
    'rsi', 'bb_upper', 'bb_middle', 'bb_lower',
    'price_to_ma5', 'price_to_ma20'
]

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

os.makedirs(REPORTS_DIR, exist_ok=True)

# Plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data_and_split():
    """Load data and prepare train/test split"""
    
    # Load processed features
    csv_file = os.path.join(DATA_DIR, 'processed_features.csv')
    
    if not os.path.exists(csv_file):
        print(f"❌ Data file not found: {csv_file}")
        return None, None, None, None
    
    print(f"📂 Loading data from: {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Remove NaN and inf
    df = df.dropna(subset=FEATURE_COLUMNS + ['label'])
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    
    print(f"✅ Loaded {len(df)} records")
    
    # Split features and labels
    X = df[FEATURE_COLUMNS].values
    y = df['label'].values
    
    # Load scaler
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    X_scaled = scaler.transform(X)
    
    # Use same split as training (80/20)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

# ============================================================================
# MODEL EVALUATION
# ============================================================================

def evaluate_model(model, model_name, X_train, X_test, y_train, y_test):
    """Comprehensive evaluation of a single model"""
    
    print(f"\n{'='*80}")
    print(f"EVALUATING: {model_name.upper()}")
    print(f"{'='*80}\n")
    
    results = {'model_name': model_name}
    
    # ========== 1. PREDICTIONS ==========
    print("1️⃣  Making predictions...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # ========== 2. BASIC METRICS ==========
    print("\n2️⃣  Calculating metrics...")
    
    results['accuracy'] = accuracy_score(y_test, y_pred)
    results['precision'] = precision_score(y_test, y_pred)
    results['recall'] = recall_score(y_test, y_pred)
    results['f1_score'] = f1_score(y_test, y_pred)
    results['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Accuracy:  {results['accuracy']:.4f}")
    print(f"   Precision: {results['precision']:.4f}")
    print(f"   Recall:    {results['recall']:.4f}")
    print(f"   F1-Score:  {results['f1_score']:.4f}")
    print(f"   ROC-AUC:   {results['roc_auc']:.4f}")
    
    # ========== 3. CONFUSION MATRIX ==========
    print("\n3️⃣  Computing confusion matrix...")
    cm = confusion_matrix(y_test, y_pred)
    results['confusion_matrix'] = cm.tolist()
    
    print(f"\n   Confusion Matrix:")
    print(f"                Predicted")
    print(f"              DOWN    UP")
    print(f"   Actual DOWN {cm[0,0]:4d}  {cm[0,1]:4d}")
    print(f"          UP   {cm[1,0]:4d}  {cm[1,1]:4d}")
    
    # ========== 4. CLASSIFICATION REPORT ==========
    print("\n4️⃣  Classification report:")
    report = classification_report(y_test, y_pred, target_names=['DOWN', 'UP'])
    print(report)
    results['classification_report'] = report
    
    # ========== 5. ROC CURVE ==========
    print("\n5️⃣  Calculating ROC curve...")
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    results['roc_curve'] = {
        'fpr': fpr.tolist(),
        'tpr': tpr.tolist(),
        'thresholds': thresholds.tolist()
    }
    
    # ========== 6. CROSS-VALIDATION ==========
    print("\n6️⃣  Running 5-fold cross-validation...")
    try:
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
        results['cv_scores'] = cv_scores.tolist()
        results['cv_mean'] = float(cv_scores.mean())
        results['cv_std'] = float(cv_scores.std())
        
        print(f"   CV Scores: {cv_scores}")
        print(f"   Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    except Exception as e:
        print(f"   ⚠️  Cross-validation failed: {e}")
        results['cv_scores'] = []
    
    # ========== 7. FEATURE IMPORTANCE ==========
    print("\n7️⃣  Feature importance...")
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_importance = sorted(
            zip(FEATURE_COLUMNS, importances),
            key=lambda x: x[1],
            reverse=True
        )
        
        results['feature_importance'] = {feat: float(imp) for feat, imp in feature_importance}
        
        print(f"\n   Top 10 Features:")
        for i, (feature, importance) in enumerate(feature_importance[:10], 1):
            print(f"   {i:2d}. {feature:20s}: {importance:.4f}")
    elif hasattr(model, 'coef_'):
        coefficients = np.abs(model.coef_[0])
        feature_importance = sorted(
            zip(FEATURE_COLUMNS, coefficients),
            key=lambda x: x[1],
            reverse=True
        )
        
        results['feature_importance'] = {feat: float(coef) for feat, coef in feature_importance}
        
        print(f"\n   Top 10 Features (by coefficient magnitude):")
        for i, (feature, coef) in enumerate(feature_importance[:10], 1):
            print(f"   {i:2d}. {feature:20s}: {coef:.4f}")
    else:
        print("   ⚠️  Model doesn't support feature importance")
        results['feature_importance'] = {}
    
    return results

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_confusion_matrices(all_results):
    """Plot confusion matrices for all models"""
    
    print("\n📊 Plotting confusion matrices...")
    
    n_models = len(all_results)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for idx, (model_name, results) in enumerate(all_results.items()):
        cm = np.array(results['confusion_matrix'])
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                   xticklabels=['DOWN', 'UP'], yticklabels=['DOWN', 'UP'])
        axes[idx].set_title(f'{model_name}\nAccuracy: {results["accuracy"]:.3f}')
        axes[idx].set_ylabel('Actual')
        axes[idx].set_xlabel('Predicted')
    
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'confusion_matrices.png'), dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: confusion_matrices.png")
    plt.close()

def plot_roc_curves(all_results):
    """Plot ROC curves for all models"""
    
    print("\n📈 Plotting ROC curves...")
    
    plt.figure(figsize=(10, 8))
    
    for model_name, results in all_results.items():
        fpr = results['roc_curve']['fpr']
        tpr = results['roc_curve']['tpr']
        auc_score = results['roc_auc']
        
        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})', linewidth=2)
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'roc_curves.png'), dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: roc_curves.png")
    plt.close()

def plot_metrics_comparison(all_results):
    """Plot bar chart comparing all metrics"""
    
    print("\n📊 Plotting metrics comparison...")
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
    models = list(all_results.keys())
    
    data = {metric: [all_results[model][metric] for model in models] for metric in metrics}
    
    df = pd.DataFrame(data, index=models)
    
    ax = df.plot(kind='bar', figsize=(12, 6), width=0.8)
    plt.title('Model Performance Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Score', fontsize=12)
    plt.xlabel('Model', fontsize=12)
    plt.legend(title='Metrics', loc='lower right', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.ylim([0, 1])
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.3f', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'metrics_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: metrics_comparison.png")
    plt.close()

def plot_feature_importance(all_results):
    """Plot feature importance for models that support it"""
    
    print("\n🔍 Plotting feature importance...")
    
    models_with_importance = {name: res for name, res in all_results.items() 
                             if res.get('feature_importance')}
    
    if not models_with_importance:
        print("   ⚠️  No models with feature importance")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, (model_name, results) in enumerate(models_with_importance.items()):
        importance_dict = results['feature_importance']
        
        # Get top 10 features
        top_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        features, importances = zip(*top_features)
        
        axes[idx].barh(range(len(features)), importances, color='steelblue')
        axes[idx].set_yticks(range(len(features)))
        axes[idx].set_yticklabels(features)
        axes[idx].set_xlabel('Importance', fontsize=10)
        axes[idx].set_title(f'{model_name} - Top 10 Features', fontsize=12, fontweight='bold')
        axes[idx].invert_yaxis()
        axes[idx].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'feature_importance.png'), dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: feature_importance.png")
    plt.close()

def plot_cross_validation_scores(all_results):
    """Plot cross-validation scores"""
    
    print("\n📊 Plotting cross-validation scores...")
    
    models = []
    means = []
    stds = []
    
    for model_name, results in all_results.items():
        if results.get('cv_scores'):
            models.append(model_name)
            means.append(results['cv_mean'])
            stds.append(results['cv_std'])
    
    if not models:
        print("   ⚠️  No cross-validation scores available")
        return
    
    plt.figure(figsize=(10, 6))
    x_pos = np.arange(len(models))
    
    plt.bar(x_pos, means, yerr=stds, align='center', alpha=0.8, 
            ecolor='black', capsize=10, color='steelblue')
    plt.xticks(x_pos, models, rotation=45, ha='right')
    plt.ylabel('F1-Score', fontsize=12)
    plt.title('5-Fold Cross-Validation Results', fontsize=14, fontweight='bold')
    plt.ylim([0, 1])
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, (mean, std) in enumerate(zip(means, stds)):
        plt.text(i, mean + std + 0.02, f'{mean:.3f}±{std:.3f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'cross_validation.png'), dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: cross_validation.png")
    plt.close()

# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_html_report(all_results):
    """Generate HTML evaluation report"""
    
    print("\n📄 Generating HTML report...")
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ML Model Evaluation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .best {{
            background: #2ecc71 !important;
            color: white;
            font-weight: bold;
        }}
        .metric {{
            font-weight: bold;
        }}
        img {{
            max-width: 100%;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .info-box {{
            background: #e8f4f8;
            padding: 20px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Machine Learning Model Evaluation Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="info-box">
            <h3>📊 Models Evaluated</h3>
            <ul>
                <li><strong>Random Forest:</strong> Ensemble of decision trees</li>
                <li><strong>Gradient Boosting:</strong> Sequential boosting algorithm</li>
                <li><strong>Logistic Regression:</strong> Linear classification model</li>
                <li><strong>SVM:</strong> Support Vector Machine with RBF kernel</li>
            </ul>
        </div>
        
        <h2>📈 Performance Metrics Comparison</h2>
        <table>
            <tr>
                <th>Model</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1-Score</th>
                <th>ROC-AUC</th>
            </tr>
"""
    
    # Find best model for each metric
    best_accuracy = max(all_results.items(), key=lambda x: x[1]['accuracy'])[0]
    best_f1 = max(all_results.items(), key=lambda x: x[1]['f1_score'])[0]
    best_roc = max(all_results.items(), key=lambda x: x[1]['roc_auc'])[0]
    
    for model_name, results in all_results.items():
        html += f"""
            <tr>
                <td class="metric">{model_name}</td>
                <td {'class="best"' if model_name == best_accuracy else ''}>{results['accuracy']:.4f}</td>
                <td>{results['precision']:.4f}</td>
                <td>{results['recall']:.4f}</td>
                <td {'class="best"' if model_name == best_f1 else ''}>{results['f1_score']:.4f}</td>
                <td {'class="best"' if model_name == best_roc else ''}>{results['roc_auc']:.4f}</td>
            </tr>
"""
    
    html += f"""
        </table>
        
        <h2>🏆 Best Models</h2>
        <ul>
            <li><strong>Best Accuracy:</strong> {best_accuracy} ({all_results[best_accuracy]['accuracy']:.4f})</li>
            <li><strong>Best F1-Score:</strong> {best_f1} ({all_results[best_f1]['f1_score']:.4f})</li>
            <li><strong>Best ROC-AUC:</strong> {best_roc} ({all_results[best_roc]['roc_auc']:.4f})</li>
        </ul>
        
        <h2>📊 Visualizations</h2>
        
        <h3>Confusion Matrices</h3>
        <img src="confusion_matrices.png" alt="Confusion Matrices">
        
        <h3>ROC Curves</h3>
        <img src="roc_curves.png" alt="ROC Curves">
        
        <h3>Metrics Comparison</h3>
        <img src="metrics_comparison.png" alt="Metrics Comparison">
        
        <h3>Feature Importance</h3>
        <img src="feature_importance.png" alt="Feature Importance">
        
        <h3>Cross-Validation Results</h3>
        <img src="cross_validation.png" alt="Cross Validation">
        
    </div>
</body>
</html>
"""
    
    report_path = os.path.join(REPORTS_DIR, 'evaluation_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"   ✓ Saved: evaluation_report.html")
    print(f"\n📍 Open in browser: {report_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main evaluation function"""
    
    print("="*80)
    print("ML MODEL EVALUATOR")
    print("Comprehensive Performance Analysis")
    print("="*80)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data_and_split()
    
    if X_train is None:
        print("\n❌ Failed to load data!")
        return
    
    # Load all models
    print(f"\n📂 Loading trained models...")
    models = {}
    
    model_files = {
        'Random Forest': 'random_forest.pkl',
        'Gradient Boosting': 'gradient_boosting.pkl',
        'Logistic Regression': 'logistic_regression.pkl',
        'SVM': 'svm.pkl'
    }
    
    for name, filename in model_files.items():
        path = os.path.join(MODELS_DIR, filename)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                models[name] = pickle.load(f)
            print(f"   ✓ {name} loaded")
        else:
            print(f"   ✗ {name} not found")
    
    if not models:
        print("\n❌ No models found! Run ml_trainer.py first.")
        return
    
    # Evaluate all models
    all_results = {}
    
    for model_name, model in models.items():
        results = evaluate_model(model, model_name, X_train, X_test, y_train, y_test)
        all_results[model_name] = results
    
    # Generate visualizations
    print(f"\n{'='*80}")
    print("GENERATING VISUALIZATIONS")
    print(f"{'='*80}")
    
    plot_confusion_matrices(all_results)
    plot_roc_curves(all_results)
    plot_metrics_comparison(all_results)
    plot_feature_importance(all_results)
    plot_cross_validation_scores(all_results)
    
    # Save results to JSON
    results_path = os.path.join(REPORTS_DIR, 'evaluation_results.json')
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4)
    print(f"\n💾 Results saved to: {results_path}")
    
    # Generate HTML report
    generate_html_report(all_results)
    
    print(f"\n{'='*80}")
    print(f"✅ EVALUATION COMPLETED!")
    print(f"   All reports saved in: {REPORTS_DIR}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
