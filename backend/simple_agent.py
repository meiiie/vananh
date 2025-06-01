"""
Agent Đơn Giản cho QuizForce AI Test
Xử lý tất cả các công việc trong một agent để tránh phức tạp.
"""

import json
import re
import os
import io
import time
import docx
from typing import Dict, Optional, Tuple, Any, List  # Thêm List vào import
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import random

load_dotenv()

class SimpleQuizAgent:
    """
    Agent AI Chuyên Nghiệp cho Việt Nam - Xử lý toàn bộ quy trình tạo quiz:
    1. Phân tích đáp án (văn bản/hình ảnh)
    2. Trích xuất câu hỏi từ DOCX
    3. Biên soạn quiz hoàn chỉnh
    
    Được thiết kế đặc biệt cho hệ thống giáo dục Việt Nam
    """
    
    def __init__(self, api_key: str = None):
        """Khởi tạo Agent AI chuyên nghiệp."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Cần có API key để khởi động agent")
        
        # Khởi tạo Gemini với cấu hình tối ưu
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Thông tin agent
        self.agent_name = "QuizMaster AI"
        self.agent_version = "2.0"  # Nâng cấp lên v2.0
        self.specialization = "Chuyên gia tạo quiz trắc nghiệm cho giáo dục Việt Nam"
        
        # Enhanced quota management
        self.requests_count = 0
        self.last_request_time = 0
        self.base_delay = 0.5
        self.max_retries = 3
        self.batch_size = 10  # Xử lý 10 câu một batch
        self.batch_delay = 5   # Đợi 5 giây giữa các batch
        self.quota_exceeded_delay = 30  # Đợi 30 giây khi gặp quota limit
        self.failed_questions = []  # Lưu các câu thất bại để xử lý lại
        
        print(f"✨ {self.agent_name} v{self.agent_version} đã sẵn sàng")
        print(f"🎯 {self.specialization}")
        print(f"⚙️ Batch processing: {self.batch_size} questions/batch, {self.batch_delay}s delay")
    
    def _smart_rate_limit(self):
        """Quản lý rate limit thông minh với exponential backoff."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Tính delay dựa trên số requests gần đây
        if self.requests_count > 20:
            delay = self.base_delay * 2  # Double delay after 20 requests
        elif self.requests_count > 10:
            delay = self.base_delay * 1.5  # 1.5x delay after 10 requests
        else:
            delay = self.base_delay
        
        # Đảm bảo delay tối thiểu
        if time_since_last < delay:
            sleep_time = delay - time_since_last
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.requests_count += 1
    
    def _make_api_request(self, prompt: str, retries: int = 0) -> str:
        """Thực hiện API request với retry logic và quota management."""
        try:
            self._smart_rate_limit()
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_str = str(e).lower()
            
            # Xử lý quota exceeded
            if "quota" in error_str or "limit" in error_str or "429" in error_str:
                if retries < self.max_retries:
                    # Exponential backoff: 2^retry_count seconds + random jitter
                    wait_time = (2 ** retries) + random.uniform(0.5, 1.5)
                    print(f"⏳ Quota limit detected, waiting {wait_time:.1f}s before retry {retries + 1}/{self.max_retries}")
                    time.sleep(wait_time)
                    return self._make_api_request(prompt, retries + 1)
                else:
                    raise Exception(f"❌ Quota limit exceeded sau {self.max_retries} attempts. Vui lòng thử lại sau ít phút.")
            
            # Xử lý các lỗi khác
            elif "safety" in error_str:
                raise Exception("❌ Content bị từ chối bởi safety filter. Vui lòng kiểm tra nội dung.")
            else:
                if retries < self.max_retries:
                    wait_time = 1 + retries
                    print(f"⚠️ API error, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                    return self._make_api_request(prompt, retries + 1)
                else:
                    raise e

    def process_text_answers(self, answer_text: str) -> Dict[int, str]:
        """Xử lý đáp án dạng văn bản với độ chính xác cao và nhiều format."""
        print("🔍 Agent đang phân tích đáp án văn bản...")
        
        # Thử phân tích bằng regex trước
        regex_result = self._parse_answers_with_regex(answer_text)
        if regex_result:
            print(f"✅ Phân tích regex thành công: {len(regex_result)} đáp án")
            return regex_result
        
        # Nếu regex không được thì dùng AI
        prompt = f"""
        Bạn là chuyên gia xử lý đáp án trắc nghiệm Việt Nam.
        
        NHIỆM VỤ: Trích xuất CHÍNH XÁC số câu và đáp án từ văn bản.
        
        QUY TẮC:
        - Tìm tất cả patterns: "số. đáp_án" hoặc "số) đáp_án" hoặc "số: đáp_án"
        - Format JSON: {{"1": "A", "2": "B", "3": "AC"}}
        - Key là string của số câu
        - Value là đáp án (A,B,C,D hoặc kết hợp AC,BD,ABC,ABCD)
        - Chuẩn hóa đáp án kết hợp theo thứ tự ABC
        
        VĂN BẢN:
        {answer_text}
        
        VÍ DỤ OUTPUT:
        {{"1": "A", "2": "BD", "3": "C", "10": "ABC"}}
        
        CHỈ TRẢ VỀ JSON:
        """
        
        try:
            response_text = self._make_api_request(prompt)
            result = self._parse_json_response(response_text)
            # Convert keys to int
            result = {int(k): v for k, v in result.items() if k.isdigit()}
            print(f"✅ Đã phân tích AI: {len(result)} đáp án")
            return result
        except Exception as e:
            print(f"❌ Lỗi xử lý đáp án văn bản: {e}")
            return {}
    
    def _parse_answers_with_regex(self, text: str) -> Dict[int, str]:
        """Phân tích đáp án bằng regex với nhiều patterns phổ biến."""
        answers = {}
        
        # Các patterns thường gặp
        patterns = [
            r'(\d+)\s*\.\s*([A-D]+)',  # 1. A hoặc 1. AC
            r'(\d+)\s*\)\s*([A-D]+)',  # 1) A
            r'(\d+)\s*:\s*([A-D]+)',   # 1: A
            r'(\d+)\s+([A-D]+)',       # 1 A
            r'Câu\s*(\d+)\s*[\.:\)]\s*([A-D]+)',  # Câu 1. A
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            temp_answers = {}
            
            for match in matches:
                try:
                    q_num = int(match[0])
                    answer = match[1].upper().strip()
                    # Sắp xếp đáp án kết hợp
                    answer = ''.join(sorted(set(answer)))
                    temp_answers[q_num] = answer
                except:
                    continue
            
            # Chọn kết quả tốt nhất
            if len(temp_answers) > len(answers):
                answers = temp_answers
        
        return answers

    def process_image_answers(self, image_data: bytes) -> Dict[int, str]:
        """Xử lý đáp án từ hình ảnh với công nghệ OCR tiên tiến."""
        print("🖼️ Agent đang phân tích đáp án từ hình ảnh...")
        
        try:
            image = Image.open(io.BytesIO(image_data))
            
            prompt = """
            Bạn là chuyên gia xử lý hình ảnh và OCR cho hệ thống giáo dục Việt Nam.
            
            NHIỆM VỤ: Đọc và trích xuất đáp án trắc nghiệm từ hình ảnh.
            
            YÊU CẦU:
            - Phân tích chính xác từng số câu và đáp án tương ứng
            - Format JSON: {"1": "A", "2": "B", "3": "AC"}
            - Xử lý cả đáp án đơn (A, B, C, D) và đáp án kép (AC, BD, ABC)
            - Bỏ qua nhiễu, chữ viết tay không rõ ràng
            
            CHỈ TRẢ VỀ JSON OBJECT:
            """
            
            self._smart_rate_limit()
            response = self.model.generate_content([prompt, image])
            result = self._parse_json_response(response.text)
            print(f"✅ Đã trích xuất {len(result)} đáp án từ hình ảnh")
            return result
        except Exception as e:
            print(f"❌ Lỗi xử lý hình ảnh: {e}")
            return {}
    
    def extract_questions_from_docx(self, docx_file) -> Dict[int, str]:
        """Trích xuất câu hỏi từ file DOCX với thuật toán thông minh cải tiến."""
        print("📄 Agent đang trích xuất câu hỏi từ file DOCX...")
        
        try:
            # Đọc nội dung DOCX
            file_stream = io.BytesIO(docx_file.getvalue())
            document = docx.Document(file_stream)
            
            # Trích xuất văn bản từ tất cả paragraph
            paragraphs = []
            for para in document.paragraphs:
                text = para.text.strip()
                if text:  # Chỉ lấy paragraph có nội dung
                    paragraphs.append(text)
            
            full_text = "\n".join(paragraphs)
            
            # Làm sạch văn bản
            cleaned_text = self._clean_vietnamese_text(full_text)
            
            # Thử nhiều phương pháp trích xuất
            question_blocks = {}
            
            # Phương pháp 1: Tách theo paragraph
            blocks_by_para = self._extract_by_paragraphs(paragraphs)
            if blocks_by_para:
                question_blocks.update(blocks_by_para)
                print(f"📋 Phương pháp paragraph: {len(blocks_by_para)} câu")
            
            # Phương pháp 2: Tách theo patterns
            blocks_by_pattern = self._extract_vietnamese_question_blocks(cleaned_text)
            if len(blocks_by_pattern) > len(question_blocks):
                question_blocks = blocks_by_pattern
                print(f"📋 Phương pháp pattern: {len(blocks_by_pattern)} câu")
            
            print(f"✅ Tổng cộng trích xuất: {len(question_blocks)} câu hỏi")
            
            # Debug info
            if question_blocks:
                sample_nums = list(question_blocks.keys())[:5]
                print(f"🔍 Số câu mẫu: {sample_nums}")
            
            return question_blocks
            
        except Exception as e:
            print(f"❌ Lỗi trích xuất file DOCX: {e}")
            return {}
    
    def _extract_by_paragraphs(self, paragraphs) -> Dict[int, str]:
        """Trích xuất câu hỏi theo từng paragraph."""
        questions = {}
        current_question = None
        current_text = []
        
        # Patterns để nhận diện đầu câu hỏi
        question_patterns = [
            r'^Câu\s*(\d+)\s*[\.:]',
            r'^Question\s*(\d+)\s*[\.:]',
            r'^(\d+)\s*[\.:]',
            r'^(\d+)\s*\)',
            r'^Bài\s*(\d+)\s*[\.:]',
        ]
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Kiểm tra xem có phải đầu câu hỏi mới không
            found_new_question = False
            for pattern in question_patterns:
                match = re.match(pattern, para, re.IGNORECASE)
                if match:
                    # Lưu câu hỏi trước đó
                    if current_question and current_text:
                        questions[current_question] = "\n".join(current_text)
                    
                    # Bắt đầu câu hỏi mới
                    current_question = int(match.group(1))
                    current_text = [para]
                    found_new_question = True
                    break
            
            if not found_new_question and current_question:
                # Thêm vào câu hỏi hiện tại
                current_text.append(para)
        
        # Lưu câu hỏi cuối cùng
        if current_question and current_text:
            questions[current_question] = "\n".join(current_text)
        
        return questions

    def _make_api_request_with_recovery(self, prompt: str, retries: int = 0, is_retry: bool = False) -> str:
        """Thực hiện API request với recovery mechanism nâng cao."""
        try:
            if not is_retry:
                self._smart_rate_limit()
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Xử lý quota exceeded với recovery mechanism
            if "quota" in error_str or "limit" in error_str or "429" in error_str:
                if retries < self.max_retries:
                    # Exponential backoff
                    wait_time = (2 ** retries) + random.uniform(0.5, 1.5)
                    print(f"⏳ Quota limit detected, waiting {wait_time:.1f}s before retry {retries + 1}/{self.max_retries}")
                    time.sleep(wait_time)
                    return self._make_api_request_with_recovery(prompt, retries + 1, is_retry=True)
                else:
                    # Sau khi thử hết retry, ném exception để batch processor xử lý
                    raise Exception(f"QUOTA_EXCEEDED_AFTER_RETRIES")
            
            # Xử lý các lỗi khác
            elif "safety" in error_str:
                raise Exception("❌ Content bị từ chối bởi safety filter. Vui lòng kiểm tra nội dung.")
            else:
                if retries < self.max_retries:
                    wait_time = 1 + retries
                    print(f"⚠️ API error, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                    return self._make_api_request_with_recovery(prompt, retries + 1, is_retry=True)
                else:
                    raise e

    def compile_question(self, question_num: int, question_text: str, correct_answer: str) -> Dict[str, Any]:
        """Biên soạn câu hỏi thành format chuẩn."""
        print(f"⚙️ Đang biên soạn câu hỏi số {question_num}...")
        
        prompt = f"""
        Bạn là chuyên gia biên soạn đề thi trắc nghiệm hàng đầu tại Việt Nam với 15 năm kinh nghiệm.
        
        NHIỆM VỤ: Phân tích và chuẩn hóa câu hỏi trắc nghiệm theo tiêu chuẩn giáo dục Việt Nam.
        
        FORMAT OUTPUT CHUẨN:
        {{
            "so_cau": {question_num},
            "cau_hoi": "Nội dung câu hỏi được làm sạch và chuẩn hóa",
            "lua_chon": {{
                "A": "Lựa chọn A - rõ ràng, súc tích",
                "B": "Lựa chọn B - rõ ràng, súc tích",
                "C": "Lựa chọn C - rõ ràng, súc tích",
                "D": "Lựa chọn D - rõ ràng, súc tích"
            }},
            "dap_an": "{correct_answer}",
            "do_kho": "trung_binh",
            "mon_hoc": "auto_detect",
            "ghi_chu": "Được xử lý bởi QuizMaster AI v2.0"
        }}
        
        YÊU CẦU XỬ LÝ:
        - Làm sạch nội dung câu hỏi, loại bỏ ký tự thừa
        - Tách riêng câu hỏi và 4 lựa chọn A, B, C, D
        - Đảm bảo nội dung tiếng Việt chuẩn, dễ hiểu
        - Nếu không tách được đủ 4 lựa chọn, tạo lựa chọn hợp lý
        
        NỘI DUNG CÂU HỎI CẦN XỬ LÝ:
        {question_text}
        
        CHỈ TRẢ VỀ JSON OBJECT:
        """
        
        try:
            response_text = self._make_api_request_with_recovery(prompt)
            compiled = self._parse_json_response(response_text)
            
            # Kiểm tra cấu trúc hợp lệ
            if isinstance(compiled, dict) and "cau_hoi" in compiled and "lua_chon" in compiled:
                compiled["so_cau"] = question_num
                compiled["dap_an"] = correct_answer
                return compiled
            else:
                # Fallback với cấu trúc an toàn
                return self._create_fallback_question(question_num, question_text, correct_answer)
                
        except Exception as e:
            print(f"❌ Lỗi biên soạn câu hỏi {question_num}: {e}")
            if "QUOTA_EXCEEDED_AFTER_RETRIES" in str(e):
                raise e
            return self._create_fallback_question(question_num, question_text, correct_answer, error=str(e))

    def process_complete_quiz(self, answer_data, docx_file, answer_type="text") -> Dict[str, Any]:
        """Xử lý toàn bộ quy trình tạo quiz từ A đến Z với batch processing thông minh."""
        print("🚀 Bắt đầu quy trình tạo quiz hoàn chỉnh với batch processing...")
        
        # Reset counter cho session mới
        self.requests_count = 0
        self.failed_questions = []
        
        results = {
            "success": False,
            "parsed_answers": {},
            "question_blocks": {},
            "compiled_questions": [],
            "errors": [],
            "statistics": {},
            "debug_info": {},
            "agent_info": {
                "name": self.agent_name,
                "version": self.agent_version,
                "specialization": self.specialization,
                "quota_requests": 0,
                "batch_info": {
                    "batch_size": self.batch_size,
                    "total_batches": 0,
                    "completed_batches": 0,
                    "failed_questions": 0,
                    "recovered_questions": 0
                }
            }
        }
        
        try:
            start_time = time.time()
            
            # BƯỚC 1-3: Xử lý đáp án và câu hỏi (giữ nguyên)
            print("📝 BƯỚC 1/4: Xử lý đáp án...")
            if answer_type == "text":
                results["parsed_answers"] = self.process_text_answers(answer_data)
            else:
                results["parsed_answers"] = self.process_image_answers(answer_data)
            
            if not results["parsed_answers"]:
                results["errors"].append("❌ Không thể phân tích đáp án. Kiểm tra định dạng: '1. A', '2. B'")
                return results
            
            print("📄 BƯỚC 2/4: Trích xuất câu hỏi từ DOCX...")
            results["question_blocks"] = self.extract_questions_from_docx(docx_file)
            
            if not results["question_blocks"]:
                results["errors"].append("❌ Không thể trích xuất câu hỏi. File DOCX phải có format: 'Câu 1.' hoặc '1.'")
                return results
            
            print("🔍 BƯỚC 3/4: Kiểm tra tương thích dữ liệu...")
            
            answer_keys = set(results["parsed_answers"].keys())
            question_keys = set(results["question_blocks"].keys())
            
            results["debug_info"] = {
                "answer_keys": sorted(list(answer_keys)),
                "question_keys": sorted(list(question_keys)),
                "answer_count": len(answer_keys),
                "question_count": len(question_keys)
            }
            
            matching_keys = answer_keys & question_keys
            
            if not matching_keys:
                mapping = self._smart_question_mapping(answer_keys, question_keys)
                if mapping:
                    new_answers = {}
                    for q_key, a_key in mapping.items():
                        new_answers[q_key] = results["parsed_answers"][a_key]
                    results["parsed_answers"] = new_answers
                    matching_keys = set(mapping.keys())
                    results["debug_info"]["applied_mapping"] = mapping
            
            if not matching_keys:
                results["errors"].append("❌ Không có câu nào khớp giữa đáp án và câu hỏi.")
                return results
            
            # BƯỚC 4: Biên soạn quiz với batch processing nâng cao
            print("⚙️ BƯỚC 4/4: Biên soạn quiz với Batch Processing...")
            
            matching_list = sorted(list(matching_keys))
            total_questions = len(matching_list)
            
            # Tính số batch
            total_batches = (total_questions + self.batch_size - 1) // self.batch_size
            results["agent_info"]["batch_info"]["total_batches"] = total_batches
            
            print(f"📋 Sẽ xử lý {total_questions} câu hỏi trong {total_batches} batch(es)")
            print(f"📊 Batch size: {self.batch_size}, Delay: {self.batch_delay}s")
            
            compiled_count = 0
            error_count = 0
            
            # Xử lý từng batch
            for batch_idx in range(total_batches):
                start_idx = batch_idx * self.batch_size
                end_idx = min(start_idx + self.batch_size, total_questions)
                batch_questions = matching_list[start_idx:end_idx]
                
                print(f"\n🔄 BATCH {batch_idx + 1}/{total_batches}: Câu {start_idx + 1}-{end_idx}")
                
                batch_success, batch_failed = self._process_batch(
                    batch_questions, results, start_idx
                )
                
                compiled_count += batch_success
                error_count += batch_failed
                
                results["agent_info"]["batch_info"]["completed_batches"] = batch_idx + 1
                
                # Delay giữa các batch (trừ batch cuối)
                if batch_idx < total_batches - 1:
                    print(f"⏳ Đợi {self.batch_delay}s trước batch tiếp theo...")
                    time.sleep(self.batch_delay)
            
            # Xử lý lại các câu thất bại (nếu có)
            if self.failed_questions:
                print(f"\n🔧 Xử lý lại {len(self.failed_questions)} câu thất bại...")
                recovered = self._retry_failed_questions(results)
                compiled_count += recovered
                error_count = len(self.failed_questions) - recovered
                results["agent_info"]["batch_info"]["recovered_questions"] = recovered
            
            results["agent_info"]["batch_info"]["failed_questions"] = error_count
            
            # Tính toán thống kê
            processing_time = time.time() - start_time
            results["statistics"] = {
                "total_questions": total_questions,
                "successful_compilations": compiled_count,
                "failed_compilations": error_count,
                "success_rate": f"{(compiled_count/total_questions*100):.1f}%",
                "processing_time": f"{processing_time:.2f}s",
                "questions_per_second": f"{total_questions/processing_time:.2f}",
                "api_requests_used": self.requests_count,
                "avg_request_time": f"{processing_time/max(self.requests_count, 1):.2f}s",
                "batch_processing": {
                    "total_batches": total_batches,
                    "avg_batch_time": f"{processing_time/total_batches:.2f}s",
                    "recovery_attempts": len(self.failed_questions)
                }
            }
            
            results["agent_info"]["quota_requests"] = self.requests_count
            results["success"] = True
            
            print(f"\n🎉 HOÀN THÀNH: {compiled_count}/{total_questions} câu thành công!")
            print(f"📊 Tổng API calls: {self.requests_count}, Thời gian: {processing_time:.2f}s")
            if error_count > 0:
                print(f"⚠️ {error_count} câu không thể xử lý (sẽ dùng fallback)")
            
        except Exception as e:
            results["errors"].append(f"❌ Lỗi hệ thống: {str(e)}")
            results["agent_info"]["quota_requests"] = self.requests_count
            print(f"❌ Lỗi xử lý: {e}")
        
        return results
    
    def _process_batch(self, batch_questions: List[int], results: Dict, start_idx: int) -> Tuple[int, int]:
        """Xử lý một batch câu hỏi với error recovery."""
        success_count = 0
        failed_count = 0
        
        for i, q_num in enumerate(batch_questions):
            question_text = results["question_blocks"][q_num]
            correct_answer = results["parsed_answers"][q_num]
            current_idx = start_idx + i + 1
            total = len(results["question_blocks"])
            
            print(f"⚙️ Đang xử lý câu {current_idx}/{total} (ID: {q_num})")
            
            try:
                compiled = self.compile_question_with_recovery(q_num, question_text, correct_answer)
                results["compiled_questions"].append(compiled)
                
                if "[LỖI XỬ LÝ]" not in compiled.get("cau_hoi", ""):
                    success_count += 1
                    print(f"✅ Thành công: Câu {q_num}")
                else:
                    failed_count += 1
                    print(f"⚠️ Fallback: Câu {q_num}")
                    
            except Exception as e:
                error_str = str(e)
                print(f"❌ Lỗi câu {q_num}: {error_str}")
                
                if "QUOTA_EXCEEDED_AFTER_RETRIES" in error_str:
                    # Thêm vào danh sách để retry sau
                    self.failed_questions.append({
                        "q_num": q_num,
                        "question_text": question_text,
                        "correct_answer": correct_answer,
                        "reason": "quota_exceeded"
                    })
                    print(f"📝 Đã thêm câu {q_num} vào danh sách retry")
                else:
                    # Tạo fallback ngay
                    fallback = self._create_fallback_question(q_num, question_text, correct_answer, error=error_str)
                    results["compiled_questions"].append(fallback)
                    print(f"🔧 Tạo fallback cho câu {q_num}")
                
                failed_count += 1
        
        return success_count, failed_count
    
    def compile_question_with_recovery(self, question_num: int, question_text: str, correct_answer: str) -> Dict[str, Any]:
        """Biên soạn câu hỏi với recovery mechanism."""
        try:
            return self.compile_question(question_num, question_text, correct_answer)
        except Exception as e:
            if "QUOTA_EXCEEDED_AFTER_RETRIES" in str(e):
                raise e  # Re-raise để batch processor xử lý
            else:
                # Tạo fallback cho các lỗi khác
                return self._create_fallback_question(question_num, question_text, correct_answer, error=str(e))
    
    def _retry_failed_questions(self, results: Dict) -> int:
        """Retry các câu hỏi thất bại sau delay."""
        if not self.failed_questions:
            return 0
        
        print(f"⏳ Đợi {self.quota_exceeded_delay}s để xử lý lại các câu thất bại...")
        time.sleep(self.quota_exceeded_delay)
        
        recovered_count = 0
        remaining_failed = []
        
        for failed_q in self.failed_questions:
            q_num = failed_q["q_num"]
            question_text = failed_q["question_text"]
            correct_answer = failed_q["correct_answer"]
            
            print(f"🔄 Retry câu {q_num}...")
            
            try:
                compiled = self.compile_question(q_num, question_text, correct_answer)
                results["compiled_questions"].append(compiled)
                
                if "[LỖI XỬ LÝ]" not in compiled.get("cau_hoi", ""):
                    recovered_count += 1
                    print(f"✅ Recovered: Câu {q_num}")
                else:
                    print(f"⚠️ Fallback: Câu {q_num}")
                    
            except Exception as e:
                print(f"❌ Vẫn lỗi câu {q_num}: {e}")
                # Tạo fallback cuối cùng
                fallback = self._create_fallback_question(q_num, question_text, correct_answer, error=str(e))
                results["compiled_questions"].append(fallback)
                remaining_failed.append(failed_q)
        
        self.failed_questions = remaining_failed
        return recovered_count

    def _parse_json_response(self, response_text: str) -> Any:
        """Phân tích phản hồi JSON với xử lý lỗi thông minh."""
        if not response_text:
            return {}
        
        try:
            # Làm sạch phản hồi
            cleaned = response_text.strip()
            
            # Loại bỏ markdown code blocks
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            # Parse JSON
            return json.loads(cleaned)
            
        except json.JSONDecodeError:
            print("⚠️ Không thể parse JSON, thử trích xuất thủ công...")
            
            # Tìm JSON object trong text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            print("❌ Không thể trích xuất JSON từ phản hồi")
            return {}
    
    def _clean_vietnamese_text(self, text: str) -> str:
        """Làm sạch văn bản tiếng Việt chuyên biệt."""
        # Loại bỏ HTML tags
        cleaned = re.sub(r'<[^>]+>', '', text)
        
        # Loại bỏ các ký tự đặc biệt không cần thiết
        cleaned = re.sub(r'\\[^\\]*\\', '', cleaned)
        
        # Chuẩn hóa khoảng trắng
        cleaned = re.sub(r'\n\s*\n+', '\n\n', cleaned)
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        cleaned = re.sub(r' *\n *', '\n', cleaned)
        
        # Loại bỏ ký tự Unicode lạ
        cleaned = re.sub(r'[^\w\s\.,\-\(\)\[\]{}:;""''!?áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđĐ]', '', cleaned)
        
        return cleaned.strip()
    
    def _extract_vietnamese_question_blocks(self, text: str) -> Dict[int, str]:
        """Trích xuất câu hỏi với patterns phù hợp tiếng Việt."""
        question_blocks = {}
        
        # Các patterns phổ biến trong đề thi Việt Nam
        patterns = [
            r'Câu\s*(\d+)\s*[\.:]',  # Câu 1. hoặc Câu 1:
            r'Question\s*(\d+)\s*[\.:]',  # Question 1.
            r'^(\d+)\s*[\.:]',  # 1. hoặc 1:
            r'\n(\d+)\s*[\.:]',  # Xuống dòng rồi số
            r'Bài\s*(\d+)\s*[\.:]',  # Bài 1.
            r'(\d+)\s*\)',  # 1)
        ]
        
        for pattern in patterns:
            parts = re.split(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
            
            if len(parts) > 2:
                temp_blocks = {}
                
                for i in range(1, len(parts), 2):
                    try:
                        q_num = int(parts[i].strip())
                        if i + 1 < len(parts):
                            q_text = parts[i + 1].strip()
                            
                            # Kiểm tra câu hỏi hợp lệ (ít nhất 20 ký tự)
                            if len(q_text) > 20:
                                # Cắt bớt nếu quá dài (tránh lấy nhiều câu)
                                if len(q_text) > 1000:
                                    # Tìm điểm cắt hợp lý (cuối câu hoặc cuối đoạn)
                                    cut_points = [m.start() for m in re.finditer(r'[\.!?]\s*(?:\n|$)', q_text[:1000])]
                                    if cut_points:
                                        q_text = q_text[:cut_points[-1] + 1]
                                    else:
                                        q_text = q_text[:1000] + "..."
                                
                                temp_blocks[q_num] = q_text
                                
                    except ValueError:
                        continue
                
                # Chọn kết quả tốt nhất
                if temp_blocks and len(temp_blocks) > len(question_blocks):
                    question_blocks = temp_blocks
                    # Nếu đã tìm được đủ nhiều câu, dừng lại
                    if len(question_blocks) >= 10:
                        break
        
        return question_blocks
    
    def _create_fallback_question(self, question_num: int, question_text: str, 
                                correct_answer: str, error: str = None) -> Dict[str, Any]:
        """Tạo câu hỏi fallback khi xử lý thất bại."""
        error_msg = f"[LỖI XỬ LÝ] {error}" if error else "[LỖI XỬ LÝ] Không thể phân tích câu hỏi"
        
        return {
            "so_cau": question_num,
            "cau_hoi": f"{error_msg}\n\nNội dung gốc: {question_text[:200]}...",
            "lua_chon": {
                "A": "Lựa chọn A - Cần xử lý thủ công",
                "B": "Lựa chọn B - Cần xử lý thủ công", 
                "C": "Lựa chọn C - Cần xử lý thủ công",
                "D": "Lựa chọn D - Cần xử lý thủ công"
            },
            "dap_an": correct_answer,
            "do_kho": "can_xu_ly",
            "mon_hoc": "unknown",
            "ghi_chu": f"Lỗi xử lý bởi {self.agent_name} - Cần kiểm tra thủ công"
        }
