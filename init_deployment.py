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
        # Check file size to ensure it's valid
        size = os.path.getsize(vector_store_path)
        print(f"      Size: {size:,} bytes")
    else:
        print(f"   ❌ FAISS index not found at {vector_store_path}")
        print("   🔄 Generating FAISS index...")

        # Create the vector store directory if it doesn't exist
        os.makedirs(os.path.dirname(vector_store_path), exist_ok=True)

        # Try to run the document processor to generate the index
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, "src/on_demand_insights/document_processor.py"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            if result.returncode == 0:
                print("   ✅ FAISS index generated successfully!")
            else:
                print(f"   ⚠️  Warning: Could not generate FAISS index")
                print(f"      Error: {result.stderr[:500] if result.stderr else 'Unknown error'}")
        except Exception as e:
            print(f"   ⚠️  Warning: Could not generate FAISS index: {str(e)}")
            print("   You may need to run manually: python src/on_demand_insights/document_processor.py")
    
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

if __name__ == "__main__":
    main()
