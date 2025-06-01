"""
Runner script for simplified QuizForce AI test.
"""

import sys
from pathlib import Path
import subprocess
import os

def main():
    """Run the simple test app."""
    print("🎯 Starting QuizForce AI Simple Test")
    print("=" * 50)
    
    # Get paths
    test_dir = Path(__file__).parent
    app_path = test_dir / "ui" / "simple_app.py"
    
    if not app_path.exists():
        print(f"❌ App file not found: {app_path}")
        return
    
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
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        print("🌐 Open: http://localhost:8502")
        print("⏹️ Press Ctrl+C to stop")
        
        subprocess.run(cmd, env=env, cwd=test_dir)
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        print("\n💡 Alternative commands:")
        print(f"cd {test_dir}")
        print("streamlit run ui/simple_app.py --server.port 8502")

if __name__ == "__main__":
    main()
