"""
Engine Bài Kiểm Tra QuizForce AI - Enhanced Version
Xử lý toàn bộ logic làm bài kiểm tra trực tuyến chuyên nghiệp với:
- Quiz Storage Management
- Practice Mode với feedback tức thời  
- Image Support
- Enhanced Statistics
- Question Editor
"""
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from pathlib import Path
import json
import random
import uuid
import shutil
import base64
import io
from PIL import Image

@dataclass
class ImageData:
    """Cấu trúc dữ liệu hình ảnh."""
    name: str
    data: bytes = None
    path: str = None
    type: str = "image/jpeg"
    size: int = 0
    description: str = ""

@dataclass
class QuestionData:
    """Cấu trúc dữ liệu câu hỏi chuẩn với hỗ trợ hình ảnh."""
    so_cau: int
    cau_hoi: str
    lua_chon: Dict[str, str]
    dap_an: str
    do_kho: str = "trung_binh"
    mon_hoc: str = "auto_detect"
    ghi_chu: str = ""
    images: List[ImageData] = field(default_factory=list)
    has_images: bool = False
    created_time: str = ""
    updated_time: str = ""

@dataclass
class TestSession:
    """Phiên làm bài kiểm tra với enhanced features."""
    session_id: str
    student_name: str
    test_title: str
    start_time: datetime
    time_limit: int  # phút
    questions: List[QuestionData]
    current_question: int = 0
    answers: Dict[int, str] = field(default_factory=dict)
    answer_times: Dict[int, datetime] = field(default_factory=dict)  # Track thời gian trả lời
    question_feedback: Dict[int, Dict] = field(default_factory=dict)  # Feedback cho practice mode
    is_finished: bool = False
    end_time: Optional[datetime] = None
    test_mode: str = "exam"  # "exam" hoặc "practice"
    settings: Dict[str, Any] = field(default_factory=dict)  # Custom settings

@dataclass 
class TestResult:
    """Kết quả bài kiểm tra enhanced."""
    session_id: str
    student_name: str
    test_title: str
    total_questions: int
    correct_answers: int
    wrong_answers: int
    unanswered: int
    score: float
    percentage: float
    time_taken: str
    detailed_results: List[Dict[str, Any]]
    finish_time: datetime
    test_mode: str = "exam"
    question_stats: Dict[str, Any] = field(default_factory=dict)  # Thống kê chi tiết
    time_stats: Dict[str, Any] = field(default_factory=dict)  # Thống kê thời gian

class QuizTestEngine:
    """Engine Bài Kiểm Tra Chuyên Nghiệp với Enhanced Features"""
    
    def __init__(self):
        """Khởi tạo engine với enhanced configuration."""
        self.active_sessions: Dict[str, TestSession] = {}
        self.completed_tests: List[TestResult] = []
        
        # Enhanced storage directories
        self.quiz_storage_dir = Path("quiz_storage")
        self.quiz_storage_dir.mkdir(exist_ok=True)
        
        self.images_dir = self.quiz_storage_dir / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        self.backups_dir = self.quiz_storage_dir / "backups"
        self.backups_dir.mkdir(exist_ok=True)
        
        self.exports_dir = self.quiz_storage_dir / "exports"
        self.exports_dir.mkdir(exist_ok=True)
        
        # Load saved data
        self.saved_quizzes = {}
        self._load_saved_quizzes()
        self._load_test_history()
        
        # Engine info
        self.engine_version = "3.0"
        self.supported_features = [
            "Quiz Storage Management",
            "Practice Mode với Feedback",
            "Image Support",
            "Advanced Statistics", 
            "Question Editor",
            "Export/Import",
            "Auto Backup"
        ]
        
        print(f"✨ QuizTestEngine v{self.engine_version} initialized")
        print(f"🎯 Features: {', '.join(self.supported_features[:3])}...")
        
    def _load_saved_quizzes(self):
        """Tải danh sách quiz đã lưu với enhanced error handling."""
        try:
            index_file = self.quiz_storage_dir / "index.json"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.saved_quizzes = data
            else:
                self.saved_quizzes = {}
                
            # Validate và clean up
            self._validate_quiz_index()
            
        except Exception as e:
            print(f"⚠️ Lỗi tải danh sách quiz: {e}")
            self.saved_quizzes = {}
            
    def _validate_quiz_index(self):
        """Validate quiz index và xóa entries không hợp lệ."""
        invalid_quizzes = []
        
        for name, info in self.saved_quizzes.items():
            file_path = Path(info.get("file_path", ""))
            if not file_path.exists():
                invalid_quizzes.append(name)
                print(f"⚠️ Quiz file không tồn tại: {name}")
        
        # Remove invalid entries
        for name in invalid_quizzes:
            del self.saved_quizzes[name]
            
        if invalid_quizzes:
            self._save_index()
            print(f"🔧 Đã xóa {len(invalid_quizzes)} quiz entries không hợp lệ")
    
    def _load_test_history(self):
        """Tải lịch sử bài kiểm tra."""
        try:
            history_file = self.quiz_storage_dir / "test_history.json"
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert back to TestResult objects
                    for item in data:
                        if isinstance(item.get('finish_time'), str):
                            item['finish_time'] = datetime.fromisoformat(item['finish_time'])
                        result = TestResult(**item)
                        self.completed_tests.append(result)
                        
            print(f"📊 Đã tải {len(self.completed_tests)} bài kiểm tra từ lịch sử")
        except Exception as e:
            print(f"⚠️ Lỗi tải lịch sử: {e}")
            self.completed_tests = []
    
    def _save_test_history(self):
        """Lưu lịch sử bài kiểm tra."""
        try:
            history_file = self.quiz_storage_dir / "test_history.json"
            data = []
            
            for result in self.completed_tests:
                result_dict = asdict(result)
                if isinstance(result_dict.get('finish_time'), datetime):
                    result_dict['finish_time'] = result_dict['finish_time'].isoformat()
                data.append(result_dict)
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️ Lỗi lưu lịch sử: {e}")
    
    def save_quiz_to_storage(self, questions_data: list, quiz_name: str = None) -> str:
        """Lưu quiz vào storage với enhanced features."""
        try:
            if not quiz_name:
                quiz_name = f"Quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Tạo file name an toàn
            safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            file_name = f"{safe_name}.json"
            file_path = self.quiz_storage_dir / file_name
            
            # Process images if any
            processed_questions = []
            total_images = 0
            
            for q in questions_data:
                processed_q = q.copy()
                
                # Handle images
                if 'images' in q and q['images']:
                    processed_images = []
                    for img in q['images']:
                        if isinstance(img, dict) and 'data' in img:
                            # Save image to disk
                            img_filename = f"{safe_name}_q{q.get('so_cau', 0)}_{len(processed_images)}.jpg"
                            img_path = self.images_dir / img_filename
                            
                            # Convert and save image
                            if isinstance(img['data'], (bytes, str)):
                                self._save_image_to_disk(img['data'], img_path)
                                
                            processed_images.append({
                                "name": img.get('name', img_filename),
                                "path": str(img_path.relative_to(self.quiz_storage_dir)),
                                "type": img.get('type', 'image/jpeg'),
                                "size": img_path.stat().st_size if img_path.exists() else 0,
                                "description": img.get('description', '')
                            })
                            total_images += 1
                        else:
                            # Keep reference-only images
                            processed_images.append(img)
                    
                    processed_q['images'] = processed_images
                    processed_q['has_images'] = len(processed_images) > 0
                
                processed_questions.append(processed_q)
            
            # Save quiz data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(processed_questions, f, ensure_ascii=False, indent=2)
            
            # Update index
            self.saved_quizzes[quiz_name] = {
                "file_path": str(file_path),
                "created_time": datetime.now(),
                "questions_count": len(processed_questions),
                "images_count": total_images,
                "size": f"{file_path.stat().st_size / 1024:.1f} KB",
                "version": self.engine_version,
                "has_images": total_images > 0
            }
            
            self._save_index()
            
            print(f"✅ Đã lưu quiz '{quiz_name}' với {len(processed_questions)} câu, {total_images} ảnh")
            return quiz_name
            
        except Exception as e:
            print(f"❌ Lỗi lưu quiz: {e}")
            return None
    
    def _save_image_to_disk(self, image_data: Union[bytes, str], file_path: Path):
        """Lưu ảnh ra disk với optimization."""
        try:
            if isinstance(image_data, str):
                # Base64 encoded
                if image_data.startswith('data:image'):
                    # Remove data URL prefix
                    image_data = image_data.split(',', 1)[1]
                image_bytes = base64.b64decode(image_data)
            else:
                image_bytes = image_data
            
            # Open and optimize image
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            max_size = (1200, 1200)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save with optimization
            img.save(file_path, 'JPEG', quality=85, optimize=True)
            
        except Exception as e:
            print(f"⚠️ Lỗi lưu ảnh {file_path}: {e}")
            # Fallback: save raw bytes
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
    
    def _save_index(self):
        """Lưu index file với enhanced data."""
        try:
            index_file = self.quiz_storage_dir / "index.json"
            index_data = {}
            
            for name, info in self.saved_quizzes.items():
                index_data[name] = {
                    "file_path": info["file_path"],
                    "created_time": info["created_time"].isoformat() if isinstance(info["created_time"], datetime) else info["created_time"],
                    "questions_count": info["questions_count"],
                    "images_count": info.get("images_count", 0),
                    "size": info["size"],
                    "version": info.get("version", "1.0"),
                    "has_images": info.get("has_images", False)
                }
            
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ Lỗi lưu index: {e}")
    
    def get_saved_quizzes(self) -> Dict[str, Any]:
        """Lấy danh sách quiz đã lưu với enhanced info."""
        self._load_saved_quizzes()
        
        # Convert string dates back to datetime
        for name, info in self.saved_quizzes.items():
            if isinstance(info["created_time"], str):
                try:
                    info["created_time"] = datetime.fromisoformat(info["created_time"])
                except:
                    info["created_time"] = datetime.now()
        
        return self.saved_quizzes
    
    def load_quiz_from_storage(self, quiz_name: str) -> List[QuestionData]:
        """Tải quiz từ storage với image support."""
        try:
            if quiz_name in self.saved_quizzes:
                file_path = Path(self.saved_quizzes[quiz_name]["file_path"])
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    questions_data = json.load(f)
                
                # Convert to QuestionData objects with image loading
                questions = []
                for q_data in questions_data:
                    # Load images if any
                    images = []
                    if q_data.get('images'):
                        for img_info in q_data['images']:
                            if 'path' in img_info:
                                # Load image from disk
                                img_path = self.quiz_storage_dir / img_info['path']
                                if img_path.exists():
                                    with open(img_path, 'rb') as img_file:
                                        img_data = img_file.read()
                                    
                                    image_obj = ImageData(
                                        name=img_info.get('name', img_path.name),
                                        data=img_data,
                                        path=str(img_path),
                                        type=img_info.get('type', 'image/jpeg'),
                                        size=img_info.get('size', len(img_data)),
                                        description=img_info.get('description', '')
                                    )
                                    images.append(image_obj)
                            else:
                                # Reference-only image
                                image_obj = ImageData(
                                    name=img_info.get('name', 'Image'),
                                    type=img_info.get('type', 'reference'),
                                    description=img_info.get('description', '')
                                )
                                images.append(image_obj)
                    
                    question = QuestionData(
                        so_cau=q_data.get('so_cau', 0),
                        cau_hoi=q_data.get('cau_hoi', ''),
                        lua_chon=q_data.get('lua_chon', {}),
                        dap_an=q_data.get('dap_an', 'A'),
                        do_kho=q_data.get('do_kho', 'trung_binh'),
                        mon_hoc=q_data.get('mon_hoc', 'auto_detect'),
                        ghi_chu=q_data.get('ghi_chu', ''),
                        images=images,
                        has_images=len(images) > 0,
                        created_time=q_data.get('created_time', ''),
                        updated_time=q_data.get('updated_time', '')
                    )
                    questions.append(question)
                
                print(f"✅ Đã tải {len(questions)} câu hỏi từ '{quiz_name}'")
                return questions
                
        except Exception as e:
            print(f"❌ Lỗi tải quiz: {e}")
        return []
    
    def delete_quiz_from_storage(self, quiz_name: str) -> bool:
        """Xóa quiz khỏi storage với cleanup."""
        try:
            if quiz_name in self.saved_quizzes:
                info = self.saved_quizzes[quiz_name]
                file_path = Path(info["file_path"])
                
                # Backup trước khi xóa
                if file_path.exists():
                    backup_name = f"{quiz_name}_deleted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    backup_path = self.backups_dir / backup_name
                    shutil.copy2(file_path, backup_path)
                    print(f"📦 Đã backup quiz vào {backup_path}")
                
                # Xóa images liên quan
                if info.get("has_images", False):
                    self._cleanup_quiz_images(quiz_name)
                
                # Xóa file chính
                if file_path.exists():
                    file_path.unlink()
                
                # Xóa khỏi index
                del self.saved_quizzes[quiz_name]
                self._save_index()
                
                print(f"✅ Đã xóa quiz '{quiz_name}'")
                return True
                
        except Exception as e:
            print(f"❌ Lỗi xóa quiz: {e}")
        return False
    
    def _cleanup_quiz_images(self, quiz_name: str):
        """Dọn dẹp images của quiz."""
        try:
            # Find and delete images related to this quiz
            safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            pattern = f"{safe_name}_q*"
            
            for img_file in self.images_dir.glob(f"{safe_name}_q*"):
                img_file.unlink()
                print(f"🗑️ Đã xóa ảnh {img_file.name}")
                
        except Exception as e:
            print(f"⚠️ Lỗi dọn dẹp ảnh: {e}")

    def load_questions_from_json(self, json_data) -> List[QuestionData]:
        """Tải câu hỏi từ JSON với enhanced parsing."""
        try:
            questions = []
            
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
            
            for item in data:
                # Handle images
                images = []
                if item.get('images'):
                    for img_data in item['images']:
                        if isinstance(img_data, dict):
                            image_obj = ImageData(
                                name=img_data.get('name', 'Image'),
                                data=img_data.get('data'),
                                path=img_data.get('path'),
                                type=img_data.get('type', 'image/jpeg'),
                                size=img_data.get('size', 0),
                                description=img_data.get('description', '')
                            )
                            images.append(image_obj)
                
                question = QuestionData(
                    so_cau=item.get('so_cau', 0),
                    cau_hoi=item.get('cau_hoi', ''),
                    lua_chon=item.get('lua_chon', {}),
                    dap_an=item.get('dap_an', 'A'),
                    do_kho=item.get('do_kho', 'trung_binh'),
                    mon_hoc=item.get('mon_hoc', 'auto_detect'),
                    ghi_chu=item.get('ghi_chu', ''),
                    images=images,
                    has_images=len(images) > 0,
                    created_time=item.get('created_time', ''),
                    updated_time=item.get('updated_time', '')
                )
                questions.append(question)
            
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
                          test_mode: str = "exam",
                          custom_settings: Dict = None) -> str:
        """Tạo phiên làm bài mới với enhanced features."""
        
        session_id = self._generate_session_id(student_name, test_title)
        
        # Process questions
        processed_questions = questions.copy()
        
        if shuffle_questions:
            random.shuffle(processed_questions)
            print(f"🔀 Đã trộn thứ tự {len(processed_questions)} câu hỏi")
        
        if shuffle_answers:
            for q in processed_questions:
                if len(q.lua_chon) == 4:  # Only shuffle if we have exactly 4 choices
                    q.lua_chon = self._shuffle_choices(q.lua_chon, q.dap_an)
            print(f"🎲 Đã trộn thứ tự đáp án")
        
        # Prepare settings
        settings = {
            "shuffle_questions": shuffle_questions,
            "shuffle_answers": shuffle_answers,
            "show_images": custom_settings.get('show_images', True) if custom_settings else True,
            "auto_save": custom_settings.get('auto_save', True) if custom_settings else True,
            **(custom_settings or {})
        }
        
        # Create session
        session = TestSession(
            session_id=session_id,
            student_name=student_name,
            test_title=test_title,
            start_time=datetime.now(),
            time_limit=time_limit,
            questions=processed_questions,
            current_question=0,
            answers={},
            answer_times={},
            question_feedback={},
            is_finished=False,
            test_mode=test_mode,
            settings=settings
        )
        
        self.active_sessions[session_id] = session
        
        mode_text = "Kiểm tra" if test_mode == "exam" else "Ôn luyện"
        print(f"✅ Đã tạo phiên {mode_text}: {session_id}")
        print(f"📊 {len(processed_questions)} câu, {time_limit} phút")
        
        return session_id
    
    def get_current_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Lấy câu hỏi hiện tại với enhanced data."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return None
            
        if session.current_question >= len(session.questions):
            return None
            
        question = session.questions[session.current_question]
        
        # Time management
        if session.test_mode == "exam":
            time_left = self._get_time_remaining(session)
            if time_left <= 0:
                # Auto-finish when time's up
                self._finish_test(session_id)
                return None
        else:
            time_left = 9999  # Unlimited for practice
        
        # Prepare image data for display
        image_data = []
        if session.settings.get('show_images', True) and question.has_images:
            for img in question.images:
                img_info = {
                    "name": img.name,
                    "type": img.type,
                    "size": img.size,
                    "description": img.description
                }
                
                if img.data:
                    # Encode for web display
                    img_info["data_url"] = self._encode_image_for_web(img.data, img.type)
                elif img.path:
                    img_info["path"] = img.path
                
                image_data.append(img_info)
        
        # Feedback for practice mode
        feedback = None
        if session.test_mode == "practice":
            feedback = session.question_feedback.get(question.so_cau)
        
        return {
            "question_number": session.current_question + 1,
            "total_questions": len(session.questions),
            "question_data": {
                "so_cau": question.so_cau,
                "cau_hoi": question.cau_hoi,
                "lua_chon": question.lua_chon,
                "do_kho": question.do_kho,
                "mon_hoc": question.mon_hoc,
                "images": image_data,
                "has_images": question.has_images
            },
            "time_remaining": time_left,
            "current_answer": session.answers.get(question.so_cau, ""),
            "progress": (session.current_question + 1) / len(session.questions) * 100,
            "test_mode": session.test_mode,
            "feedback": feedback,
            "session_settings": session.settings
        }
    
    def _encode_image_for_web(self, image_data: bytes, image_type: str) -> str:
        """Encode image for web display."""
        try:
            encoded = base64.b64encode(image_data).decode('utf-8')
            mime_type = image_type if image_type.startswith('image/') else 'image/jpeg'
            return f"data:{mime_type};base64,{encoded}"
        except Exception as e:
            print(f"⚠️ Lỗi encode ảnh: {e}")
            return ""
    
    def submit_answer(self, session_id: str, answer: str) -> Dict[str, Any]:
        """Nộp đáp án với enhanced feedback và tracking."""
        session = self.active_sessions.get(session_id)
        if not session or session.is_finished:
            return {"success": False, "error": "Session not found or finished"}
            
        if session.current_question >= len(session.questions):
            return {"success": False, "error": "No current question"}
            
        current_q = session.questions[session.current_question]
        clean_answer = answer.upper().strip()
        
        # Record answer và time
        session.answers[current_q.so_cau] = clean_answer
        session.answer_times[current_q.so_cau] = datetime.now()
        
        feedback = {"success": True}
        
        # Enhanced feedback cho practice mode
        if session.test_mode == "practice":
            is_correct = clean_answer == current_q.dap_an.upper()
            
            detailed_feedback = {
                "is_correct": is_correct,
                "user_answer": clean_answer,
                "correct_answer": current_q.dap_an.upper(),
                "explanation": self._generate_explanation(current_q, is_correct),
                "show_feedback": True,
                "difficulty": current_q.do_kho,
                "subject": current_q.mon_hoc,
                "answer_time": datetime.now()
            }
            
            # Store feedback in session
            session.question_feedback[current_q.so_cau] = detailed_feedback
            feedback.update(detailed_feedback)
            
            print(f"📝 Practice feedback cho câu {current_q.so_cau}: {'✅' if is_correct else '❌'}")
        
        # Auto-save progress
        if session.settings.get('auto_save', True):
            self._auto_save_progress(session)
        
        return feedback
    
    def _generate_explanation(self, question: QuestionData, is_correct: bool) -> str:
        """Generate explanation for practice mode."""
        if is_correct:
            explanations = [
                f"Chính xác! Đáp án {question.dap_an} là đúng.",
                f"Tuyệt vời! Bạn đã chọn đúng đáp án {question.dap_an}.",
                f"Đúng rồi! {question.dap_an} là câu trả lời chính xác."
            ]
        else:
            explanations = [
                f"Đáp án đúng là {question.dap_an}. Hãy xem lại kiến thức này.",
                f"Chưa chính xác. Câu trả lời đúng là {question.dap_an}.",
                f"Đáp án {question.dap_an} mới là chính xác. Cần ôn lại phần này."
            ]
        
        base_explanation = random.choice(explanations)
        
        # Add difficulty-based advice
        if question.do_kho == "kho":
            base_explanation += " Đây là câu hỏi khó, cần luyện tập thêm."
        elif question.do_kho == "de":
            if not is_correct:
                base_explanation += " Đây là câu hỏi dễ, hãy cẩn thận hơn."
        
        return base_explanation
    
    def _auto_save_progress(self, session: TestSession):
        """Tự động lưu tiến độ."""
        try:
            progress_file = self.quiz_storage_dir / f"progress_{session.session_id}.json"
            progress_data = {
                "session_id": session.session_id,
                "student_name": session.student_name,
                "test_title": session.test_title,
                "current_question": session.current_question,
                "answers": session.answers,
                "start_time": session.start_time.isoformat(),
                "test_mode": session.test_mode,
                "last_save": datetime.now().isoformat()
            }
            
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️ Lỗi auto-save: {e}")

    def next_question(self, session_id: str) -> bool:
        """Chuyển đến câu hỏi tiếp theo."""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        if session.current_question < len(session.questions) - 1:
            session.current_question += 1
            return True
        return False
    
    def previous_question(self, session_id: str) -> bool:
        """Quay lại câu hỏi trước."""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        if session.current_question > 0:
            session.current_question -= 1
            return True
        return False
    
    def goto_question(self, session_id: str, question_number: int) -> bool:
        """Chuyển đến câu hỏi cụ thể."""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        if 1 <= question_number <= len(session.questions):
            session.current_question = question_number - 1
            return True
        return False
    
    def get_test_overview(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Lấy tổng quan bài kiểm tra với enhanced info."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        answered_questions = len(session.answers)
        time_remaining = self._get_time_remaining(session) if session.test_mode == "exam" else 9999
        time_elapsed = self._get_time_elapsed(session)
        
        # Calculate progress stats
        correct_count = 0
        if session.test_mode == "practice":
            for q_num, feedback in session.question_feedback.items():
                if feedback.get('is_correct', False):
                    correct_count += 1
        
        # Question status
        question_status = []
        for i, q in enumerate(session.questions):
            status = {
                "question_number": i + 1,
                "so_cau": q.so_cau,
                "answered": q.so_cau in session.answers,
                "answer": session.answers.get(q.so_cau, ""),
                "has_images": q.has_images,
                "difficulty": q.do_kho
            }
            
            if session.test_mode == "practice" and q.so_cau in session.question_feedback:
                status["is_correct"] = session.question_feedback[q.so_cau].get('is_correct', False)
                status["feedback_available"] = True
            
            question_status.append(status)
        
        return {
            "student_name": session.student_name,
            "test_title": session.test_title,
            "total_questions": len(session.questions),
            "answered_questions": answered_questions,
            "correct_answers": correct_count,  # Only for practice mode
            "progress": (answered_questions / len(session.questions)) * 100,
            "time_remaining": time_remaining,
            "time_elapsed": time_elapsed,
            "test_mode": session.test_mode,
            "question_status": question_status,
            "session_settings": session.settings,
            "has_images_count": sum(1 for q in session.questions if q.has_images)
        }
    
    def finish_test(self, session_id: str) -> Optional[TestResult]:
        """Hoàn thành bài kiểm tra với enhanced result."""
        return self._finish_test(session_id)
    
    def _finish_test(self, session_id: str) -> Optional[TestResult]:
        """Xử lý hoàn thành bài kiểm tra với enhanced statistics."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        session.is_finished = True
        session.end_time = datetime.now()
        
        # Enhanced grading
        result = self._enhanced_grade_test(session)
        
        # Save result
        self.completed_tests.append(result)
        self._save_test_history()
        
        # Cleanup progress file
        try:
            progress_file = self.quiz_storage_dir / f"progress_{session_id}.json"
            if progress_file.exists():
                progress_file.unlink()
        except:
            pass
        
        # Remove from active sessions
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        print(f"🎉 Hoàn thành bài kiểm tra: {result.student_name} - {result.score}/10")
        return result
    
    def _enhanced_grade_test(self, session: TestSession) -> TestResult:
        """Chấm điểm bài kiểm tra với enhanced analysis."""
        correct = 0
        wrong = 0
        unanswered = 0
        detailed_results = []
        
        # Time analysis
        total_time_per_question = []
        difficulty_performance = {"de": {"correct": 0, "total": 0}, 
                                "trung_binh": {"correct": 0, "total": 0},
                                "kho": {"correct": 0, "total": 0}}
        
        for question in session.questions:
            user_answer = session.answers.get(question.so_cau, "")
            is_correct = user_answer.upper() == question.dap_an.upper() if user_answer else False
            
            # Count answers
            if not user_answer:
                unanswered += 1
                result_status = "Không trả lời"
            elif is_correct:
                correct += 1
                result_status = "Đúng"
            else:
                wrong += 1
                result_status = "Sai"
            
            # Time analysis
            answer_time = session.answer_times.get(question.so_cau)
            time_spent = None
            if answer_time and session.start_time:
                # Calculate time from start to this answer
                prev_questions = [q for q in session.questions if q.so_cau < question.so_cau]
                if prev_questions:
                    prev_answer_times = [session.answer_times.get(q.so_cau) for q in prev_questions]
                    prev_answer_times = [t for t in prev_answer_times if t]
                    if prev_answer_times:
                        time_spent = (answer_time - max(prev_answer_times)).total_seconds()
                    else:
                        time_spent = (answer_time - session.start_time).total_seconds()
                else:
                    time_spent = (answer_time - session.start_time).total_seconds()
                
                if time_spent > 0:
                    total_time_per_question.append(time_spent)
            
            # Difficulty analysis
            difficulty = question.do_kho
            if difficulty in difficulty_performance:
                difficulty_performance[difficulty]["total"] += 1
                if is_correct:
                    difficulty_performance[difficulty]["correct"] += 1
            
            # Prepare detailed result
            detailed_result = {
                "so_cau": question.so_cau,
                "cau_hoi": question.cau_hoi,
                "lua_chon": question.lua_chon,
                "dap_an_dung": question.dap_an,
                "dap_an_chon": user_answer if user_answer else "Không trả lời",
                "ket_qua": result_status,
                "do_kho": question.do_kho,
                "mon_hoc": question.mon_hoc,
                "has_images": question.has_images,
                "time_spent": time_spent,
                "is_correct": is_correct
            }
            
            # Add practice mode specific data
            if session.test_mode == "practice":
                feedback = session.question_feedback.get(question.so_cau, {})
                detailed_result["feedback"] = feedback.get("explanation", "")
                detailed_result["answer_timestamp"] = feedback.get("answer_time", "").isoformat() if feedback.get("answer_time") else ""
            
            detailed_results.append(detailed_result)
        
        # Calculate scores
        total = len(session.questions)
        percentage = (correct / total) * 100 if total > 0 else 0
        score = (correct / total) * 10 if total > 0 else 0
        
        # Time statistics
        avg_time_per_question = sum(total_time_per_question) / len(total_time_per_question) if total_time_per_question else 0
        
        time_stats = {
            "total_time": self._get_time_elapsed(session),
            "average_per_question": f"{avg_time_per_question:.1f}s",
            "fastest_question": f"{min(total_time_per_question):.1f}s" if total_time_per_question else "N/A",
            "slowest_question": f"{max(total_time_per_question):.1f}s" if total_time_per_question else "N/A"
        }
        
        # Question statistics
        question_stats = {
            "by_difficulty": difficulty_performance,
            "by_subject": self._analyze_by_subject(detailed_results),
            "images_questions": sum(1 for q in session.questions if q.has_images),
            "completion_rate": f"{((total - unanswered) / total * 100):.1f}%" if total > 0 else "0%"
        }
        
        return TestResult(
            session_id=session.session_id,
            student_name=session.student_name,
            test_title=session.test_title,
            total_questions=total,
            correct_answers=correct,
            wrong_answers=wrong,
            unanswered=unanswered,
            score=round(score, 2),
            percentage=round(percentage, 1),
            time_taken=self._get_time_elapsed(session),
            detailed_results=detailed_results,
            finish_time=session.end_time or datetime.now(),
            test_mode=session.test_mode,
            question_stats=question_stats,
            time_stats=time_stats
        )
    
    def _analyze_by_subject(self, detailed_results: List[Dict]) -> Dict[str, Dict]:
        """Phân tích kết quả theo môn học."""
        subjects = {}
        
        for result in detailed_results:
            subject = result.get("mon_hoc", "unknown")
            if subject not in subjects:
                subjects[subject] = {"correct": 0, "total": 0}
            
            subjects[subject]["total"] += 1
            if result.get("is_correct", False):
                subjects[subject]["correct"] += 1
        
        # Calculate percentages
        for subject, stats in subjects.items():
            if stats["total"] > 0:
                stats["percentage"] = round((stats["correct"] / stats["total"]) * 100, 1)
            else:
                stats["percentage"] = 0
        
        return subjects
    
    def get_test_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê các bài kiểm tra với enhanced analytics."""
        if not self.completed_tests:
            return {"message": "Chưa có bài kiểm tra nào được hoàn thành."}
        
        total_tests = len(self.completed_tests)
        scores = [test.score for test in self.completed_tests]
        percentages = [test.percentage for test in self.completed_tests]
        
        # Basic stats
        avg_score = sum(scores) / len(scores) if scores else 0
        avg_percentage = sum(percentages) / len(percentages) if percentages else 0
        highest_score = max(scores) if scores else 0
        lowest_score = min(scores) if scores else 0
        pass_rate = len([s for s in scores if s >= 5]) / len(scores) * 100 if scores else 0
        
        # Enhanced analytics
        mode_stats = {"exam": 0, "practice": 0}
        difficulty_analysis = {}
        subject_analysis = {}
        monthly_performance = {}
        
        for test in self.completed_tests:
            # Mode statistics
            mode_stats[test.test_mode] = mode_stats.get(test.test_mode, 0) + 1
            
            # Monthly performance
            month_key = test.finish_time.strftime("%Y-%m")
            if month_key not in monthly_performance:
                monthly_performance[month_key] = {"count": 0, "avg_score": 0, "total_score": 0}
            monthly_performance[month_key]["count"] += 1
            monthly_performance[month_key]["total_score"] += test.score
            monthly_performance[month_key]["avg_score"] = monthly_performance[month_key]["total_score"] / monthly_performance[month_key]["count"]
            
            # Difficulty and subject analysis
            if hasattr(test, 'question_stats') and test.question_stats:
                # Difficulty
                for diff, stats in test.question_stats.get("by_difficulty", {}).items():
                    if diff not in difficulty_analysis:
                        difficulty_analysis[diff] = {"correct": 0, "total": 0}
                    difficulty_analysis[diff]["correct"] += stats["correct"]
                    difficulty_analysis[diff]["total"] += stats["total"]
                
                # Subject
                for subj, stats in test.question_stats.get("by_subject", {}).items():
                    if subj not in subject_analysis:
                        subject_analysis[subj] = {"correct": 0, "total": 0}
                    subject_analysis[subj]["correct"] += stats["correct"]
                    subject_analysis[subj]["total"] += stats["total"]
        
        # Calculate percentages for difficulty/subject
        for diff in difficulty_analysis:
            total = difficulty_analysis[diff]["total"]
            if total > 0:
                difficulty_analysis[diff]["percentage"] = round((difficulty_analysis[diff]["correct"] / total) * 100, 1)
        
        for subj in subject_analysis:
            total = subject_analysis[subj]["total"]
            if total > 0:
                subject_analysis[subj]["percentage"] = round((subject_analysis[subj]["correct"] / total) * 100, 1)
        
        # Recent tests
        recent_tests = []
        for test in sorted(self.completed_tests, key=lambda x: x.finish_time, reverse=True)[:15]:
            recent_tests.append({
                "student": test.student_name,
                "title": test.test_title[:30] + "..." if len(test.test_title) > 30 else test.test_title,
                "score": test.score,
                "percentage": test.percentage,
                "mode": test.test_mode,
                "time": test.finish_time.strftime("%d/%m/%Y %H:%M"),
                "questions": test.total_questions,
                "time_taken": test.time_taken
            })
        
        return {
            "total_tests": total_tests,
            "average_score": round(avg_score, 2),
            "average_percentage": round(avg_percentage, 1),
            "highest_score": highest_score,
            "lowest_score": lowest_score,
            "pass_rate": round(pass_rate, 1),
            "mode_distribution": mode_stats,
            "difficulty_analysis": difficulty_analysis,
            "subject_analysis": subject_analysis,
            "monthly_performance": monthly_performance,
            "recent_tests": recent_tests,
            "engine_info": {
                "version": self.engine_version,
                "features": self.supported_features,
                "total_quizzes_stored": len(self.saved_quizzes),
                "active_sessions": len(self.active_sessions)
            }
        }
    
    def update_question_in_quiz(self, quiz_name: str, question_index: int, updated_question: Dict[str, Any]) -> bool:
        """Cập nhật câu hỏi trong quiz đã lưu với image support."""
        try:
            if quiz_name in self.saved_quizzes:
                file_path = Path(self.saved_quizzes[quiz_name]["file_path"])
                
                # Load current data
                with open(file_path, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                
                # Update question
                if 0 <= question_index < len(quiz_data):
                    # Handle images if any
                    if 'images' in updated_question and updated_question['images']:
                        processed_images = []
                        for img in updated_question['images']:
                            if isinstance(img, dict) and 'data' in img:
                                # Save new image
                                img_filename = f"{quiz_name}_q{updated_question.get('so_cau', question_index)}_{len(processed_images)}.jpg"
                                img_path = self.images_dir / img_filename
                                self._save_image_to_disk(img['data'], img_path)
                                
                                processed_images.append({
                                    "name": img.get('name', img_filename),
                                    "path": str(img_path.relative_to(self.quiz_storage_dir)),
                                    "type": img.get('type', 'image/jpeg'),
                                    "size": img_path.stat().st_size if img_path.exists() else 0,
                                    "description": img.get('description', '')
                                })
                            else:
                                processed_images.append(img)
                        
                        updated_question['images'] = processed_images
                        updated_question['has_images'] = len(processed_images) > 0
                    
                    # Add update timestamp
                    updated_question['updated_time'] = datetime.now().isoformat()
                    
                    quiz_data[question_index] = updated_question
                    
                    # Save back
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ Đã cập nhật câu {question_index + 1} trong quiz '{quiz_name}'")
                    return True
                    
        except Exception as e:
            print(f"❌ Lỗi cập nhật câu hỏi: {e}")
        return False
    
    def add_image_to_question(self, quiz_name: str, question_index: int, image_data: bytes, 
                            image_name: str, description: str = "") -> bool:
        """Thêm hình ảnh vào câu hỏi với enhanced handling."""
        try:
            if quiz_name not in self.saved_quizzes:
                return False
            
            file_path = Path(self.saved_quizzes[quiz_name]["file_path"])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)
            
            if 0 <= question_index < len(quiz_data):
                # Create image filename
                safe_name = "".join(c for c in quiz_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                img_filename = f"{safe_name}_q{quiz_data[question_index].get('so_cau', question_index)}_{image_name}"
                img_path = self.images_dir / img_filename
                
                # Save image
                self._save_image_to_disk(image_data, img_path)
                
                # Update question metadata
                if "images" not in quiz_data[question_index]:
                    quiz_data[question_index]["images"] = []
                
                quiz_data[question_index]["images"].append({
                    "name": image_name,
                    "path": str(img_path.relative_to(self.quiz_storage_dir)),
                    "type": "image/jpeg",
                    "size": img_path.stat().st_size if img_path.exists() else 0,
                    "description": description
                })
                
                quiz_data[question_index]["has_images"] = True
                quiz_data[question_index]["updated_time"] = datetime.now().isoformat()
                
                # Save quiz data
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(quiz_data, f, ensure_ascii=False, indent=2)
                
                # Update index
                self.saved_quizzes[quiz_name]["images_count"] = self.saved_quizzes[quiz_name].get("images_count", 0) + 1
                self.saved_quizzes[quiz_name]["has_images"] = True
                self._save_index()
                
                print(f"✅ Đã thêm ảnh '{image_name}' vào câu {question_index + 1}")
                return True
                
        except Exception as e:
            print(f"❌ Lỗi thêm ảnh: {e}")
        return False
    
    def remove_image_from_question(self, quiz_name: str, question_index: int, image_name: str) -> bool:
        """Xóa ảnh khỏi câu hỏi."""
        try:
            if quiz_name not in self.saved_quizzes:
                return False
            
            file_path = Path(self.saved_quizzes[quiz_name]["file_path"])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)
            
            if 0 <= question_index < len(quiz_data):
                images = quiz_data[question_index].get("images", [])
                updated_images = []
                
                for img in images:
                    if img.get("name") == image_name:
                        # Delete image file
                        img_path = self.quiz_storage_dir / img.get("path", "")
                        if img_path.exists():
                            img_path.unlink()
                        print(f"🗑️ Đã xóa file ảnh: {img_path}")
                    else:
                        updated_images.append(img)
                
                quiz_data[question_index]["images"] = updated_images
                quiz_data[question_index]["has_images"] = len(updated_images) > 0
                quiz_data[question_index]["updated_time"] = datetime.now().isoformat()
                
                # Save quiz data
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(quiz_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Đã xóa ảnh '{image_name}' khỏi câu {question_index + 1}")
                return True
                
        except Exception as e:
            print(f"❌ Lỗi xóa ảnh: {e}")
        return False
    
    def export_quiz(self, quiz_name: str, format: str = "json") -> Optional[str]:
        """Export quiz với multiple formats."""
        try:
            if quiz_name not in self.saved_quizzes:
                return None
            
            # Load quiz data
            questions = self.load_quiz_from_storage(quiz_name)
            if not questions:
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format.lower() == "json":
                # JSON export với images embedded
                export_data = []
                for q in questions:
                    q_dict = asdict(q)
                    
                    # Embed images as base64
                    if q.images:
                        embedded_images = []
                        for img in q.images:
                            if img.data:
                                encoded = base64.b64encode(img.data).decode('utf-8')
                                embedded_images.append({
                                    "name": img.name,
                                    "data": encoded,
                                    "type": img.type,
                                    "description": img.description
                                })
                        q_dict["images"] = embedded_images
                    
                    export_data.append(q_dict)
                
                # Save export file
                export_filename = f"{quiz_name}_export_{timestamp}.json"
                export_path = self.exports_dir / export_filename
                
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                print(f"📦 Đã export quiz '{quiz_name}' -> {export_path}")
                return str(export_path)
                
        except Exception as e:
            print(f"❌ Lỗi export quiz: {e}")
        return None
    
    def import_quiz(self, file_path: str, quiz_name: str = None) -> bool:
        """Import quiz từ file external."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)
            
            # Generate quiz name if not provided
            if not quiz_name:
                quiz_name = f"Imported_{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save to storage
            result = self.save_quiz_to_storage(quiz_data, quiz_name)
            
            if result:
                print(f"✅ Đã import quiz '{quiz_name}' từ {file_path}")
                return True
            
        except Exception as e:
            print(f"❌ Lỗi import quiz: {e}")
        return False
    
    def _generate_session_id(self, student_name: str, test_title: str) -> str:
        """Tạo session ID duy nhất."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_suffix = uuid.uuid4().hex[:6]
        return f"session_{timestamp}_{random_suffix}"
    
    def _shuffle_choices(self, choices: Dict[str, str], correct_answer: str) -> Dict[str, str]:
        """Trộn thứ tự các lựa chọn với enhanced algorithm."""
        if len(choices) != 4:
            return choices
        
        # Get content và shuffle
        choice_contents = list(choices.values())
        random.shuffle(choice_contents)
        
        # Create new mapping
        new_choices = {}
        new_keys = ['A', 'B', 'C', 'D']
        
        for i, content in enumerate(choice_contents):
            new_choices[new_keys[i]] = content
        
        return new_choices
    
    def _get_time_remaining(self, session: TestSession) -> int:
        """Lấy thời gian còn lại (giây)."""
        if session.test_mode != "exam":
            return 9999
        
        elapsed = datetime.now() - session.start_time
        total_seconds = session.time_limit * 60
        remaining = total_seconds - elapsed.total_seconds()
        
        return max(0, int(remaining))
    
    def _get_time_elapsed(self, session: TestSession) -> str:
        """Lấy thời gian đã làm bài."""
        if session.end_time:
            delta = session.end_time - session.start_time
        else:
            delta = datetime.now() - session.start_time
        
        return self._format_duration(delta)
    
    def _format_duration(self, delta: timedelta) -> str:
        """Format thời gian thành chuỗi."""
        total_seconds = int(delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Lấy thông tin storage tổng quan."""
        total_quizzes = len(self.saved_quizzes)
        total_tests = len(self.completed_tests)
        
        # Calculate storage size
        total_size = 0
        image_count = 0
        
        for quiz_info in self.saved_quizzes.values():
            if Path(quiz_info["file_path"]).exists():
                total_size += Path(quiz_info["file_path"]).stat().st_size
            image_count += quiz_info.get("images_count", 0)
        
        # Count image files
        image_files = list(self.images_dir.glob("*"))
        image_storage_size = sum(f.stat().st_size for f in image_files if f.is_file())
        
        return {
            "total_quizzes": total_quizzes,
            "total_tests_completed": total_tests,
            "total_storage_size": f"{(total_size + image_storage_size) / 1024 / 1024:.2f} MB",
            "quiz_files_size": f"{total_size / 1024:.1f} KB",
            "images_count": image_count,
            "images_storage_size": f"{image_storage_size / 1024:.1f} KB",
            "storage_directories": {
                "quiz_storage": str(self.quiz_storage_dir),
                "images": str(self.images_dir),
                "backups": str(self.backups_dir),
                "exports": str(self.exports_dir)
            },
            "engine_version": self.engine_version
        }