#!/usr/bin/env python3
"""
Run All Notebook Cells in Order
Execute each cell script individually to test the complete notebook
"""

import subprocess
import sys
import os

def run_cell(cell_file, cell_name):
    """Run a single cell script"""
    
    print(f"\n{'='*60}")
    print(f"🔄 Running {cell_name}")
    print(f"📁 File: {cell_file}")
    print(f"{'='*60}")
    
    if not os.path.exists(cell_file):
        print(f"❌ File not found: {cell_file}")
        return False
    
    try:
        result = subprocess.run([sys.executable, cell_file], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {cell_name} completed successfully")
            return True
        else:
            print(f"❌ {cell_name} failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {cell_name} timed out")
        return False
    except Exception as e:
        print(f"❌ Exception in {cell_name}: {e}")
        return False

def main():
    """Run all cells in order"""
    
    print("🚀 Running All Notebook Cells")
    print("=" * 60)
    
    cells = [
        ("cell_01_imports.py", "Cell 1: Import Libraries"),
        ("cell_02_trainer_class.py", "Cell 2: Trainer Class"),
        ("cell_03_load_dataset.py", "Cell 3: Load Dataset"),
    ]
    
    success_count = 0
    total_cells = len(cells)
    
    for cell_file, cell_name in cells:
        success = run_cell(cell_file, cell_name)
        
        if success:
            success_count += 1
        else:
            print(f"\n❓ Continue to next cell? (y/n): ", end="")
            try:
                response = input().lower().strip()
                if response not in ['y', 'yes']:
                    print("🛑 Stopping execution")
                    break
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                break
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📋 EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful cells: {success_count}/{total_cells}")
    print(f"❌ Failed cells: {total_cells - success_count}/{total_cells}")
    
    if success_count == total_cells:
        print(f"\n🎉 ALL CELLS SUCCESSFUL!")
        print(f"✅ Your notebook environment is working perfectly!")
        print(f"\n🚀 Next steps:")
        print(f"1. Open Jupyter: jupyter notebook")
        print(f"2. Run: FER2013_Emotion_Model_Training.ipynb")
        print(f"3. All cells should work without errors")
    else:
        print(f"\n⚠️ Some cells failed. Check the errors above.")
        print(f"🔧 Common fixes:")
        print(f"   pip install numpy pandas matplotlib tensorflow")
        print(f"   pip install scikit-learn opencv-python pillow seaborn")

if __name__ == "__main__":
    main()