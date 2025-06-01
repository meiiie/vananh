"""
Giao Diện Làm Bài Kiểm Tra QuizForce AI
Interface chuyên nghiệp cho học sinh làm bài kiểm tra trực tuyến
"""

import streamlit as st
import json
import time
from datetime import datetime
import sys
from pathlib import Path

# Import engine
sys.path.append(str(Path(__file__).parent.parent))
from backend.quiz_test_engine import QuizTestEngine

def render_quiz_test_page():
    """Render trang làm bài kiểm tra."""
    # Chỉ set page config khi chạy standalone
    if __name__ == "__main__":
        st.set_page_config(
            page_title="QuizForce AI - Làm Bài Kiểm Tra",
            page_icon="📝",
            layout="wide"
        )
    
    # Initialize engine
    if 'quiz_engine' not in st.session_state:
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
                help="File JSON được tạo từ QuizMaster AI"
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
                    questions_data = st.session_state.quiz_results['compiled_questions']
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
            if st.button("✅ Có", use_container_width=True):
                result = engine.finish_test(session_id)
                st.session_state.test_result = result
                st.session_state.current_session_id = None
                st.session_state.confirm_finish = False
                st.rerun()
        with col2:
            if st.button("❌ Không", use_container_width=True):
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
    current_index = 0
    if current_answer:
        for i, choice in enumerate(choices.keys()):
            if choice == current_answer:
                current_index = i
                break
    
    selected_answer = st.radio(
        "Chọn đáp án:",
        answer_options,
        index=current_index if current_answer else None,
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
        if st.button("⬅️ Câu Trước", disabled=current_q['question_number'] == 1):
            engine.previous_question(session_id)
            st.rerun()
    
    with col2:
        if st.button("📋 Tổng Quan"):
            st.session_state.show_overview = True
            st.rerun()
    
    with col3:
        if st.button("🔄 Làm Mới"):
            st.rerun()
    
    with col4:
        if current_q['question_number'] < current_q['total_questions']:
            if st.button("➡️ Câu Tiếp"):
                engine.next_question(session_id)
                st.rerun()
        else:
            if st.button("🏁 Hoàn Thành", type="primary"):
                st.session_state.confirm_finish = True
                st.rerun()
    
    # Auto-refresh for timer
    if time_remaining > 0:
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
            st.rerun()

if __name__ == "__main__":
    render_quiz_test_page()
