"""
Runner script for QuizForce AI Quiz Test Interface.
Khởi chạy giao diện làm bài kiểm tra riêng biệt.
"""

import sys
from pathlib import Path
import subprocess
import os

def main():
    """Run the quiz test interface."""
    print("📝 Starting QuizForce AI Quiz Test Interface")
    print("=" * 50)
    
    # Get paths
    test_dir = Path(__file__).parent
    app_path = test_dir / "ui" / "quiz_test_interface.py"
    
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
            "--server.port", "8503",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        print("🌐 Open: http://localhost:8503")
        print("⏹️ Press Ctrl+C to stop")
        
        subprocess.run(cmd, env=env, cwd=test_dir)
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        print("\n💡 Alternative commands:")
        print(f"cd {test_dir}")
        print("streamlit run ui/quiz_test_interface.py --server.port 8503")

if __name__ == "__main__":
    main()
