#!/usr/bin/env python3
"""
================================================================================
QUICK START - ML Pipeline Demo
================================================================================
Demonstrates the complete ML workflow with real algorithms
Run this to see everything in action!
================================================================================
"""

import os
import sys

# Add parent directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def main():
    print_header("🚀 ML PIPELINE QUICK START")
    
    print("""
This demo will run the complete Machine Learning pipeline:

STEP 1: Feature Engineering (Spark)
  ✓ Load raw price data
  ✓ Calculate technical indicators (MA, RSI, Bollinger Bands, etc.)
  ✓ Save processed features

STEP 2: Train ML Models (Supervised & Unsupervised)
  ✓ Random Forest Classifier
  ✓ Gradient Boosting Classifier  
  ✓ Logistic Regression
  ✓ Support Vector Machine (SVM)
  ✓ K-Means Clustering (market regimes)
  ✓ PCA (dimensionality reduction)

STEP 3: Evaluate Models
  ✓ Calculate metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
  ✓ Generate confusion matrices
  ✓ Plot ROC curves
  ✓ Cross-validation scores
  ✓ Feature importance analysis

STEP 4: Make Predictions
  ✓ Load trained models
  ✓ Predict price direction for all assets
  ✓ Ensemble voting for robust predictions
  ✓ Save predictions for dashboard

STEP 5: View Results
  ✓ Start web dashboard
  ✓ See real-time predictions
  ✓ View model performance reports
    """)
    
    print("\n" + "-"*80)
    response = input("\nReady to start? [y/N]: ")
    
    if response.lower() != 'y':
        print("\n❌ Cancelled. Run this script again when ready.")
        return
    
    # Step 1: Feature Engineering
    print_header("STEP 1: Feature Engineering with Apache Spark")
    print("Running: spark_streaming_processor.py")
    print("\nThis will:")
    print("  • Load raw price data")
    print("  • Calculate 15 technical indicators")
    print("  • Save to processed_features.csv")
    print("\n⏳ This may take 1-2 minutes...")
    
    os.chdir(BASE_DIR)
    os.system(f"{sys.executable} scripts/spark_streaming_processor.py")
    
    input("\n✅ Step 1 complete. Press Enter to continue...")
    
    # Step 2: Train Models
    print_header("STEP 2: Train ML Models (Supervised & Unsupervised)")
    print("Running: ml_trainer.py")
    print("\nThis will train:")
    print("  • Random Forest (100 trees)")
    print("  • Gradient Boosting (100 estimators)")
    print("  • Logistic Regression")
    print("  • SVM (RBF kernel)")
    print("  • K-Means (4 clusters)")
    print("  • PCA (95% variance)")
    print("\n⏳ This may take 2-5 minutes...")
    
    os.system(f"{sys.executable} scripts/ml_trainer.py")
    
    input("\n✅ Step 2 complete. Press Enter to continue...")
    
    # Step 3: Evaluate Models
    print_header("STEP 3: Evaluate Model Performance")
    print("Running: ml_evaluator.py")
    print("\nThis will generate:")
    print("  • Confusion matrices")
    print("  • ROC curves")
    print("  • Metrics comparison chart")
    print("  • Feature importance plots")
    print("  • Cross-validation results")
    print("  • HTML evaluation report")
    print("\n⏳ This may take 1-2 minutes...")
    
    os.system(f"{sys.executable} scripts/ml_evaluator.py")
    
    input("\n✅ Step 3 complete. Press Enter to continue...")
    
    # Step 4: Make Predictions
    print_header("STEP 4: Generate Predictions")
    print("Running: ml_predictor.py")
    print("\nThis will:")
    print("  • Load trained models")
    print("  • Make predictions for all 14 assets")
    print("  • Use ensemble voting")
    print("  • Save to latest_predictions.json")
    
    os.system(f"{sys.executable} scripts/ml_predictor.py")
    
    input("\n✅ Step 4 complete. Press Enter to continue...")
    
    # Step 5: Results
    print_header("STEP 5: View Results")
    
    print("\n📊 Model Evaluation Report:")
    report_path = os.path.join(BASE_DIR, "reports", "evaluation_report.html")
    if os.path.exists(report_path):
        print(f"   ✓ Open in browser: {report_path}")
    else:
        print("   ⚠️  Report not found")
    
    print("\n🎯 Predictions:")
    predictions_path = os.path.join(BASE_DIR, "data", "latest_predictions.json")
    if os.path.exists(predictions_path):
        print(f"   ✓ Saved to: {predictions_path}")
        
        # Show sample prediction
        import json
        with open(predictions_path, 'r') as f:
            predictions = json.load(f)
        
        if predictions:
            print("\n   📈 Sample Prediction:")
            sample = predictions[0]
            print(f"      Asset: {sample['asset']}")
            print(f"      Direction: {sample['direction']}")
            print(f"      Confidence: {sample['confidence']:.1%}")
            print(f"      Market Regime: {sample.get('market_regime', 'Unknown')}")
    else:
        print("   ⚠️  Predictions not found")
    
    print("\n🌐 Web Dashboard:")
    print("   To view predictions in real-time:")
    print(f"   1. Run: {sys.executable} app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Click: 🎯 Predictions tab")
    
    print_header("✅ ML PIPELINE COMPLETE!")
    
    print("""
Summary of what was accomplished:

✅ Feature Engineering: Technical indicators calculated
✅ Model Training: 6 models trained (4 supervised + 2 unsupervised)
✅ Model Evaluation: Comprehensive performance metrics generated
✅ Predictions: Real-time predictions for 14 financial assets
✅ Reports: HTML reports and visualizations created

All algorithms are REAL, STANDARD ML algorithms from scikit-learn:
  • Random Forest (Breiman, 2001)
  • Gradient Boosting (Friedman, 2001)
  • Logistic Regression (Cox, 1958)
  • Support Vector Machine (Cortes & Vapnik, 1995)
  • K-Means Clustering (Lloyd, 1982)
  • PCA (Pearson, 1901)

No custom or "cooked up" algorithms - just proven, industry-standard methods!
    """)
    
    print("\n📚 For more information, see:")
    print("   • ML_IMPLEMENTATION.md - Complete documentation")
    print("   • reports/evaluation_report.html - Model performance")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
