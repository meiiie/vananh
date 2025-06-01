"""
Runner script for simplified QuizForce AI test.
"""

import sys
from pathlib import Path
import subprocess
import os

def check_requirements():
    """Kiểm tra các requirements cần thiết."""
    print("🔍 Checking requirements...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check essential modules
    required_modules = [
        'streamlit',
        'google.generativeai',
        'docx',
        'PIL'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'google.generativeai':
                import google.generativeai
            elif module == 'docx':
                import docx
            elif module == 'PIL':
                from PIL import Image
            else:
                __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ Missing modules: {', '.join(missing_modules)}")
        print("Install with: pip install streamlit google-generativeai python-docx pillow python-dotenv")
        return False
    
    return True

def check_files():
    """Kiểm tra các file cần thiết."""
    print("\n📁 Checking files...")
    
    test_dir = Path(__file__).parent
    
    required_files = [
        "ui/simple_app.py",
        "backend/__init__.py",
        "backend/simple_agent.py",
        "backend/quiz_test_engine.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = test_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Run the simple test app."""
    print("🎯 QuizForce AI Simple Test")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed!")
        return
    
    # Check files
    if not check_files():
        print("\n❌ File check failed!")
        return
    
    # Get paths
    test_dir = Path(__file__).parent
    app_path = test_dir / "ui" / "simple_app.py"
    
    print(f"\n📍 App path: {app_path}")
    print(f"📍 Working directory: {test_dir}")
    
    # Set environment
    env = os.environ.copy()
    env['PYTHONPATH'] = str(test_dir.parent)
    
    # Run streamlit
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port", "8502",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.address", "localhost"
        ]
        
        print(f"\n🚀 Running command:")
        print(f"   {' '.join(cmd)}")
        print(f"\n🌐 Opening: http://localhost:8502")
        print("⏹️  Press Ctrl+C to stop")
        print("-" * 50)
        
        # Run and capture output
        result = subprocess.run(cmd, env=env, cwd=test_dir, 
                              capture_output=False, text=True)
        
        if result.returncode != 0:
            print(f"❌ Process exited with code: {result.returncode}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        print(f"Error type: {type(e).__name__}")
        
        print("\n💡 Troubleshooting:")
        print("1. Check if all dependencies are installed:")
        print("   pip install streamlit google-generativeai python-docx pillow python-dotenv")
        print("\n2. Try running directly:")
        print(f"   cd {test_dir}")
        print("   streamlit run ui/simple_app.py --server.port 8502")
        print("\n3. Check Python path:")
        print(f"   PYTHONPATH={test_dir.parent}")

if __name__ == "__main__":
    main()
