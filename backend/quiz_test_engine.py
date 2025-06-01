"""
Engine Bài Kiểm Tra QuizForce AI
Xử lý toàn bộ logic làm bài kiểm tra trực tuyến chuyên nghiệp
"""

import json
import time
import random
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib
from pathlib import Path

@dataclass
class QuestionData:
    """Cấu trúc dữ liệu câu hỏi chuẩn."""
    so_cau: int
    cau_hoi: str
    lua_chon: Dict[str, str]
    dap_an: str
    do_kho: str = "trung_binh"
    mon_hoc: str = "auto_detect"
    ghi_chu: str = ""

@dataclass
class TestSession:
    """Phiên làm bài kiểm tra."""
    session_id: str
    student_name: str
    test_title: str
    start_time: datetime
    time_limit: int  # phút
    questions: List[QuestionData]
    current_question: int = 0
    answers: Dict[int, str] = None
    is_finished: bool = False
    end_time: Optional[datetime] = None
    test_mode: str = "exam"  # "exam" hoặc "practice"
    
    def __post_init__(self):
        if self.answers is None:
            self.answers = {}

@dataclass
class TestResult:
    """Kết quả bài kiểm tra."""
    session_id: str
    student_name: str
    test_title: str
    total_questions: int
    correct_answers: int
    wrong_answers: int
    score: float
    percentage: float
    time_taken: str
    detailed_results: List[Dict[str, Any]]
    finish_time: datetime
    test_mode: str = "exam"

class QuizTestEngine:
    """
    Engine Bài Kiểm Tra Chuyên Nghiệp
    - Quản lý phiên làm bài
    - Xử lý thời gian
    - Chấm điểm tự động
    - Thống kê chi tiết
    - Lưu trữ bài kiểm tra
    - Chế độ ôn luyện trực tiếp
    """
    
    def __init__(self):
        """Khởi tạo engine."""
        self.active_sessions: Dict[str, TestSession] = {}
        self.completed_tests: List[TestResult] = []
        
        # Tạo thư mục lưu trữ
        self.quiz_storage_dir = Path("quiz_storage")
        self.quiz_storage_dir.mkdir(exist_ok=True)
        
        # Load saved quizzes
        self._load_saved_quizzes()
        
    def _load_saved_quizzes(self):
        """Tải danh sách quiz đã lưu."""
        try:
            self.saved_quizzes = {}
            for file_path in self.quiz_storage_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        quiz_data = json.load(f)
                        quiz_info = {
                            "file_path": str(file_path),
                            "name": file_path.stem,
                            "questions_count": len(quiz_data) if isinstance(quiz_data, list) else 0,
                            "created_time": datetime.fromtimestamp(file_path.stat().st_mtime),
                            "size": f"{file_path.stat().st_size / 1024:.1f} KB"
                        }
                        self.saved_quizzes[quiz_info["name"]] = quiz_info
                except Exception as e:
                    print(f"Lỗi tải quiz {file_path}: {e}")
        except Exception as e:
            print(f"Lỗi tải danh sách quiz: {e}")
            self.saved_quizzes = {}
    
    def save_quiz_to_storage(self, questions_data: list, quiz_name: str = None) -> str:
        """Lưu quiz vào storage để sử dụng sau."""
        try:
            if not quiz_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                quiz_name = f"Quiz_{timestamp}"
            
            # Đảm bảo tên file hợp lệ
            safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            
            file_path = self.quiz_storage_dir / f"{safe_name}.json"
            
            # Lưu file JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(questions_data, f, ensure_ascii=False, indent=2)
            
            # Cập nhật danh sách
            self._load_saved_quizzes()
            
            return safe_name
        except Exception as e:
            print(f"Lỗi lưu quiz: {e}")
            return None
    
    def get_saved_quizzes(self) -> Dict[str, Any]:
        """Lấy danh sách quiz đã lưu."""
        self._load_saved_quizzes()
        return self.saved_quizzes
    
    def load_quiz_from_storage(self, quiz_name: str) -> List[QuestionData]:
        """Tải quiz từ storage."""
        try:
            if quiz_name in self.saved_quizzes:
                file_path = self.saved_quizzes[quiz_name]["file_path"]
                with open(file_path, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                return self.load_questions_from_json(quiz_data)
        except Exception as e:
            print(f"Lỗi tải quiz từ storage: {e}")
        return []
    
    def delete_quiz_from_storage(self, quiz_name: str) -> bool:
        """Xóa quiz khỏi storage."""
        try:
            if quiz_name in self.saved_quizzes:
                file_path = Path(self.saved_quizzes[quiz_name]["file_path"])
                file_path.unlink()
                self._load_saved_quizzes()
                return True
        except Exception as e:
            print(f"Lỗi xóa quiz: {e}")
        return False

    def load_questions_from_json(self, json_data: str) -> List[QuestionData]:
        """Tải câu hỏi từ JSON."""
        try:
            if isinstance(json_data, str):
                questions_raw = json.loads(json_data)
            else:
                questions_raw = json_data
                
            questions = []
            for q_data in questions_raw:
                question = QuestionData(
                    so_cau=q_data.get('so_cau', 0),
                    cau_hoi=q_data.get('cau_hoi', ''),
                    lua_chon=q_data.get('lua_chon', {}),
                    dap_an=q_data.get('dap_an', ''),
                    do_kho=q_data.get('do_kho', 'trung_binh'),
                    mon_hoc=q_data.get('mon_hoc', 'auto_detect'),
                    ghi_chu=q_data.get('ghi_chu', '')
                )
                questions.append(question)
                
            # Sắp xếp theo số câu
            questions.sort(key=lambda x: x.so_cau)
            return questions
            
        except Exception as e:
            print(f"❌ Lỗi tải câu hỏi từ JSON: {e}")
            return []
    
    def create_test_session(self, 
                          student_name: str,
                          test_title: str,
                          questions: List[QuestionData],
                          time_limit: int = 60,
                          shuffle_questions: bool = True,
                          shuffle_answers: bool = True,
                          test_mode: str = "exam") -> str:
        """Tạo phiên làm bài mới với chế độ kiểm tra hoặc ôn luyện."""
        
        # Tạo session ID duy nhất
        session_id = self._generate_session_id(student_name, test_title)
        
        # Xử lý câu hỏi
        processed_questions = questions.copy()
        
        if shuffle_questions:
            random.shuffle(processed_questions)
            # Cập nhật lại số câu theo thứ tự mới
            for i, q in enumerate(processed_questions):
                q.so_cau = i + 1
        
        if shuffle_answers:
            for q in processed_questions:
                q.lua_chon = self._shuffle_choices(q.lua_chon, q.dap_an)
        
        # Tạo session
        session = TestSession(
            session_id=session_id,
            student_name=student_name,
            test_title=test_title,
            start_time=datetime.now(),
            time_limit=time_limit,
            questions=processed_questions,
            current_question=0,
            answers={},
            is_finished=False,
            test_mode=test_mode
        )
        
        self.active_sessions[session_id] = session
        return session_id
    
    def get_current_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Lấy câu hỏi hiện tại."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return None
            
        if session.current_question >= len(session.questions):
            return None
            
        question = session.questions[session.current_question]
        
        # Kiểm tra thời gian (chỉ áp dụng cho chế độ exam)
        if session.test_mode == "exam":
            time_left = self._get_time_remaining(session)
            if time_left <= 0:
                self._finish_test(session_id)
                return None
        else:
            time_left = -1  # Không giới hạn thời gian cho practice mode
        
        # Thông tin phản hồi cho chế độ ôn luyện
        feedback = None
        if session.test_mode == "practice":
            current_answer = session.answers.get(question.so_cau, "")
            if current_answer:
                is_correct = current_answer.upper() == question.dap_an.upper()
                feedback = {
                    "is_correct": is_correct,
                    "correct_answer": question.dap_an,
                    "user_answer": current_answer,
                    "explanation": f"Đáp án đúng là {question.dap_an}"
                }
        
        return {
            "question_number": session.current_question + 1,
            "total_questions": len(session.questions),
            "question_data": asdict(question),
            "time_remaining": time_left,
            "current_answer": session.answers.get(question.so_cau, ""),
            "progress": (session.current_question + 1) / len(session.questions) * 100,
            "test_mode": session.test_mode,
            "feedback": feedback
        }
    
    def submit_answer(self, session_id: str, answer: str) -> Dict[str, Any]:
        """Nộp đáp án cho câu hiện tại và trả về feedback cho practice mode."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return {"success": False}
            
        if session.current_question >= len(session.questions):
            return {"success": False}
            
        current_q = session.questions[session.current_question]
        session.answers[current_q.so_cau] = answer.upper().strip()
        
        # Tạo feedback cho practice mode
        feedback = {"success": True}
        if session.test_mode == "practice":
            is_correct = answer.upper().strip() == current_q.dap_an.upper()
            feedback.update({
                "is_correct": is_correct,
                "correct_answer": current_q.dap_an,
                "user_answer": answer.upper().strip(),
                "explanation": f"Đáp án đúng là {current_q.dap_an}",
                "show_feedback": True
            })
        
        return feedback
    
    def next_question(self, session_id: str) -> bool:
        """Chuyển câu hỏi tiếp theo."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return False
            
        session.current_question += 1
        return True
    
    def previous_question(self, session_id: str) -> bool:
        """Quay lại câu hỏi trước."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return False
            
        if session.current_question > 0:
            session.current_question -= 1
            return True
        return False
    
    def goto_question(self, session_id: str, question_number: int) -> bool:
        """Chuyển đến câu hỏi cụ thể."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return False
            
        if 1 <= question_number <= len(session.questions):
            session.current_question = question_number - 1
            return True
        return False
    
    def get_test_overview(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Lấy tổng quan bài kiểm tra."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
            
        answered_count = len(session.answers)
        unanswered = []
        
        for i, q in enumerate(session.questions):
            if q.so_cau not in session.answers or not session.answers[q.so_cau]:
                unanswered.append(i + 1)
        
        return {
            "student_name": session.student_name,
            "test_title": session.test_title,
            "total_questions": len(session.questions),
            "answered_questions": answered_count,
            "unanswered_questions": unanswered,
            "time_remaining": self._get_time_remaining(session),
            "time_elapsed": self._get_time_elapsed(session),
            "progress": answered_count / len(session.questions) * 100
        }
    
    def finish_test(self, session_id: str) -> Optional[TestResult]:
        """Hoàn thành bài kiểm tra."""
        return self._finish_test(session_id)
    
    def _finish_test(self, session_id: str) -> Optional[TestResult]:
        """Hoàn thành và chấm điểm bài kiểm tra."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
            
        session.is_finished = True
        session.end_time = datetime.now()
        
        # Chấm điểm
        result = self._grade_test(session)
        self.completed_tests.append(result)
        
        return result
    
    def _grade_test(self, session: TestSession) -> TestResult:
        """Chấm điểm bài kiểm tra."""
        correct_count = 0
        detailed_results = []
        
        for question in session.questions:
            user_answer = session.answers.get(question.so_cau, "").upper()
            correct_answer = question.dap_an.upper()
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            detailed_results.append({
                "so_cau": question.so_cau,
                "cau_hoi": question.cau_hoi[:100] + "..." if len(question.cau_hoi) > 100 else question.cau_hoi,
                "lua_chon": question.lua_chon,
                "dap_an_dung": correct_answer,
                "dap_an_chon": user_answer or "Không trả lời",
                "ket_qua": "Đúng" if is_correct else "Sai",
                "do_kho": question.do_kho,
                "is_correct": is_correct  # Thêm flag để dễ xử lý UI
            })
        
        total_questions = len(session.questions)
        wrong_count = total_questions - correct_count
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Tính điểm theo thang 10
        score = (correct_count / total_questions) * 10 if total_questions > 0 else 0
        
        time_taken = self._format_duration(session.end_time - session.start_time)
        
        return TestResult(
            session_id=session.session_id,
            student_name=session.student_name,
            test_title=session.test_title,
            total_questions=total_questions,
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            score=round(score, 2),
            percentage=round(percentage, 2),
            time_taken=time_taken,
            detailed_results=detailed_results,
            finish_time=session.end_time,
            test_mode=session.test_mode
        )
    
    def get_test_statistics(self) -> Dict[str, Any]:
        """Thống kê tổng quan các bài kiểm tra."""
        if not self.completed_tests:
            return {"message": "Chưa có bài kiểm tra nào hoàn thành"}
        
        total_tests = len(self.completed_tests)
        scores = [result.score for result in self.completed_tests]
        percentages = [result.percentage for result in self.completed_tests]
        
        return {
            "total_tests": total_tests,
            "average_score": round(sum(scores) / total_tests, 2),
            "average_percentage": round(sum(percentages) / total_tests, 2),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "pass_rate": len([s for s in scores if s >= 5]) / total_tests * 100,
            "recent_tests": [
                {
                    "student": result.student_name,
                    "score": result.score,
                    "percentage": result.percentage,
                    "time": result.finish_time.strftime("%H:%M %d/%m/%Y")
                }
                for result in sorted(self.completed_tests, key=lambda x: x.finish_time, reverse=True)[:5]
            ]
        }
    
    def _generate_session_id(self, student_name: str, test_title: str) -> str:
        """Tạo session ID duy nhất."""
        timestamp = str(int(time.time()))
        data = f"{student_name}_{test_title}_{timestamp}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def _shuffle_choices(self, choices: Dict[str, str], correct_answer: str) -> Dict[str, str]:
        """Trộn lựa chọn nhưng giữ nguyên đáp án đúng."""
        if len(choices) != 4:
            return choices
            
        # Lấy các giá trị lựa chọn
        choice_values = list(choices.values())
        random.shuffle(choice_values)
        
        # Tạo mapping mới
        new_choices = {}
        choice_keys = ['A', 'B', 'C', 'D']
        
        for i, key in enumerate(choice_keys):
            new_choices[key] = choice_values[i]
        
        return new_choices
    
    def _get_time_remaining(self, session: TestSession) -> int:
        """Tính thời gian còn lại (giây)."""
        elapsed = datetime.now() - session.start_time
        total_seconds = session.time_limit * 60
        remaining = total_seconds - elapsed.total_seconds()
        return max(0, int(remaining))
    
    def _get_time_elapsed(self, session: TestSession) -> str:
        """Tính thời gian đã trôi qua."""
        elapsed = datetime.now() - session.start_time
        return self._format_duration(elapsed)
    
    def _format_duration(self, delta: timedelta) -> str:
        """Format thời gian thành chuỗi dễ đọc."""
        total_seconds = int(delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def update_question(self, quiz_name: str, question_index: int, updated_question: Dict[str, Any]) -> bool:
        """Cập nhật câu hỏi trong quiz đã lưu."""
        try:
            if quiz_name in self.saved_quizzes:
                file_path = self.saved_quizzes[quiz_name]["file_path"]
                
                # Load current data
                with open(file_path, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                
                # Update question
                if 0 <= question_index < len(quiz_data):
                    quiz_data[question_index] = updated_question
                    
                    # Save back
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
                    
                    return True
        except Exception as e:
            print(f"Lỗi cập nhật câu hỏi: {e}")
        return False
    
    def add_image_to_question(self, quiz_name: str, question_index: int, image_data: bytes, image_name: str) -> bool:
        """Thêm hình ảnh vào câu hỏi."""
        try:
            # Tạo thư mục ảnh
            images_dir = self.quiz_storage_dir / "images"
            images_dir.mkdir(exist_ok=True)
            
            # Lưu ảnh
            image_path = images_dir / f"{quiz_name}_{question_index}_{image_name}"
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            # Cập nhật metadata câu hỏi
            if quiz_name in self.saved_quizzes:
                file_path = self.saved_quizzes[quiz_name]["file_path"]
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                
                if 0 <= question_index < len(quiz_data):
                    if "images" not in quiz_data[question_index]:
                        quiz_data[question_index]["images"] = []
                    
                    quiz_data[question_index]["images"].append({
                        "name": image_name,
                        "path": str(image_path.relative_to(self.quiz_storage_dir))
                    })
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
                    
                    return True
        except Exception as e:
            print(f"Lỗi thêm ảnh: {e}")
        return False
    
    def get_question_images(self, quiz_name: str, question_index: int) -> List[Dict[str, str]]:
        """Lấy danh sách ảnh của câu hỏi."""
        try:
            if quiz_name in self.saved_quizzes:
                file_path = self.saved_quizzes[quiz_name]["file_path"]
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                
                if 0 <= question_index < len(quiz_data):
                    images = quiz_data[question_index].get("images", [])
                    # Convert relative paths to absolute
                    for img in images:
                        img["full_path"] = str(self.quiz_storage_dir / img["path"])
                    return images
        except Exception as e:
            print(f"Lỗi lấy ảnh: {e}")
        return []
