"""
Ứng Dụng QuizForce AI - Phiên Bản Test Đơn Giản
Giao diện một trang với độ phức tạp tối thiểu, tối ưu cho người Việt Nam.
"""

import streamlit as st
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

# Thêm backend vào path - sửa lại đường dẫn
current_dir = Path(__file__).parent
test_dir = current_dir.parent
project_root = test_dir.parent

# Thêm cả project root và test directory vào path
sys.path.append(str(project_root))
sys.path.append(str(test_dir))

try:
    # Thử import từ backend chính trước
    from backend.simple_agent import SimpleQuizAgent
except ImportError:
    try:
        # Nếu không được thì thử từ test backend
        from test.backend.simple_agent import SimpleQuizAgent
    except ImportError as e:
        st.error(f"❌ Lỗi import module: {e}")
        st.info("""
        **Hướng dẫn sửa lỗi:**
        
        1. Đảm bảo cấu trúc thư mục:
        ```
        quizforce_project/
        ├── backend/
        │   ├── __init__.py
        │   ├── simple_agent.py
        │   └── quiz_test_engine.py
        ├── test/
        │   ├── backend/
        │   │   ├── __init__.py
        │   │   ├── simple_agent.py
        │   │   └── quiz_test_engine.py
        │   └── ui/
        │       └── simple_app.py
        ```
        
        2. Chạy từ thư mục gốc:
        ```bash
        cd quizforce_project/test
        streamlit run ui/simple_app.py
        ```
        """)
        st.stop()

def main():
    """Ứng dụng chính."""
    st.set_page_config(
        page_title="QuizForce AI - Hệ Thống Tạo Quiz Thông Minh",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    page = st.sidebar.selectbox(
        "🧭 Điều hướng:",
        ["🎯 Tạo Quiz", "📝 Làm Bài Kiểm Tra", "📊 Thống Kê"],
        index=0
    )
    
    if page == "🎯 Tạo Quiz":
        render_quiz_creation_page()
    elif page == "📝 Làm Bài Kiểm Tra":
        render_quiz_test_page()
    elif page == "📊 Thống Kê":
        render_statistics_page()

def render_quiz_creation_page():
    """Render trang tạo quiz (code hiện tại)."""
    # Header chuyên nghiệp
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🎯 QuizForce AI</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0;'>Hệ Thống Tạo Quiz Trắc Nghiệm Thông Minh cho Giáo Dục Việt Nam</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar cấu hình
    with st.sidebar:
        render_professional_sidebar()
    
    # Giao diện chính
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        render_input_section()
    
    with col2:
        render_results_section()
    
    # Footer thông tin
    render_footer()

def render_statistics_page():
    """Render trang thống kê."""
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%); border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>📊 Thống Kê Hệ Thống</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0;'>Báo Cáo Chi Tiết Các Bài Kiểm Tra</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize engine if needed
    if 'quiz_engine' not in st.session_state:
        try:
            from backend.quiz_test_engine import QuizTestEngine
        except ImportError:
            try:
                from test.backend.quiz_test_engine import QuizTestEngine
            except ImportError as e:
                st.error(f"❌ Lỗi import QuizTestEngine: {e}")
                st.info("Module quiz_test_engine chưa được tạo. Tính năng này sẽ khả dụng sau.")
                return
        
        st.session_state.quiz_engine = QuizTestEngine()
    
    engine = st.session_state.quiz_engine
    stats = engine.get_test_statistics()
    
    if 'message' in stats:
        st.info("ℹ️ " + stats['message'])
        st.markdown("""
        ### 🎯 Hướng Dẫn Sử Dụng
        
        1. **Tạo Quiz** ở trang "Tạo Quiz"
        2. **Làm Bài Kiểm Tra** ở trang "Làm Bài Kiểm Tra"  
        3. **Xem Thống Kê** sẽ hiển thị tại đây
        
        Hệ thống sẽ tự động lưu kết quả các bài kiểm tra đã hoàn thành.
        """)
        return
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Tổng Bài Kiểm Tra", stats['total_tests'])
    
    with col2:
        st.metric("📊 Điểm Trung Bình", f"{stats['average_score']}/10")
    
    with col3:
        st.metric("🎯 Tỷ Lệ Đậu", f"{stats['pass_rate']:.1f}%")
    
    with col4:
        st.metric("🏆 Điểm Cao Nhất", f"{stats['highest_score']}/10")
    
    # Recent tests
    st.markdown("### 📋 Các Bài Kiểm Tra Gần Đây")
    
    if stats['recent_tests']:
        for test in stats['recent_tests']:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            
            with col1:
                st.write(f"👨‍🎓 **{test['student']}**")
            
            with col2:
                score_color = "🟢" if test['score'] >= 8 else "🟡" if test['score'] >= 5 else "🔴"
                st.write(f"{score_color} {test['score']}/10")
            
            with col3:
                st.write(f"📊 {test['percentage']:.1f}%")
            
            with col4:
                st.write(f"🕒 {test['time']}")
    else:
        st.info("Chưa có bài kiểm tra nào gần đây.")

def render_professional_sidebar():
    """Render sidebar chuyên nghiệp."""
    st.markdown("### ⚙️ Cấu Hình Hệ Thống")
    
    # API Key configuration
    with st.expander("🔑 Cấu Hình API", expanded=True):
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=os.getenv("GOOGLE_API_KEY", ""),
            help="Nhập API key của Google Gemini để sử dụng AI",
            placeholder="Dán API key của bạn vào đây..."
        )
        
        if api_key:
            st.success("✅ API Key đã được cấu hình")
            st.session_state.api_key = api_key
        else:
            st.error("❌ Cần API Key để sử dụng hệ thống")
            st.markdown("""
            **Hướng dẫn lấy API Key:**
            1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Đăng nhập tài khoản Google
            3. Tạo API key mới
            4. Copy và dán vào ô trên
            """)
    
    # Thông tin hệ thống
    with st.expander("📊 Thông Tin Hệ Thống"):
        st.info("""
        **QuizMaster AI v1.0**
        - 🤖 AI Engine: Google Gemini 2.0 Flash
        - 🎯 Chuyên môn: Tạo quiz trắc nghiệm Việt Nam
        - 📚 Hỗ trợ: Tất cả môn học phổ thông
        - 🌟 Tính năng: OCR, xử lý DOCX, JSON export
        """)
    
    # Hướng dẫn sử dụng
    with st.expander("📖 Hướng Dẫn Sử Dụng"):
        st.markdown("""
        **Quy trình 4 bước:**
        
        1. **Chuẩn bị đáp án**
           - Văn bản: `1. A`, `2. B`, `3. AC`
           - Hoặc chụp ảnh đáp án
        
        2. **Upload file DOCX**
           - Chứa câu hỏi có định dạng: `Câu 1.` hoặc `1.`
           - Mỗi câu có 4 lựa chọn A, B, C, D
        
        3. **Nhấn "Tạo Quiz"**
           - AI sẽ xử lý tự động
           - Thời gian: 30-60 giây
        
        4. **Tải xuống kết quả**
           - File JSON chuẩn
           - Sẵn sàng import vào hệ thống khác
        """)

def render_input_section():
    """Render phần nhập liệu."""
    st.markdown("### 📝 Dữ Liệu Đầu Vào")
    
    # Phần đáp án
    st.markdown("#### 1️⃣ Đáp Án Câu Hỏi")
    
    answer_tabs = st.tabs(["📝 Nhập Văn Bản", "🖼️ Upload Hình Ảnh"])
    
    answer_text = None
    answer_image = None
    
    with answer_tabs[0]:
        st.markdown("**Nhập đáp án theo định dạng:**")
        answer_text = st.text_area(
            "Danh sách đáp án:",
            placeholder="""Ví dụ:
1. A
2. B  
3. AC
4. D
5. BD
...""",
            height=180,
            help="Mỗi dòng một câu hỏi, format: số. đáp_án"
        )
        
        if answer_text:
            # Hiển thị preview
            lines = [line.strip() for line in answer_text.split('\n') if line.strip()]
            st.success(f"✅ Đã nhập {len(lines)} dòng đáp án")
    
    with answer_tabs[1]:
        answer_image = st.file_uploader(
            "Tải ảnh chứa đáp án:",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Upload ảnh chụp đáp án, AI sẽ tự động đọc"
        )
        
        if answer_image:
            st.image(answer_image, caption="Ảnh đáp án đã upload", width=300)
            st.success("✅ Đã upload ảnh thành công")
    
    st.divider()
    
    # Phần file DOCX
    st.markdown("#### 2️⃣ File Câu Hỏi DOCX")
    
    docx_file = st.file_uploader(
        "Upload file DOCX chứa câu hỏi:",
        type=['docx'],
        help="File Word chứa câu hỏi trắc nghiệm"
    )
    
    if docx_file:
        st.success(f"✅ Đã upload file: {docx_file.name}")
        st.info(f"📊 Kích thước file: {len(docx_file.getvalue())/1024:.1f} KB")
    
    st.divider()
    
    # Nút xử lý
    st.markdown("#### 3️⃣ Tạo Quiz")
    
    # Kiểm tra điều kiện
    has_api_key = hasattr(st.session_state, 'api_key') and st.session_state.api_key
    has_answers = (answer_text and answer_text.strip()) or answer_image
    has_docx = docx_file is not None
    
    can_process = has_api_key and has_answers and has_docx
    
    if not has_api_key:
        st.error("❌ Chưa cấu hình API Key (xem sidebar)")
    elif not has_answers:
        st.warning("⚠️ Chưa có đáp án (nhập văn bản hoặc upload ảnh)")
    elif not has_docx:
        st.warning("⚠️ Chưa upload file DOCX")
    else:
        st.success("✅ Đã sẵn sàng tạo quiz!")
    
    # Nút xử lý với style đẹp
    if st.button(
        "🚀 Tạo Quiz Thông Minh",
        disabled=not can_process,
        use_container_width=True,
        type="primary"
    ):
        if can_process:
            answer_method = "text" if answer_text else "image"
            answer_data = answer_text if answer_text else answer_image
            
            process_quiz_with_progress(
                api_key=st.session_state.api_key,
                answer_data=answer_data,
                docx_file=docx_file,
                answer_method=answer_method
            )

def render_results_section():
    """Render phần kết quả."""
    st.markdown("### 📊 Kết Quả Xử Lý")
    
    # Hiển thị kết quả nếu có
    if 'quiz_results' in st.session_state and st.session_state.quiz_results:
        display_professional_results(st.session_state.quiz_results)
    else:
        # Placeholder khi chưa có kết quả
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 10px; border: 2px dashed #dee2e6;'>
            <h3 style='color: #6c757d; margin-bottom: 1rem;'>🎯 Sẵn Sàng Tạo Quiz</h3>
            <p style='color: #6c757d; margin: 0;'>Cấu hình dữ liệu bên trái và nhấn "Tạo Quiz"</p>
            <p style='color: #6c757d; margin: 0;'>Kết quả sẽ hiển thị tại đây</p>
        </div>
        """, unsafe_allow_html=True)

def process_quiz_with_progress(api_key: str, answer_data, docx_file, answer_method: str):
    """Xử lý tạo quiz với thanh tiến trình chuyên nghiệp."""
    
    # Container cho progress
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Đang Xử Lý...")
        
        # Progress bar và status
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_text = st.empty()
        
        start_time = time.time()
        
        try:
            # Bước 1: Khởi tạo AI Agent
            status_text.success("🤖 Đang khởi tạo QuizMaster AI...")
            time_text.info(f"⏱️ Thời gian: {time.time() - start_time:.1f}s")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            agent = SimpleQuizAgent(api_key=api_key)
            
            # Bước 2: Chuẩn bị dữ liệu
            status_text.success("📋 Đang chuẩn bị dữ liệu đầu vào...")
            time_text.info(f"⏱️ Thời gian: {time.time() - start_time:.1f}s")
            progress_bar.progress(25)
            time.sleep(0.3)
            
            if answer_method == "text":
                answer_input = answer_data
            else:
                answer_input = answer_data.getvalue()
            
            # Bước 3: Xử lý chính
            status_text.success("⚙️ Đang thực hiện xử lý AI (có thể mất 30-60 giây)...")
            time_text.info(f"⏱️ Thời gian: {time.time() - start_time:.1f}s")
            progress_bar.progress(50)
            
            # Gọi agent xử lý
            results = agent.process_complete_quiz(
                answer_data=answer_input,
                docx_file=docx_file,
                answer_type=answer_method
            )
            
            progress_bar.progress(90)
            
            # Bước 4: Hoàn thành
            status_text.success("✅ Xử lý hoàn tất!")
            time_text.success(f"🎉 Tổng thời gian: {time.time() - start_time:.1f}s")
            progress_bar.progress(100)
            
            # Lưu kết quả và rerun
            st.session_state.quiz_results = results
            
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            status_text.error(f"❌ Có lỗi xảy ra: {str(e)}")
            time_text.error(f"⏱️ Thời gian: {time.time() - start_time:.1f}s")
            st.error("Vui lòng kiểm tra lại dữ liệu đầu vào và thử lại.")

def display_professional_results(results: dict):
    """Hiển thị kết quả chuyên nghiệp với thông tin debug chi tiết."""
    
    if not results.get("success"):
        st.error("❌ **Xử lý thất bại**")
        
        if results.get("errors"):
            st.markdown("### 🚨 Chi Tiết Lỗi:")
            for error in results["errors"]:
                st.markdown(error)
        
        # Hiển thị thông tin debug nếu có
        debug_info = results.get("debug_info", {})
        if debug_info:
            st.markdown("### 🔍 Thông Tin Debug:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📝 Đáp án tìm thấy:**")
                answer_keys = debug_info.get("answer_keys", [])
                if answer_keys:
                    st.success(f"✅ {len(answer_keys)} đáp án")
                    st.code(str(answer_keys[:20]))  # Hiển thị 20 đầu tiên
                else:
                    st.error("❌ Không tìm thấy đáp án nào")
            
            with col2:
                st.markdown("**📄 Câu hỏi tìm thấy:**")
                question_keys = debug_info.get("question_keys", [])
                if question_keys:
                    st.success(f"✅ {len(question_keys)} câu hỏi")
                    st.code(str(question_keys[:20]))  # Hiển thị 20 đầu tiên
                else:
                    st.error("❌ Không tìm thấy câu hỏi nào")
            
            # Hiển thị mapping nếu có
            if debug_info.get("applied_mapping"):
                st.markdown("**🔄 Mapping đã áp dụng:**")
                st.json(debug_info["applied_mapping"])
        
        # Hướng dẫn khắc phục
        st.markdown("### 💡 Hướng Dẫn Khắc Phục:")
        st.info("""
        **Kiểm tra đáp án:**
        - Format đúng: `1. A`, `2. B`, `3. AC`
        - Mỗi dòng một câu
        - Số thứ tự liên tục từ 1
        
        **Kiểm tra file DOCX:**
        - Câu hỏi bắt đầu: `Câu 1.` hoặc `1.`
        - Mỗi câu có 4 lựa chọn A, B, C, D
        - Số thứ tự khớp với đáp án
        """)
        
        return
    
    # Header thành công
    st.success("🎉 **Tạo Quiz Thành Công!**")
    
    # Thống kê tổng quan
    stats = results.get("statistics", {})
    agent_info = results.get("agent_info", {})
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Đáp Án", len(results.get("parsed_answers", {})))
    with col2:
        st.metric("📄 Câu Hỏi", len(results.get("question_blocks", {})))
    with col3:
        st.metric("✅ Hoàn Thành", len(results.get("compiled_questions", [])))
    with col4:
        success_rate = stats.get("success_rate", "N/A")
        st.metric("🎯 Tỷ Lệ", success_rate)
    
    # Thông tin chi tiết
    if stats:
        st.markdown("**📊 Thống Kê Chi Tiết:**")
        st.json(stats)
    
    # Danh sách câu hỏi
    compiled_questions = results.get("compiled_questions", [])
    
    if compiled_questions:
        st.markdown("---")
        st.markdown("### 📋 Danh Sách Câu Hỏi")
        
        # Nút download
        quiz_json = json.dumps(compiled_questions, ensure_ascii=False, indent=2)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"QuizForce_AI_{timestamp}.json"
        
        st.download_button(
            "💾 Tải Xuống File JSON",
            data=quiz_json,
            file_name=filename,
            mime="application/json",
            use_container_width=True,
            type="primary"
        )
        
        # Preview câu hỏi
        st.markdown(f"**Xem trước ({len(compiled_questions)} câu hỏi):**")
        
        # Show first 3 questions
        for i, question in enumerate(compiled_questions[:3]):
            so_cau = question.get('so_cau', i+1)
            cau_hoi = question.get('cau_hoi', 'Không có câu hỏi')
            
            with st.expander(f"Câu {so_cau}: {cau_hoi[:60]}..."):
                st.markdown(f"**Câu hỏi:** {cau_hoi}")
                
                choices = question.get('lua_chon', {})
                for choice, content in choices.items():
                    st.write(f"**{choice}.** {content}")
                
                dap_an = question.get('dap_an', 'N/A')
                st.markdown(f"**🎯 Đáp án đúng:** `{dap_an}`")
                
                # Thông tin thêm
                do_kho = question.get('do_kho', 'N/A')
                mon_hoc = question.get('mon_hoc', 'N/A')
                st.caption(f"Độ khó: {do_kho} | Môn học: {mon_hoc}")
        
        if len(compiled_questions) > 3:
            st.info(f"... và {len(compiled_questions) - 3} câu hỏi khác trong file JSON")
    
    else:
        st.warning("⚠️ Không có câu hỏi nào được tạo thành công")
    
    # Debug info
    with st.expander("🔍 Thông Tin Debug (Dành Cho Developer)"):
        st.write("**Agent Info:**")
        st.json(results.get("agent_info", {}))
        
        debug_info = results.get("debug_info", {})
        if debug_info:
            st.write("**Debug Info:**")
            st.json(debug_info)
        
        st.write("**Raw Parsed Answers:**")
        parsed_answers = results.get("parsed_answers", {})
        st.write(f"Tổng số: {len(parsed_answers)}")
        st.json(dict(list(parsed_answers.items())[:10]))  # Hiển thị 10 đầu tiên
        
        st.write("**Question Blocks Info:**")
        question_blocks = results.get("question_blocks", {})
        st.write(f"Tổng số: {len(question_blocks)}")
        sample_questions = {k: v[:100] + "..." if len(v) > 100 else v 
                          for k, v in list(question_blocks.items())[:5]}
        st.json(sample_questions)

def render_footer():
    """Render footer thông tin."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 1rem;'>
        <p><strong>QuizForce AI v1.0</strong> - Hệ thống tạo quiz thông minh cho giáo dục Việt Nam</p>
        <p>Powered by Google Gemini AI | Designed for Vietnamese Education System</p>
        <p>© 2024 - Phát triển bởi AI Agent chuyên nghiệp</p>
    </div>
    """, unsafe_allow_html=True)

def render_quiz_test_page():
    """Render trang làm bài kiểm tra - tích hợp trực tiếp."""
    # Initialize engine
    if 'quiz_engine' not in st.session_state:
        try:
            from backend.quiz_test_engine import QuizTestEngine
        except ImportError:
            try:
                from test.backend.quiz_test_engine import QuizTestEngine
            except ImportError as e:
                st.error(f"❌ Lỗi import QuizTestEngine: {e}")
                st.info("Module quiz_test_engine chưa được tạo. Tính năng này sẽ khả dụng sau.")
                return
        
        st.session_state.quiz_engine = QuizTestEngine()
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%); border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>📝 QuizForce AI - Làm Bài Kiểm Tra</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0;'>Hệ Thống Kiểm Tra Trực Tuyến Chuyên Nghiệp</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if in test session
    if 'current_session_id' in st.session_state and st.session_state.current_session_id:
        render_test_interface()
    else:
        render_test_setup()

def render_test_setup():
    """Render giao diện thiết lập bài kiểm tra."""
    st.markdown("## 🎯 Thiết Lập Bài Kiểm Tra")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Phần nhập thông tin
        st.markdown("### 👨‍🎓 Thông Tin Học Sinh")
        
        student_name = st.text_input(
            "Họ và tên:",
            placeholder="Nguyễn Văn A",
            help="Nhập họ tên đầy đủ của học sinh"
        )
        
        test_title = st.text_input(
            "Tên bài kiểm tra:",
            placeholder="Kiểm tra Toán học - Chương 1",
            help="Đặt tên cho bài kiểm tra này"
        )
        
        st.markdown("### 📚 Tải Câu Hỏi")
        
        # Tabs cho các cách tải câu hỏi
        source_tabs = st.tabs(["📄 Upload File JSON", "🔄 Từ Quiz Đã Tạo"])
        
        questions_data = None
        
        with source_tabs[0]:
            st.markdown("**Upload file JSON chứa câu hỏi:**")
            uploaded_file = st.file_uploader(
                "Chọn file JSON:",
                type=['json'],
                help="File JSON được tạo từ QuizMaster AI",
                key="test_json_upload"
            )
            
            if uploaded_file:
                try:
                    questions_data = json.load(uploaded_file)
                    st.success(f"✅ Đã tải {len(questions_data)} câu hỏi từ file JSON")
                    
                    # Preview
                    with st.expander("👀 Xem trước câu hỏi"):
                        for i, q in enumerate(questions_data[:3]):
                            st.write(f"**Câu {q.get('so_cau', i+1)}:** {q.get('cau_hoi', '')[:100]}...")
                        if len(questions_data) > 3:
                            st.info(f"... và {len(questions_data) - 3} câu hỏi khác")
                            
                except Exception as e:
                    st.error(f"❌ Lỗi đọc file JSON: {str(e)}")
        
        with source_tabs[1]:
            st.markdown("**Sử dụng câu hỏi từ quiz đã tạo:**")
            
            if 'quiz_results' in st.session_state and st.session_state.quiz_results:
                if st.session_state.quiz_results.get('success') and st.session_state.quiz_results.get('compiled_questions'):
                    if st.button("🔄 Sử Dụng Quiz Đã Tạo", use_container_width=True):
                        questions_data = st.session_state.quiz_results['compiled_questions']
                        st.session_state.selected_quiz_data = questions_data
                        st.rerun()
                    
                    # Kiểm tra nếu đã chọn
                    if 'selected_quiz_data' in st.session_state:
                        questions_data = st.session_state.selected_quiz_data
                        st.success(f"✅ Sử dụng {len(questions_data)} câu hỏi từ quiz vừa tạo")
                        
                        # Preview
                        with st.expander("👀 Xem trước câu hỏi"):
                            for i, q in enumerate(questions_data[:3]):
                                st.write(f"**Câu {q.get('so_cau', i+1)}:** {q.get('cau_hoi', '')[:100]}...")
                            if len(questions_data) > 3:
                                st.info(f"... và {len(questions_data) - 3} câu hỏi khác")
                else:
                    st.warning("⚠️ Quiz chưa được tạo thành công. Vui lòng tạo quiz trước.")
            else:
                st.info("ℹ️ Chưa có quiz nào được tạo. Hãy tạo quiz ở trang chính trước.")
    
    with col2:
        # Cấu hình bài kiểm tra
        st.markdown("### ⚙️ Cấu Hình Bài Kiểm Tra")
        
        time_limit = st.selectbox(
            "Thời gian làm bài:",
            [15, 30, 45, 60, 90, 120],
            index=3,
            format_func=lambda x: f"{x} phút",
            help="Chọn thời gian làm bài phù hợp"
        )
        
        shuffle_questions = st.checkbox(
            "🔀 Trộn thứ tự câu hỏi",
            value=True,
            help="Câu hỏi sẽ hiển thị ngẫu nhiên"
        )
        
        shuffle_answers = st.checkbox(
            "🎲 Trộn thứ tự đáp án",
            value=True,
            help="Các lựa chọn A, B, C, D sẽ được trộn ngẫu nhiên"
        )
        
        st.markdown("### ℹ️ Hướng Dẫn")
        st.info("""
        **Quy tắc làm bài:**
        - Đọc kỹ đề bài trước khi chọn đáp án
        - Có thể quay lại câu đã làm để sửa
        - Thời gian sẽ tự động dừng khi hết giờ
        - Nhấn "Hoàn thành" để nộp bài
        
        **Lưu ý:**
        - Không được làm bài cùng lúc nhiều tab
        - Đảm bảo kết nối internet ổn định
        """)
    
    # Nút bắt đầu
    st.markdown("---")
    
    can_start = (
        student_name and student_name.strip() and
        test_title and test_title.strip() and
        questions_data and len(questions_data) > 0
    )
    
    if not can_start:
        if not student_name:
            st.warning("⚠️ Vui lòng nhập họ tên học sinh")
        elif not test_title:
            st.warning("⚠️ Vui lòng nhập tên bài kiểm tra")
        elif not questions_data:
            st.warning("⚠️ Vui lòng tải câu hỏi từ file JSON hoặc quiz đã tạo")
    else:
        st.success("✅ Đã sẵn sàng bắt đầu làm bài!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚀 Bắt Đầu Làm Bài Kiểm Tra",
            disabled=not can_start,
            use_container_width=True,
            type="primary"
        ):
            if can_start:
                start_new_test(student_name, test_title, questions_data, time_limit, shuffle_questions, shuffle_answers)

def start_new_test(student_name: str, test_title: str, questions_data: list, 
                  time_limit: int, shuffle_questions: bool, shuffle_answers: bool):
    """Bắt đầu bài kiểm tra mới."""
    try:
        # Load questions
        engine = st.session_state.quiz_engine
        questions = engine.load_questions_from_json(questions_data)
        
        if not questions:
            st.error("❌ Không thể tải câu hỏi. Vui lòng kiểm tra file JSON.")
            return
        
        # Create session
        session_id = engine.create_test_session(
            student_name=student_name,
            test_title=test_title,
            questions=questions,
            time_limit=time_limit,
            shuffle_questions=shuffle_questions,
            shuffle_answers=shuffle_answers
        )
        
        # Save session to streamlit state
        st.session_state.current_session_id = session_id
        
        st.success("🎉 Bài kiểm tra đã được tạo! Đang chuyển hướng...")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Lỗi tạo bài kiểm tra: {str(e)}")

def render_test_interface():
    """Render giao diện làm bài kiểm tra."""
    session_id = st.session_state.current_session_id
    engine = st.session_state.quiz_engine
    
    # Get current question
    current_q = engine.get_current_question(session_id)
    
    if not current_q:
        # Test finished or error
        render_test_completed()
        return
    
    # Test overview in sidebar
    with st.sidebar:
        render_test_sidebar(session_id)
    
    # Main test interface
    render_question_interface(session_id, current_q)

def render_test_sidebar(session_id: str):
    """Render sidebar thông tin bài kiểm tra."""
    engine = st.session_state.quiz_engine
    overview = engine.get_test_overview(session_id)
    
    if not overview:
        return
    
    st.markdown("### 📊 Thông Tin Bài Kiểm Tra")
    
    # Student info
    st.info(f"""
    **Học sinh:** {overview['student_name']}
    **Bài kiểm tra:** {overview['test_title']}
    """)
    
    # Progress
    st.markdown("### 📈 Tiến Độ")
    progress = overview['progress']
    st.progress(progress / 100)
    st.write(f"Đã làm: {overview['answered_questions']}/{overview['total_questions']} câu")
    
    # Time
    st.markdown("### ⏰ Thời Gian")
    time_remaining = overview['time_remaining']
    
    if time_remaining > 0:
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        
        # Warning colors
        if time_remaining <= 300:  # 5 minutes
            st.error(f"⚠️ Còn lại: {minutes:02d}:{seconds:02d}")
        elif time_remaining <= 600:  # 10 minutes
            st.warning(f"⏱️ Còn lại: {minutes:02d}:{seconds:02d}")
        else:
            st.success(f"⏱️ Còn lại: {minutes:02d}:{seconds:02d}")
    else:
        st.error("⏰ Hết thời gian!")
    
    st.write(f"Đã làm: {overview['time_elapsed']}")
    
    # Question navigator
    st.markdown("### 🗂️ Điều Hướng Câu Hỏi")
    
    # Grid of question numbers
    cols_per_row = 5
    total_questions = overview['total_questions']
    
    for row_start in range(1, total_questions + 1, cols_per_row):
        cols = st.columns(cols_per_row)
        
        for i, col in enumerate(cols):
            q_num = row_start + i
            if q_num <= total_questions:
                # Color coding
                if q_num in [q.so_cau for q in engine.active_sessions[session_id].questions 
                           if q.so_cau in engine.active_sessions[session_id].answers]:
                    button_type = "secondary"  # Answered
                    label = f"✅{q_num}"
                else:
                    button_type = "primary"  # Not answered
                    label = f"{q_num}"
                
                if col.button(label, key=f"nav_{q_num}", use_container_width=True):
                    engine.goto_question(session_id, q_num)
                    st.rerun()
    
    # Quick actions
    st.markdown("### 🎯 Hành Động")
    
    if st.button("📋 Xem Tổng Quan", use_container_width=True):
        st.session_state.show_overview = True
        st.rerun()
    
    if st.button("🏁 Hoàn Thành Bài Kiểm Tra", use_container_width=True, type="primary"):
        if st.session_state.get('confirm_finish'):
            result = engine.finish_test(session_id)
            st.session_state.test_result = result
            st.session_state.current_session_id = None
            st.rerun()
        else:
            st.session_state.confirm_finish = True
            st.rerun()
    
    if st.session_state.get('confirm_finish'):
        st.warning("⚠️ Bạn có chắc muốn hoàn thành bài kiểm tra?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Có", use_container_width=True, key="confirm_yes"):
                result = engine.finish_test(session_id)
                st.session_state.test_result = result
                st.session_state.current_session_id = None
                st.session_state.confirm_finish = False
                st.rerun()
        with col2:
            if st.button("❌ Không", use_container_width=True, key="confirm_no"):
                st.session_state.confirm_finish = False
                st.rerun()

def render_question_interface(session_id: str, current_q: dict):
    """Render giao diện câu hỏi hiện tại."""
    engine = st.session_state.quiz_engine
    question_data = current_q['question_data']
    
    # Question header
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"### Câu {current_q['question_number']}/{current_q['total_questions']}")
    
    with col2:
        # Time remaining (auto-refresh)
        time_container = st.empty()
        time_remaining = current_q['time_remaining']
        if time_remaining > 0:
            minutes = time_remaining // 60
            seconds = time_remaining % 60
            time_container.markdown(f"⏱️ **Thời gian còn lại: {minutes:02d}:{seconds:02d}**")
        else:
            time_container.error("⏰ **Hết thời gian!**")
    
    with col3:
        progress = current_q['progress']
        st.markdown(f"📊 **Tiến độ: {progress:.1f}%**")
    
    st.markdown("---")
    
    # Question content
    st.markdown("### 📝 Câu Hỏi")
    
    # Display question with nice formatting
    question_text = question_data['cau_hoi']
    st.markdown(f"""
    <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #007bff; margin-bottom: 1rem;'>
        <h4 style='margin: 0; color: #495057;'>{question_text}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer choices
    st.markdown("### 🔤 Lựa Chọn Đáp Án")
    
    choices = question_data['lua_chon']
    current_answer = current_q['current_answer']
    
    # Display choices as radio buttons
    answer_options = []
    for choice, content in choices.items():
        answer_options.append(f"{choice}. {content}")
    
    # Find current selection index
    current_index = None
    if current_answer:
        for i, choice in enumerate(choices.keys()):
            if choice == current_answer:
                current_index = i
                break
    
    selected_answer = st.radio(
        "Chọn đáp án:",
        answer_options,
        index=current_index,
        key=f"answer_{current_q['question_number']}"
    )
    
    # Extract answer letter
    if selected_answer:
        selected_letter = selected_answer.split('.')[0]
        # Submit answer
        engine.submit_answer(session_id, selected_letter)
    
    # Question metadata
    col1, col2 = st.columns(2)
    with col1:
        do_kho = question_data.get('do_kho', 'trung_binh')
        difficulty_color = {
            'de': '🟢',
            'trung_binh': '🟡', 
            'kho': '🔴'
        }.get(do_kho, '🟡')
        st.caption(f"{difficulty_color} Độ khó: {do_kho}")
    
    with col2:
        mon_hoc = question_data.get('mon_hoc', 'auto_detect')
        st.caption(f"📚 Môn học: {mon_hoc}")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("⬅️ Câu Trước", disabled=current_q['question_number'] == 1, key="prev_btn"):
            engine.previous_question(session_id)
            st.rerun()
    
    with col2:
        if st.button("📋 Tổng Quan", key="overview_btn"):
            st.session_state.show_overview = True
            st.rerun()
    
    with col3:
        if st.button("🔄 Làm Mới", key="refresh_btn"):
            st.rerun()
    
    with col4:
        if current_q['question_number'] < current_q['total_questions']:
            if st.button("➡️ Câu Tiếp", key="next_btn"):
                engine.next_question(session_id)
                st.rerun()
        else:
            if st.button("🏁 Hoàn Thành", type="primary", key="finish_btn"):
                st.session_state.confirm_finish = True
                st.rerun()
    
    # Auto-refresh for timer (giảm frequency để tránh lag)
    if time_remaining > 0 and time_remaining % 5 == 0:  # Refresh mỗi 5 giây
        time.sleep(1)
        st.rerun()

def render_test_completed():
    """Render kết quả bài kiểm tra."""
    if 'test_result' not in st.session_state:
        st.error("❌ Không tìm thấy kết quả bài kiểm tra")
        if st.button("🏠 Về Trang Chủ"):
            st.session_state.current_session_id = None
            st.rerun()
        return
    
    result = st.session_state.test_result
    
    # Header
    st.markdown("## 🎉 Hoàn Thành Bài Kiểm Tra!")
    
    # Overall results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Tổng Số Câu", result.total_questions)
    
    with col2:
        st.metric("✅ Câu Đúng", result.correct_answers)
    
    with col3:
        st.metric("❌ Câu Sai", result.wrong_answers)
    
    with col4:
        st.metric("🎯 Điểm Số", f"{result.score}/10")
    
    # Score visualization
    percentage = result.percentage
    if percentage >= 80:
        score_color = "success"
        score_emoji = "🏆"
        score_text = "Xuất sắc!"
    elif percentage >= 70:
        score_color = "info"
        score_emoji = "🎖️"
        score_text = "Khá tốt!"
    elif percentage >= 50:
        score_color = "warning"
        score_emoji = "📈"
        score_text = "Trung bình"
    else:
        score_color = "error"
        score_emoji = "📚"
        score_text = "Cần cố gắng hơn"
    
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 2rem 0;'>
        <h1 style='color: white; margin: 0; font-size: 3rem;'>{score_emoji}</h1>
        <h2 style='color: white; margin: 0.5rem 0;'>{result.percentage:.1f}% - {score_text}</h2>
        <p style='color: #f0f0f0; margin: 0;'>Thời gian làm bài: {result.time_taken}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("### 📊 Chi Tiết Kết Quả")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_filter = st.selectbox(
            "Hiển thị:",
            ["Tất cả", "Chỉ câu đúng", "Chỉ câu sai"],
            key="result_filter"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sắp xếp theo:",
            ["Số câu", "Kết quả", "Độ khó"],
            key="result_sort"
        )
    
    # Filter and sort results
    detailed = result.detailed_results
    
    if show_filter == "Chỉ câu đúng":
        detailed = [r for r in detailed if r['ket_qua'] == 'Đúng']
    elif show_filter == "Chỉ câu sai":
        detailed = [r for r in detailed if r['ket_qua'] == 'Sai']
    
    if sort_by == "Kết quả":
        detailed = sorted(detailed, key=lambda x: x['ket_qua'])
    elif sort_by == "Độ khó":
        detailed = sorted(detailed, key=lambda x: x['do_kho'])
    
    # Display results
    for i, item in enumerate(detailed):
        with st.expander(f"Câu {item['so_cau']}: {item['ket_qua']} {'✅' if item['ket_qua'] == 'Đúng' else '❌'}"):
            st.markdown(f"**Câu hỏi:** {item['cau_hoi']}")
            
            # Show choices
            for choice, content in item['lua_chon'].items():
                if choice == item['dap_an_dung']:
                    st.success(f"✅ **{choice}.** {content} *(Đáp án đúng)*")
                elif choice == item['dap_an_chon']:
                    if item['ket_qua'] == 'Sai':
                        st.error(f"❌ **{choice}.** {content} *(Bạn đã chọn)*")
                    else:
                        st.success(f"✅ **{choice}.** {content} *(Bạn đã chọn)*")
                else:
                    st.write(f"**{choice}.** {content}")
            
            if item['dap_an_chon'] == "Không trả lời":
                st.warning("⚠️ Bạn chưa trả lời câu này")
            
            st.caption(f"Độ khó: {item['do_kho']}")
    
    # Actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Về Trang Chủ", use_container_width=True):
            # Clear session
            st.session_state.current_session_id = None
            st.session_state.test_result = None
            st.session_state.selected_quiz_data = None
            st.rerun()
    
    with col2:
        # Export results as JSON
        result_json = {
            "student_name": result.student_name,
            "test_title": result.test_title,
            "score": result.score,
            "percentage": result.percentage,
            "time_taken": result.time_taken,
            "finish_time": result.finish_time.isoformat(),
            "detailed_results": result.detailed_results
        }
        
        st.download_button(
            "💾 Tải Kết Quả JSON",
            data=json.dumps(result_json, ensure_ascii=False, indent=2),
            file_name=f"ket_qua_{result.student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 Làm Bài Mới", use_container_width=True, type="primary"):
            # Clear session but keep engine
            st.session_state.current_session_id = None
            st.session_state.test_result = None
            st.session_state.selected_quiz_data = None
            st.rerun()

if __name__ == "__main__":
    main()
