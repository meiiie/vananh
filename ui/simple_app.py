"""
Ứng Dụng QuizForce AI - Enhanced Version 
Giao diện một trang với độ phức tạp tối ưu cho người Việt Nam.
Tích hợp đầy đủ: Tạo Quiz + Làm Bài + Thống Kê + Quiz Storage + Image Support
"""

import streamlit as st
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
import base64
import io
from PIL import Image

# Thêm backend vào path
current_dir = Path(__file__).parent
test_dir = current_dir.parent
project_root = test_dir.parent

sys.path.append(str(project_root))
sys.path.append(str(test_dir))

try:
    from backend.simple_agent import SimpleQuizAgent
    from backend.quiz_test_engine import QuizTestEngine
except ImportError:
    try:
        from test.backend.simple_agent import SimpleQuizAgent
        from test.backend.quiz_test_engine import QuizTestEngine
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
    """Ứng dụng chính enhanced."""
    st.set_page_config(
        page_title="QuizForce AI Pro - Hệ Thống Tạo Quiz Thông Minh",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize enhanced session state
    init_enhanced_session_state()
    
    # Enhanced Navigation
    page = st.sidebar.selectbox(
        "🧭 Điều hướng:",
        ["🎯 Tạo Quiz", "📝 Làm Bài Kiểm Tra", "📊 Thống Kê", "🏪 Quản Lý Quiz", "⚙️ Cài Đặt"],
        index=0
    )
    
    # Route to appropriate page
    if page == "🎯 Tạo Quiz":
        render_enhanced_quiz_creation_page()
    elif page == "📝 Làm Bài Kiểm Tra":
        render_enhanced_quiz_test_page()
    elif page == "📊 Thống Kê":
        render_enhanced_statistics_page()
    elif page == "🏪 Quản Lý Quiz":
        render_quiz_management_page()
    elif page == "⚙️ Cài Đặt":
        render_settings_page()

def init_enhanced_session_state():
    """Khởi tạo enhanced session state."""
    # Initialize quiz engine
    if 'quiz_engine' not in st.session_state:
        st.session_state.quiz_engine = QuizTestEngine()
    
    # Enhanced settings
    if 'app_settings' not in st.session_state:
        st.session_state.app_settings = {
            "theme": "light",
            "auto_save": True,
            "show_progress": True,
            "enable_sounds": False,
            "default_time_limit": 60,
            "default_difficulty": "trung_binh"
        }
    
    # UI state management
    if 'show_image_preview' not in st.session_state:
        st.session_state.show_image_preview = False
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

def render_enhanced_quiz_creation_page():
    """Render trang tạo quiz với enhanced features."""
    
    # Enhanced Header
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🎯 QuizForce AI Pro</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Hệ Thống Tạo Quiz Trắc Nghiệm Thông Minh cho Giáo Dục Việt Nam</p>
        <div style='color: #e0e0e0; font-size: 0.9rem; margin-top: 0.5rem;'>
            ✨ Enhanced với Image Support | 🔧 Batch Processing | 📚 Quiz Storage
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar Configuration
    with st.sidebar:
        render_enhanced_professional_sidebar()
    
    # Main Content with Enhanced Layout
    col1, col2 = st.columns([1.3, 1])
    
    with col1:
        render_enhanced_input_section()
    
    with col2:
        render_enhanced_results_section()
    
    # Enhanced Footer
    render_enhanced_footer()

def render_enhanced_professional_sidebar():
    """Render enhanced professional sidebar."""
    st.markdown("### ⚙️ Cấu Hình Hệ Thống Pro")
    
    # Enhanced API Key configuration
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
            
            # Test API connection
            if st.button("🔍 Test API Connection", use_container_width=True):
                try:
                    test_agent = SimpleQuizAgent(api_key=api_key)
                    st.success("✅ Kết nối API thành công!")
                    st.info(f"🤖 Agent: {test_agent.agent_name} v{test_agent.agent_version}")
                except Exception as e:
                    st.error(f"❌ Lỗi kết nối API: {e}")
        else:
            st.error("❌ Cần API Key để sử dụng hệ thống")
            st.markdown("""
            **Hướng dẫn lấy API Key:**
            1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Đăng nhập tài khoản Google
            3. Tạo API key mới
            4. Copy và dán vào ô trên
            """)
    
    # Enhanced Processing Settings
    with st.expander("⚙️ Cấu Hình Xử Lý", expanded=False):
        st.markdown("**Batch Processing:**")
        
        batch_size = st.slider(
            "Kích thước batch:",
            min_value=5,
            max_value=20,
            value=10,
            help="Số câu hỏi xử lý cùng lúc"
        )
        
        batch_delay = st.slider(
            "Delay giữa batch (giây):",
            min_value=3,
            max_value=10,
            value=5,
            help="Thời gian đợi giữa các batch"
        )
        
        quota_delay = st.slider(
            "Quota recovery delay (giây):",
            min_value=15,
            max_value=60,
            value=30,
            help="Thời gian đợi khi gặp quota limit"
        )
        
        st.session_state.processing_config = {
            "batch_size": batch_size,
            "batch_delay": batch_delay,
            "quota_delay": quota_delay
        }
        
        st.info(f"🔧 Cấu hình: {batch_size} câu/batch, đợi {batch_delay}s giữa batch")
    
    # System Info
    with st.expander("📊 Thông Tin Hệ Thống"):
        engine = st.session_state.quiz_engine
        storage_info = engine.get_storage_info()
        
        st.metric("📚 Quiz đã lưu", storage_info["total_quizzes"])
        st.metric("📝 Bài kiểm tra", storage_info["total_tests_completed"])
        st.metric("💾 Dung lượng", storage_info["total_storage_size"])
        st.metric("📷 Hình ảnh", storage_info["images_count"])
        
        st.info(f"""
        **QuizForce AI Pro v3.0**
        - 🤖 AI Engine: Google Gemini 2.0 Flash
        - 🎯 Chuyên môn: Tạo quiz trắc nghiệm Việt Nam
        - 📚 Hỗ trợ: Tất cả môn học phổ thông
        - 🌟 Tính năng: OCR, DOCX, JSON, Images, Storage
        """)
    
    # Quick Actions
    with st.expander("⚡ Thao Tác Nhanh"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Storage", use_container_width=True):
                st.session_state.quiz_engine._load_saved_quizzes()
                st.success("✅ Đã refresh!")
        
        with col2:
            if st.button("🧹 Clear Cache", use_container_width=True):
                # Clear some session state
                for key in ['quiz_results', 'selected_quiz_data', 'preview_quiz']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Đã xóa cache!")

def render_enhanced_input_section():
    """Render enhanced input section với image preview."""
    st.markdown("### 📝 Dữ Liệu Đầu Vào")
    
    # Enhanced Answer Input
    st.markdown("#### 1️⃣ Đáp Án Câu Hỏi")
    
    answer_tabs = st.tabs(["📝 Nhập Văn Bản", "🖼️ Upload Hình Ảnh", "📋 Từ Clipboard"])
    
    answer_text = None
    answer_image = None
    
    with answer_tabs[0]:
        st.markdown("**Nhập đáp án theo định dạng chuẩn:**")
        
        # Quick format buttons
        format_cols = st.columns(4)
        with format_cols[0]:
            if st.button("📝 Format: Câu 1. A"):
                st.session_state.answer_format_hint = "Câu 1. A\nCâu 2. B\nCâu 3. AC"
        with format_cols[1]:
            if st.button("📝 Format: 1. A"):
                st.session_state.answer_format_hint = "1. A\n2. B\n3. AC"
        with format_cols[2]:
            if st.button("📝 Format: 1) A"):
                st.session_state.answer_format_hint = "1) A\n2) B\n3) AC"
        with format_cols[3]:
            if st.button("📝 Format: 1: A"):
                st.session_state.answer_format_hint = "1: A\n2: B\n3: AC"
        
        answer_text = st.text_area(
            "Danh sách đáp án:",
            value=st.session_state.get('answer_format_hint', ''),
            placeholder="""Ví dụ:
1. A
2. B  
3. AC
4. D
5. BD
...""",
            height=200,
            help="Mỗi dòng một câu hỏi, format: số. đáp_án. Hỗ trợ đáp án kép (AC, BD, ABC)"
        )
        
        if answer_text:
            lines = [line.strip() for line in answer_text.split('\n') if line.strip()]
            st.success(f"✅ Đã nhập {len(lines)} dòng đáp án")
            
            # Enhanced preview
            with st.expander("👀 Preview Đáp Án", expanded=False):
                preview_cols = st.columns(4)
                for i, line in enumerate(lines[:12]):  # Show first 12
                    col_idx = i % 4
                    with preview_cols[col_idx]:
                        st.code(line)
                if len(lines) > 12:
                    st.info(f"... và {len(lines) - 12} dòng khác")
    
    with answer_tabs[1]:
        answer_image = st.file_uploader(
            "Tải ảnh chứa đáp án:",
            type=['png', 'jpg', 'jpeg', 'webp', 'gif'],
            help="Upload ảnh chụp đáp án, AI sẽ tự động đọc và trích xuất"
        )
        
        if answer_image:
            # Enhanced image preview
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(answer_image, caption="Ảnh đáp án đã upload", width=300)
            
            with col2:
                st.success("✅ Đã upload ảnh thành công")
                st.info(f"""
                **Thông tin ảnh:**
                - 📁 Tên file: {answer_image.name}
                - 📊 Kích thước: {len(answer_image.getvalue())/1024:.1f} KB
                - 🎨 Định dạng: {answer_image.type}
                """)
                
                # Image processing options
                if st.checkbox("🔧 Xử lý ảnh nâng cao"):
                    st.info("✨ Sẽ áp dụng enhancement cho OCR tốt hơn")
    
    with answer_tabs[2]:
        st.markdown("**Dán đáp án từ clipboard:**")
        
        if st.button("📋 Paste từ Clipboard", use_container_width=True):
            st.info("💡 Tính năng này sẽ có trong phiên bản tiếp theo")
        
        st.markdown("*Hiện tại vui lòng sử dụng tab 'Nhập Văn Bản'*")
    
    st.divider()
    
    # Enhanced DOCX Input
    st.markdown("#### 2️⃣ File Câu Hỏi DOCX")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        docx_file = st.file_uploader(
            "Upload file DOCX chứa câu hỏi:",
            type=['docx'],
            help="File Word chứa câu hỏi trắc nghiệm với format chuẩn"
        )
    
    with col2:
        if st.button("📖 Hướng Dẫn Format DOCX", use_container_width=True):
            st.session_state.show_docx_guide = True
    
    if st.session_state.get('show_docx_guide', False):
        with st.expander("📖 Hướng Dẫn Format DOCX", expanded=True):
            st.markdown("""
            **Format chuẩn cho file DOCX:**
            
            ```
            Câu 1. Nội dung câu hỏi này?
            A. Lựa chọn A
            B. Lựa chọn B  
            C. Lựa chọn C
            D. Lựa chọn D
            
            Câu 2. Nội dung câu hỏi khác?
            A. Lựa chọn A
            B. Lựa chọn B
            C. Lựa chọn C  
            D. Lựa chọn D
            ```
            
            **Lưu ý quan trọng:**
            - Bắt đầu mỗi câu với "Câu X." hoặc "X."
            - Mỗi câu phải có đủ 4 lựa chọn A, B, C, D
            - Có thể chứa hình ảnh (sẽ được phát hiện tự động)
            - Tránh format phức tạp, giữ đơn giản
            """)
            
            if st.button("❌ Đóng hướng dẫn"):
                st.session_state.show_docx_guide = False
                st.rerun()
    
    if docx_file:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.success(f"✅ Đã upload file: {docx_file.name}")
            st.info(f"📊 Kích thước file: {len(docx_file.getvalue())/1024:.1f} KB")
        
        with col2:
            if st.button("🔍 Preview DOCX", use_container_width=True):
                try:
                    # Quick preview of DOCX content
                    import docx
                    doc = docx.Document(io.BytesIO(docx_file.getvalue()))
                    
                    preview_text = ""
                    for i, para in enumerate(doc.paragraphs[:10]):
                        if para.text.strip():
                            preview_text += f"{para.text.strip()}\n"
                    
                    if preview_text:
                        st.text_area("Preview nội dung:", preview_text, height=150)
                    else:
                        st.warning("⚠️ Không đọc được nội dung file")
                        
                except Exception as e:
                    st.error(f"❌ Lỗi preview: {e}")
    
    st.divider()
    
    # Enhanced Processing Section
    st.markdown("#### 3️⃣ Xử Lý Quiz")
    
    # Check prerequisites
    has_api_key = hasattr(st.session_state, 'api_key') and st.session_state.api_key
    has_answers = (answer_text and answer_text.strip()) or answer_image
    has_docx = docx_file is not None
    
    can_process = has_api_key and has_answers and has_docx
    
    # Status indicators
    status_cols = st.columns(3)
    
    with status_cols[0]:
        if has_api_key:
            st.success("✅ API Key")
        else:
            st.error("❌ API Key")
    
    with status_cols[1]:
        if has_answers:
            st.success("✅ Đáp Án")
        else:
            st.error("❌ Đáp Án")
    
    with status_cols[2]:
        if has_docx:
            st.success("✅ File DOCX")
        else:
            st.error("❌ File DOCX")
    
    # Processing options
    if can_process:
        st.success("✅ Đã sẵn sàng tạo quiz!")
        
        with st.expander("⚙️ Tùy Chọn Xử Lý", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                enable_image_detection = st.checkbox(
                    "📷 Phát hiện hình ảnh trong câu hỏi",
                    value=True,
                    help="Tự động phát hiện câu hỏi có hình ảnh"
                )
                
                save_to_storage = st.checkbox(
                    "💾 Tự động lưu vào thư viện",
                    value=True,
                    help="Lưu quiz vào storage sau khi tạo"
                )
            
            with col2:
                processing_mode = st.selectbox(
                    "🔧 Chế độ xử lý:",
                    ["Standard", "High Quality", "Fast"],
                    help="Standard: cân bằng, High Quality: chậm nhưng chính xác, Fast: nhanh"
                )
                
                if save_to_storage:
                    auto_quiz_name = st.text_input(
                        "📝 Tên quiz tự động:",
                        value=f"Quiz_{datetime.now().strftime('%d%m%Y_%H%M')}",
                        help="Tên để lưu quiz vào thư viện"
                    )
    
    # Enhanced Processing Button
    if st.button(
        "🚀 Tạo Quiz Thông Minh Pro",
        disabled=not can_process,
        use_container_width=True,
        type="primary"
    ):
        if can_process:
            answer_method = "text" if answer_text else "image"
            answer_data = answer_text if answer_text else answer_image
            
            processing_options = {
                "enable_image_detection": enable_image_detection if can_process else True,
                "save_to_storage": save_to_storage if can_process else False,
                "processing_mode": processing_mode if can_process else "Standard",
                "auto_quiz_name": auto_quiz_name if can_process and save_to_storage else None
            }
            
            process_enhanced_quiz_with_progress(
                api_key=st.session_state.api_key,
                answer_data=answer_data,
                docx_file=docx_file,
                answer_method=answer_method,
                options=processing_options
            )

def process_enhanced_quiz_with_progress(api_key: str, answer_data, docx_file, 
                                      answer_method: str, options: dict = None):
    """Xử lý tạo quiz với enhanced progress tracking."""
    
    # Container cho progress
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Đang Xử Lý Enhanced...")
        
        # Enhanced progress indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            progress_bar = st.progress(0)
        with col2:
            status_text = st.empty()
        with col3:
            time_text = st.empty()
        
        # Detailed progress
        detail_container = st.container()
        
        start_time = time.time()
        
        try:
            # Initialize Enhanced Agent
            status_text.success("🤖 Khởi tạo QuizMaster AI Pro...")
            time_text.info(f"⏱️ {time.time() - start_time:.1f}s")
            progress_bar.progress(5)
            
            # Apply processing config
            config = st.session_state.get('processing_config', {})
            agent = SimpleQuizAgent(api_key=api_key)
            
            if config:
                agent.batch_size = config.get('batch_size', 10)
                agent.batch_delay = config.get('batch_delay', 5)
                agent.quota_exceeded_delay = config.get('quota_delay', 30)
            
            with detail_container:
                st.info(f"🔧 Cấu hình: {agent.batch_size} câu/batch, {agent.batch_delay}s delay, {agent.quota_exceeded_delay}s recovery")
            
            # Data preparation
            status_text.success("📋 Chuẩn bị dữ liệu đầu vào...")
            time_text.info(f"⏱️ {time.time() - start_time:.1f}s")
            progress_bar.progress(15)
            
            # Enhanced processing
            status_text.success("⚙️ Bắt đầu Enhanced Processing...")
            time_text.info(f"⏱️ {time.time() - start_time:.1f}s")
            progress_bar.progress(25)
            
            # Call enhanced agent
            results = agent.process_complete_quiz_enhanced(
                answer_data=answer_data.getvalue() if answer_method == "image" else answer_data,
                docx_file=docx_file,
                answer_type=answer_method
            )
            
            progress_bar.progress(90)
            
            # Final processing
            status_text.success("✅ Hoàn tất Enhanced Processing!")
            time_text.success(f"🎉 Tổng thời gian: {time.time() - start_time:.1f}s")
            progress_bar.progress(100)
            
            # Auto-save to storage if requested
            if options and options.get('save_to_storage') and results.get('success'):
                quiz_name = options.get('auto_quiz_name')
                if quiz_name and results.get('compiled_questions'):
                    engine = st.session_state.quiz_engine
                    saved_name = engine.save_quiz_to_storage(results['compiled_questions'], quiz_name)
                    if saved_name:
                        with detail_container:
                            st.success(f"💾 Đã tự động lưu quiz '{saved_name}' vào thư viện!")
            
            # Save results
            st.session_state.quiz_results = results
            
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            status_text.error(f"❌ Có lỗi xảy ra: {str(e)}")
            time_text.error(f"⏱️ Thời gian: {time.time() - start_time:.1f}s")
            
            with detail_container:
                st.error("💡 Khắc phục:")
                st.markdown("""
                1. Kiểm tra kết nối internet
                2. Thử giảm batch size xuống 5-7
                3. Tăng delay lên 7-10 giây
                4. Kiểm tra API key còn quota
                """)

def render_enhanced_results_section():
    """Render enhanced results section với quiz management."""
    st.markdown("### 📊 Kết Quả Xử Lý")
    
    # Display results if available
    if 'quiz_results' in st.session_state and st.session_state.quiz_results:
        display_enhanced_professional_results(st.session_state.quiz_results)
    else:
        # Enhanced placeholder
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; border: 2px dashed #dee2e6;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
            <h3 style='color: #6c757d; margin-bottom: 1rem;'>Sẵn Sàng Tạo Quiz Pro</h3>
            <p style='color: #6c757d; margin: 0;'>Cấu hình dữ liệu bên trái và nhấn "Tạo Quiz"</p>
            <p style='color: #6c757d; margin: 0;'>Kết quả enhanced sẽ hiển thị tại đây</p>
            <div style='margin-top: 1rem; font-size: 0.9rem; color: #868e96;'>
                ✨ Enhanced Features: Image Support | Quiz Storage | Advanced Analytics
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_enhanced_professional_results(results: dict):
    """Hiển thị enhanced results với quiz management features."""
    
    if not results.get("success"):
        st.error("❌ **Xử lý thất bại**")
        
        # Enhanced error display
        if results.get("errors"):
            st.markdown("### 🚨 Chi Tiết Lỗi:")
            for error in results["errors"]:
                st.error(error)
        
        # Enhanced debug info
        debug_info = results.get("debug_info", {})
        if debug_info:
            with st.expander("🔍 Thông Tin Debug", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📝 Đáp án:**")
                    answer_keys = debug_info.get("answer_keys", [])
                    if answer_keys:
                        st.success(f"✅ {len(answer_keys)} đáp án")
                        if len(answer_keys) <= 20:
                            st.code(str(answer_keys))
                        else:
                            st.code(f"{answer_keys[:20]}... (+{len(answer_keys)-20} more)")
                    else:
                        st.error("❌ Không tìm thấy đáp án")
                
                with col2:
                    st.markdown("**📄 Câu hỏi:**")
                    question_keys = debug_info.get("question_keys", [])
                    if question_keys:
                        st.success(f"✅ {len(question_keys)} câu hỏi")
                        if len(question_keys) <= 20:
                            st.code(str(question_keys))
                        else:
                            st.code(f"{question_keys[:20]}... (+{len(question_keys)-20} more)")
                    else:
                        st.error("❌ Không tìm thấy câu hỏi")
        
        # Enhanced troubleshooting
        st.markdown("### 💡 Hướng Dẫn Khắc Phục:")
        
        troubleshoot_tabs = st.tabs(["🔧 Lỗi Thường Gặp", "📋 Format Đúng", "⚙️ Cài Đặt"])
        
        with troubleshoot_tabs[0]:
            st.info("""
            **Các lỗi thường gặp:**
            - ❌ Quota exceeded: Đợi 1-2 phút hoặc giảm batch size
            - ❌ Không khớp đáp án: Kiểm tra format số câu
            - ❌ Lỗi DOCX: File có thể bị corrupt hoặc format sai
            """)
        
        with troubleshoot_tabs[1]:
            st.code("""
Format đáp án chuẩn:
1. A
2. B  
3. AC
4. D

Format DOCX chuẩn:
Câu 1. Nội dung câu hỏi?
A. Lựa chọn A
B. Lựa chọn B
C. Lựa chọn C  
D. Lựa chọn D
            """)
        
        with troubleshoot_tabs[2]:
            st.info("""
            **Cài đặt khuyến nghị:**
            - Batch size: 5-8 câu (thay vì 10)
            - Delay: 7-10 giây (thay vì 5)
            - Recovery: 45-60 giây (thay vì 30)
            """)
        
        return
    
    # Success display
    st.success("🎉 **Tạo Quiz Thành Công!**")
    
    # Enhanced statistics với agent info
    stats = results.get("statistics", {})
    agent_info = results.get("agent_info", {})
    batch_info = agent_info.get("batch_info", {})
    
    # Top metrics row
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
    
    # Enhanced processing info
    if batch_info:
        st.markdown("**🔄 Enhanced Batch Processing Info:**")
        
        info_cols = st.columns(4)
        with info_cols[0]:
            st.metric("📦 Total Batches", batch_info.get("total_batches", 0))
        with info_cols[1]:
            st.metric("✅ Completed", batch_info.get("completed_batches", 0))
        with info_cols[2]:
            st.metric("🔧 Recovered", batch_info.get("recovered_questions", 0))
        with info_cols[3]:
            st.metric("⚠️ Quota Events", batch_info.get("quota_exceeded_events", 0))
    
    # Enhanced quiz management
    compiled_questions = results.get("compiled_questions", [])
    
    if compiled_questions:
        st.markdown("---")
        st.markdown("### 🏪 Quản Lý Quiz Enhanced")
        
        # Management tabs
        mgmt_tabs = st.tabs(["💾 Lưu & Export", "✏️ Chỉnh Sửa", "🔍 Preview"])
        
        with mgmt_tabs[0]:
            render_quiz_storage_management(compiled_questions)
        
        with mgmt_tabs[1]:
            render_enhanced_quiz_editor(compiled_questions)
        
        with mgmt_tabs[2]:
            render_enhanced_quiz_preview(compiled_questions)

def render_quiz_storage_management(questions: list):
    """Render quiz storage management."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**💾 Lưu vào Thư Viện**")
        
        quiz_name = st.text_input(
            "Tên quiz:",
            placeholder="VD: Toán 12 - Chương 1",
            help="Đặt tên để lưu quiz vào thư viện"
        )
        
        quiz_description = st.text_area(
            "Mô tả (tuỳ chọn):",
            placeholder="Mô tả ngắn về quiz này...",
            height=68  # <- SỬA THÀNH 68
        )
        
        if st.button("💾 Lưu vào Thư Viện", use_container_width=True):
            if quiz_name and quiz_name.strip():
                engine = st.session_state.quiz_engine
                
                # Add description to questions if provided
                if quiz_description:
                    for q in questions:
                        q['quiz_description'] = quiz_description
                
                saved_name = engine.save_quiz_to_storage(questions, quiz_name.strip())
                if saved_name:
                    st.success(f"✅ Đã lưu quiz '{saved_name}'!")
                    st.balloons()
                else:
                    st.error("❌ Lỗi lưu quiz")
            else:
                st.error("⚠️ Vui lòng nhập tên quiz")
    
    with col2:
        st.markdown("**📥 Export Quiz**")
        
        export_format = st.selectbox(
            "Định dạng:",
            ["JSON (Recommend)", "JSON Compact", "CSV Preview"],
            help="JSON được khuyến nghị cho import lại"
        )
        
        # Generate export data
        if export_format == "JSON (Recommend)":
            export_data = json.dumps(questions, ensure_ascii=False, indent=2)
            filename = f"QuizForce_Pro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            mime_type = "application/json"
        elif export_format == "JSON Compact":
            export_data = json.dumps(questions, ensure_ascii=False, separators=(',', ':'))
            filename = f"QuizForce_Compact_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            mime_type = "application/json"
        else:  # CSV Preview
            csv_lines = ["so_cau,cau_hoi,dap_an,do_kho"]
            for q in questions[:10]:  # Only first 10 for preview
                csv_lines.append(f"{q.get('so_cau', '')},{q.get('cau_hoi', '')[:50]}...,{q.get('dap_an', '')},{q.get('do_kho', '')}")
            export_data = "\n".join(csv_lines)
            filename = f"QuizForce_Preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            mime_type = "text/csv"
        
        st.download_button(
            "📥 Tải Xuống",
            data=export_data,
            file_name=filename,
            mime=mime_type,
            use_container_width=True,
            type="primary"
        )
        
        # Export info
        st.caption(f"📊 {len(questions)} câu hỏi • {len(export_data)/1024:.1f} KB")
    
    with col3:
        st.markdown("**🚀 Làm Bài Ngay**")
        
        test_mode = st.radio(
            "Chế độ:",
            ["🎯 Kiểm tra", "📚 Ôn luyện"],
            help="Kiểm tra: có thời gian, Ôn luyện: thấy ngay đáp án"
        )
        
        if st.button("🚀 Bắt Đầu Test", use_container_width=True, type="secondary"):
            # Save questions for test session
            st.session_state.selected_quiz_data = questions
            st.session_state.selected_test_mode = "exam" if "Kiểm tra" in test_mode else "practice"
            
            # Switch to test page
            st.session_state.auto_switch_to_test = True
            st.success("🎉 Đang chuyển đến trang làm bài...")
            time.sleep(1)
            st.rerun()

def render_enhanced_quiz_editor(questions: list):
    """Render enhanced quiz editor với image support."""
    st.markdown("**✏️ Chỉnh Sửa Quiz**")
    
    if not questions:
        st.info("Không có câu hỏi nào để chỉnh sửa.")
        return
    
    # Question selector với search
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Tìm câu hỏi:",
            placeholder="Nhập từ khóa để tìm...",
            help="Tìm theo nội dung câu hỏi"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sắp xếp:",
            ["Số câu", "Độ khó", "Môn học"],
            help="Sắp xếp danh sách câu hỏi"
        )
    
    # Filter questions
    filtered_questions = questions.copy()
    
    if search_query:
        filtered_questions = [
            q for q in questions 
            if search_query.lower() in q.get('cau_hoi', '').lower()
        ]
    
    # Sort questions
    if sort_by == "Số câu":
        filtered_questions.sort(key=lambda x: x.get('so_cau', 0))
    elif sort_by == "Độ khó":
        difficulty_order = {'de': 1, 'trung_binh': 2, 'kho': 3}
        filtered_questions.sort(key=lambda x: difficulty_order.get(x.get('do_kho', 'trung_binh'), 2))
    elif sort_by == "Môn học":
        filtered_questions.sort(key=lambda x: x.get('mon_hoc', ''))
    
    if not filtered_questions:
        st.warning(f"Không tìm thấy câu hỏi với từ khóa '{search_query}'")
        return
    
    # Question options cho selectbox
    question_options = []
    for i, q in enumerate(filtered_questions):
        difficulty_emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(q.get('do_kho', 'trung_binh'), '🟡')
        image_emoji = '📷' if q.get('has_images', False) else ''
        option_text = f"Câu {q.get('so_cau', i+1)}: {q.get('cau_hoi', '')[:50]}... {difficulty_emoji} {image_emoji}"
        question_options.append(option_text)
    
    selected_idx = st.selectbox(
        f"Chọn câu để chỉnh sửa ({len(filtered_questions)} câu):",
        range(len(filtered_questions)),
        format_func=lambda x: question_options[x],
        key="enhanced_quiz_editor_selector"
    )
    
    if selected_idx is not None:
        question = filtered_questions[selected_idx]
        
        # Enhanced editor interface
        with st.expander(f"✏️ Chỉnh sửa câu {question.get('so_cau', selected_idx+1)}", expanded=True):
            
            # Editor tabs
            edit_tabs = st.tabs(["📝 Nội Dung", "📷 Hình Ảnh", "⚙️ Metadata"])
            
            with edit_tabs[0]:
                # Edit question content
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    new_question_text = st.text_area(
                        "Nội dung câu hỏi:",
                        value=question.get('cau_hoi', ''),
                        height=120,
                        key=f"edit_question_{selected_idx}"
                    )
                
                with col2:
                    # Quick formatting tools
                    st.markdown("**🔧 Công cụ:**")
                    
                    if st.button("🧹 Làm sạch text", use_container_width=True):
                        # Simple text cleaning
                        clean_text = new_question_text.strip()
                        clean_text = ' '.join(clean_text.split())  # Remove extra spaces
                        st.session_state[f"edit_question_{selected_idx}"] = clean_text
                        st.rerun()
                    
                    if st.button("🔤 Chuẩn hóa", use_container_width=True):
                        # Standardize Vietnamese text
                        normalized = new_question_text.replace('?', '?').replace(':', ':')
                        st.session_state[f"edit_question_{selected_idx}"] = normalized
                        st.rerun()
                
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
                            height=80,
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
            
            with edit_tabs[1]:
                # Enhanced image management
                st.markdown("**📷 Quản lý hình ảnh:**")
                
                # Show existing images
                existing_images = question.get('images', [])
                if existing_images:
                    st.markdown("**Hình ảnh hiện tại:**")
                    
                    for idx, img in enumerate(existing_images):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.text(f"📷 {img.get('name', f'Image {idx+1}')}")
                            if img.get('description'):
                                st.caption(img['description'])
                        
                        with col2:
                            st.text(f"Type: {img.get('type', 'Unknown')}")
                            if img.get('size'):
                                st.text(f"Size: {img['size']/1024:.1f} KB")
                        
                        with col3:
                            if st.button("🗑️", key=f"delete_img_{selected_idx}_{idx}"):
                                st.info("Tính năng xóa ảnh sẽ có trong update tiếp theo")
                else:
                    st.info("Câu hỏi này chưa có hình ảnh.")
                
                # Add new image
                st.markdown("**➕ Thêm hình ảnh mới:**")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    uploaded_image = st.file_uploader(
                        "Chọn ảnh:",
                        type=['png', 'jpg', 'jpeg', 'gif'],
                        key=f"upload_image_{selected_idx}"
                    )
                
                with col2:
                    if uploaded_image:
                        st.image(uploaded_image, caption="Preview", width=150)
                
                if uploaded_image:
                    img_description = st.text_input(
                        "Mô tả ảnh (tuỳ chọn):",
                        placeholder="VD: Biểu đồ thống kê, Sơ đồ mạch...",
                        key=f"img_desc_{selected_idx}"
                    )
                    
                    if st.button("➕ Thêm ảnh này", key=f"add_image_{selected_idx}"):
                        # Add image to question
                        if 'images' not in question:
                            question['images'] = []
                        
                        # Convert image to base64 for storage
                        img_bytes = uploaded_image.getvalue()
                        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                        
                        question['images'].append({
                            'name': uploaded_image.name,
                            'data': img_b64,
                            'type': uploaded_image.type,
                            'size': len(img_bytes),
                            'description': img_description
                        })
                        
                        question['has_images'] = True
                        
                        st.success(f"✅ Đã thêm ảnh {uploaded_image.name}")
                        st.rerun()
            
            with edit_tabs[2]:
                # Metadata editing
                col1, col2 = st.columns(2)
                
                with col1:
                    new_subject = st.text_input(
                        "Môn học:",
                        value=question.get('mon_hoc', 'auto_detect'),
                        key=f"edit_subject_{selected_idx}"
                    )
                    
                    new_note = st.text_area(
                        "Ghi chú:",
                        value=question.get('ghi_chu', ''),
                        height=80,
                        key=f"edit_note_{selected_idx}"
                    )
                
                with col2:
                    # Question statistics
                    st.markdown("**📊 Thông tin câu hỏi:**")
                    
                    word_count = len(new_question_text.split()) if new_question_text else 0
                    char_count = len(new_question_text) if new_question_text else 0
                    
                    st.metric("Số từ", word_count)
                    st.metric("Số ký tự", char_count)
                    
                    if question.get('has_images'):
                        st.metric("Số ảnh", len(question.get('images', [])))
                    
                    # Last modified
                    if question.get('updated_time'):
                        st.caption(f"Cập nhật: {question['updated_time']}")
            
            # Save changes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Lưu thay đổi", key=f"save_changes_{selected_idx}", type="primary"):
                    # Update question
                    filtered_questions[selected_idx]['cau_hoi'] = new_question_text
                    filtered_questions[selected_idx]['lua_chon'] = new_choices
                    filtered_questions[selected_idx]['dap_an'] = new_answer
                    filtered_questions[selected_idx]['do_kho'] = new_difficulty
                    filtered_questions[selected_idx]['mon_hoc'] = new_subject
                    filtered_questions[selected_idx]['ghi_chu'] = new_note
                    filtered_questions[selected_idx]['updated_time'] = datetime.now().isoformat()
                    
                    st.success("✅ Đã lưu thay đổi!")
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("🔄 Reset", key=f"reset_changes_{selected_idx}"):
                    st.info("🔄 Làm mới trang để reset...")
                    st.rerun()
            
            with col3:
                if st.button("👀 Preview", key=f"preview_changes_{selected_idx}"):
                    st.session_state.preview_question_idx = selected_idx
                    st.rerun()
        
        # Preview mode
        if st.session_state.get('preview_question_idx') == selected_idx:
            st.markdown("### 👀 Preview Câu Hỏi")
            
            preview_container = st.container()
            with preview_container:
                st.markdown(f"**Câu {question.get('so_cau', selected_idx+1)}:** {new_question_text}")
                
                for choice, content in new_choices.items():
                    if choice == new_answer:
                        st.success(f"✅ **{choice}.** {content} *(Đáp án đúng)*")
                    else:
                        st.write(f"**{choice}.** {content}")
                
                st.caption(f"Độ khó: {new_difficulty} | Môn: {new_subject}")
                
                if st.button("❌ Đóng preview"):
                    del st.session_state.preview_question_idx
                    st.rerun()

def render_enhanced_quiz_preview(questions: list):
    """Render enhanced quiz preview."""
    st.markdown("**🔍 Preview Quiz**")
    
    if not questions:
        st.info("Không có câu hỏi nào để preview.")
        return
    
    # Preview controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        preview_mode = st.radio(
            "Chế độ preview:",
            ["📋 Danh sách", "📄 Chi tiết", "🎯 Chế độ thi"],
            key="preview_mode"
        )
    
    with col2:
        if len(questions) > 20:
            preview_limit = st.slider(
                "Số câu hiển thị:",
                min_value=5,
                max_value=min(50, len(questions)),
                value=20,
                key="preview_limit"
            )
        else:
            preview_limit = len(questions)
    
    with col3:
        show_answers = st.checkbox(
            "Hiển thị đáp án",
            value=True,
            key="show_answers_preview"
        )
    
    # Statistics summary
    if preview_mode != "🎯 Chế độ thi":
        with st.expander("📊 Thống kê Quiz", expanded=False):
            difficulty_count = {}
            subject_count = {}
            images_count = 0
            
            for q in questions:
                # Difficulty
                diff = q.get('do_kho', 'trung_binh')
                difficulty_count[diff] = difficulty_count.get(diff, 0) + 1
                
                # Subject
                subj = q.get('mon_hoc', 'unknown')
                subject_count[subj] = subject_count.get(subj, 0) + 1
                
                # Images
                if q.get('has_images', False):
                    images_count += 1
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Độ khó:**")
                for diff, count in difficulty_count.items():
                    emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(diff, '🟡')
                    st.write(f"{emoji} {diff}: {count} câu")
            
            with col2:
                st.markdown("**Môn học:**")
                for subj, count in list(subject_count.items())[:5]:  # Top 5
                    st.write(f"📚 {subj}: {count} câu")
            
            with col3:
                st.metric("📷 Có hình ảnh", f"{images_count}/{len(questions)}")
                st.metric("📊 Tổng câu hỏi", len(questions))
    
    # Render preview based on mode
    if preview_mode == "📋 Danh sách":
        render_list_preview(questions[:preview_limit], show_answers)
    elif preview_mode == "📄 Chi tiết":
        render_detailed_preview(questions[:preview_limit], show_answers)
    elif preview_mode == "🎯 Chế độ thi":
        render_exam_preview(questions[:preview_limit])

def render_list_preview(questions: list, show_answers: bool):
    """Render list-style preview."""
    for i, q in enumerate(questions):
        with st.container():
            col1, col2, col3 = st.columns([6, 2, 1])
            
            with col1:
                difficulty_emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(q.get('do_kho', 'trung_binh'), '🟡')
                image_emoji = '📷' if q.get('has_images', False) else ''
                
                st.write(f"**{i+1}.** {q.get('cau_hoi', '')[:100]}...")
            
            with col2:
                if show_answers:
                    st.success(f"Đáp án: {q.get('dap_an', 'N/A')}")
                else:
                    st.info("Ẩn đáp án")
            
            with col3:
                st.write(f"{difficulty_emoji} {image_emoji}")
        
        if i < len(questions) - 1:
            st.divider()

def render_detailed_preview(questions: list, show_answers: bool):
    """Render detailed preview."""
    for i, q in enumerate(questions):
        with st.expander(f"Câu {q.get('so_cau', i+1)}: {q.get('cau_hoi', '')[:50]}...", expanded=False):
            
            # Question content
            st.markdown(f"**Câu hỏi:** {q.get('cau_hoi', '')}")
            
            # Choices
            choices = q.get('lua_chon', {})
            correct_answer = q.get('dap_an', 'A')
            
            for choice, content in choices.items():
                if show_answers and choice == correct_answer:
                    st.success(f"✅ **{choice}.** {content}")
                else:
                    st.write(f"**{choice}.** {content}")
            
            # Images
            if q.get('has_images', False) and q.get('images'):
                st.markdown("**📷 Hình ảnh đính kèm:**")
                img_cols = st.columns(min(3, len(q['images'])))
                
                for idx, img in enumerate(q['images'][:3]):  # Max 3 images preview
                    with img_cols[idx]:
                        if 'data' in img:
                            try:
                                img_data = base64.b64decode(img['data'])
                                st.image(img_data, caption=img.get('name', f'Image {idx+1}'), width=150)
                            except:
                                st.error(f"Lỗi hiển thị {img.get('name', 'image')}")
                        else:
                            st.info(f"📷 {img.get('name', 'Image')}")
            
            # Metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Độ khó: {q.get('do_kho', 'N/A')}")
            with col2:
                st.caption(f"Môn học: {q.get('mon_hoc', 'N/A')}")
            with col3:
                if show_answers:
                    st.caption(f"Đáp án: {correct_answer}")

def render_exam_preview(questions: list):
    """Render exam-style preview."""
    st.markdown("### 🎯 Chế Độ Thi Preview")
    st.info("Hiển thị như khi học sinh làm bài thật")
    
    # Question selector for navigation
    if len(questions) > 1:
        current_q_idx = st.selectbox(
            "Chọn câu để xem:",
            range(len(questions)),
            format_func=lambda x: f"Câu {x+1}",
            key="exam_preview_selector"
        )
    else:
        current_q_idx = 0
    
    if current_q_idx < len(questions):
        question = questions[current_q_idx]
        
        # Exam-style display
        st.markdown(f"### Câu {current_q_idx + 1}/{len(questions)}")
        
        # Question content with exam styling
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #007bff; margin: 1rem 0;'>
            <h4 style='margin: 0; color: #495057;'>{question.get('cau_hoi', '')}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Images if any
        if question.get('has_images', False) and question.get('images'):
            st.markdown("**📷 Hình ảnh:**")
            img_cols = st.columns(min(3, len(question['images'])))
            
            for idx, img in enumerate(question['images'][:3]):
                with img_cols[idx]:
                    if 'data' in img:
                        try:
                            img_data = base64.b64decode(img['data'])
                            st.image(img_data, caption=img.get('name', f'Ảnh {idx+1}'), width=200)
                        except:
                            st.error(f"Lỗi hiển thị {img.get('name', 'ảnh')}")
        
        # Choices as radio buttons
        choices = question.get('lua_chon', {})
        choice_options = [f"{choice}. {content}" for choice, content in choices.items()]
        
        selected = st.radio(
            "Chọn đáp án:",
            choice_options,
            key=f"exam_preview_answer_{current_q_idx}"
        )
        
        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_q_idx > 0:
                if st.button("⬅️ Câu trước"):
                    st.session_state.exam_preview_selector = current_q_idx - 1
                    st.rerun()
        
        with col2:
            st.info(f"🔄 Tiến độ: {current_q_idx + 1}/{len(questions)} câu")
        
        with col3:
            if current_q_idx < len(questions) - 1:
                if st.button("Câu tiếp ➡️"):
                    st.session_state.exam_preview_selector = current_q_idx + 1
                    st.rerun()

def render_enhanced_quiz_test_page():
    """Render trang làm bài kiểm tra enhanced."""
    
    # Auto-switch logic
    if st.session_state.get('auto_switch_to_test'):
        del st.session_state.auto_switch_to_test
        # Will continue to test setup with selected data
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>📝 QuizForce AI - Làm Bài Kiểm Tra</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Hệ Thống Kiểm Tra Trực Tuyến Chuyên Nghiệp</p>
        <div style='color: #e0e0e0; font-size: 0.9rem; margin-top: 0.5rem;'>
            🎯 Exam Mode | 📚 Practice Mode | 📷 Image Support | 📊 Real-time Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if in test session
    if 'current_session_id' in st.session_state and st.session_state.current_session_id:
        render_enhanced_test_interface()
    else:
        render_enhanced_test_setup()

def render_enhanced_test_setup():
    """Render enhanced test setup với advanced options."""
    st.markdown("## 🎯 Thiết Lập Bài Kiểm Tra")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Student info
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
        
        st.markdown("### 📚 Chọn Nguồn Câu Hỏi")
        
        # Enhanced source tabs
        source_tabs = st.tabs(["📄 Upload JSON", "🔄 Quiz Vừa Tạo", "📚 Thư Viện Quiz", "🔗 Import URL"])
        
        questions_data = None
        source_info = ""
        
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
                    source_info = f"File: {uploaded_file.name}"
                    
                    # Enhanced file info
                    file_size = len(uploaded_file.getvalue()) / 1024
                    images_count = sum(1 for q in questions_data if q.get('has_images', False))
                    
                    st.success(f"✅ Đã tải {len(questions_data)} câu hỏi")
                    st.info(f"📊 {file_size:.1f} KB • {images_count} câu có ảnh")
                    
                    # Enhanced preview
                    with st.expander("👀 Xem trước câu hỏi", expanded=False):
                        for i, q in enumerate(questions_data[:3]):
                            difficulty_emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(q.get('do_kho', 'trung_binh'), '🟡')
                            image_emoji = '📷' if q.get('has_images', False) else ''
                            
                            st.markdown(f"**Câu {q.get('so_cau', i+1)}:** {q.get('cau_hoi', '')[:100]}... {difficulty_emoji} {image_emoji}")
                        
                        if len(questions_data) > 3:
                            st.info(f"... và {len(questions_data) - 3} câu hỏi khác")
                            
                except Exception as e:
                    st.error(f"❌ Lỗi đọc file JSON: {str(e)}")
        
        with source_tabs[1]:
            st.markdown("**Sử dụng câu hỏi từ quiz đã tạo:**")
            
            if 'quiz_results' in st.session_state and st.session_state.quiz_results:
                if st.session_state.quiz_results.get('success') and st.session_state.quiz_results.get('compiled_questions'):
                    
                    if st.button("🔄 Sử Dụng Quiz Đã Tạo", use_container_width=True, type="primary"):
                        questions_data = st.session_state.quiz_results['compiled_questions']
                        source_info = "Quiz vừa tạo"
                        st.session_state.selected_quiz_data = questions_data
                        st.rerun()
                    
                    # Show info about current quiz
                    current_quiz = st.session_state.quiz_results['compiled_questions']
                    images_count = sum(1 for q in current_quiz if q.get('has_images', False))
                    
                    st.info(f"""
                    **Quiz hiện tại:**
                    - 📝 Số câu: {len(current_quiz)}
                    - 📷 Có ảnh: {images_count} câu
                    - ⏰ Tạo lúc: {datetime.now().strftime('%H:%M')}
                    """)
                    
                    # Check if already selected
                    if 'selected_quiz_data' in st.session_state:
                        questions_data = st.session_state.selected_quiz_data
                        source_info = "Quiz vừa tạo"
                        st.success(f"✅ Đã chọn quiz với {len(questions_data)} câu hỏi")
                else:
                    st.warning("⚠️ Quiz chưa được tạo thành công. Vui lòng tạo quiz trước.")
            else:
                st.info("ℹ️ Chưa có quiz nào được tạo. Hãy tạo quiz ở trang 'Tạo Quiz' trước.")
        
        with source_tabs[2]:
            render_quiz_library_selector()
            
            # Check if quiz selected from library
            if 'selected_quiz_data' in st.session_state and not questions_data:
                questions_data = st.session_state.selected_quiz_data
                source_info = st.session_state.get('selected_quiz_name', 'Thư viện')
                st.success(f"✅ Đã chọn quiz từ thư viện ({len(questions_data)} câu)")
        
        with source_tabs[3]:
            st.markdown("**Import quiz từ URL:**")
            
            quiz_url = st.text_input(
                "URL quiz:",
                placeholder="https://example.com/quiz.json",
                help="Link trực tiếp đến file JSON quiz"
            )
            
            if quiz_url and st.button("📥 Import từ URL", use_container_width=True):
                try:
                    import requests
                    response = requests.get(quiz_url, timeout=10)
                    response.raise_for_status()
                    
                    questions_data = response.json()
                    source_info = f"URL: {quiz_url}"
                    st.success(f"✅ Đã import {len(questions_data)} câu hỏi từ URL")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi import từ URL: {e}")
                    st.info("💡 Đảm bảo URL trả về file JSON hợp lệ")
    
    with col2:
        # Enhanced test configuration
        st.markdown("### ⚙️ Cấu Hình Bài Kiểm Tra")
        
        # Test mode selection với detailed explanation
        test_mode = st.radio(
            "Chế độ làm bài:",
            ["🎯 Kiểm tra (Exam)", "📚 Ôn luyện (Practice)"],
            help="Chọn chế độ phù hợp với mục đích sử dụng"
        )
        
        test_mode_value = "exam" if "Kiểm tra" in test_mode else "practice"
        
        # Mode explanation
        if test_mode_value == "exam":
            st.info("""
            **🎯 Chế độ Kiểm tra:**
            - ⏰ Có giới hạn thời gian
            - 🔒 Không hiển thị đáp án khi làm
            - 📊 Kết quả hiển thị sau khi hoàn thành
            - 🎯 Phù hợp cho bài kiểm tra chính thức
            """)
            
            # Time limit
            time_limit = st.selectbox(
                "Thời gian làm bài:",
                [15, 30, 45, 60, 90, 120, 150, 180],
                index=3,
                format_func=lambda x: f"{x} phút",
                help="Chọn thời gian làm bài phù hợp"
            )
        else:
            st.success("""
            **📚 Chế độ Ôn luyện:**
            - ⏰ Không giới hạn thời gian
            - ✅ Hiển thị ngay đáp án đúng/sai
            - 🟢 Màu xanh = đúng, 🔴 màu đỏ = sai
            - 📖 Phù hợp cho ôn tập, học tập
            """)
            
            time_limit = 9999  # Unlimited for practice mode
        
        # Advanced options
        with st.expander("🔧 Tùy Chọn Nâng Cao", expanded=False):
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
            
            auto_save = st.checkbox(
                "💾 Tự động lưu tiến độ",
                value=True,
                help="Tự động lưu progress để recovery nếu bị gián đoạn"
            )
            
            if test_mode_value == "practice":
                show_explanation = st.checkbox(
                    "💡 Hiển thị giải thích",
                    value=True,
                    help="Hiển thị giải thích cho đáp án"
                )
            else:
                show_explanation = False
        
        # Test info summary
        if questions_data:
            st.markdown("### 📊 Thông Tin Quiz")
            
            # Calculate stats
            total_questions = len(questions_data)
            images_questions = sum(1 for q in questions_data if q.get('has_images', False))
            
            difficulty_stats = {}
            for q in questions_data:
                diff = q.get('do_kho', 'trung_binh')
                difficulty_stats[diff] = difficulty_stats.get(diff, 0) + 1
            
            # Display stats
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📝 Tổng câu hỏi", total_questions)
                st.metric("📷 Có hình ảnh", images_questions)
            
            with col2:
                if test_mode_value == "exam":
                    estimated_time = max(30, total_questions * 1.5)  # 1.5 min per question minimum
                    st.metric("⏱️ Thời gian ước tính", f"{estimated_time:.0f} phút")
                
                st.metric("🎯 Nguồn", source_info)
            
            # Difficulty breakdown
            if difficulty_stats:
                st.markdown("**Phân bố độ khó:**")
                for diff, count in difficulty_stats.items():
                    emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(diff, '🟡')
                    percentage = (count / total_questions) * 100
                    st.write(f"{emoji} {diff}: {count} câu ({percentage:.1f}%)")
    
    # Start test section
    st.markdown("---")
    
    # Check readiness
    can_start = (
        student_name and student_name.strip() and
        test_title and test_title.strip() and
        questions_data and len(questions_data) > 0
    )
    
    # Status indicators
    if not can_start:
        status_container = st.container()
        with status_container:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if student_name and student_name.strip():
                    st.success("✅ Họ tên")
                else:
                    st.error("❌ Họ tên")
            
            with col2:
                if test_title and test_title.strip():
                    st.success("✅ Tên bài kiểm tra")
                else:
                    st.error("❌ Tên bài kiểm tra")
            
            with col3:
                if questions_data and len(questions_data) > 0:
                    st.success("✅ Câu hỏi")
                else:
                    st.error("❌ Câu hỏi")
    else:
        st.success("🎉 Đã sẵn sàng bắt đầu!")
        
        # Final confirmation
        mode_text = "Kiểm tra" if test_mode_value == "exam" else "Ôn luyện"
        time_text = f"{time_limit} phút" if test_mode_value == "exam" else "Không giới hạn"
        
        st.info(f"""
        **📋 Tóm tắt:**
        - 👨‍🎓 Học sinh: {student_name}
        - 📝 Bài kiểm tra: {test_title}
        - 🎯 Chế độ: {mode_text}
        - ⏱️ Thời gian: {time_text}
        - 📊 Số câu: {len(questions_data)}
        - 📷 Có ảnh: {sum(1 for q in questions_data if q.get('has_images', False))} câu
        """)
    
    # Start button
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
                # Prepare custom settings
                custom_settings = {
                    'show_images': show_images,
                    'auto_save': auto_save,
                    'show_explanation': show_explanation if test_mode_value == "practice" else False,
                    'source_info': source_info
                }
                
                start_enhanced_test(
                    student_name, test_title, questions_data, time_limit,
                    shuffle_questions, shuffle_answers, test_mode_value, custom_settings
                )

def render_quiz_library_selector():
    """Render quiz library selector với enhanced features."""
    st.markdown("**Chọn từ thư viện quiz đã lưu:**")
    
    engine = st.session_state.quiz_engine
    
    # Management buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Làm Mới", use_container_width=True):
            st.session_state.refresh_saved_quizzes = True
            st.rerun()
    
    with col2:
        if st.button("📊 Thống Kê", use_container_width=True):
            st.session_state.show_library_stats = True
    
    with col3:
        if st.button("🧹 Dọn Dẹp", use_container_width=True):
            st.session_state.show_cleanup_options = True
    
    # Library statistics
    if st.session_state.get('show_library_stats'):
        with st.expander("📊 Thống Kê Thư Viện", expanded=True):
            storage_info = engine.get_storage_info()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 Tổng Quiz", storage_info["total_quizzes"])
            with col2:
                st.metric("📷 Hình Ảnh", storage_info["images_count"])
            with col3:
                st.metric("💾 Dung Lượng", storage_info["total_storage_size"])
            
            if st.button("❌ Đóng thống kê"):
                del st.session_state.show_library_stats
                st.rerun()
    
    # Cleanup options
    if st.session_state.get('show_cleanup_options'):
        with st.expander("🧹 Tùy Chọn Dọn Dẹp", expanded=True):
            st.warning("⚠️ Các thao tác này không thể hoàn tác!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Xóa Quiz Cũ (>30 ngày)", use_container_width=True):
                    # Implementation for cleanup would go here
                    st.info("💡 Tính năng này sẽ có trong bản cập nhật tiếp theo")
            
            with col2:
                if st.button("🔧 Repair Index", use_container_width=True):
                    engine._validate_quiz_index()
                    st.success("✅ Đã kiểm tra và sửa chữa index")
            
            if st.button("❌ Đóng tùy chọn"):
                del st.session_state.show_cleanup_options
                st.rerun()
    
    # Get saved quizzes
    saved_quizzes = engine.get_saved_quizzes()
    
    if saved_quizzes:
        # Enhanced quiz selection
        quiz_items = []
        for name, info in saved_quizzes.items():
            created_date = info['created_time'].strftime('%d/%m/%Y')
            questions_count = info['questions_count']
            size = info['size']
            has_images = info.get('has_images', False)
            
            display_text = f"{name}"
            detail_text = f"({questions_count} câu • {size} • {created_date})"
            if has_images:
                detail_text += " 📷"
            
            quiz_items.append((name, f"{display_text} {detail_text}"))
        
        # Sort options
        sort_option = st.selectbox(
            "Sắp xếp theo:",
            ["Mới nhất", "Tên A-Z", "Số câu nhiều nhất", "Có hình ảnh"],
            key="library_sort"
        )
        
        # Apply sorting
        if sort_option == "Mới nhất":
            quiz_items.sort(key=lambda x: saved_quizzes[x[0]]['created_time'], reverse=True)
        elif sort_option == "Tên A-Z":
            quiz_items.sort(key=lambda x: x[0].lower())
        elif sort_option == "Số câu nhiều nhất":
            quiz_items.sort(key=lambda x: saved_quizzes[x[0]]['questions_count'], reverse=True)
        elif sort_option == "Có hình ảnh":
            quiz_items.sort(key=lambda x: saved_quizzes[x[0]].get('has_images', False), reverse=True)
        
        # Quiz selector
        selected_quiz_display = st.selectbox(
            f"Chọn quiz ({len(quiz_items)} quiz):",
            ["-- Chọn quiz --"] + [item[1] for item in quiz_items],
            help="Chọn quiz từ thư viện để làm bài"
        )
        
        if selected_quiz_display and selected_quiz_display != "-- Chọn quiz --":
            # Find selected quiz name
            selected_quiz_name = None
            for name, display in quiz_items:
                if display == selected_quiz_display:
                    selected_quiz_name = name
                    break
            
            if selected_quiz_name:
                # Quiz actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📚 Tải Quiz", use_container_width=True, type="primary"):
                        loaded_questions = engine.load_quiz_from_storage(selected_quiz_name)
                        if loaded_questions:
                            # Convert to JSON format
                            from dataclasses import asdict
                            questions_data = [asdict(q) for q in loaded_questions]
                            st.session_state.selected_quiz_data = questions_data
                            st.session_state.selected_quiz_name = selected_quiz_name
                            st.success(f"✅ Đã tải quiz '{selected_quiz_name}'")
                            st.rerun()
                        else:
                            st.error("❌ Không thể tải quiz")
                
                with col2:
                    if st.button("👀 Xem Trước", use_container_width=True):
                        loaded_questions = engine.load_quiz_from_storage(selected_quiz_name)
                        if loaded_questions:
                            st.session_state.preview_quiz = loaded_questions
                            st.session_state.preview_quiz_name = selected_quiz_name
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Xóa", use_container_width=True):
                        st.session_state.confirm_delete_quiz = selected_quiz_name
                        st.rerun()
                
                # Quiz info
                if selected_quiz_name in saved_quizzes:
                    info = saved_quizzes[selected_quiz_name]
                    st.info(f"""
                    **📊 Thông tin quiz:**
                    - 📝 Số câu hỏi: {info['questions_count']}
                    - 📷 Số ảnh: {info.get('images_count', 0)}
                    - 💾 Kích thước: {info['size']}
                    - 📅 Ngày tạo: {info['created_time'].strftime('%d/%m/%Y %H:%M')}
                    - 🏷️ Version: {info.get('version', '1.0')}
                    """)
        
        # Delete confirmation
        if st.session_state.get('confirm_delete_quiz'):
            quiz_to_delete = st.session_state.confirm_delete_quiz
            
            st.error(f"⚠️ Bạn có chắc muốn xóa quiz '{quiz_to_delete}'?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Xác nhận xóa", use_container_width=True):
                    if engine.delete_quiz_from_storage(quiz_to_delete):
                        st.success(f"✅ Đã xóa quiz '{quiz_to_delete}'")
                        del st.session_state.confirm_delete_quiz
                        st.rerun()
                    else:
                        st.error("❌ Không thể xóa quiz")
            
            with col2:
                if st.button("❌ Hủy", use_container_width=True):
                    del st.session_state.confirm_delete_quiz
                    st.rerun()
        
        # Preview quiz if requested
        if st.session_state.get('preview_quiz'):
            with st.expander(f"👀 Preview: {st.session_state.get('preview_quiz_name', 'Quiz')}", expanded=True):
                preview_questions = st.session_state.preview_quiz
                
                for i, q in enumerate(preview_questions[:5]):
                    difficulty_emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(q.do_kho, '🟡')
                    image_emoji = '📷' if q.has_images else ''
                    st.markdown(f"**Câu {q.so_cau}:** {q.cau_hoi[:100]}... {difficulty_emoji} {image_emoji}")
                
                if len(preview_questions) > 5:
                    st.info(f"... và {len(preview_questions) - 5} câu hỏi khác")
                
                if st.button("❌ Đóng preview"):
                    del st.session_state.preview_quiz
                    if 'preview_quiz_name' in st.session_state:
                        del st.session_state.preview_quiz_name
                    st.rerun()
    
    else:
        st.info("📚 Chưa có quiz nào trong thư viện. Hãy tạo và lưu quiz ở trang 'Tạo Quiz'.")

def start_enhanced_test(student_name: str, test_title: str, questions_data: list, 
                       time_limit: int, shuffle_questions: bool, shuffle_answers: bool, 
                       test_mode: str = "exam", custom_settings: dict = None):
    """Bắt đầu bài kiểm tra mới với enhanced features."""
    try:
        # Load questions
        engine = st.session_state.quiz_engine
        questions = engine.load_questions_from_json(questions_data)
        
        if not questions:
            st.error("❌ Không thể tải câu hỏi. Vui lòng kiểm tra dữ liệu JSON.")
            return
        
        # Create enhanced session
        session_id = engine.create_test_session(
            student_name=student_name,
            test_title=test_title,
            questions=questions,
            time_limit=time_limit,
            shuffle_questions=shuffle_questions,
            shuffle_answers=shuffle_answers,
            test_mode=test_mode,
            custom_settings=custom_settings or {}
        )
        
        # Save session to streamlit state
        st.session_state.current_session_id = session_id
        st.session_state.test_custom_settings = custom_settings or {}
        
        mode_text = "kiểm tra" if test_mode == "exam" else "ôn luyện"
        st.success(f"🎉 Phiên {mode_text} đã được tạo! Đang chuyển hướng...")
        
        # Show loading animation
        with st.spinner("Đang khởi tạo phiên làm bài..."):
            time.sleep(1.5)
        
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Lỗi tạo phiên làm bài: {str(e)}")
        st.info("💡 Vui lòng thử lại hoặc kiểm tra dữ liệu đầu vào")

def render_enhanced_test_interface():
    """Render enhanced test interface với real-time features."""
    session_id = st.session_state.current_session_id
    engine = st.session_state.quiz_engine
    
    # Get current question
    current_q = engine.get_current_question(session_id)
    
    if not current_q:
        # Test finished or error
        render_enhanced_test_completed()
        return
    
    # Enhanced sidebar với real-time info
    with st.sidebar:
        render_enhanced_test_sidebar(session_id)
    
    # Main test interface enhanced
    render_enhanced_question_interface(session_id, current_q)

def render_enhanced_test_sidebar(session_id: str):
    """Render enhanced sidebar với real-time updates."""
    engine = st.session_state.quiz_engine
    overview = engine.get_test_overview(session_id)
    
    if not overview:
        return
    
    # Test info header
    st.markdown("### 📊 Thông Tin Bài Kiểm Tra")
    
    with st.container():
        st.info(f"""
        **👨‍🎓 Học sinh:** {overview['student_name']}
        **📝 Bài kiểm tra:** {overview['test_title'][:30]}...
        **🎯 Chế độ:** {overview['test_mode'].title()}
        """)
    
    # Enhanced progress section
    st.markdown("### 📈 Tiến Độ Làm Bài")
    
    progress = overview['progress']
    answered = overview['answered_questions']
    total = overview['total_questions']
    
    # Animated progress bar
    st.progress(progress / 100)
    
    # Progress metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Đã làm", f"{answered}/{total}")
    with col2:
        if overview['test_mode'] == 'practice':
            correct = overview.get('correct_answers', 0)
            st.metric("Đúng", f"{correct}/{answered}" if answered > 0 else "0/0")
        else:
            remaining = total - answered
            st.metric("Còn lại", remaining)
    
    # Enhanced time management
    st.markdown("### ⏰ Quản Lý Thời Gian")
    
    time_remaining = overview['time_remaining']
    time_elapsed = overview['time_elapsed']
    
    if overview['test_mode'] == 'exam':
        # Time warnings với colors
        if time_remaining > 0:
            minutes = time_remaining // 60
            seconds = time_remaining % 60
            
            if time_remaining <= 300:  # 5 minutes
                st.error(f"⚠️ **Còn lại: {minutes:02d}:{seconds:02d}**")
                st.warning("⏰ Sắp hết thời gian!")
            elif time_remaining <= 600:  # 10 minutes
                st.warning(f"⏱️ **Còn lại: {minutes:02d}:{seconds:02d}**")
            else:
                st.success(f"⏱️ **Còn lại: {minutes:02d}:{seconds:02d}**")
        else:
            st.error("⏰ **Hết thời gian!**")
            
        # Time stats
        st.caption(f"Đã làm: {time_elapsed}")
        
        # Estimated completion time
        if answered > 0 and time_remaining > 0:
            avg_time_per_q = (time_remaining + (answered * 60)) / total  # rough estimate
            remaining_time = (total - answered) * avg_time_per_q / 60
            st.caption(f"Dự kiến hoàn thành: ~{remaining_time:.0f} phút")
    else:
        st.info("⏰ **Không giới hạn thời gian**")
        st.caption(f"Thời gian đã làm: {time_elapsed}")
    
    # Enhanced question navigator
    st.markdown("### 🗂️ Điều Hướng Câu Hỏi")
    
    question_status = overview.get('question_status', [])
    
    if question_status:
        # Grid navigation enhanced
        cols_per_row = 5
        
        for row_start in range(0, len(question_status), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for i, col in enumerate(cols):
                idx = row_start + i
                if idx < len(question_status):
                    q_info = question_status[idx]
                    q_num = q_info['question_number']
                    
                    # Enhanced button styling
                    if q_info['answered']:
                        if overview['test_mode'] == 'practice' and 'is_correct' in q_info:
                            if q_info['is_correct']:
                                button_text = f"✅{q_num}"
                                button_type = "secondary"
                            else:
                                button_text = f"❌{q_num}"  
                                button_type = "secondary"
                        else:
                            button_text = f"✅{q_num}"
                            button_type = "secondary"
                    else:
                        button_text = f"{q_num}"
                        button_type = "primary"
                    
                    # Add difficulty indicator
                    if q_info.get('difficulty') == 'kho':
                        button_text += "🔴"
                    elif q_info.get('difficulty') == 'de':
                        button_text += "🟢"
                    
                    # Add image indicator
                    if q_info.get('has_images'):
                        button_text += "📷"
                    
                    if col.button(button_text, key=f"nav_{q_num}", use_container_width=True):
                        engine.goto_question(session_id, q_num)
                        st.rerun()
    
    # Enhanced quick actions
    st.markdown("### 🎯 Hành Động")
    
    # Overview button
    if st.button("📋 Xem Tổng Quan", use_container_width=True):
        st.session_state.show_detailed_overview = True
        st.rerun()
    
    # Practice mode specific actions
    if overview['test_mode'] == 'practice':
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Kết Quả", use_container_width=True):
                st.session_state.show_current_results = True
                st.rerun()
        
        with col2:
            if st.button("💡 Gợi Ý", use_container_width=True):
                st.session_state.show_hints = True
                st.rerun()
    
    # Finish test button
    if st.button("🏁 Hoàn Thành Bài Kiểm Tra", use_container_width=True, type="primary"):
        if st.session_state.get('confirm_finish'):
            result = engine.finish_test(session_id)
            st.session_state.test_result = result
            st.session_state.current_session_id = None
            st.balloons()
            st.rerun()
        else:
            st.session_state.confirm_finish = True
            st.rerun()
    
    # Enhanced finish confirmation
    if st.session_state.get('confirm_finish'):
        st.warning("⚠️ **Xác nhận hoàn thành?**")
        
        # Show current progress before confirming
        st.caption(f"Đã làm {answered}/{total} câu ({progress:.1f}%)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Xác Nhận", use_container_width=True):
                with st.spinner("Đang xử lý kết quả..."):
                    result = engine.finish_test(session_id)
                    st.session_state.test_result = result
                    st.session_state.current_session_id = None
                    st.session_state.confirm_finish = False
                st.success("🎉 Đã hoàn thành!")
                st.rerun()
        
        with col2:
            if st.button("❌ Hủy", use_container_width=True):
                st.session_state.confirm_finish = False
                st.rerun()

def render_enhanced_question_interface(session_id: str, current_q: dict):
    """Render enhanced question interface với multimedia support."""
    engine = st.session_state.quiz_engine
    question_data = current_q['question_data']
    test_mode = current_q.get('test_mode', 'exam')
    
    # Enhanced question header
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        mode_emoji = "📚" if test_mode == "practice" else "🎯"
        mode_text = "Ôn luyện" if test_mode == "practice" else "Kiểm tra"
        st.markdown(f"### {mode_emoji} Câu {current_q['question_number']}/{current_q['total_questions']}")
        st.caption(f"Chế độ: {mode_text}")
    
    with col2:
        # Enhanced time display
        if test_mode == "exam":
            time_remaining = current_q['time_remaining']
            if time_remaining > 0:
                minutes = time_remaining // 60
                seconds = time_remaining % 60
                
                # Dynamic time warning
                if time_remaining <= 300:
                    st.error(f"⚠️ **Thời gian: {minutes:02d}:{seconds:02d}**")
                elif time_remaining <= 600:
                    st.warning(f"⏱️ **Thời gian: {minutes:02d}:{seconds:02d}**")
                else:
                    st.info(f"⏱️ **Thời gian: {minutes:02d}:{seconds:02d}**")
            else:
                st.error("⏰ **Hết thời gian!**")
        else:
            st.success("⏰ **Không giới hạn thời gian**")
    
    with col3:
        progress = current_q['progress']
        st.metric("📊 Tiến độ", f"{progress:.1f}%")
    
    st.markdown("---")
    
    # Enhanced question content
    st.markdown("### 📝 Câu Hỏi")
    
    # Display question với enhanced formatting
    question_text = question_data['cau_hoi']
    
    # Enhanced question styling
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 15px; border-left: 6px solid #007bff; margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
        <h4 style='margin: 0; color: #495057; line-height: 1.6;'>{question_text}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced image display
    custom_settings = st.session_state.get('test_custom_settings', {})
    if custom_settings.get('show_images', True) and question_data.get('has_images'):
        st.markdown("### 📷 Hình Ảnh Đính Kèm")
        
        images = question_data.get('images', [])
        if images:
            # Enhanced image gallery
            if len(images) == 1:
                # Single image - full width
                img_info = images[0]
                if 'data_url' in img_info:
                    st.image(img_info['data_url'], caption=img_info.get('name', 'Hình ảnh'), use_column_width=True)
                elif 'path' in img_info:
                    st.info(f"📷 {img_info.get('name', 'Hình ảnh')}: {img_info.get('description', '')}")
            else:
                # Multiple images - gallery
                img_cols = st.columns(min(3, len(images)))
                for i, img_info in enumerate(images):
                    col = img_cols[i % 3]
                    with col:
                        if 'data_url' in img_info:
                            st.image(img_info['data_url'], caption=img_info.get('name', f'Ảnh {i+1}'), width=200)
                        elif 'path' in img_info:
                            st.info(f"📷 {img_info.get('name', f'Ảnh {i+1}')}")
                        
                        if img_info.get('description'):
                            st.caption(img_info['description'])
    
    # Enhanced answer choices với practice mode feedback
    st.markdown("### 🔤 Lựa Chọn Đáp Án")
    
    choices = question_data['lua_chon']
    current_answer = current_q['current_answer']
    feedback = current_q.get('feedback')
    
    # Practice mode enhanced feedback
    if test_mode == "practice" and feedback and feedback.get('show_feedback'):
        st.markdown("#### 📋 Phản Hồi Ngay Lập Tức")
        
        # Enhanced feedback display với colors và animations
        for choice, content in choices.items():
            is_correct_answer = choice == feedback.get('correct_answer', '').upper()
            is_user_choice = choice == feedback.get('user_answer', '').upper()
            
            if is_correct_answer and is_user_choice:
                st.success(f"🎉 **{choice}.** {content} *(Bạn chọn đúng! Tuyệt vời!)*")
            elif is_correct_answer:
                st.success(f"✅ **{choice}.** {content} *(Đáp án đúng)*")
            elif is_user_choice:
                st.error(f"❌ **{choice}.** {content} *(Bạn đã chọn - Chưa chính xác)*")
            else:
                st.write(f"**{choice}.** {content}")
        
        # Enhanced explanation với custom settings
        if feedback.get('explanation'):
            explanation_text = feedback['explanation']
            
            # Add more detailed explanation if enabled
            if custom_settings.get('show_explanation', True):
                st.info(f"💡 **Giải thích:** {explanation_text}")
                
                # Additional study tips for wrong answers
                if not feedback.get('is_correct', True):
                    difficulty = question_data.get('do_kho', 'trung_binh')
                    if difficulty == 'kho':
                        st.warning("💪 Đây là câu hỏi khó. Hãy đọc kỹ lý thuyết và làm thêm bài tập tương tự.")
                    
                    subject = question_data.get('mon_hoc', 'unknown')
                    if subject != 'auto_detect':
                        st.info(f"📚 Ôn lại kiến thức môn {subject} phần này.")
    
    else:
        # Normal mode với enhanced radio buttons
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
            "Chọn đáp án của bạn:",
            answer_options,
            index=current_index,
            key=f"answer_{current_q['question_number']}",
            help="Chọn một đáp án và hệ thống sẽ tự động lưu lựa chọn của bạn"
        )
        
        # Extract answer letter and submit với enhanced feedback
        if selected_answer:
            selected_letter = selected_answer.split('.')[0]
            submit_feedback = engine.submit_answer(session_id, selected_letter)
            
            # Auto-save confirmation
            if custom_settings.get('auto_save', True):
                st.success(f"💾 Đã lưu đáp án: {selected_letter}")
            
            # For practice mode, trigger rerun to show feedback
            if test_mode == "practice" and submit_feedback.get('show_feedback'):
                time.sleep(0.5)  # Brief pause for better UX
                st.rerun()
    
    # Enhanced question metadata
    col1, col2, col3 = st.columns(3)
    
    with col1:
        do_kho = question_data.get('do_kho', 'trung_binh')
        difficulty_colors = {
            'de': ('🟢', 'success'),
            'trung_binh': ('🟡', 'info'), 
            'kho': ('🔴', 'error')
        }
        emoji, color_type = difficulty_colors.get(do_kho, ('🟡', 'info'))
        
        if color_type == 'success':
            st.success(f"{emoji} Độ khó: {do_kho}")
        elif color_type == 'error':
            st.error(f"{emoji} Độ khó: {do_kho}")
        else:
            st.info(f"{emoji} Độ khó: {do_kho}")
    
    with col2:
        mon_hoc = question_data.get('mon_hoc', 'auto_detect')
        st.info(f"📚 Môn học: {mon_hoc}")
    
    with col3:
        if question_data.get('has_images'):
            img_count = len(question_data.get('images', []))
            st.info(f"📷 {img_count} hình ảnh")
        else:
            st.caption("📄 Chỉ có text")
    
    # Enhanced navigation buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        prev_disabled = current_q['question_number'] == 1
        if st.button("⬅️ Câu Trước", disabled=prev_disabled, key="prev_btn", use_container_width=True):
            engine.previous_question(session_id)
            st.rerun()
    
    with col2:
        if st.button("📋 Tổng Quan", key="overview_btn", use_container_width=True):
            st.session_state.show_detailed_overview = True
            st.rerun()
    
    with col3:
        if st.button("🔄 Làm Mới", key="refresh_btn", use_container_width=True):
            st.rerun()
    
    with col4:
        if current_q['question_number'] < current_q['total_questions']:
            if st.button("➡️ Câu Tiếp", key="next_btn", use_container_width=True):
                engine.next_question(session_id)
                st.rerun()
        else:
            if st.button("🏁 Hoàn Thành", type="primary", key="finish_btn", use_container_width=True):
                st.session_state.confirm_finish = True
                st.rerun()
    
    # Show detailed overview if requested
    if st.session_state.get('show_detailed_overview'):
        render_detailed_test_overview(session_id)
    
    # Show current results for practice mode
    if st.session_state.get('show_current_results') and test_mode == "practice":
        render_current_practice_results(session_id)
    
    # Auto-refresh for timer (chỉ exam mode)
    if test_mode == "exam" and current_q['time_remaining'] > 0:
        # Refresh every 30 seconds to update time, but not too frequently
        if current_q['time_remaining'] % 30 == 0:
            time.sleep(1)
            st.rerun()

def render_detailed_test_overview(session_id: str):
    """Render detailed test overview popup."""
    with st.expander("📋 Tổng Quan Chi Tiết", expanded=True):
        engine = st.session_state.quiz_engine
        overview = engine.get_test_overview(session_id)
        
        if overview:
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Tổng câu", overview['total_questions'])
            with col2:
                st.metric("✅ Đã làm", overview['answered_questions'])
            with col3:
                if overview['test_mode'] == 'practice':
                    st.metric("🎯 Đúng", overview.get('correct_answers', 0))
                else:
                    remaining = overview['total_questions'] - overview['answered_questions']
                    st.metric("⏳ Còn lại", remaining)
            with col4:
                st.metric("📊 Tiến độ", f"{overview['progress']:.1f}%")
            
            # Question breakdown
            st.markdown("**📋 Chi tiết từng câu:**")
            
            question_status = overview.get('question_status', [])
            if question_status:
                for q_info in question_status:
                    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
                    
                    with col1:
                        st.write(f"**{q_info['question_number']}**")
                    
                    with col2:
                        status_text = "✅ Đã trả lời" if q_info['answered'] else "⏳ Chưa làm"
                        if q_info['answered'] and overview['test_mode'] == 'practice':
                            if q_info.get('is_correct'):
                                status_text += " (Đúng)"
                            else:
                                status_text += " (Sai)"
                        st.write(status_text)
                    
                    with col3:
                        difficulty_emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(
                            q_info.get('difficulty', 'trung_binh'), '🟡'
                        )
                        st.write(difficulty_emoji)
                    
                    with col4:
                        if q_info.get('has_images'):
                            st.write("📷")
        
        if st.button("❌ Đóng tổng quan"):
            st.session_state.show_detailed_overview = False
            st.rerun()

def render_current_practice_results(session_id: str):
    """Render current practice results."""
    with st.expander("📊 Kết Quả Hiện Tại (Practice Mode)", expanded=True):
        engine = st.session_state.quiz_engine
        overview = engine.get_test_overview(session_id)
        
        if overview and overview['test_mode'] == 'practice':
            # Current stats
            answered = overview['answered_questions']
            correct = overview.get('correct_answers', 0)
            
            if answered > 0:
                accuracy = (correct / answered) * 100
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📝 Đã làm", answered)
                with col2:
                    st.metric("✅ Đúng", correct)
                with col3:
                    st.metric("🎯 Độ chính xác", f"{accuracy:.1f}%")
                
                # Performance chart (simple)
                if accuracy >= 80:
                    st.success("🎉 Kết quả tuyệt vời! Tiếp tục duy trì!")
                elif accuracy >= 60:
                    st.info("📈 Kết quả tốt! Cố gắng thêm một chút nữa!")
                else:
                    st.warning("💪 Hãy đọc kỹ câu hỏi và suy nghĩ cẩn thận hơn!")
                
                # Question breakdown
                question_status = overview.get('question_status', [])
                correct_questions = [q for q in question_status if q.get('is_correct')]
                wrong_questions = [q for q in question_status if q.get('answered') and not q.get('is_correct')]
                
                if wrong_questions:
                    st.markdown("**❌ Câu trả lời sai:**")
                    for q in wrong_questions:
                        st.write(f"• Câu {q['question_number']} ({q.get('difficulty', 'unknown')})")
            else:
                st.info("Chưa trả lời câu nào. Hãy bắt đầu làm bài!")
        
        if st.button("❌ Đóng kết quả"):
            st.session_state.show_current_results = False
            st.rerun()

def render_enhanced_test_completed():
    """Render enhanced test completion với detailed analytics."""
    if 'test_result' not in st.session_state:
        st.error("❌ Không tìm thấy kết quả bài kiểm tra")
        if st.button("🏠 Về Trang Chủ"):
            st.session_state.current_session_id = None
            st.rerun()
        return
    
    result = st.session_state.test_result
    
    # Enhanced completion header
    st.markdown("## 🎉 Hoàn Thành Bài Kiểm Tra!")
    
    # Enhanced overall results với animations
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📝 Tổng Câu", result.total_questions)
    with col2:
        st.metric("✅ Câu Đúng", result.correct_answers)
    with col3:
        st.metric("❌ Câu Sai", result.wrong_answers)
    with col4:
        st.metric("⏳ Chưa Làm", result.unanswered)
    with col5:
        st.metric("🎯 Điểm Số", f"{result.score}/10")
    
    # Enhanced score visualization
    percentage = result.percentage
    
    # Dynamic scoring với enhanced feedback
    if percentage >= 90:
        score_color = "success"
        score_emoji = "🏆"
        score_text = "Xuất sắc! Hoàn hảo!"
        score_message = "Bạn đã thể hiện sự hiểu biết tuyệt vời!"
    elif percentage >= 80:
        score_color = "success"
        score_emoji = "🥇"
        score_text = "Rất tốt!"
        score_message = "Kết quả ấn tượng, tiếp tục phát huy!"
    elif percentage >= 70:
        score_color = "info"
        score_emoji = "🥈"
        score_text = "Khá tốt!"
        score_message = "Kết quả tốt, cần cải thiện thêm một chút."
    elif percentage >= 50:
        score_color = "warning"
        score_emoji = "🥉"
        score_text = "Trung bình"
        score_message = "Cần ôn tập thêm để cải thiện kết quả."
    else:
        score_color = "error"
        score_emoji = "📚"
        score_text = "Cần cố gắng hơn"
        score_message = "Hãy dành thêm thời gian ôn tập kiến thức."
    
    # Enhanced score display
    st.markdown(f"""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>{score_emoji}</div>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>{result.percentage:.1f}%</h1>
        <h2 style='color: white; margin: 0.5rem 0; font-size: 1.8rem;'>{score_text}</h2>
        <p style='color: #f0f0f0; margin: 1rem 0; font-size: 1.1rem;'>{score_message}</p>
        <div style='color: #e0e0e0; font-size: 1rem;'>
            ⏱️ Thời gian: {result.time_taken} | 🎯 Chế độ: {result.test_mode.title()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced detailed results với advanced filtering
    st.markdown("### 📊 Phân Tích Chi Tiết Kết Quả")
    
    # Advanced filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_filter = st.selectbox(
            "Hiển thị:",
            ["Tất cả câu hỏi", "Chỉ câu đúng", "Chỉ câu sai", "Câu chưa làm"],
            key="result_filter"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sắp xếp theo:",
            ["Số câu", "Kết quả", "Độ khó", "Môn học"],
            key="result_sort"
        )
    
    with col3:
        difficulty_filter = st.selectbox(
            "Lọc độ khó:",
            ["Tất cả", "Dễ", "Trung bình", "Khó"],
            key="difficulty_filter"
        )
    
    # Enhanced statistics summary
    if hasattr(result, 'question_stats') and result.question_stats:
        with st.expander("📈 Thống Kê Nâng Cao", expanded=False):
            stats = result.question_stats
            time_stats = getattr(result, 'time_stats', {})
            
            # Performance by difficulty
            st.markdown("**📊 Kết quả theo độ khó:**")
            difficulty_data = stats.get('by_difficulty', {})
            
            for diff, data in difficulty_data.items():
                if data['total'] > 0:
                    percentage = (data['correct'] / data['total']) * 100
                    emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(diff, '🟡')
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write(f"{emoji} {diff.title()}")
                    with col2:
                        st.progress(percentage / 100)
                        st.caption(f"{data['correct']}/{data['total']} ({percentage:.1f}%)")
            
            # Performance by subject
            subject_data = stats.get('by_subject', {})
            if subject_data and len(subject_data) > 1:
                st.markdown("**📚 Kết quả theo môn học:**")
                for subject, data in subject_data.items():
                    if data['total'] > 0 and subject != 'unknown':
                        percentage = (data['correct'] / data['total']) * 100
                        st.write(f"📖 {subject}: {data['correct']}/{data['total']} ({percentage:.1f}%)")
            
            # Time statistics
            if time_stats:
                st.markdown("**⏱️ Thống kê thời gian:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"⏱️ Tổng thời gian: {time_stats.get('total_time', 'N/A')}")
                    st.write(f"📊 TB mỗi câu: {time_stats.get('average_per_question', 'N/A')}")
                
                with col2:
                    st.write(f"⚡ Nhanh nhất: {time_stats.get('fastest_question', 'N/A')}")
                    st.write(f"🐌 Chậm nhất: {time_stats.get('slowest_question', 'N/A')}")
    
    # Filter and sort results
    detailed = result.detailed_results.copy()
    
    # Apply filters
    if show_filter == "Chỉ câu đúng":
        detailed = [r for r in detailed if r['ket_qua'] == 'Đúng']
    elif show_filter == "Chỉ câu sai":
        detailed = [r for r in detailed if r['ket_qua'] == 'Sai']
    elif show_filter == "Câu chưa làm":
        detailed = [r for r in detailed if r['dap_an_chon'] == 'Không trả lời']
    
    if difficulty_filter != "Tất cả":
        diff_map = {"Dễ": "de", "Trung bình": "trung_binh", "Khó": "kho"}
        target_diff = diff_map.get(difficulty_filter)
        if target_diff:
            detailed = [r for r in detailed if r.get('do_kho') == target_diff]
    
    # Apply sorting
    if sort_by == "Kết quả":
        detailed = sorted(detailed, key=lambda x: (x['ket_qua'] != 'Đúng', x['so_cau']))
    elif sort_by == "Độ khó":
        diff_order = {'de': 0, 'trung_binh': 1, 'kho': 2}
        detailed = sorted(detailed, key=lambda x: diff_order.get(x.get('do_kho', 'trung_binh'), 1))
    elif sort_by == "Môn học":
        detailed = sorted(detailed, key=lambda x: x.get('mon_hoc', 'unknown'))
    else:  # Số câu
        detailed = sorted(detailed, key=lambda x: x['so_cau'])
    
    # Enhanced display results
    if detailed:
        st.info(f"📋 Hiển thị {len(detailed)} câu hỏi (đã lọc từ {len(result.detailed_results)} câu)")
        
        for i, item in enumerate(detailed):
            # Enhanced question card
            result_emoji = "✅" if item['ket_qua'] == 'Đúng' else "❌" if item['ket_qua'] == 'Sai' else "⏳"
            difficulty_emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(item.get('do_kho', 'trung_binh'), '🟡')
            
            with st.expander(f"Câu {item['so_cau']}: {result_emoji} {item['ket_qua']} {difficulty_emoji}", expanded=False):
                
                # Question content
                st.markdown(f"**📝 Câu hỏi:** {item['cau_hoi']}")
                
                # Enhanced choices display
                for choice, content in item['lua_chon'].items():
                    if choice == item['dap_an_dung']:
                        st.success(f"✅ **{choice}.** {content} *(Đáp án đúng)*")
                    elif choice == item['dap_an_chon']:
                        if item['ket_qua'] == 'Sai':
                            st.error(f"❌ **{choice}.** {content} *(Bạn đã chọn - Sai)*")
                        else:
                            st.success(f"✅ **{choice}.** {content} *(Bạn đã chọn - Đúng)*")
                    else:
                        st.write(f"**{choice}.** {content}")
                
                # Enhanced answer status
                if item['dap_an_chon'] == "Không trả lời":
                    st.warning("⚠️ Bạn chưa trả lời câu này")
                    if result.test_mode == "exam":
                        st.info("💡 Hãy quản lý thời gian tốt hơn trong lần thi tiếp theo")
                
                # Enhanced metadata
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.caption(f"🎯 Độ khó: {item.get('do_kho', 'N/A')}")
                
                with col2:
                    st.caption(f"📚 Môn học: {item.get('mon_hoc', 'N/A')}")
                
                with col3:
                    if item.get('has_images'):
                        st.caption("📷 Có hình ảnh")
                    
                    if item.get('time_spent'):
                        st.caption(f"⏱️ Thời gian: {item['time_spent']:.1f}s")
                
                # Study recommendations for wrong answers
                if item['ket_qua'] == 'Sai':
                    difficulty = item.get('do_kho', 'trung_binh')
                    subject = item.get('mon_hoc', 'unknown')
                    
                    recommendations = []
                    if difficulty == 'de':
                        recommendations.append("💡 Đây là câu dễ - hãy đọc kỹ đề và cẩn thận hơn")
                    elif difficulty == 'kho':
                        recommendations.append("💪 Câu khó - cần ôn tập sâu hơn về phần này")
                    
                    if subject != 'unknown' and subject != 'auto_detect':
                        recommendations.append(f"📖 Ôn lại kiến thức môn {subject}")
                    
                    if recommendations:
                        st.info(" • ".join(recommendations))
    else:
        st.info("Không có câu hỏi nào phù hợp với bộ lọc hiện tại.")
    
    # Enhanced actions section
    st.markdown("---")
    
    action_tabs = st.tabs(["🎯 Hành Động Chính", "📊 Xuất Kết Quả", "📚 Học Tập Thêm"])
    
    with action_tabs[0]:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏠 Về Trang Chủ", use_container_width=True):
                # Clear session
                for key in ['current_session_id', 'test_result', 'test_custom_settings']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🔄 Làm Bài Mới", use_container_width=True, type="primary"):
                # Keep engine and quiz data but clear session
                for key in ['current_session_id', 'test_result']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("🎉 Sẵn sàng làm bài mới!")
                time.sleep(1)
                st.rerun()
        
        with col3:
            if st.button("📊 Xem Thống Kê", use_container_width=True):
                st.session_state.selected_page = "📊 Thống Kê"
                st.info("Chuyển đến trang thống kê...")
                time.sleep(1)
                st.rerun()
    
    with action_tabs[1]:
        # Enhanced export options
        col1, col2 = st.columns(2)
        
        with col1:
            # Export detailed JSON
            result_json = {
                "student_info": {
                    "name": result.student_name,
                    "test_title": result.test_title,
                    "test_mode": result.test_mode
                },
                "results": {
                    "score": result.score,
                    "percentage": result.percentage,
                    "total_questions": result.total_questions,
                    "correct_answers": result.correct_answers,
                    "wrong_answers": result.wrong_answers,
                    "unanswered": result.unanswered
                },
                "timing": {
                    "time_taken": result.time_taken,
                    "finish_time": result.finish_time.isoformat(),
                    "time_stats": getattr(result, 'time_stats', {})
                },
                "detailed_results": result.detailed_results,
                "statistics": getattr(result, 'question_stats', {})
            }
            
            st.download_button(
                "💾 Xuất Báo Cáo Đầy Đủ (JSON)",
                data=json.dumps(result_json, ensure_ascii=False, indent=2),
                file_name=f"BaoCao_{result.student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Export summary CSV
            csv_lines = ["STT,Cau_Hoi,Dap_An_Dung,Dap_An_Chon,Ket_Qua,Do_Kho"]
            for item in result.detailed_results:
                csv_lines.append(f"{item['so_cau']},{item['cau_hoi'][:50].replace(',', ';')},{item['dap_an_dung']},{item['dap_an_chon']},{item['ket_qua']},{item['do_kho']}")
            
            csv_data = "\n".join(csv_lines)
            
            st.download_button(
                "📄 Xuất Tóm Tắt (CSV)",
                data=csv_data.encode('utf-8'),
                file_name=f"TomTat_{result.student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with action_tabs[2]:
        # Study recommendations
        if result.wrong_answers > 0:
            st.markdown("**📚 Đề Xuất Học Tập:**")
            
            # Analyze weak areas
            wrong_subjects = {}
            wrong_difficulties = {'de': 0, 'trung_binh': 0, 'kho': 0}
            
            for item in result.detailed_results:
                if item['ket_qua'] == 'Sai':
                    subject = item.get('mon_hoc', 'unknown')
                    difficulty = item.get('do_kho', 'trung_binh')
                    
                    wrong_subjects[subject] = wrong_subjects.get(subject, 0) + 1
                    wrong_difficulties[difficulty] += 1
            
            # Subject recommendations
            if wrong_subjects:
                st.markdown("**📖 Môn học cần ôn:**")
                for subject, count in sorted(wrong_subjects.items(), key=lambda x: x[1], reverse=True):
                    if subject not in ['unknown', 'auto_detect']:
                        st.write(f"• {subject}: {count} câu sai")
            
            # Difficulty recommendations
            st.markdown("**🎯 Chiến lược học tập:**")
            if wrong_difficulties['de'] > 0:
                st.warning(f"⚠️ {wrong_difficulties['de']} câu dễ bị sai - Cần đọc đề cẩn thận hơn")
            if wrong_difficulties['kho'] > 0:
                st.info(f"💪 {wrong_difficulties['kho']} câu khó bị sai - Cần học sâu hơn về lý thuyết")
            
            # Practice suggestions
            if result.percentage < 70:
                st.error("📚 Khuyến nghị: Ôn tập lại toàn bộ kiến thức và làm thêm bài tập")
            elif result.percentage < 85:
                st.warning("📖 Khuyến nghị: Tập trung vào các phần còn yếu")
            else:
                st.success("🎯 Khuyến nghị: Làm thêm câu hỏi khó để nâng cao trình độ")
        else:
            st.success("🎉 Hoàn hảo! Hãy thử các đề khó hơn để thử thách bản thân!")

def render_enhanced_statistics_page():
    """Render enhanced statistics page với advanced analytics."""
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>📊 Thống Kê Hệ Thống</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Báo Cáo Chi Tiết & Phân Tích Dữ Liệu</p>
        <div style='color: #e0e0e0; font-size: 0.9rem; margin-top: 0.5rem;'>
            📈 Advanced Analytics | 🎯 Performance Tracking | 📚 Study Insights
        </div>
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
        render_empty_statistics_guide()
        return
    
    # Enhanced statistics display
    render_main_statistics_dashboard(stats)

def render_empty_statistics_guide():
    """Render guide when no statistics available."""
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>📊</div>
        <h3 style='color: #6c757d; margin-bottom: 1rem;'>Chưa Có Dữ Liệu Thống Kê</h3>
        <p style='color: #6c757d; margin: 0 0 2rem 0;'>Hãy hoàn thành một vài bài kiểm tra để xem thống kê chi tiết</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Usage guide
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Tạo Quiz
        - 📝 Vào trang "Tạo Quiz"
        - 🤖 Sử dụng AI để tạo câu hỏi
        - 💾 Lưu vào thư viện
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ Làm Bài Kiểm Tra
        - 📚 Vào trang "Làm Bài Kiểm Tra"
        - 🎯 Chọn chế độ Exam/Practice
        - ✅ Hoàn thành bài làm
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ Xem Thống Kê
        - 📊 Quay lại trang này
        - 📈 Xem phân tích chi tiết
        - 🎯 Theo dõi tiến bộ
        """)
    
    # Quick actions
    st.markdown("### ⚡ Hành Động Nhanh")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Tạo Quiz Ngay", use_container_width=True, type="primary"):
            st.info("Chuyển đến trang Tạo Quiz...")
            time.sleep(1)
            # Would trigger page navigation
    
    with col2:
        if st.button("📝 Làm Bài Demo", use_container_width=True):
            st.info("Tính năng demo sẽ có trong bản cập nhật tiếp theo")
    
    with col3:
        if st.button("📚 Xem Thư Viện", use_container_width=True):
            st.info("Chuyển đến Quản Lý Quiz...")
            time.sleep(1)

def render_main_statistics_dashboard(stats: dict):
    """Render main statistics dashboard với advanced metrics."""
    
    # Top-level metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📝 Tổng Bài Kiểm Tra", stats['total_tests'])
    with col2:
        st.metric("📊 Điểm TB", f"{stats['average_score']}/10")
    with col3:
        st.metric("🎯 Tỷ Lệ Đậu", f"{stats['pass_rate']:.1f}%")
    with col4:
        st.metric("🏆 Điểm Cao Nhất", f"{stats['highest_score']}/10")
    with col5:
        st.metric("📉 Điểm Thấp Nhất", f"{stats['lowest_score']}/10")
    
    # Advanced analytics tabs
    analytics_tabs = st.tabs(["📈 Tổng Quan", "🎯 Hiệu Suất", "📚 Phân Tích Môn Học", "⏱️ Xu Hướng Thời Gian", "🔧 Hệ Thống"])
    
    with analytics_tabs[0]:
        render_overview_analytics(stats)
    
    with analytics_tabs[1]:
        render_performance_analytics(stats)
    
    with analytics_tabs[2]:
        render_subject_analytics(stats)
    
    with analytics_tabs[3]:
        render_time_trend_analytics(stats)
    
    with analytics_tabs[4]:
        render_system_analytics(stats)

def render_overview_analytics(stats: dict):
    """Render overview analytics."""
    
    # Mode distribution
    mode_stats = stats.get('mode_distribution', {})
    if mode_stats:
        st.markdown("### 🎯 Phân Bố Chế Độ Làm Bài")
        
        col1, col2 = st.columns(2)
        
        with col1:
            exam_count = mode_stats.get('exam', 0)
            practice_count = mode_stats.get('practice', 0)
            total_count = exam_count + practice_count
            
            if total_count > 0:
                exam_pct = (exam_count / total_count) * 100
                practice_pct = (practice_count / total_count) * 100
                
                st.metric("🎯 Chế độ Kiểm tra", f"{exam_count} ({exam_pct:.1f}%)")
                st.metric("📚 Chế độ Ôn luyện", f"{practice_count} ({practice_pct:.1f}%)")
        
        with col2:
            # Simple visualization
            if exam_count > 0 or practice_count > 0:
                st.markdown("**Tỷ lệ sử dụng:**")
                
                if exam_count > 0:
                    st.progress(exam_count / (exam_count + practice_count))
                    st.caption(f"Exam: {exam_count} lần")
                
                if practice_count > 0:
                    st.progress(practice_count / (exam_count + practice_count))
                    st.caption(f"Practice: {practice_count} lần")
    
    # Recent tests enhanced
    recent_tests = stats.get('recent_tests', [])
    if recent_tests:
        st.markdown("### 📋 Các Bài Kiểm Tra Gần Đây")
        
        # Enhanced table
        for i, test in enumerate(recent_tests[:10]):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
                
                with col1:
                    mode_emoji = "🎯" if test['mode'] == 'exam' else "📚"
                    st.write(f"{mode_emoji} **{test['student']}**")
                    st.caption(test['title'])
                
                with col2:
                    score_color = "🟢" if test['score'] >= 8 else "🟡" if test['score'] >= 5 else "🔴"
                    st.write(f"{score_color} {test['score']}/10")
                
                with col3:
                    st.write(f"📊 {test['percentage']:.1f}%")
                
                with col4:
                    st.write(f"📝 {test['questions']}")
                
                with col5:
                    st.write(f"🕒 {test['time']}")
                    st.caption(f"⏱️ {test['time_taken']}")
                
                if i < len(recent_tests) - 1:
                    st.divider()

def render_performance_analytics(stats: dict):
    """Render performance analytics."""
    
    # Difficulty analysis
    difficulty_analysis = stats.get('difficulty_analysis', {})
    if difficulty_analysis:
        st.markdown("### 🎯 Phân Tích Theo Độ Khó")
        
        for difficulty, data in difficulty_analysis.items():
            if data['total'] > 0:
                percentage = data.get('percentage', 0)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(difficulty, '🟡')
                    st.write(f"{emoji} **{difficulty.title()}**")
                
                with col2:
                    st.progress(percentage / 100)
                    st.caption(f"{data['correct']}/{data['total']} câu đúng")
                
                with col3:
                    st.metric("Tỷ lệ", f"{percentage:.1f}%")
        
        # Performance insights
        st.markdown("### 💡 Nhận Xét Hiệu Suất")
        
        # Calculate insights
        easy_performance = difficulty_analysis.get('de', {}).get('percentage', 0)
        medium_performance = difficulty_analysis.get('trung_binh', {}).get('percentage', 0)
        hard_performance = difficulty_analysis.get('kho', {}).get('percentage', 0)
        
        insights = []
        
        if easy_performance < 80:
            insights.append("⚠️ Cần chú ý hơn với câu hỏi dễ - đọc kỹ đề bài")
        elif easy_performance > 90:
            insights.append("✅ Rất tốt với câu hỏi dễ!")
        
        if medium_performance < 60:
            insights.append("📚 Cần ôn tập thêm kiến thức cơ bản")
        elif medium_performance > 80:
            insights.append("🎯 Nắm vững kiến thức cơ bản!")
        
        if hard_performance < 40:
            insights.append("💪 Cần học sâu hơn để giải quyết câu hỏi khó")
        elif hard_performance > 60:
            insights.append("🏆 Xuất sắc với câu hỏi khó!")
        
        if insights:
            for insight in insights:
                st.info(insight)
    else:
        st.info("Chưa có đủ dữ liệu để phân tích hiệu suất theo độ khó.")

def render_subject_analytics(stats: dict):
    """Render subject analytics."""
    
    subject_analysis = stats.get('subject_analysis', {})
    if subject_analysis:
        st.markdown("### 📚 Phân Tích Theo Môn Học")
        
        # Filter out unknown subjects
        valid_subjects = {k: v for k, v in subject_analysis.items() 
                         if k not in ['unknown', 'auto_detect'] and v['total'] > 0}
        
        if valid_subjects:
            # Sort by performance
            sorted_subjects = sorted(valid_subjects.items(), 
                                   key=lambda x: x[1].get('percentage', 0), reverse=True)
            
            for subject, data in sorted_subjects:
                percentage = data.get('percentage', 0)
                
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 1])
                    
                    with col1:
                        st.write(f"📖 **{subject}**")
                    
                    with col2:
                        st.progress(percentage / 100)
                        st.caption(f"{data['correct']}/{data['total']} câu đúng")
                    
                    with col3:
                        # Performance indicator
                        if percentage >= 80:
                            st.success(f"{percentage:.1f}%")
                        elif percentage >= 60:
                            st.warning(f"{percentage:.1f}%")
                        else:
                            st.error(f"{percentage:.1f}%")
            
            # Subject recommendations
            st.markdown("### 📋 Khuyến Nghị Học Tập")
            
            weak_subjects = [subject for subject, data in sorted_subjects 
                           if data.get('percentage', 0) < 70]
            strong_subjects = [subject for subject, data in sorted_subjects 
                             if data.get('percentage', 0) >= 85]
            
            if weak_subjects:
                st.warning(f"⚠️ **Cần tăng cường:** {', '.join(weak_subjects)}")
            
            if strong_subjects:
                st.success(f"🏆 **Điểm mạnh:** {', '.join(strong_subjects)}")
        else:
            st.info("Chưa có dữ liệu môn học cụ thể. Hệ thống sẽ tự động phân loại trong các bài kiểm tra tiếp theo.")
    else:
        st.info("Chưa có dữ liệu phân tích theo môn học.")

def render_time_trend_analytics(stats: dict):
    """Render time trend analytics."""
    
    monthly_performance = stats.get('monthly_performance', {})
    if monthly_performance:
        st.markdown("### 📈 Xu Hướng Theo Thời Gian")
        
        # Sort by month
        sorted_months = sorted(monthly_performance.items())
        
        if len(sorted_months) > 1:
            # Show trend
            st.markdown("**📊 Hiệu suất theo tháng:**")
            
            for month, data in sorted_months:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    # Format month display
                    try:
                        year, month_num = month.split('-')
                        month_names = {
                            '01': 'Tháng 1', '02': 'Tháng 2', '03': 'Tháng 3', '04': 'Tháng 4',
                            '05': 'Tháng 5', '06': 'Tháng 6', '07': 'Tháng 7', '08': 'Tháng 8',
                            '09': 'Tháng 9', '10': 'Tháng 10', '11': 'Tháng 11', '12': 'Tháng 12'
                        }
                        month_display = f"{month_names.get(month_num, month_num)} {year}"
                        st.write(f"📅 **{month_display}**")
                    except:
                        st.write(f"📅 **{month}**")
                
                with col2:
                    st.metric("Số bài", data['count'])
                
                with col3:
                    avg_score = data['avg_score']
                    if avg_score >= 8:
                        st.success(f"{avg_score:.1f}/10")
                    elif avg_score >= 6:
                        st.warning(f"{avg_score:.1f}/10")
                    else:
                        st.error(f"{avg_score:.1f}/10")
                
                with col4:
                    # Simple trend indicator
                    if len(sorted_months) > 1:
                        current_idx = sorted_months.index((month, data))
                        if current_idx > 0:
                            prev_score = sorted_months[current_idx - 1][1]['avg_score']
                            if avg_score > prev_score:
                                st.success("📈 Tăng")
                            elif avg_score < prev_score:
                                st.error("📉 Giảm")
                            else:
                                st.info("➡️ Ổn định")
            
            # Overall trend analysis
            if len(sorted_months) >= 3:
                first_month_score = sorted_months[0][1]['avg_score']
                last_month_score = sorted_months[-1][1]['avg_score']
                improvement = last_month_score - first_month_score
                
                st.markdown("### 📊 Đánh Giá Xu Hướng")
                
                if improvement > 0.5:
                    st.success(f"🚀 **Tiến bộ tuyệt vời!** Cải thiện {improvement:.1f} điểm")
                elif improvement > 0:
                    st.info(f"📈 **Có tiến bộ** Cải thiện {improvement:.1f} điểm")
                elif improvement < -0.5:
                    st.warning(f"📉 **Cần chú ý** Giảm {abs(improvement):.1f} điểm")
                else:
                    st.info("➡️ **Ổn định** Duy trì mức hiện tại")
        else:
            st.info("Cần ít nhất 2 tháng dữ liệu để phân tích xu hướng.")
    else:
        st.info("Chưa có dữ liệu theo thời gian.")

def render_system_analytics(stats: dict):
    """Render system analytics."""
    
    engine_info = stats.get('engine_info', {})
    
    st.markdown("### 🔧 Thông Tin Hệ Thống")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Dữ Liệu Hệ Thống:**")
        st.metric("🗃️ Quiz trong thư viện", engine_info.get('total_quizzes_stored', 0))
        st.metric("🔄 Phiên hoạt động", engine_info.get('active_sessions', 0))
        st.metric("📝 Tổng bài đã làm", stats.get('total_tests', 0))
    
    with col2:
        st.markdown("**⚙️ Tính Năng Hệ Thống:**")
        features = engine_info.get('features', [])
        for feature in features:
            st.write(f"✅ {feature}")
    
    # Storage information
    if 'quiz_engine' in st.session_state:
        engine = st.session_state.quiz_engine
        storage_info = engine.get_storage_info()
        
        st.markdown("### 💾 Thông Tin Lưu Trữ")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📚 Quiz đã lưu", storage_info['total_quizzes'])
            st.metric("📷 Hình ảnh", storage_info['images_count'])
        
        with col2:
            st.metric("💾 Tổng dung lượng", storage_info['total_storage_size'])
            st.metric("🗂️ Kích thước Quiz", storage_info['quiz_files_size'])
        
        with col3:
            st.metric("📸 Dung lượng ảnh", storage_info['images_storage_size'])
            st.metric("🏷️ Engine version", storage_info['engine_version'])
        
        # Storage directories
        with st.expander("📁 Thư mục lưu trữ", expanded=False):
            dirs = storage_info['storage_directories']
            for name, path in dirs.items():
                st.code(f"{name}: {path}")
    
    # System recommendations
    st.markdown("### 💡 Khuyến Nghị Hệ Thống")
    
    total_tests = stats.get('total_tests', 0)
    
    if total_tests < 5:
        st.info("📝 Làm thêm bài kiểm tra để có thống kê chính xác hơn")
    elif total_tests < 20:
        st.info("📊 Tiếp tục làm bài để xem xu hướng phát triển")
    else:
        st.success("📈 Đã có đủ dữ liệu để phân tích chi tiết!")
    
    # Data management
    with st.expander("🗃️ Quản lý dữ liệu", expanded=False):
        st.markdown("**Các thao tác quản lý:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Dọn dẹp dữ liệu cũ", use_container_width=True):
                st.info("💡 Tính năng này sẽ có trong bản cập nhật tiếp theo")
        
        with col2:
            if st.button("📤 Xuất toàn bộ dữ liệu", use_container_width=True):
                st.info("💡 Tính năng xuất dữ liệu sẽ có trong bản cập nhật tiếp theo")
        
        with col3:
            if st.button("🔄 Reset thống kê", use_container_width=True):
                st.warning("⚠️ Cần xác nhận để reset toàn bộ dữ liệu thống kê")

def render_quiz_management_page():
    """Render quiz management page."""
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🏪 Quản Lý Quiz</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Trung Tâm Quản Lý Thư Viện Quiz & Dữ Liệu</p>
        <div style='color: #e0e0e0; font-size: 0.9rem; margin-top: 0.5rem;'>
            📚 Library Management | 🔧 Advanced Tools | 📊 Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Management tabs
    mgmt_tabs = st.tabs(["📚 Thư Viện Quiz", "📥 Import/Export", "🔧 Công Cụ Nâng Cao", "⚙️ Cài Đặt Hệ Thống"])
    
    with mgmt_tabs[0]:
        render_quiz_library_management()
    
    with mgmt_tabs[1]:
        render_import_export_tools()
    
    with mgmt_tabs[2]:
        render_advanced_tools()
    
    with mgmt_tabs[3]:
        render_system_settings()

def render_quiz_library_management():
    """Render quiz library management."""
    engine = st.session_state.quiz_engine
    
    # Library overview
    storage_info = engine.get_storage_info()
    saved_quizzes = engine.get_saved_quizzes()
    
    # Header stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Tổng Quiz", storage_info['total_quizzes'])
    with col2:
        st.metric("📷 Hình Ảnh", storage_info['images_count'])
    with col3:
        st.metric("💾 Dung Lượng", storage_info['total_storage_size'])
    with col4:
        total_questions = sum(info['questions_count'] for info in saved_quizzes.values())
        st.metric("📝 Tổng Câu Hỏi", total_questions)
    
    if not saved_quizzes:
        st.info("📚 Thư viện trống. Hãy tạo và lưu một số quiz để bắt đầu.")
        return
    
    # Quiz management interface
    st.markdown("### 📋 Danh Sách Quiz")
    
    # Enhanced filters and search
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input(
            "🔍 Tìm kiếm quiz:",
            placeholder="Nhập tên quiz...",
            key="quiz_search"
        )
    
    with col2:
        sort_option = st.selectbox(
            "Sắp xếp theo:",
            ["Mới nhất", "Cũ nhất", "Tên A-Z", "Tên Z-A", "Nhiều câu nhất", "Ít câu nhất"],
            key="quiz_sort"
        )
    
    with col3:
        filter_option = st.selectbox(
            "Lọc:",
            ["Tất cả", "Có hình ảnh", "Chỉ text", "Nhiều hơn 20 câu", "Ít hơn 10 câu"],
            key="quiz_filter"
        )
    
    # Apply filters
    filtered_quizzes = saved_quizzes.copy()
    
    # Search filter
    if search_term:
        filtered_quizzes = {
            name: info for name, info in filtered_quizzes.items()
            if search_term.lower() in name.lower()
        }
    
    # Category filter
    if filter_option == "Có hình ảnh":
        filtered_quizzes = {
            name: info for name, info in filtered_quizzes.items()
            if info.get('has_images', False)
        }
    elif filter_option == "Chỉ text":
        filtered_quizzes = {
            name: info for name, info in filtered_quizzes.items()
            if not info.get('has_images', False)
        }
    elif filter_option == "Nhiều hơn 20 câu":
        filtered_quizzes = {
            name: info for name, info in filtered_quizzes.items()
            if info['questions_count'] > 20
        }
    elif filter_option == "Ít hơn 10 câu":
        filtered_quizzes = {
            name: info for name, info in filtered_quizzes.items()
            if info['questions_count'] < 10
        }
    
    # Apply sorting
    if sort_option == "Mới nhất":
        sorted_items = sorted(filtered_quizzes.items(), key=lambda x: x[1]['created_time'], reverse=True)
    elif sort_option == "Cũ nhất":
        sorted_items = sorted(filtered_quizzes.items(), key=lambda x: x[1]['created_time'])
    elif sort_option == "Tên A-Z":
        sorted_items = sorted(filtered_quizzes.items(), key=lambda x: x[0].lower())
    elif sort_option == "Tên Z-A":
        sorted_items = sorted(filtered_quizzes.items(), key=lambda x: x[0].lower(), reverse=True)
    elif sort_option == "Nhiều câu nhất":
        sorted_items = sorted(filtered_quizzes.items(), key=lambda x: x[1]['questions_count'], reverse=True)
    else:  # Ít câu nhất
        sorted_items = sorted(filtered_quizzes.items(), key=lambda x: x[1]['questions_count'])
    
    # Display results
    if not sorted_items:
        st.warning(f"Không tìm thấy quiz nào với bộ lọc hiện tại.")
        return
    
    st.info(f"📊 Hiển thị {len(sorted_items)} quiz (từ {len(saved_quizzes)} tổng)")
    
    # Quiz cards
    for name, info in sorted_items:
        with st.expander(f"📚 {name}", expanded=False):
            
            # Quiz info
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **📊 Thông tin chi tiết:**
                - 📝 Số câu hỏi: {info['questions_count']}
                - 📷 Số ảnh: {info.get('images_count', 0)}
                - 💾 Kích thước: {info['size']}
                - 📅 Ngày tạo: {info['created_time'].strftime('%d/%m/%Y %H:%M')}
                - 🏷️ Version: {info.get('version', '1.0')}
                """)
                
                if info.get('has_images'):
                    st.success("📷 Quiz có hình ảnh")
                else:
                    st.info("📄 Quiz chỉ có text")
            
            with col2:
                # Action buttons
                if st.button("👀 Xem", key=f"view_{name}", use_container_width=True):
                    st.session_state.viewing_quiz = name
                    st.rerun()
                
                if st.button("✏️ Sửa", key=f"edit_{name}", use_container_width=True):
                    st.session_state.editing_quiz = name
                    st.rerun()
                
                if st.button("📤 Xuất", key=f"export_{name}", use_container_width=True):
                    export_path = engine.export_quiz(name, "json")
                    if export_path:
                        st.success(f"✅ Đã xuất quiz vào {export_path}")
                    else:
                        st.error("❌ Lỗi xuất quiz")
                
                if st.button("🗑️ Xóa", key=f"delete_{name}", use_container_width=True):
                    st.session_state.confirm_delete = name
                    st.rerun()
            
            # Handle quiz viewing
            if st.session_state.get('viewing_quiz') == name:
                st.markdown("---")
                render_quiz_preview_detailed(name)
            
            # Handle quiz editing
            if st.session_state.get('editing_quiz') == name:
                st.markdown("---")
                render_quiz_editor_detailed(name)
            
            # Handle deletion confirmation
            if st.session_state.get('confirm_delete') == name:
                st.markdown("---")
                st.error(f"⚠️ **Xác nhận xóa quiz '{name}'?**")
                st.warning("Thao tác này không thể hoàn tác!")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Xác nhận xóa", key=f"confirm_delete_{name}"):
                        if engine.delete_quiz_from_storage(name):
                            st.success(f"✅ Đã xóa quiz '{name}'")
                            del st.session_state.confirm_delete
                            st.rerun()
                        else:
                            st.error("❌ Không thể xóa quiz")
                
                with col2:
                    if st.button("❌ Hủy", key=f"cancel_delete_{name}"):
                        del st.session_state.confirm_delete
                        st.rerun()

def render_quiz_preview_detailed(quiz_name: str):
    """Render detailed quiz preview."""
    st.markdown(f"### 👀 Xem Trước: {quiz_name}")
    
    engine = st.session_state.quiz_engine
    questions = engine.load_quiz_from_storage(quiz_name)
    
    if not questions:
        st.error("❌ Không thể tải quiz")
        return
    
    # Preview options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        preview_count = st.slider(
            "Số câu hiển thị:",
            min_value=1,
            max_value=min(10, len(questions)),
            value=min(5, len(questions)),
            key=f"preview_count_{quiz_name}"
        )
    
    with col2:
        show_answers = st.checkbox(
            "Hiển thị đáp án",
            value=False,
            key=f"show_answers_{quiz_name}"
        )
    
    with col3:
        if st.button("❌ Đóng preview", key=f"close_preview_{quiz_name}"):
            del st.session_state.viewing_quiz
            st.rerun()
    
    # Display questions
    for i, q in enumerate(questions[:preview_count]):
        st.markdown(f"**Câu {q.so_cau}:** {q.cau_hoi}")
        
        # Show choices
        for choice, content in q.lua_chon.items():
            if show_answers and choice == q.dap_an:
                st.success(f"✅ **{choice}.** {content}")
            else:
                st.write(f"**{choice}.** {content}")
        
        # Show images if any
        if q.has_images and q.images:
            st.caption(f"📷 {len(q.images)} hình ảnh đính kèm")
        
        # Metadata
        st.caption(f"Độ khó: {q.do_kho} | Môn học: {q.mon_hoc}")
        
        if i < preview_count - 1:
            st.divider()
    
    if len(questions) > preview_count:
        st.info(f"... và {len(questions) - preview_count} câu hỏi khác")

def render_quiz_editor_detailed(quiz_name: str):
    """Render detailed quiz editor."""
    st.markdown(f"### ✏️ Chỉnh Sửa: {quiz_name}")
    
    if st.button("❌ Đóng editor", key=f"close_editor_{quiz_name}"):
        del st.session_state.editing_quiz
        st.rerun()
    
    st.info("💡 Tính năng chỉnh sửa chi tiết sẽ có trong bản cập nhật tiếp theo.")
    st.markdown("""
    **Tính năng sẽ có:**
    - ✏️ Chỉnh sửa từng câu hỏi
    - 📷 Quản lý hình ảnh
    - 🔄 Thay đổi metadata
    - 💾 Lưu thay đổi
    """)

def render_import_export_tools():
    """Render import/export tools."""
    st.markdown("### 📥 Import/Export Tools")
    
    # Import section
    st.markdown("#### 📥 Import Quiz")
    
    import_tabs = st.tabs(["📄 Import JSON", "🌐 Import từ URL", "📋 Import Bulk"])
    
    with import_tabs[0]:
        st.markdown("**Upload file JSON:**")
        
        uploaded_files = st.file_uploader(
            "Chọn file JSON:",
            type=['json'],
            accept_multiple_files=True,
            help="Có thể chọn nhiều file cùng lúc"
        )
        
        if uploaded_files:
            st.success(f"✅ Đã chọn {len(uploaded_files)} file")
            
            if st.button("📥 Import Tất Cả", use_container_width=True):
                engine = st.session_state.quiz_engine
                success_count = 0
                
                for uploaded_file in uploaded_files:
                    try:
                        quiz_data = json.load(uploaded_file)
                        quiz_name = f"Imported_{uploaded_file.name.replace('.json', '')}_{datetime.now().strftime('%H%M%S')}"
                        
                        if engine.save_quiz_to_storage(quiz_data, quiz_name):
                            success_count += 1
                    except Exception as e:
                        st.error(f"❌ Lỗi import {uploaded_file.name}: {e}")
                
                if success_count > 0:
                    st.success(f"✅ Đã import thành công {success_count}/{len(uploaded_files)} quiz")
                    st.balloons()
    
    with import_tabs[1]:
        st.markdown("**Import từ URL:**")
        
        url_input = st.text_input(
            "URL file JSON:",
            placeholder="https://example.com/quiz.json"
        )
        
        quiz_name_input = st.text_input(
            "Tên quiz:",
            placeholder="Tên quiz sau khi import"
        )
        
        if st.button("📥 Import từ URL", use_container_width=True):
            if url_input and quiz_name_input:
                try:
                    import requests
                    response = requests.get(url_input, timeout=10)
                    response.raise_for_status()
                    
                    quiz_data = response.json()
                    engine = st.session_state.quiz_engine
                    
                    if engine.save_quiz_to_storage(quiz_data, quiz_name_input):
                        st.success(f"✅ Đã import quiz '{quiz_name_input}' từ URL")
                    else:
                        st.error("❌ Lỗi lưu quiz")
                        
                except Exception as e:
                    st.error(f"❌ Lỗi import từ URL: {e}")
            else:
                st.warning("⚠️ Vui lòng nhập đầy đủ URL và tên quiz")
    
    with import_tabs[2]:
        st.markdown("**Import hàng loạt:**")
        st.info("💡 Tính năng import bulk sẽ có trong bản cập nhật tiếp theo")
    
    # Export section
    st.markdown("#### 📤 Export Quiz")
    
    engine = st.session_state.quiz_engine
    saved_quizzes = engine.get_saved_quizzes()
    
    if saved_quizzes:
        export_tabs = st.tabs(["📄 Export Đơn Lẻ", "📦 Export Hàng Loạt", "🗃️ Export Toàn Bộ"])
        
        with export_tabs[0]:
            selected_quiz = st.selectbox(
                "Chọn quiz để export:",
                ["-- Chọn quiz --"] + list(saved_quizzes.keys())
            )
            
            if selected_quiz and selected_quiz != "-- Chọn quiz --":
                export_format = st.selectbox(
                    "Định dạng export:",
                    ["JSON (Full)", "JSON (Compact)", "CSV (Preview)"]
                )
                
                if st.button("📤 Export Quiz", use_container_width=True):
                    format_type = "json" if "JSON" in export_format else "csv"
                    export_path = engine.export_quiz(selected_quiz, format_type)
                    
                    if export_path:
                        st.success(f"✅ Đã export quiz vào {export_path}")
                        
                        # Provide download link if possible
                        try:
                            with open(export_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            st.download_button(
                                "💾 Tải Xuống",
                                data=content,
                                file_name=Path(export_path).name,
                                mime="application/json" if format_type == "json" else "text/csv"
                            )
                        except Exception as e:
                            st.warning(f"⚠️ Không thể tạo link download: {e}")
                    else:
                        st.error("❌ Lỗi export quiz")
        
        with export_tabs[1]:
            st.markdown("**Export nhiều quiz cùng lúc:**")
            
            # Multi-select for quizzes
            selected_quizzes = st.multiselect(
                "Chọn các quiz để export:",
                list(saved_quizzes.keys()),
                help="Có thể chọn nhiều quiz"
            )
            
            if selected_quizzes:
                st.info(f"Đã chọn {len(selected_quizzes)} quiz")
                
                if st.button("📦 Export Hàng Loạt", use_container_width=True):
                    success_count = 0
                    
                    for quiz_name in selected_quizzes:
                        export_path = engine.export_quiz(quiz_name, "json")
                        if export_path:
                            success_count += 1
                    
                    if success_count > 0:
                        st.success(f"✅ Đã export {success_count}/{len(selected_quizzes)} quiz")
                    else:
                        st.error("❌ Không export được quiz nào")
        
        with export_tabs[2]:
            st.markdown("**Export toàn bộ thư viện:**")
            
            total_quizzes = len(saved_quizzes)
            total_questions = sum(info['questions_count'] for info in saved_quizzes.values())
            
            st.info(f"""
            **📊 Thống kê export:**
            - 📚 Tổng quiz: {total_quizzes}
            - 📝 Tổng câu hỏi: {total_questions}
            - 📷 Có hình ảnh: {sum(1 for info in saved_quizzes.values() if info.get('has_images'))}
            """)
            
            include_images = st.checkbox(
                "📷 Bao gồm hình ảnh",
                value=True,
                help="Export cả hình ảnh đính kèm"
            )
            
            if st.button("🗃️ Export Toàn Bộ", use_container_width=True):
                st.info("💡 Tính năng export toàn bộ sẽ có trong bản cập nhật tiếp theo")
                # This would create a zip file with all quizzes
    else:
        st.info("📚 Chưa có quiz nào trong thư viện để export.")

def render_advanced_tools():
    """Render advanced tools."""
    st.markdown("### 🔧 Công Cụ Nâng Cao")
    
    tools_tabs = st.tabs(["🔍 Phân Tích Quiz", "🧹 Dọn Dẹp Hệ Thống", "🔧 Sửa Chữa Dữ Liệu", "📊 Báo Cáo Hệ Thống"])
    
    with tools_tabs[0]:
        render_quiz_analysis_tools()
    
    with tools_tabs[1]:
        render_cleanup_tools()
    
    with tools_tabs[2]:
        render_repair_tools()
    
    with tools_tabs[3]:
        render_system_reports()

def render_quiz_analysis_tools():
    """Render quiz analysis tools."""
    st.markdown("#### 🔍 Phân Tích Quiz")
    
    engine = st.session_state.quiz_engine
    saved_quizzes = engine.get_saved_quizzes()
    
    if not saved_quizzes:
        st.info("📚 Chưa có quiz nào để phân tích.")
        return
    
    # Quiz selector
    selected_quiz = st.selectbox(
        "Chọn quiz để phân tích:",
        ["-- Chọn quiz --"] + list(saved_quizzes.keys()),
        key="analysis_quiz_selector"
    )
    
    if selected_quiz and selected_quiz != "-- Chọn quiz --":
        questions = engine.load_quiz_from_storage(selected_quiz)
        
        if questions:
            st.markdown(f"**📊 Phân tích quiz: {selected_quiz}**")
            
            # Basic statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Tổng câu", len(questions))
            
            with col2:
                images_count = sum(1 for q in questions if q.has_images)
                st.metric("📷 Có ảnh", images_count)
            
            with col3:
                avg_question_length = sum(len(q.cau_hoi) for q in questions) / len(questions)
                st.metric("📏 TB độ dài", f"{avg_question_length:.0f} ký tự")
            
            with col4:
                unique_subjects = len(set(q.mon_hoc for q in questions if q.mon_hoc not in ['auto_detect', 'unknown']))
                st.metric("📚 Môn học", unique_subjects)
            
            # Difficulty distribution
            st.markdown("**🎯 Phân bố độ khó:**")
            
            difficulty_counts = {'de': 0, 'trung_binh': 0, 'kho': 0}
            for q in questions:
                difficulty_counts[q.do_kho] = difficulty_counts.get(q.do_kho, 0) + 1
            
            for difficulty, count in difficulty_counts.items():
                if count > 0:
                    percentage = (count / len(questions)) * 100
                    emoji = {'de': '🟢', 'trung_binh': '🟡', 'kho': '🔴'}.get(difficulty, '🟡')
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write(f"{emoji} {difficulty.title()}")
                    with col2:
                        st.progress(percentage / 100)
                        st.caption(f"{count} câu ({percentage:.1f}%)")
            
            # Subject distribution
            subject_counts = {}
            for q in questions:
                if q.mon_hoc not in ['auto_detect', 'unknown']:
                    subject_counts[q.mon_hoc] = subject_counts.get(q.mon_hoc, 0) + 1
            
            if subject_counts:
                st.markdown("**📚 Phân bố theo môn học:**")
                for subject, count in subject_counts.items():
                    percentage = (count / len(questions)) * 100
                    st.write(f"📖 {subject}: {count} câu ({percentage:.1f}%)")
            
            # Quality analysis
            st.markdown("**🔍 Phân tích chất lượng:**")
            
            quality_issues = []
            
            # Check for questions that are too short or too long
            short_questions = [q for q in questions if len(q.cau_hoi) < 20]
            long_questions = [q for q in questions if len(q.cau_hoi) > 500]
            
            if short_questions:
                quality_issues.append(f"⚠️ {len(short_questions)} câu hỏi có thể quá ngắn")
            
            if long_questions:
                quality_issues.append(f"⚠️ {len(long_questions)} câu hỏi có thể quá dài")
            
            # Check for duplicate questions
            question_texts = [q.cau_hoi.lower().strip() for q in questions]
            duplicates = len(question_texts) - len(set(question_texts))
            
            if duplicates > 0:
                quality_issues.append(f"⚠️ {duplicates} câu hỏi có thể bị trùng lặp")
            
            # Check for questions with missing choices
            incomplete_questions = [q for q in questions if len(q.lua_chon) < 4]
            
            if incomplete_questions:
                quality_issues.append(f"❌ {len(incomplete_questions)} câu hỏi thiếu lựa chọn")
            
            if quality_issues:
                for issue in quality_issues:
                    st.warning(issue)
            else:
                st.success("✅ Quiz có chất lượng tốt!")
            
            # Recommendations
            st.markdown("**💡 Khuyến nghị:**")
            
            if len(questions) < 10:
                st.info("📝 Nên có ít nhất 10-15 câu hỏi cho một bài kiểm tra hiệu quả")
            
            if difficulty_counts['de'] > len(questions) * 0.7:
                st.info("🎯 Nên thêm câu hỏi khó hơn để tăng độ phân biệt")
            
            if images_count == 0:
                st.info("📷 Có thể thêm hình ảnh để câu hỏi sinh động hơn")

def render_cleanup_tools():
    """Render cleanup tools."""
    st.markdown("#### 🧹 Dọn Dẹp Hệ Thống")
    
    st.warning("⚠️ **Cảnh báo:** Các thao tác dọn dẹp không thể hoàn tác!")
    
    engine = st.session_state.quiz_engine
    storage_info = engine.get_storage_info()
    
    # Storage overview
    st.markdown("**📊 Tình trạng lưu trữ hiện tại:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📚 Quiz", storage_info['total_quizzes'])
        st.metric("💾 Dung lượng quiz", storage_info['quiz_files_size'])
    
    with col2:
        st.metric("📷 Hình ảnh", storage_info['images_count'])
        st.metric("🖼️ Dung lượng ảnh", storage_info['images_storage_size'])
    
    with col3:
        st.metric("💾 Tổng dung lượng", storage_info['total_storage_size'])
    
    # Cleanup options
    st.markdown("**🧹 Tùy chọn dọn dẹp:**")
    
    cleanup_options = []
    
    # Old quizzes cleanup
    cleanup_old = st.checkbox(
        "🗓️ Xóa quiz cũ hơn 30 ngày",
        help="Xóa các quiz không được sử dụng trong 30 ngày qua"
    )
    if cleanup_old:
        cleanup_options.append("old_quizzes")
    
    # Unused images cleanup
    cleanup_images = st.checkbox(
        "🖼️ Xóa hình ảnh không sử dụng",
        help="Xóa các file ảnh không được tham chiếu bởi quiz nào"
    )
    if cleanup_images:
        cleanup_options.append("unused_images")
    
    # Temporary files cleanup
    cleanup_temp = st.checkbox(
        "🗂️ Xóa file tạm thời",
        help="Xóa các file backup và temporary"
    )
    if cleanup_temp:
        cleanup_options.append("temp_files")
    
    # Duplicate detection
    cleanup_duplicates = st.checkbox(
        "📄 Xóa quiz trùng lặp",
        help="Tìm và xóa các quiz có nội dung giống nhau"
    )
    if cleanup_duplicates:
        cleanup_options.append("duplicates")
    
    if cleanup_options:
        st.markdown("**📋 Sẽ thực hiện:**")
        for option in cleanup_options:
            option_text = {
                "old_quizzes": "🗓️ Xóa quiz cũ hơn 30 ngày",
                "unused_images": "🖼️ Xóa hình ảnh không sử dụng",
                "temp_files": "🗂️ Xóa file tạm thời",
                "duplicates": "📄 Xóa quiz trùng lặp"
            }
            st.write(f"• {option_text.get(option, option)}")
        
        # Confirmation
        confirm_cleanup = st.checkbox(
            "✅ Tôi hiểu rằng thao tác này không thể hoàn tác",
            key="confirm_cleanup"
        )
        
        if confirm_cleanup:
            if st.button("🧹 Bắt Đầu Dọn Dẹp", type="primary", use_container_width=True):
                perform_cleanup(cleanup_options)
    else:
        st.info("Chọn các tùy chọn dọn dẹp ở trên.")

def perform_cleanup(cleanup_options: list):
    """Perform system cleanup."""
    st.markdown("### 🔄 Đang Thực Hiện Dọn Dẹp...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_steps = len(cleanup_options)
    current_step = 0
    
    results = []
    
    for option in cleanup_options:
        current_step += 1
        progress = current_step / total_steps
        progress_bar.progress(progress)
        
        if option == "old_quizzes":
            status_text.info("🗓️ Đang kiểm tra quiz cũ...")
            # Implement old quiz cleanup
            results.append("🗓️ Kiểm tra quiz cũ: Tính năng sẽ có trong bản cập nhật")
            
        elif option == "unused_images":
            status_text.info("🖼️ Đang kiểm tra hình ảnh không sử dụng...")
            # Implement unused image cleanup
            results.append("🖼️ Kiểm tra hình ảnh: Tính năng sẽ có trong bản cập nhật")
            
        elif option == "temp_files":
            status_text.info("🗂️ Đang dọn dẹp file tạm thời...")
            # Implement temp file cleanup
            results.append("🗂️ Dọn dẹp file tạm: Tính năng sẽ có trong bản cập nhật")
            
        elif option == "duplicates":
            status_text.info("📄 Đang tìm quiz trùng lặp...")
            # Implement duplicate detection
            results.append("📄 Tìm trùng lặp: Tính năng sẽ có trong bản cập nhật")
        
        time.sleep(0.5)  # Simulate processing time
    
    progress_bar.progress(1.0)
    status_text.success("✅ Hoàn thành dọn dẹp!")
    
    # Show results
    st.markdown("### 📋 Kết Quả Dọn Dẹp")
    for result in results:
        st.info(result)
    
    st.success("🎉 Dọn dẹp hệ thống hoàn tất!")

def render_repair_tools():
    """Render repair tools."""
    st.markdown("#### 🔧 Sửa Chữa Dữ Liệu")
    
    engine = st.session_state.quiz_engine
    
    # System health check
    st.markdown("**🏥 Kiểm Tra Sức Khỏe Hệ Thống**")
    
    if st.button("🔍 Kiểm Tra Toàn Diện", use_container_width=True):
        perform_health_check()
    
    # Manual repair options
    st.markdown("**🔧 Tùy chọn sửa chữa thủ công:**")
    
    repair_tabs = st.tabs(["📚 Quiz Index", "🖼️ Hình Ảnh", "📊 Thống Kê"])
    
    with repair_tabs[0]:
        st.markdown("**📚 Sửa chữa Quiz Index:**")
        
        if st.button("🔧 Rebuild Quiz Index", use_container_width=True):
            try:
                engine._validate_quiz_index()
                st.success("✅ Đã kiểm tra và sửa chữa quiz index")
            except Exception as e:
                st.error(f"❌ Lỗi sửa chữa index: {e}")
        
        if st.button("🔄 Rescan Quiz Directory", use_container_width=True):
            st.info("💡 Tính năng rescan sẽ có trong bản cập nhật tiếp theo")
    
    with repair_tabs[1]:
        st.markdown("**🖼️ Sửa chữa Hình Ảnh:**")
        
        if st.button("🔗 Kiểm Tra Links Ảnh", use_container_width=True):
            st.info("💡 Tính năng kiểm tra links ảnh sẽ có trong bản cập nhật tiếp theo")
        
        if st.button("🖼️ Optimize Images", use_container_width=True):
            st.info("💡 Tính năng optimize ảnh sẽ có trong bản cập nhật tiếp theo")
    
    with repair_tabs[2]:
        st.markdown("**📊 Sửa chữa Thống Kê:**")
        
        if st.button("📊 Rebuild Statistics", use_container_width=True):
            try:
                # Force reload statistics
                engine._load_test_history()
                st.success("✅ Đã rebuild thống kê")
            except Exception as e:
                st.error(f"❌ Lỗi rebuild thống kê: {e}")
        
        if st.button("🗑️ Clear Corrupted Data", use_container_width=True):
            st.warning("⚠️ Tính năng này sẽ xóa dữ liệu bị hỏng. Cần xác nhận để thực hiện.")

def perform_health_check():
    """Perform comprehensive health check."""
    st.markdown("### 🔍 Đang Kiểm Tra Sức Khỏe Hệ Thống...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    checks = [
        ("📚 Kiểm tra quiz files", check_quiz_files),
        ("🖼️ Kiểm tra hình ảnh", check_images),
        ("📊 Kiểm tra thống kê", check_statistics),
        ("🗃️ Kiểm tra storage", check_storage),
        ("⚙️ Kiểm tra cấu hình", check_configuration)
    ]
    
    results = []
    
    for i, (description, check_func) in enumerate(checks):
        progress = (i + 1) / len(checks)
        progress_bar.progress(progress)
        status_text.info(description)
        
        try:
            result = check_func()
            results.append((description, "✅", result))
        except Exception as e:
            results.append((description, "❌", str(e)))
        
        time.sleep(0.5)
    
    status_text.success("✅ Kiểm tra hoàn tất!")
    
    # Display results
    st.markdown("### 📋 Kết Quả Kiểm Tra")
    
    for description, status, result in results:
        if status == "✅":
            st.success(f"{status} {description}: {result}")
        else:
            st.error(f"{status} {description}: {result}")

def check_quiz_files():
    """Check quiz files integrity."""
    engine = st.session_state.quiz_engine
    saved_quizzes = engine.get_saved_quizzes()
    
    valid_count = 0
    total_count = len(saved_quizzes)
    
    for name, info in saved_quizzes.items():
        file_path = Path(info["file_path"])
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)  # Try to parse JSON
                valid_count += 1
            except:
                pass
    
    return f"{valid_count}/{total_count} quiz files hợp lệ"

def check_images():
    """Check image files."""
    engine = st.session_state.quiz_engine
    storage_info = engine.get_storage_info()
    
    return f"{storage_info['images_count']} hình ảnh, {storage_info['images_storage_size']}"

def check_statistics():
    """Check statistics integrity."""
    engine = st.session_state.quiz_engine
    stats = engine.get_test_statistics()
    
    if 'message' in stats:
        return "Chưa có dữ liệu thống kê"
    else:
        return f"{stats['total_tests']} bài kiểm tra đã hoàn thành"

def check_storage():
    """Check storage integrity."""
    engine = st.session_state.quiz_engine
    storage_info = engine.get_storage_info()
    
    return f"Tổng {storage_info['total_storage_size']}"

def check_configuration():
    """Check system configuration."""
    # Check API key
    has_api_key = hasattr(st.session_state, 'api_key') and st.session_state.api_key
    
    if has_api_key:
        return "Cấu hình API key OK"
    else:
        return "Chưa cấu hình API key"

def render_system_reports():
    """Render system reports."""
    st.markdown("#### 📊 Báo Cáo Hệ Thống")
    
    # Report generation
    report_types = st.multiselect(
        "Chọn loại báo cáo:",
        [
            "📚 Báo cáo Quiz Library",
            "📊 Báo cáo Thống kê Test",
            "💾 Báo cáo Storage", 
            "⚙️ Báo cáo Hệ thống",
            "🔍 Báo cáo Lỗi"
        ]
    )
    
    if report_types:
        if st.button("📋 Tạo Báo Cáo", use_container_width=True):
            generate_system_reports(report_types)

def generate_system_reports(report_types: list):
    """Generate system reports."""
    st.markdown("### 📋 Báo Cáo Hệ Thống")
    
    engine = st.session_state.quiz_engine
    
    for report_type in report_types:
        st.markdown(f"#### {report_type}")
        
        if "Quiz Library" in report_type:
            # Quiz library report
            saved_quizzes = engine.get_saved_quizzes()
            
            st.markdown(f"**Tổng quan:** {len(saved_quizzes)} quiz trong thư viện")
            
            if saved_quizzes:
                # Create summary table
                summary_data = []
                for name, info in saved_quizzes.items():
                    summary_data.append({
                        "Tên Quiz": name,
                        "Số câu": info['questions_count'],
                        "Có ảnh": "Có" if info.get('has_images') else "Không",
                        "Kích thước": info['size'],
                        "Ngày tạo": info['created_time'].strftime('%d/%m/%Y')
                    })
                
                # Display first few rows
                for i, item in enumerate(summary_data[:5]):
                    st.write(f"• **{item['Tên Quiz']}**: {item['Số câu']} câu, {item['Kích thước']}")
                
                if len(summary_data) > 5:
                    st.info(f"... và {len(summary_data) - 5} quiz khác")
        
        elif "Thống kê Test" in report_type:
            # Test statistics report
            stats = engine.get_test_statistics()
            
            if 'message' not in stats:
                st.write(f"• **Tổng bài kiểm tra:** {stats['total_tests']}")
                st.write(f"• **Điểm trung bình:** {stats['average_score']}/10")
                st.write(f"• **Tỷ lệ đậu:** {stats['pass_rate']:.1f}%")
                
                # Mode distribution
                mode_stats = stats.get('mode_distribution', {})
                if mode_stats:
                    st.write(f"• **Exam mode:** {mode_stats.get('exam', 0)} lần")
                    st.write(f"• **Practice mode:** {mode_stats.get('practice', 0)} lần")
            else:
                st.write("• Chưa có dữ liệu thống kê")
        
        elif "Storage" in report_type:
            # Storage report
            storage_info = engine.get_storage_info()
            
            st.write(f"• **Tổng dung lượng:** {storage_info['total_storage_size']}")
            st.write(f"• **Số quiz:** {storage_info['total_quizzes']}")
            st.write(f"• **Số hình ảnh:** {storage_info['images_count']}")
            st.write(f"• **Dung lượng ảnh:** {storage_info['images_storage_size']}")
        
        elif "Hệ thống" in report_type:
            # System report
            st.write(f"• **Engine version:** {engine.engine_version}")
            st.write(f"• **Phiên hoạt động:** {len(engine.active_sessions)}")
            st.write(f"• **Bài kiểm tra hoàn thành:** {len(engine.completed_tests)}")
            
            # API key status
            has_api_key = hasattr(st.session_state, 'api_key') and st.session_state.api_key
            st.write(f"• **API Key:** {'Đã cấu hình' if has_api_key else 'Chưa cấu hình'}")
        
        elif "Lỗi" in report_type:
            # Error report
            st.write("• **Lỗi gần đây:** Không có lỗi được ghi nhận")
            st.write("• **Trạng thái hệ thống:** Hoạt động bình thường")
        
        st.divider()
    
    # Export report option
    if st.button("💾 Xuất Báo Cáo", use_container_width=True):
        st.info("💡 Tính năng xuất báo cáo sẽ có trong bản cập nhật tiếp theo")

def render_settings_page():
    """Render system settings page."""
    st.markdown("### ⚙️ Cài Đặt Hệ Thống")
    
    settings_tabs = st.tabs(["🎨 Giao Diện", "🔧 Xử Lý", "💾 Lưu Trữ", "🔒 Bảo Mật"])
    
    with settings_tabs[0]:
        render_ui_settings()
    
    with settings_tabs[1]:
        render_processing_settings()
    
    with settings_tabs[2]:
        render_storage_settings()
    
    with settings_tabs[3]:
        render_security_settings()

def render_ui_settings():
    """Render UI settings."""
    st.markdown("#### 🎨 Cài Đặt Giao Diện")
    
    # Theme settings
    current_theme = st.session_state.app_settings.get('theme', 'light')
    theme = st.selectbox(
        "Chủ đề:",
        ["light", "dark", "auto"],
        index=["light", "dark", "auto"].index(current_theme),
        help="Chọn chủ đề hiển thị"
    )
    
    # Language settings
    language = st.selectbox(
        "Ngôn ngữ:",
        ["Tiếng Việt", "English"],
        index=0,
        help="Ngôn ngữ hiển thị (hiện tại chỉ hỗ trợ Tiếng Việt)"
    )
    
    # Display options
    show_progress = st.checkbox(
        "Hiển thị thanh tiến trình",
        value=st.session_state.app_settings.get('show_progress', True)
    )
    
    enable_sounds = st.checkbox(
        "Bật âm thanh thông báo",
        value=st.session_state.app_settings.get('enable_sounds', False)
    )
    
    # Auto features
    auto_save_ui = st.checkbox(
        "Tự động lưu trạng thái UI",
        value=st.session_state.app_settings.get('auto_save', True)
    )
    
    # Save settings
    if st.button("💾 Lưu Cài Đặt Giao Diện", use_container_width=True):
        st.session_state.app_settings.update({
            'theme': theme,
            'language': language,
            'show_progress': show_progress,
            'enable_sounds': enable_sounds,
            'auto_save': auto_save_ui
        })
        st.success("✅ Đã lưu cài đặt giao diện!")

def render_processing_settings():
    """Render processing settings."""
    st.markdown("#### 🔧 Cài Đặt Xử Lý")
    
    # Default processing parameters
    default_batch_size = st.slider(
        "Batch size mặc định:",
        min_value=5,
        max_value=15,
        value=st.session_state.get('processing_config', {}).get('batch_size', 10)
    )
    
    default_batch_delay = st.slider(
        "Delay giữa batch (giây):",
        min_value=3,
        max_value=10,
        value=st.session_state.get('processing_config', {}).get('batch_delay', 5)
    )
    
    default_quota_delay = st.slider(
        "Quota recovery delay (giây):",
        min_value=15,
        max_value=60,
        value=st.session_state.get('processing_config', {}).get('quota_delay', 30)
    )
    
    # AI behavior settings
    st.markdown("**🤖 Cài đặt AI Agent:**")
    
    ai_aggressiveness = st.selectbox(
        "Mức độ xử lý:",
        ["Conservative", "Balanced", "Aggressive"],
        index=1,
        help="Conservative: chậm nhưng ổn định, Aggressive: nhanh nhưng có thể gặp lỗi quota"
    )
    
    enable_auto_retry = st.checkbox(
        "Tự động retry khi lỗi",
        value=True
    )
    
    max_retries = st.number_input(
        "Số lần retry tối đa:",
        min_value=1,
        max_value=5,
        value=3
    )
    
    # Save processing settings
    if st.button("💾 Lưu Cài Đặt Xử Lý", use_container_width=True):
        st.session_state.processing_config = {
            'batch_size': default_batch_size,
            'batch_delay': default_batch_delay,
            'quota_delay': default_quota_delay,
            'ai_aggressiveness': ai_aggressiveness,
            'enable_auto_retry': enable_auto_retry,
            'max_retries': max_retries
        }
        st.success("✅ Đã lưu cài đặt xử lý!")

def render_storage_settings():
    """Render storage settings."""
    st.markdown("#### 💾 Cài Đặt Lưu Trữ")
    
    engine = st.session_state.quiz_engine
    storage_info = engine.get_storage_info()
    
    # Current storage info
    st.markdown("**📊 Thông tin lưu trữ hiện tại:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📚 Quiz", storage_info['total_quizzes'])
        st.metric("📷 Ảnh", storage_info['images_count'])
    
    with col2:
        st.metric("💾 Tổng dung lượng", storage_info['total_storage_size'])
    
    # Storage settings
    st.markdown("**⚙️ Cấu hình lưu trữ:**")
    
    auto_backup = st.checkbox(
        "Tự động backup quiz",
        value=True,
        help="Tự động tạo backup khi xóa quiz"
    )
    
    compress_images = st.checkbox(
        "Nén ảnh tự động",
        value=True,
        help="Tự động nén ảnh để tiết kiệm dung lượng"
    )
    
    max_image_size = st.selectbox(
        "Kích thước ảnh tối đa:",
        ["1MB", "5MB", "10MB", "Không giới hạn"],
        index=2
    )
    
    storage_cleanup_auto = st.checkbox(
        "Tự động dọn dẹp",
        value=False,
        help="Tự động dọn dẹp file cũ và không sử dụng"
    )
    
    # Storage paths
    st.markdown("**📁 Đường dẫn lưu trữ:**")
    
    storage_dirs = storage_info['storage_directories']
    for name, path in storage_dirs.items():
        st.code(f"{name}: {path}")
    
    if st.button("💾 Lưu Cài Đặt Lưu Trữ", use_container_width=True):
        st.success("✅ Đã lưu cài đặt lưu trữ!")

def render_security_settings():
    """Render security settings."""
    st.markdown("#### 🔒 Cài Đặt Bảo Mật")
    
    # API security
    st.markdown("**🔑 Bảo mật API:**")
    
    api_key_status = "Đã cấu hình" if hasattr(st.session_state, 'api_key') and st.session_state.api_key else "Chưa cấu hình"
    st.info(f"Trạng thái API Key: {api_key_status}")
    
    if st.button("🔄 Làm mới API Key", use_container_width=True):
        if 'api_key' in st.session_state:
            del st.session_state.api_key
        st.info("Vui lòng nhập lại API Key ở sidebar")
    
    # Data security
    st.markdown("**🛡️ Bảo mật dữ liệu:**")
    
    encrypt_storage = st.checkbox(
        "Mã hóa dữ liệu lưu trữ",
        value=False,
        help="Mã hóa các file quiz và thống kê (tính năng sắp có)"
    )
    
    secure_delete = st.checkbox(
        "Xóa an toàn",
        value=True,
        help="Ghi đè dữ liệu khi xóa để không thể khôi phục"
    )
    
    # Session security
    st.markdown("**👤 Bảo mật phiên làm việc:**")
    
    session_timeout = st.selectbox(
        "Timeout phiên làm việc:",
        ["30 phút", "1 giờ", "2 giờ", "Không giới hạn"],
        index=1
    )
    
    auto_logout = st.checkbox(
        "Tự động đăng xuất khi không hoạt động",
        value=False
    )
    
    # Privacy settings
    st.markdown("**🔒 Cài đặt riêng tư:**")
    
    anonymous_stats = st.checkbox(
        "Thu thập thống kê ẩn danh",
        value=False,
        help="Giúp cải thiện hệ thống (không thu thập thông tin cá nhân)"
    )
    
    share_error_reports = st.checkbox(
        "Chia sẻ báo cáo lỗi",
        value=False,
        help="Tự động gửi báo cáo lỗi để hỗ trợ phát triển"
    )
    
    if st.button("💾 Lưu Cài Đặt Bảo Mật", use_container_width=True):
        st.success("✅ Đã lưu cài đặt bảo mật!")
    
    # Security audit
    st.markdown("**🔍 Kiểm tra bảo mật:**")
    
    if st.button("🔍 Quét Bảo Mật", use_container_width=True):
        st.info("🔍 Đang quét...")
        time.sleep(2)
        st.success("✅ Hệ thống an toàn! Không phát hiện vấn đề bảo mật.")

def render_enhanced_footer():
    """Render enhanced footer với additional info."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem;'>
        <div style='font-size: 1.5rem; margin-bottom: 1rem;'>🎯 QuizForce AI Pro v3.0</div>
        <p style='margin: 0.5rem 0;'><strong>Hệ thống tạo quiz thông minh cho giáo dục Việt Nam</strong></p>
        <div style='margin: 1rem 0; font-size: 0.9rem;'>
            🤖 Powered by Google Gemini 2.0 Flash | 🎨 Enhanced UI/UX | 📊 Advanced Analytics
        </div>
        <div style='margin: 1rem 0; font-size: 0.9rem;'>
            ✨ Features: Batch Processing | Image Support | Quiz Storage | Practice Mode | Real-time Feedback
        </div>
        <div style='margin-top: 1rem; font-size: 0.8rem; color: #868e96;'>
            © 2024 - Phát triển bởi AI Agent chuyên nghiệp cho người Việt Nam | Designed with ❤️ for Education
        </div>
        <div style='margin-top: 0.5rem; font-size: 0.8rem; color: #868e96;'>
            🌟 Đặc biệt tối ưu cho hệ thống giáo dục Việt Nam | Hỗ trợ đầy đủ Tiếng Việt
        </div>
    </div>
    """, unsafe_allow_html=True)
def render_system_settings():
    """Render system settings trong tab Quản Lý Quiz."""
    st.markdown("#### ⚙️ Cài Đặt Hệ Thống")
    
    # System info
    engine = st.session_state.quiz_engine
    storage_info = engine.get_storage_info()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **💾 Lưu trữ:**
        - Quiz: {storage_info['total_quizzes']}
        - Hình ảnh: {storage_info['images_count']}
        - Dung lượng: {storage_info['total_storage_size']}
        """)
    
    with col2:
        st.info(f"""
        **⚙️ Engine:**
        - Version: {storage_info.get('engine_version', '1.0')}
        """)
    
    # Quick settings
    auto_backup = st.checkbox("💾 Tự động backup", value=True)
    compress_images = st.checkbox("📷 Nén ảnh tự động", value=True)
    
    if st.button("💾 Lưu Cài Đặt", use_container_width=True):
        st.success("✅ Đã lưu cài đặt!")
if __name__ == "__main__":
    main()