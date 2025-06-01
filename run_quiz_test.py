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
        print("💡 Will create a simple test interface...")
        
        # Create simple test interface if not exists
        app_path.parent.mkdir(exist_ok=True)
        create_simple_quiz_interface(app_path)
    
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

def create_simple_quiz_interface(app_path):
    """Tạo giao diện test đơn giản nếu chưa có."""
    content = '''
import streamlit as st

st.set_page_config(
    page_title="QuizForce AI - Quiz Test",
    page_icon="📝",
    layout="wide"
)

st.title("📝 QuizForce AI - Quiz Test Interface")
st.info("🚧 Giao diện này đang được phát triển...")

st.markdown("""
### 🎯 Tính năng sẽ có:
- ✅ Làm bài kiểm tra trực tuyến
- ✅ Hỗ trợ nhiều chế độ (exam/practice)
- ✅ Timer tự động
- ✅ Chấm điểm và thống kê

### 📝 Hiện tại:
Vui lòng sử dụng giao diện chính tại: **http://localhost:8502**
""")

if st.button("🏠 Về Trang Chính"):
    st.markdown("Truy cập: http://localhost:8502")
'''
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created simple interface at: {app_path}")

if __name__ == "__main__":
    main()
