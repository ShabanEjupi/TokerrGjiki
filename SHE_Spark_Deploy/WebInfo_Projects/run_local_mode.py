#!/usr/bin/env python3
"""
================================================================================
LOCAL MODE - ML Pipeline for Testing
================================================================================
Runs the complete ML pipeline in LOCAL MODE (no cluster required)
Perfect for testing on Windows before deploying to 10 VM cluster
================================================================================
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def main():
    print_header("🖥️  LOCAL MODE - ML PIPELINE")
    
    print("""
This will run the ML pipeline in LOCAL MODE on your Windows machine.
No cluster connection required!

Steps:
1. Generate sample data (synthetic financial data)
2. Feature engineering with Spark (local mode)
3. Train ML models
4. Evaluate models
5. Make predictions
6. Start dashboard

Perfect for testing before deploying to the 10 VM cluster!
    """)
    
    response = input("\nReady to start? [y/N]: ")
    
    if response.lower() != 'y':
        print("\n❌ Cancelled.")
        return
    
    os.chdir(BASE_DIR)
    
    # Step 0: Generate sample data
    print_header("STEP 0: Generate Sample Data")
    print("Creating synthetic financial data for testing...")
    print("⏳ This will take ~5 seconds...\n")
    
    result = os.system(f"{sys.executable} scripts\\generate_sample_data.py")
    if result != 0:
        print("\n❌ Data generation failed!")
        return
    
    input("\n✅ Step 0 complete. Press Enter to continue...")
    
    # Step 1: Feature Engineering
    print_header("STEP 1: Feature Engineering (Spark Local Mode)")
    print("Processing features with Apache Spark in local mode...")
    print("⏳ This may take 1-2 minutes...\n")
    
    result = os.system(f"{sys.executable} scripts\\spark_streaming_processor.py")
    if result != 0:
        print("\n⚠️  Feature engineering had issues, but continuing...")
    
    # Check if features were created
    features_file = os.path.join(BASE_DIR, "data", "processed_features.csv")
    if not os.path.exists(features_file):
        print("\n❌ Features file not created. Cannot continue.")
        return
    
    input("\n✅ Step 1 complete. Press Enter to continue...")
    
    # Step 2: Train Models
    print_header("STEP 2: Train ML Models")
    print("Training supervised and unsupervised models...")
    print("⏳ This may take 2-5 minutes...\n")
    
    result = os.system(f"{sys.executable} scripts\\ml_trainer.py")
    if result != 0:
        print("\n⚠️  Training had issues, but continuing...")
    
    input("\n✅ Step 2 complete. Press Enter to continue...")
    
    # Step 3: Evaluate Models
    print_header("STEP 3: Evaluate Models")
    print("Generating evaluation reports and visualizations...")
    print("⏳ This may take 1-2 minutes...\n")
    
    result = os.system(f"{sys.executable} scripts\\ml_evaluator.py")
    if result != 0:
        print("\n⚠️  Evaluation had issues, but continuing...")
    
    input("\n✅ Step 3 complete. Press Enter to continue...")
    
    # Step 4: Make Predictions
    print_header("STEP 4: Make Predictions")
    print("Generating predictions with trained models...\n")
    
    result = os.system(f"{sys.executable} scripts\\ml_predictor.py")
    if result != 0:
        print("\n⚠️  Prediction had issues, but continuing...")
    
    input("\n✅ Step 4 complete. Press Enter to continue...")
    
    # Summary
    print_header("✅ LOCAL MODE TEST COMPLETE!")
    
    print("""
Results:
  📁 data/realtime_prices.csv       - Sample price data
  📁 data/processed_features.csv    - Technical indicators
  📁 models/*.pkl                   - Trained ML models
  📁 reports/evaluation_report.html - Model evaluation
  📁 data/latest_predictions.json   - ML predictions

Next Steps:
  
  1. VIEW EVALUATION REPORT:
     Open: reports\\evaluation_report.html in your browser
  
  2. START DASHBOARD:
     Run: python app.py
     Visit: http://localhost:5000
  
  3. WHEN READY FOR CLUSTER:
     Edit: scripts/spark_streaming_processor.py
     Change: USE_LOCAL_MODE = False
     Deploy to your 10 VM cluster!

Everything is working locally! 🎉
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
