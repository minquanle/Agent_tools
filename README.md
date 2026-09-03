# Agent Tool Calling Demo

Đây là mã nguồn thực hành đi kèm với bài hướng dẫn **"Tạo Agent biết dùng công cụ (Tool Calling)"**.

Mã nguồn này minh họa cơ chế hoạt động của một mô hình ngôn ngữ lớn (LLM) khi được trang bị công cụ (Tool Calling). Sử dụng thư viện LangChain và mô hình Google Gemini, hệ thống cho phép LLM đóng vai trò "bộ não" điều phối, quyết định khi nào cần gọi công cụ (ví dụ: máy tính toán học, bộ đếm từ), và sau đó tự động tổng hợp kết quả để trả lời người dùng.

## Cấu trúc thư mục
- `agent_tools.py`: Chứa mã nguồn chính bao gồm việc định nghĩa các công cụ bằng decorator `@tool`, khởi tạo mô hình Gemini, và xây dựng vòng lặp điều phối (Orchestration Loop) để gọi công cụ.
- `.env.example`: Mẫu cấu hình biến môi trường chứa khóa API.
- `requirements.txt`: Danh sách các thư viện cần thiết.

## Hướng dẫn chạy Demo

**Bước 1: Thiết lập môi trường**

Cài đặt các thư viện trực tiếp thông qua pip:
```bash
py -3.11 -m pip install -r requirements.txt
```
*(Lưu ý: Bạn cũng có thể tạo môi trường ảo venv trước khi cài đặt nếu muốn tránh xung đột với các dự án khác).*

**Bước 2: Thiết lập API Key**
- Copy file `.env.example` thành `.env`
- Mở file `.env` và điền khóa API của Google Gemini vào:
```
GOOGLE_API_KEY=AIzaSy_Ghi_Khoa_API_Cua_Ban_Vao_Day
```

**Bước 3: Chạy ứng dụng**
Mở terminal và chạy lệnh:
```bash
python agent_tools.py
```
*(Chương trình sẽ mở ra dấu nhắc lệnh để bạn có thể chat trực tiếp với Agent và liên tục hỏi đáp các câu hỏi tuỳ ý. Gõ `exit` hoặc `quit` để thoát.)*
