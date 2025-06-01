# QuizForce AI - Hệ Thống Test Đơn Giản

## 🎯 Tổng Quan

Đây là phiên bản test đơn giản của QuizForce AI, được thiết kế đặc biệt cho hệ thống giáo dục Việt Nam với độ tin cậy cao và không phụ thuộc phức tạp.

## ✨ Tính Năng Chính

- ✅ **Agent AI Chuyên Nghiệp**: Xử lý toàn bộ quy trình trong một agent
- ✅ **Xử Lý Đáp Án Thông Minh**: Hỗ trợ văn bản và hình ảnh
- ✅ **Trích Xuất DOCX Nâng Cao**: Thuật toán tối ưu cho tiếng Việt
- ✅ **JSON Export Chuẩn**: Format phù hợp hệ thống giáo dục VN
- ✅ **Giao Diện Thân Thiện**: Thiết kế cho người Việt Nam
- ✅ **Làm Bài Kiểm Tra Trực Tuyến**: Hệ thống làm bài chuyên nghiệp ⭐ MỚI
- ✅ **Chấm Điểm Tự Động**: Thống kê chi tiết kết quả ⭐ MỚI
- ✅ **Ít Phụ Thuộc**: Chỉ những package cần thiết

## 🛠️ Yêu Cầu Hệ Thống

```bash
pip install streamlit google-generativeai python-docx pillow python-dotenv
```

## 🚀 Cách Sử Dụng

### Phương pháp 1: Ứng dụng tích hợp (Khuyên dùng)
```bash
cd test
python run_simple_test.py
# Hoặc
cd test/ui
streamlit run simple_app.py --server.port 8502
```

**Tính năng có sẵn:**
- 🎯 Tạo Quiz (tab 1)
- 📝 Làm Bài Kiểm Tra (tab 2) ⭐ MỚI
- 📊 Thống Kê (tab 3) ⭐ MỚI

### Phương pháp 2: Chạy riêng làm bài kiểm tra
```bash
cd test
python run_quiz_test.py
# Hoặc
cd test/ui
streamlit run quiz_test_interface.py --server.port 8503
```

## 🎯 Quy Trình Sử Dụng Hoàn Chỉnh

### Bước 1: Tạo Quiz
1. Chuẩn bị đáp án (văn bản hoặc ảnh)
2. Upload file DOCX chứa câu hỏi
3. Nhấn "Tạo Quiz Thông Minh"
4. Tải xuống file JSON

### Bước 2: Làm Bài Kiểm Tra ⭐ MỚI
1. **Chuyển tab "📝 Làm Bài Kiểm Tra"**
2. Nhập thông tin học sinh
3. Chọn nguồn câu hỏi:
   - Upload file JSON
   - Hoặc sử dụng quiz vừa tạo
4. Cấu hình bài kiểm tra:
   - Thời gian làm bài: 15-120 phút
   - Trộn thứ tự câu hỏi
   - Trộn thứ tự đáp án
5. Bắt đầu làm bài

### Bước 3: Xem Kết Quả ⭐ MỚI
- Điểm số tự động (thang 10)
- Phân tích chi tiết từng câu
- Thống kê thời gian
- Export kết quả JSON

## ⚙️ Cấu Hình

### 1. Thiết lập API Key

Tạo file `.env` trong thư mục gốc:
```env
GOOGLE_API_KEY=api_key_cua_ban_o_day
```

Hoặc nhập trực tiếp trong giao diện ứng dụng.

### 2. Lấy Google Gemini API Key

1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Đăng nhập tài khoản Google
3. Tạo API key mới
4. Copy và lưu vào `.env` hoặc nhập vào app

## 📝 Định Dạng Dữ Liệu Đầu Vào

### Đáp Án (Văn Bản)
```
1. A
2. B
3. AC
4. D
5. BD
```

### Đáp Án (Hình Ảnh)
- Hỗ trợ: PNG, JPG, JPEG, WEBP
- AI sẽ tự động đọc và trích xuất đáp án

### Câu Hỏi (File DOCX)
- File Word chứa câu hỏi định dạng: "Câu 1.", "Question 1:", hoặc "1."
- Mỗi câu hỏi có 4 lựa chọn A, B, C, D
- Hỗ trợ tiếng Việt với dấu

## 📊 Kết Quả Đầu Ra

### Format JSON Chuẩn
```json
{
  "so_cau": 1,
  "cau_hoi": "Nội dung câu hỏi",
  "lua_chon": {
    "A": "Lựa chọn A",
    "B": "Lựa chọn B", 
    "C": "Lựa chọn C",
    "D": "Lựa chọn D"
  },
  "dap_an": "A",
  "do_kho": "trung_binh",
  "mon_hoc": "auto_detect",
  "ghi_chu": "Được xử lý bởi QuizMaster AI"
}
```

### Thống Kê Kèm Theo
- Số lượng câu hỏi được xử lý
- Tỷ lệ thành công
- Thời gian xử lý
- Thông tin debug chi tiết

## 🎯 Đặc Điểm Kỹ Thuật

### Agent AI QuizMaster
- **Model**: Google Gemini 2.0 Flash
- **Chuyên môn**: Hệ thống giáo dục Việt Nam
- **Khả năng**: OCR, NLP, JSON parsing
- **Tối ưu**: Xử lý tiếng Việt có dấu

### Giới Hạn Hiện Tại
- Chỉ sử dụng Gemini 2.0 Flash model
- Không có xử lý lỗi phức tạp
- Không có tính năng nâng cao như profiles, SK
- Rate limiting cơ bản (0.3s delay giữa các câu)

## 🔧 Xử Lý Sự Cố

### 1. Lỗi API Key
**Triệu chứng**: "API key is required"  
**Giải pháp**: Kiểm tra API key Google Gemini có hiệu lực và đủ quota

### 2. Không Tìm Thấy Câu Hỏi
**Triệu chứng**: "Không thể trích xuất câu hỏi"  
**Giải pháp**: Kiểm tra format DOCX - câu hỏi phải bắt đầu bằng "Câu X." hoặc "X."

### 3. Không Parse Được Đáp Án
**Triệu chứng**: "Không thể phân tích đáp án"  
**Giải pháp**: Kiểm tra format đáp án - phải là "số. chữ_cái"

### 4. Không Có Câu Nào Khớp ⭐ MỚI
**Triệu chứng**: "Không có câu nào khớp giữa đáp án và câu hỏi"  
**Nguyên nhân**: Số thứ tự câu hỏi và đáp án không giống nhau  
**Giải pháp**:
1. **Kiểm tra số thứ tự**: Đảm bảo đáp án và câu hỏi có cùng số thứ tự
   - Đáp án: `1. A, 2. B, 3. C`
   - Câu hỏi: `Câu 1., Câu 2., Câu 3.` hoặc `1., 2., 3.`

2. **Xem thông tin Debug**: App sẽ hiển thị:
   - Số câu đáp án tìm thấy: `[1, 2, 3, 4, 5]`
   - Số câu hỏi tìm thấy: `[1, 2, 3, 4, 5]`

3. **Mapping tự động**: Hệ thống có 3 chiến lược tự động:
   - Mapping 1-1 theo thứ tự
   - Mapping theo offset (nếu số bắt đầu khác nhau)
   - Mapping gần nhất

4. **Ví dụ sửa lỗi**:
   ```
   # Sai - Số không khớp
   Đáp án: 1. A, 2. B, 3. C
   DOCX: Question 5., Question 6., Question 7.
   
   # Đúng - Số khớp
   Đáp án: 1. A, 2. B, 3. C  
   DOCX: Câu 1., Câu 2., Câu 3.
   
   # Hoặc mapping tự động
   Đáp án: 1. A, 2. B, 3. C
   DOCX: Câu 5., Câu 6., Câu 7. (offset +4)
   ```

### 5. Rate Limit
**Triệu chứng**: Lỗi quota exceeded  
**Giải pháp**: App đã có delay 0.3s, có thể tăng lên nếu cần

### 6. Các Lỗi Format Thường Gặp ⭐ MỚI
**Đáp án không đúng format**:
```
❌ Sai: "Câu 1: A", "1 - A", "1.A"
✅ Đúng: "1. A", "1) A", "1: A"
```

**Câu hỏi không đúng format**:
```
❌ Sai: "Question A:", "Bài tập 1", "I. "
✅ Đúng: "Câu 1.", "Question 1.", "1.", "1)"
```

## 💡 Mẹo Debug Nhanh

1. **Kiểm tra thông tin Debug**: Luôn mở phần debug để xem số thứ tự
2. **Test với ít câu**: Thử 3-5 câu trước, sau đó mở rộng
3. **Copy format mẫu**: Sử dụng format đã test thành công
4. **Kiểm tra Unicode**: Đảm bảo file DOCX không có ký tự lạ

## 📁 Cấu Trúc Thư Mục

```
test/
├── backend/
│   ├── simple_agent.py           # Agent AI tạo quiz
│   └── quiz_test_engine.py       # Engine làm bài kiểm tra ⭐ MỚI
├── ui/
│   ├── simple_app.py             # Ứng dụng chính tích hợp
│   └── quiz_test_interface.py    # Giao diện làm bài riêng ⭐ MỚI
├── run_simple_test.py            # Script chạy app chính
├── run_quiz_test.py              # Script chạy làm bài riêng ⭐ MỚI
└── README.md                     # File này
```

## 🌟 Tính Năng Làm Bài Kiểm Tra ⭐ MỚI

### Đặc Điểm Nổi Bật
- **Giao diện chuyên nghiệp**: Thiết kế như phần mềm thi thật
- **Quản lý thời gian**: Đếm ngược real-time, cảnh báo
- **Điều hướng linh hoạt**: Quay lại câu đã làm, nhảy câu
- **Chống gian lận cơ bản**: Trộn câu hỏi và đáp án
- **Chấm điểm tự động**: Kết quả ngay lập tức
- **Thống kê chi tiết**: Phân tích từng câu, thời gian

### Các Chế Độ Sử Dụng
1. **Kiểm tra chính thức**: Upload JSON, thời gian cố định
2. **Luyện tập**: Sử dụng quiz vừa tạo, thời gian linh hoạt
3. **Demo**: Test với vài câu để làm quen

### Hỗ Trợ Đa Dạng
- **Thời gian**: 15 phút đến 2 giờ
- **Số câu**: Không giới hạn (khuyến nghị dưới 100 câu)
- **Độ khó**: Tự động phân loại từ quiz
- **Môn học**: Hỗ trợ tất cả môn phổ thông

## 🎓 Hướng Dẫn Cho Giáo Viên

### Quy Trình Tạo Quiz
1. **Chuẩn bị đáp án**: Viết hoặc chụp ảnh đáp án
2. **Soạn file Word**: Tạo file DOCX chứa câu hỏi
3. **Upload và xử lý**: Sử dụng app để tạo quiz
4. **Kiểm tra kết quả**: Xem preview và tải file JSON
5. **Import vào hệ thống**: Sử dụng file JSON trong LMS

### Quy Trình Tổ Chức Kiểm Tra ⭐ MỚI
1. **Tạo quiz**: Theo quy trình trên
2. **Cấu hình bài kiểm tra**:
   - Đặt thời gian phù hợp
   - Bật tính năng trộn để chống gian lận
3. **Hướng dẫn học sinh**:
   - Upload file JSON hoặc làm ngay sau khi tạo quiz
   - Nhập đầy đủ thông tin
4. **Theo dõi kết quả**: Xem thống kê tại tab "📊 Thống Kê"

### Mẹo Sử Dụng Hiệu Quả
- ✅ Đặt tên câu hỏi rõ ràng: "Câu 1.", "Câu 2."
- ✅ Mỗi câu 4 lựa chọn A, B, C, D
- ✅ Kiểm tra đáp án trước khi upload
- ✅ File DOCX không quá 50 câu/lần để tối ưu
- ✅ **Test với ít câu trước khi thi chính thức** ⭐ MỚI
- ✅ **Hướng dẫn học sinh làm quen giao diện trước** ⭐ MỚI

## 🤝 Hỗ Trợ

### Liên Hệ Kỹ Thuật
- **Agent**: QuizMaster AI v1.0
- **Chuyên môn**: Hệ thống giáo dục Việt Nam
- **Hỗ trợ**: Tất cả môn học phổ thông

### Báo Lỗi
Nếu gặp vấn đề, vui lòng cung cấp:
1. File DOCX và đáp án mẫu
2. Screenshot lỗi
3. Mô tả chi tiết vấn đề

---

**Phát triển bởi đội ngũ AI Agent chuyên nghiệp cho giáo dục Việt Nam** 🇻🇳
#   v a n a n h  
 