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
    """Hiển thị kết quả chuyên nghiệp với thông tin batch processing."""
    
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
    
    # Thống kê tổng quan với batch info
    stats = results.get("statistics", {})
    agent_info = results.get("agent_info", {})
    batch_info = agent_info.get("batch_info", {})
    
    # Enhanced metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📝 Đáp Án", len(results.get("parsed_answers", {})))
    with col2:
        st.metric("📄 Câu Hỏi", len(results.get("question_blocks", {})))
    with col3:
        st.metric("✅ Hoàn Thành", len(results.get("compiled_questions", [])))
    with col4:
        success_rate = stats.get("success_rate", "N/A")
        st.metric("🎯 Tỷ Lệ", success_rate)
    with col5:
        total_batches = batch_info.get("total_batches", 0)
        st.metric("📦 Batch", f"{total_batches}")
    
    # Batch processing info
    if batch_info:
        st.markdown("**🔄 Thông Tin Batch Processing:**")
        
        batch_cols = st.columns(4)
        with batch_cols[0]:
            st.metric("📦 Total Batches", batch_info.get("total_batches", 0))
        with batch_cols[1]:
            st.metric("✅ Completed", batch_info.get("completed_batches", 0))
        with batch_cols[2]:
            st.metric("🔧 Recovered", batch_info.get("recovered_questions", 0))
        with batch_cols[3]:
            st.metric("❌ Failed", batch_info.get("failed_questions", 0))
    
    # Danh sách câu hỏi với storage management
    compiled_questions = results.get("compiled_questions", [])
    
    if compiled_questions:
        st.markdown("---")
        st.markdown("### 📋 Quản Lý Quiz")
        
        # Storage and download options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Lưu vào storage
            if 'quiz_engine' not in st.session_state:
                try:
                    from backend.quiz_test_engine import QuizTestEngine
                except ImportError:
                    try:
                        from test.backend.quiz_test_engine import QuizTestEngine
                    except ImportError:
                        st.warning("⚠️ Không thể lưu quiz vào storage")
                        QuizTestEngine = None
                
                if QuizTestEngine:
                    st.session_state.quiz_engine = QuizTestEngine
            
            if 'quiz_engine' in st.session_state:
                quiz_name = st.text_input(
                    "💾 Tên quiz để lưu:",
                    placeholder="VD: Toán 12 - Chương 1",
                    help="Đặt tên để lưu quiz vào thư viện"
                )
                
                if st.button("💾 Lưu vào Thư Viện", use_container_width=True):
                    if quiz_name and quiz_name.strip():
                        engine = st.session_state.quiz_engine
                        saved_name = engine.save_quiz_to_storage(compiled_questions, quiz_name.strip())
                        if saved_name:
                            st.success(f"✅ Đã lưu quiz '{saved_name}'!")
                            st.session_state.refresh_saved_quizzes = True
                        else:
                            st.error("❌ Lỗi lưu quiz")
                    else:
                        st.error("⚠️ Vui lòng nhập tên quiz")
        
        with col2:
            # Download JSON
            quiz_json = json.dumps(compiled_questions, ensure_ascii=False, indent=2)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"QuizForce_AI_{timestamp}.json"
            
            st.download_button(
                "📥 Tải Xuống JSON",
                data=quiz_json,
                file_name=filename,
                mime="application/json",
                use_container_width=True,
                type="primary"
            )
        
        with col3:
            # Quick test button
            if st.button("🚀 Làm Bài Ngay", use_container_width=True, type="secondary"):
                st.session_state.selected_quiz_data = compiled_questions
                st.session_state.page = "📝 Làm Bài Kiểm Tra"
                st.rerun()
        
        # Quiz editor
        render_quiz_editor(compiled_questions)
    
    else:
        st.warning("⚠️ Không có câu hỏi nào được tạo thành công")

def render_quiz_editor(questions: list):
    """Render quiz editor với khả năng chỉnh sửa và thêm ảnh."""
    st.markdown("### ✏️ Chỉnh Sửa Quiz")
    
    if not questions:
        st.info("Không có câu hỏi nào để chỉnh sửa.")
        return
    
    # Question selector
    question_options = [f"Câu {q.get('so_cau', i+1)}: {q.get('cau_hoi', '')[:50]}..." 
                       for i, q in enumerate(questions)]
    
    selected_idx = st.selectbox(
        "Chọn câu hỏi để chỉnh sửa:",
        range(len(questions)),
        format_func=lambda x: question_options[x],
        key="quiz_editor_selector"
    )
    
    if selected_idx is not None:
        question = questions[selected_idx]
        
        with st.expander(f"✏️ Chỉnh sửa câu {question.get('so_cau', selected_idx+1)}", expanded=True):
            
            # Edit question text
            new_question_text = st.text_area(
                "Nội dung câu hỏi:",
                value=question.get('cau_hoi', ''),
                height=100,
                key=f"edit_question_{selected_idx}"
            )
            
            # Edit choices
            st.markdown("**Chỉnh sửa lựa chọn:**")
            choices = question.get('lua_chon', {})
            new_choices = {}
            
            choice_cols = st.columns(2)
            for i, (choice, content) in enumerate(choices.items()):
                col = choice_cols[i % 2]
                with col:
                    new_choices[choice] = st.text_area(
                        f"Lựa chọn {choice}:",
                        value=content,
                        height=60,
                        key=f"edit_choice_{selected_idx}_{choice}"
                    )
            
            # Edit correct answer
            col1, col2 = st.columns(2)
            with col1:
                current_answer = question.get('dap_an', 'A')
                new_answer = st.selectbox(
                    "Đáp án đúng:",
                    list(choices.keys()),
                    index=list(choices.keys()).index(current_answer) if current_answer in choices else 0,
                    key=f"edit_answer_{selected_idx}"
                )
            
            with col2:
                difficulty_options = ['de', 'trung_binh', 'kho']
                current_difficulty = question.get('do_kho', 'trung_binh')
                new_difficulty = st.selectbox(
                    "Độ khó:",
                    difficulty_options,
                    index=difficulty_options.index(current_difficulty) if current_difficulty in difficulty_options else 1,
                    key=f"edit_difficulty_{selected_idx}"
                )
            
            # Image management
            st.markdown("**📷 Quản lý hình ảnh:**")
            
            # Show existing images
            existing_images = question.get('images', [])
            if existing_images:
                st.markdown("Hình ảnh hiện tại:")
                for img in existing_images:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"📷 {img.get('name', 'Unknown')}")
                    with col2:
                        if st.button("🗑️", key=f"delete_img_{selected_idx}_{img.get('name', '')}"):
                            # Remove image logic would go here
                            st.info("Tính năng xóa ảnh sẽ có trong phiên bản tiếp theo")
            
            # Add new image
            uploaded_image = st.file_uploader(
                "Thêm hình ảnh mới:",
                type=['png', 'jpg', 'jpeg', 'gif'],
                key=f"upload_image_{selected_idx}"
            )
            
            if uploaded_image:
                st.image(uploaded_image, caption="Ảnh mới", width=200)
                
                if st.button("➕ Thêm ảnh này", key=f"add_image_{selected_idx}"):
                    # Add image logic
                    if 'images' not in question:
                        question['images'] = []
                    
                    question['images'].append({
                        'name': uploaded_image.name,
                        'data': uploaded_image.getvalue(),
                        'type': uploaded_image.type
                    })
                    
                    st.success(f"✅ Đã thêm ảnh {uploaded_image.name}")
                    st.rerun()
            
            # Save changes
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Lưu thay đổi", key=f"save_changes_{selected_idx}", type="primary"):
                    # Update question
                    questions[selected_idx]['cau_hoi'] = new_question_text
                    questions[selected_idx]['lua_chon'] = new_choices
                    questions[selected_idx]['dap_an'] = new_answer
                    questions[selected_idx]['do_kho'] = new_difficulty
                    
                    st.success("✅ Đã lưu thay đổi!")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Reset", key=f"reset_changes_{selected_idx}"):
                    st.rerun()

def render_test_setup():
    """Render giao diện thiết lập bài kiểm tra với quiz storage."""
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
        
        # Tabs cho các cách tải câu hỏi với quiz storage
        source_tabs = st.tabs(["📄 Upload File JSON", "🔄 Từ Quiz Đã Tạo", "📚 Thư Viện Quiz"])
        
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
                    
                    # Preview with images
                    with st.expander("👀 Xem trước câu hỏi"):
                        for i, q in enumerate(questions_data[:3]):
                            st.write(f"**Câu {q.get('so_cau', i+1)}:** {q.get('cau_hoi', '')[:100]}...")
                            
                            # Show images if any
                            if q.get('images'):
                                st.caption(f"📷 {len(q['images'])} hình ảnh đính kèm")
                        
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
                                if q.get('images'):
                                    st.caption(f"📷 {len(q.images)} hình ảnh")
                            if len(questions_data) > 3:
                                st.info(f"... và {len(questions_data) - 3} câu hỏi khác")
                else:
                    st.warning("⚠️ Quiz chưa được tạo thành công. Vui lòng tạo quiz trước.")
            else:
                st.info("ℹ️ Chưa có quiz nào được tạo. Hãy tạo quiz ở trang chính trước.")
        
        with source_tabs[2]:
            st.markdown("**Chọn từ thư viện quiz đã lưu:**")
            
            # Initialize engine
            if 'quiz_engine' not in st.session_state:
                try:
                    from backend.quiz_test_engine import QuizTestEngine
                except ImportError:
                    try:
                        from test.backend.quiz_test_engine import QuizTestEngine
                    except ImportError:
                        st.error("❌ Không thể tải engine")
                        QuizTestEngine = None
                
                if QuizTestEngine:
                    st.session_state.quiz_engine = QuizTestEngine
            
            if 'quiz_engine' in st.session_state:
                engine = st.session_state.quiz_engine
                
                # Management buttons
                col_refresh, col_delete = st.columns([1, 1])
                with col_refresh:
                    if st.button("🔄 Làm Mới Danh Sách", use_container_width=True):
                        st.session_state.refresh_saved_quizzes = True
                        st.rerun()
                
                # Get saved quizzes
                saved_quizzes = engine.get_saved_quizzes()
                
                if saved_quizzes:
                    # Quiz selection with enhanced info
                    quiz_options = []
                    for name, info in saved_quizzes.items():
                        quiz_options.append(f"{name} ({info['questions_count']} câu - {info['size']} - {info['created_time'].strftime('%d/%m/%Y')})")
                    
                    selected_quiz_display = st.selectbox(
                        "Chọn quiz:",
                        ["-- Chọn quiz --"] + quiz_options,
                        help="Chọn quiz từ thư viện để làm bài"
                    )
                    
                    if selected_quiz_display and selected_quiz_display != "-- Chọn quiz --":
                        selected_quiz_name = selected_quiz_display.split(" (")[0]
                        
                        # Load and preview quiz
                        col_load, col_preview = st.columns(2)
                        
                        with col_load:
                            if st.button("📚 Tải Quiz Này", use_container_width=True):
                                loaded_questions = engine.load_quiz_from_storage(selected_quiz_name)
                                if loaded_questions:
                                    # Convert to JSON format
                                    from dataclasses import asdict
                                    questions_data = [asdict(q) for q in loaded_questions]
                                    st.session_state.selected_quiz_data = questions_data
                                    st.success(f"✅ Đã tải quiz '{selected_quiz_name}' ({len(questions_data)} câu)")
                                    st.rerun()
                                else:
                                    st.error("❌ Không thể tải quiz")
                        
                        with col_preview:
                            if st.button("👀 Xem Trước", use_container_width=True):
                                loaded_questions = engine.load_quiz_from_storage(selected_quiz_name)
                                if loaded_questions:
                                    st.session_state.preview_quiz = loaded_questions
                                    st.rerun()
                        
                        # Quiz info
                        if selected_quiz_name in saved_quizzes:
                            info = saved_quizzes[selected_quiz_name]
                            st.info(f"""
                            **📊 Thông tin quiz:**
                            - 📝 Số câu hỏi: {info['questions_count']}
                            - 💾 Kích thước: {info['size']}
                            - 📅 Ngày tạo: {info['created_time'].strftime('%d/%m/%Y %H:%M')}
                            """)
                        
                        # Delete quiz
                        with col_delete:
                            if st.button("🗑️ Xóa Quiz", use_container_width=True):
                                if engine.delete_quiz_from_storage(selected_quiz_name):
                                    st.success(f"✅ Đã xóa quiz '{selected_quiz_name}'")
                                    st.rerun()
                                else:
                                    st.error("❌ Không thể xóa quiz")
                
                else:
                    st.info("📚 Chưa có quiz nào trong thư viện. Hãy tạo và lưu quiz ở trang 'Tạo Quiz'.")
                
                # Check if quiz selected from library
                if 'selected_quiz_data' in st.session_state and not questions_data:
                    questions_data = st.session_state.selected_quiz_data
                    st.success(f"✅ Đã chọn quiz từ thư viện ({len(questions_data)} câu)")
        
        # Preview quiz if requested
        if 'preview_quiz' in st.session_state:
            with st.expander("👀 Xem trước quiz đã chọn", expanded=True):
                preview_questions = st.session_state.preview_quiz
                for i, q in enumerate(preview_questions[:5]):
                    st.markdown(f"**Câu {q.so_cau}:** {q.cau_hoi[:100]}...")
                    if hasattr(q, 'images') and q.images:
                        st.caption(f"📷 {len(q.images)} hình ảnh đính kèm")
                
                if len(preview_questions) > 5:
                    st.info(f"... và {len(preview_questions) - 5} câu hỏi khác")
                
                if st.button("❌ Đóng xem trước"):
                    del st.session_state.preview_quiz
                    st.rerun()
    
    with col2:
        # Cấu hình bài kiểm tra với enhanced options
        st.markdown("### ⚙️ Cấu Hình Bài Kiểm Tra")
        
        # Test mode selection
        test_mode = st.radio(
            "Chế độ làm bài:",
            ["🎯 Kiểm tra (Exam)", "📚 Ôn luyện (Practice)"],
            help="Kiểm tra: giới hạn thời gian, không hiển thị đáp án. Ôn luyện: không giới hạn thời gian, hiển thị kết quả ngay"
        )
        
        test_mode_value = "exam" if "Kiểm tra" in test_mode else "practice"
        
        # Time limit (only for exam mode)
        if test_mode_value == "exam":
            time_limit = st.selectbox(
                "Thời gian làm bài:",
                [15, 30, 45, 60, 90, 120],
                index=3,
                format_func=lambda x: f"{x} phút",
                help="Chọn thời gian làm bài phù hợp"
            )
        else:
            time_limit = 9999  # Unlimited for practice mode
            st.info("⏰ Chế độ ôn luyện: Không giới hạn thời gian")
        
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
        
        show_images = st.checkbox(
            "📷 Hiển thị hình ảnh",
            value=True,
            help="Hiển thị hình ảnh đính kèm trong câu hỏi"
        )
        
        st.markdown("### ℹ️ Hướng Dẫn")
        
        if test_mode_value == "exam":
            st.info("""
            **🎯 Chế độ Kiểm Tra:**
            - ⏰ Có giới hạn thời gian
            - 🔒 Không hiển thị đáp án khi làm
            - 📊 Kết quả hiển thị sau khi hoàn thành
            - 🎯 Phù hợp cho bài kiểm tra chính thức
            """)
        else:
            st.success("""
            **📚 Chế độ Ôn Luyện:**
            - ⏰ Không giới hạn thời gian
            - ✅ Hiển thị ngay đáp án đúng/sai
            - 🟢 Màu xanh = đúng, 🔴 màu đỏ = sai
            - 📖 Phù hợp cho ôn tập, học tập
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
            st.warning("⚠️ Vui lòng tải câu hỏi từ file JSON, quiz đã tạo hoặc thư viện")
    else:
        mode_text = "Kiểm tra" if test_mode_value == "exam" else "Ôn luyện"
        st.success(f"✅ Đã sẵn sàng bắt đầu {mode_text.lower()}!")
        
        # Show question count and image info
        images_count = sum(1 for q in questions_data if q.get('images'))
        if images_count > 0:
            st.info(f"📷 Có {images_count} câu hỏi chứa hình ảnh")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        button_text = "🚀 Bắt Đầu Làm Bài Kiểm Tra" if test_mode_value == "exam" else "📚 Bắt Đầu Ôn Luyện"
        
        if st.button(
            button_text,
            disabled=not can_start,
            use_container_width=True,
            type="primary"
        ):
            if can_start:
                start_new_test(student_name, test_title, questions_data, time_limit, 
                             shuffle_questions, shuffle_answers, test_mode_value, show_images)

def start_new_test(student_name: str, test_title: str, questions_data: list, 
                  time_limit: int, shuffle_questions: bool, shuffle_answers: bool, 
                  test_mode: str = "exam", show_images: bool = True):
    """Bắt đầu bài kiểm tra mới với enhanced options."""
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
            shuffle_answers=shuffle_answers,
            test_mode=test_mode
        )
        
        # Save session to streamlit state
        st.session_state.current_session_id = session_id
        st.session_state.show_images = show_images
        
        mode_text = "kiểm tra" if test_mode == "exam" else "ôn luyện"
        st.success(f"🎉 Phiên {mode_text} đã được tạo! Đang chuyển hướng...")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Lỗi tạo phiên làm bài: {str(e)}")

def render_question_interface(session_id: str, current_q: dict):
    """Render giao diện câu hỏi với feedback cho practice mode và hiển thị ảnh."""
    engine = st.session_state.quiz_engine
    question_data = current_q['question_data']
    test_mode = current_q.get('test_mode', 'exam')
    
    # Question header
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        mode_emoji = "📚" if test_mode == "practice" else "🎯"
        mode_text = "Ôn luyện" if test_mode == "practice" else "Kiểm tra"
        st.markdown(f"### {mode_emoji} Câu {current_q['question_number']}/{current_q['total_questions']}")
        st.caption(f"Chế độ: {mode_text}")
    
    with col2:
        # Time remaining (chỉ hiển thị cho exam mode)
        if test_mode == "exam":
            time_container = st.empty()
            time_remaining = current_q['time_remaining']
            if time_remaining > 0:
                minutes = time_remaining // 60
                seconds = time_remaining % 60
                time_container.markdown(f"⏱️ **Thời gian còn lại: {minutes:02d}:{seconds:02d}**")
            else:
                time_container.error("⏰ **Hết thời gian!**")
        else:
            st.markdown("⏰ **Không giới hạn thời gian**")
    
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
    
    # Display images if any and enabled
    if st.session_state.get('show_images', True) and question_data.get('images'):
        st.markdown("### 📷 Hình Ảnh Đính Kèm")
        
        image_cols = st.columns(min(len(question_data['images']), 3))
        for i, img_info in enumerate(question_data['images']):
            col = image_cols[i % 3]
            with col:
                try:
                    if 'data' in img_info:
                        # Image data embedded in question
                        st.image(img_info['data'], caption=img_info.get('name', f'Ảnh {i+1}'), width=200)
                    elif 'full_path' in img_info:
                        # Image file path
                        st.image(img_info['full_path'], caption=img_info.get('name', f'Ảnh {i+1}'), width=200)
                except Exception as e:
                    st.warning(f"⚠️ Không thể hiển thị ảnh: {img_info.get('name', f'Ảnh {i+1}')}")
    
    # Answer choices with feedback for practice mode
    st.markdown("### 🔤 Lựa Chọn Đáp Án")
    
    choices = question_data['lua_chon']
    current_answer = current_q['current_answer']
    feedback = current_q.get('feedback')
    
    # Display choices with color coding for practice mode
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
    
    # For practice mode, show feedback after answering
    if test_mode == "practice" and feedback and feedback.get('show_feedback'):
        st.markdown("#### 📋 Phản Hồi Ngay Lập Tức")
        
        # Show choices with color coding
        for choice, content in choices.items():
            is_correct_answer = choice == feedback.get('correct_answer', '').upper()
            is_user_choice = choice == feedback.get('user_answer', '').upper()
            
            if is_correct_answer and is_user_choice:
                st.success(f"✅ **{choice}.** {content} *(Bạn chọn đúng!)*")
            elif is_correct_answer:
                st.success(f"✅ **{choice}.** {content} *(Đáp án đúng)*")
            elif is_user_choice:
                st.error(f"❌ **{choice}.** {content} *(Bạn đã chọn - Sai)*")
            else:
                st.write(f"**{choice}.** {content}")
        
        # Explanation
        if feedback.get('explanation'):
            st.info(f"💡 **Giải thích:** {feedback['explanation']}")
    
    else:
        # Normal radio buttons for exam mode or no answer yet
        selected_answer = st.radio(
            "Chọn đáp án:",
            answer_options,
            index=current_index,
            key=f"answer_{current_q['question_number']}"
        )
        
        # Extract answer letter and submit
        if selected_answer:
            selected_letter = selected_answer.split('.')[0]
            # Submit answer and get feedback
            submit_feedback = engine.submit_answer(session_id, selected_letter)
            
            # For practice mode, trigger rerun to show feedback
            if test_mode == "practice" and submit_feedback.get('show_feedback'):
                st.rerun()
    
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
            if st.button("🏁 Hoàn thành", type="primary", key="finish_btn"):
                st.session_state.confirm_finish = True
                st.rerun()
    
    # Auto-refresh for timer (chỉ cho exam mode)
    if test_mode == "exam" and time_remaining > 0 and time_remaining % 5 == 0:
        time.sleep(1)
        st.rerun()

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
        
        # Tabs cho các cách tải câu hỏi với quiz storage
        source_tabs = st.tabs(["📄 Upload File JSON", "🔄 Từ Quiz Đã Tạo", "📚 Thư Viện Quiz"])
        
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
                    
                    # Preview with images
                    with st.expander("👀 Xem trước câu hỏi"):
                        for i, q in enumerate(questions_data[:3]):
                            st.write(f"**Câu {q.get('so_cau', i+1)}:** {q.get('cau_hoi', '')[:100]}...")
                            
                            # Show images if any
                            if q.get('images'):
                                st.caption(f"📷 {len(q['images'])} hình ảnh đính kèm")
                        
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
                                if q.get('images'):
                                    st.caption(f"📷 {len(q.images)} hình ảnh")
                            if len(questions_data) > 3:
                                st.info(f"... và {len(questions_data) - 3} câu hỏi khác")
                else:
                    st.warning("⚠️ Quiz chưa được tạo thành công. Vui lòng tạo quiz trước.")
            else:
                st.info("ℹ️ Chưa có quiz nào được tạo. Hãy tạo quiz ở trang chính trước.")
        
        with source_tabs[2]:
            st.markdown("**Chọn từ thư viện quiz đã lưu:**")
            
            # Initialize engine
            if 'quiz_engine' not in st.session_state:
                try:
                    from backend.quiz_test_engine import QuizTestEngine
                except ImportError:
                    try:
                        from test.backend.quiz_test_engine import QuizTestEngine
                    except ImportError:
                        st.error("❌ Không thể tải engine")
                        QuizTestEngine = None
                
                if QuizTestEngine:
                    st.session_state.quiz_engine = QuizTestEngine
            
            if 'quiz_engine' in st.session_state:
                engine = st.session_state.quiz_engine
                
                # Management buttons
                col_refresh, col_delete = st.columns([1, 1])
                with col_refresh:
                    if st.button("🔄 Làm Mới Danh Sách", use_container_width=True):
                        st.session_state.refresh_saved_quizzes = True
                        st.rerun()
                
                # Get saved quizzes
                saved_quizzes = engine.get_saved_quizzes()
                
                if saved_quizzes:
                    # Quiz selection with enhanced info
                    quiz_options = []
                    for name, info in saved_quizzes.items():
                        quiz_options.append(f"{name} ({info['questions_count']} câu - {info['size']} - {info['created_time'].strftime('%d/%m/%Y')})")
                    
                    selected_quiz_display = st.selectbox(
                        "Chọn quiz:",
                        ["-- Chọn quiz --"] + quiz_options,
                        help="Chọn quiz từ thư viện để làm bài"
                    )
                    
                    if selected_quiz_display and selected_quiz_display != "-- Chọn quiz --":
                        selected_quiz_name = selected_quiz_display.split(" (")[0]
                        
                        # Load and preview quiz
                        col_load, col_preview = st.columns(2)
                        
                        with col_load:
                            if st.button("📚 Tải Quiz Này", use_container_width=True):
                                loaded_questions = engine.load_quiz_from_storage(selected_quiz_name)
                                if loaded_questions:
                                    # Convert to JSON format
                                    from dataclasses import asdict
                                    questions_data = [asdict(q) for q in loaded_questions]
                                    st.session_state.selected_quiz_data = questions_data
                                    st.success(f"✅ Đã tải quiz '{selected_quiz_name}' ({len(questions_data)} câu)")
                                    st.rerun()
                                else:
                                    st.error("❌ Không thể tải quiz")
                        
                        with col_preview:
                            if st.button("👀 Xem Trước", use_container_width=True):
                                loaded_questions = engine.load_quiz_from_storage(selected_quiz_name)
                                if loaded_questions:
                                    st.session_state.preview_quiz = loaded_questions
                                    st.rerun()
                        
                        # Quiz info
                        if selected_quiz_name in saved_quizzes:
                            info = saved_quizzes[selected_quiz_name]
                            st.info(f"""
                            **📊 Thông tin quiz:**
                            - 📝 Số câu hỏi: {info['questions_count']}
                            - 💾 Kích thước: {info['size']}
                            - 📅 Ngày tạo: {info['created_time'].strftime('%d/%m/%Y %H:%M')}
                            """)
                        
                        # Delete quiz
                        with col_delete:
                            if st.button("🗑️ Xóa Quiz", use_container_width=True):
                                if engine.delete_quiz_from_storage(selected_quiz_name):
                                    st.success(f"✅ Đã xóa quiz '{selected_quiz_name}'")
                                    st.rerun()
                                else:
                                    st.error("❌ Không thể xóa quiz")
                
                else:
                    st.info("📚 Chưa có quiz nào trong thư viện. Hãy tạo và lưu quiz ở trang 'Tạo Quiz'.")
                
                # Check if quiz selected from library
                if 'selected_quiz_data' in st.session_state and not questions_data:
                    questions_data = st.session_state.selected_quiz_data
                    st.success(f"✅ Đã chọn quiz từ thư viện ({len(questions_data)} câu)")
        
        # Preview quiz if requested
        if 'preview_quiz' in st.session_state:
            with st.expander("👀 Xem trước quiz đã chọn", expanded=True):
                preview_questions = st.session_state.preview_quiz
                for i, q in enumerate(preview_questions[:5]):
                    st.markdown(f"**Câu {q.so_cau}:** {q.cau_hoi[:100]}...")
                    if hasattr(q, 'images') and q.images:
                        st.caption(f"📷 {len(q.images)} hình ảnh đính kèm")
                
                if len(preview_questions) > 5:
                    st.info(f"... và {len(preview_questions) - 5} câu hỏi khác")
                
                if st.button("❌ Đóng xem trước"):
                    del st.session_state.preview_quiz
                    st.rerun()
    
    with col2:
        # Cấu hình bài kiểm tra với enhanced options
        st.markdown("### ⚙️ Cấu Hình Bài Kiểm Tra")
        
        # Test mode selection
        test_mode = st.radio(
            "Chế độ làm bài:",
            ["🎯 Kiểm tra (Exam)", "📚 Ôn luyện (Practice)"],
            help="Kiểm tra: giới hạn thời gian, không hiển thị đáp án. Ôn luyện: không giới hạn thời gian, hiển thị kết quả ngay"
        )
        
        test_mode_value = "exam" if "Kiểm tra" in test_mode else "practice"
        
        # Time limit (only for exam mode)
        if test_mode_value == "exam":
            time_limit = st.selectbox(
                "Thời gian làm bài:",
                [15, 30, 45, 60, 90, 120],
                index=3,
                format_func=lambda x: f"{x} phút",
                help="Chọn thời gian làm bài phù hợp"
            )
        else:
            time_limit = 9999  # Unlimited for practice mode
            st.info("⏰ Chế độ ôn luyện: Không giới hạn thời gian")
        
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
        
        show_images = st.checkbox(
            "📷 Hiển thị hình ảnh",
            value=True,
            help="Hiển thị hình ảnh đính kèm trong câu hỏi"
        )
        
        st.markdown("### ℹ️ Hướng Dẫn")
        
        if test_mode_value == "exam":
            st.info("""
            **🎯 Chế độ Kiểm Tra:**
            - ⏰ Có giới hạn thời gian
            - 🔒 Không hiển thị đáp án khi làm
            - 📊 Kết quả hiển thị sau khi hoàn thành
            - 🎯 Phù hợp cho bài kiểm tra chính thức
            """)
        else:
            st.success("""
            **📚 Chế độ Ôn Luyện:**
            - ⏰ Không giới hạn thời gian
            - ✅ Hiển thị ngay đáp án đúng/sai
            - 🟢 Màu xanh = đúng, 🔴 màu đỏ = sai
            - 📖 Phù hợp cho ôn tập, học tập
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
            st.warning("⚠️ Vui lòng tải câu hỏi từ file JSON, quiz đã tạo hoặc thư viện")
    else:
        mode_text = "Kiểm tra" if test_mode_value == "exam" else "Ôn luyện"
        st.success(f"✅ Đã sẵn sàng bắt đầu {mode_text.lower()}!")
        
        # Show question count and image info
        images_count = sum(1 for q in questions_data if q.get('images'))
        if images_count > 0:
            st.info(f"📷 Có {images_count} câu hỏi chứa hình ảnh")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        button_text = "🚀 Bắt Đầu Làm Bài Kiểm Tra" if test_mode_value == "exam" else "📚 Bắt Đầu Ôn Luyện"
        
        if st.button(
            button_text,
            disabled=not can_start,
            use_container_width=True,
            type="primary"
        ):
            if can_start:
                start_new_test(student_name, test_title, questions_data, time_limit, 
                             shuffle_questions, shuffle_answers, test_mode_value, show_images)

def start_new_test(student_name: str, test_title: str, questions_data: list, 
                  time_limit: int, shuffle_questions: bool, shuffle_answers: bool, 
                  test_mode: str = "exam", show_images: bool = True):
    """Bắt đầu bài kiểm tra mới với enhanced options."""
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
            shuffle_answers=shuffle_answers,
            test_mode=test_mode
        )
        
        # Save session to streamlit state
        st.session_state.current_session_id = session_id
        st.session_state.show_images = show_images
        
        mode_text = "kiểm tra" if test_mode == "exam" else "ôn luyện"
        st.success(f"🎉 Phiên {mode_text} đã được tạo! Đang chuyển hướng...")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Lỗi tạo phiên làm bài: {str(e)}")

def render_question_interface(session_id: str, current_q: dict):
    """Render giao diện câu hỏi với feedback cho practice mode và hiển thị ảnh."""
    engine = st.session_state.quiz_engine
    question_data = current_q['question_data']
    test_mode = current_q.get('test_mode', 'exam')
    
    # Question header
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        mode_emoji = "📚" if test_mode == "practice" else "🎯"
        mode_text = "Ôn luyện" if test_mode == "practice" else "Kiểm tra"
        st.markdown(f"### {mode_emoji} Câu {current_q['question_number']}/{current_q['total_questions']}")
        st.caption(f"Chế độ: {mode_text}")
    
    with col2:
        # Time remaining (chỉ hiển thị cho exam mode)
        if test_mode == "exam":
            time_container = st.empty()
            time_remaining = current_q['time_remaining']
            if time_remaining > 0:
                minutes = time_remaining // 60
                seconds = time_remaining % 60
                time_container.markdown(f"⏱️ **Thời gian còn lại: {minutes:02d}:{seconds:02d}**")
            else:
                time_container.error("⏰ **Hết thời gian!**")
        else:
            st.markdown("⏰ **Không giới hạn thời gian**")
    
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
    
    # Display images if any and enabled
    if st.session_state.get('show_images', True) and question_data.get('images'):
        st.markdown("### 📷 Hình Ảnh Đính Kèm")
        
        image_cols = st.columns(min(len(question_data['images']), 3))
        for i, img_info in enumerate(question_data['images']):
            col = image_cols[i % 3]
            with col:
                try:
                    if 'data' in img_info:
                        # Image data embedded in question
                        st.image(img_info['data'], caption=img_info.get('name', f'Ảnh {i+1}'), width=200)
                    elif 'full_path' in img_info:
                        # Image file path
                        st.image(img_info['full_path'], caption=img_info.get('name', f'Ảnh {i+1}'), width=200)
                except Exception as e:
                    st.warning(f"⚠️ Không thể hiển thị ảnh: {img_info.get('name', f'Ảnh {i+1}')}")
    
    # Answer choices with feedback for practice mode
    st.markdown("### 🔤 Lựa Chọn Đáp Án")
    
    choices = question_data['lua_chon']
    current_answer = current_q['current_answer']
    feedback = current_q.get('feedback')
    
    # Display choices with color coding for practice mode
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
    
    # For practice mode, show feedback after answering
    if test_mode == "practice" and feedback and feedback.get('show_feedback'):
        st.markdown("#### 📋 Phản Hồi Ngay Lập Tức")
        
        # Show choices with color coding
        for choice, content in choices.items():
            is_correct_answer = choice == feedback.get('correct_answer', '').upper()
            is_user_choice = choice == feedback.get('user_answer', '').upper()
            
            if is_correct_answer and is_user_choice:
                st.success(f"✅ **{choice}.** {content} *(Bạn chọn đúng!)*")
            elif is_correct_answer:
                st.success(f"✅ **{choice}.** {content} *(Đáp án đúng)*")
            elif is_user_choice:
                st.error(f"❌ **{choice}.** {content} *(Bạn đã chọn - Sai)*")
            else:
                st.write(f"**{choice}.** {content}")
        
        # Explanation
        if feedback.get('explanation'):
            st.info(f"💡 **Giải thích:** {feedback['explanation']}")
    
    else:
        # Normal radio buttons for exam mode or no answer yet
        selected_answer = st.radio(
            "Chọn đáp án:",
            answer_options,
            index=current_index,
            key=f"answer_{current_q['question_number']}"
        )
        
        # Extract answer letter and submit
        if selected_answer:
            selected_letter = selected_answer.split('.')[0]
            # Submit answer and get feedback
            submit_feedback = engine.submit_answer(session_id, selected_letter)
            
            # For practice mode, trigger rerun to show feedback
            if test_mode == "practice" and submit_feedback.get('show_feedback'):
                st.rerun()
    
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
            if st.button("🏁 Hoàn thành", type="primary", key="finish_btn"):
                st.session_state.confirm_finish = True
                st.rerun()
    
    # Auto-refresh for timer (chỉ cho exam mode)
    if test_mode == "exam" and time_remaining > 0 and time_remaining % 5 == 0:
        time.sleep(1)
        st.rerun()
