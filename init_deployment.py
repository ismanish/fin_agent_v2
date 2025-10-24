#!/usr/bin/env python3
"""
Post-deployment initialization script for the Financial AQRR Application.
This script sets up the necessary data structures after deployment.
"""

import os
import sys
import time

def main():
    print("=" * 60)
    print("Financial AQRR Application - Deployment Initialization")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    required_vars = ['OPENAI_API_KEY', 'SEC_API_KEY', 'FINNHUB_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"   ❌ {var} is not set")
        else:
            print(f"   ✅ {var} is configured")
    
    if missing_vars:
        print("\n⚠️  Warning: Some API keys are missing!")
        print("   The application may not work properly without these keys.")
    
    # Check if FAISS index exists
    print("\n2. Checking FAISS vector store...")
    vector_store_path = os.path.join('utils', 'vector_store', 'index.faiss')
    
    if os.path.exists(vector_store_path):
        print(f"   ✅ FAISS index exists at {vector_store_path}")
    else:
        print(f"   ❌ FAISS index not found at {vector_store_path}")
        print("   Run: python src/on_demand_insights/document_processor.py")
    
    # Check output directories
    print("\n3. Creating output directories...")
    output_dirs = [
        'output/pdf/AQRR',
        'output/word/AQRR',
        'output/json',
        'output/csv',
        'logs/HFA',
        'logs/COMP',
        'logs/CAP',
        'utils/chat'
    ]
    
    for dir_path in output_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✅ {dir_path}")
    
    print("\n" + "=" * 60)
    print("Initialization complete!")
    print("=" * 60)
    
    if missing_vars:
        print("\nℹ️  Remember to set the missing environment variables in Railway!")
    
    if not os.path.exists(vector_store_path):
        print("\nℹ️  To generate the FAISS index, run:")
        print("   python src/on_demand_insights/document_processor.py")

if __name__ == "__main__":
    main()
