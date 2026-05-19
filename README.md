# 🤖 Dự Án Caro AI (Gomoku-Style AI Engine)

## 🌟 1. Luật chơi

- **Kích thước bàn cờ:** Mặc định là **9x9** (có thể cấu hình linh hoạt trong `config.py` hoặc nhập thủ công lúc khởi chạy).
- **Điều kiện thắng (Win Condition):** Có **4 hoặc nhiều hơn** quân cờ liên tiếp theo hàng dọc, hàng ngang hoặc hai đường chéo.

## 🛠️ 2. Cách Cài Đặt Môi Trường

Để cài đặt dự án và cấu hình môi trường chạy trên máy tính của bạn (đặc biệt hỗ trợ tốt trên môi trường Windows/macOS/Linux), vui lòng làm theo các bước chi tiết sau:

### Bước 1: Chuẩn bị phiên bản Python
Đảm bảo máy tính của bạn đã được cài đặt **Python phiên bản 3.8 trở lên**.

### Bước 2: Tải/Di chuyển vào thư mục dự án
Mở terminal (PowerShell / Command Prompt trên Windows hoặc Terminal trên macOS/Linux) và di chuyển vào thư mục gốc của dự án: 24020220_23020024_23020646_CaroAI

### Bước 3: Khởi tạo môi trường ảo (Virtual Environment - Khuyến nghị)
Việc tạo môi trường ảo giúp cô lập các thư viện của dự án, tránh xung đột hệ thống:
```powershell
python -m venv venv
```

### Bước 4: Kích hoạt môi trường ảo
Tùy thuộc vào hệ điều hành và shell bạn đang sử dụng:
- **Trên Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\activate
  ```
- **Trên Windows (Command Prompt - cmd):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Trên macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### Bước 5: Cài đặt các thư viện
Cài đặt toàn bộ các thư viện được liệt kê trong file `requirements.txt` bằng công cụ quản lý gói `pip`:
```powershell
pip install -r requirements.txt
```

## 🚀 3. Chạy Chương Trình


```powershell
python -m source_code.main
```

Chương trình sẽ hiển thị Menu chính như sau:
```text
=======================================================
  CARO AI  –  Main Menu
=======================================================
  1  Level 1 – Play vs Minimax
  2  Level 2 – Play vs Alpha-Beta (+ compare option)
  3  Level 3 – Run experiments & generate report
=======================================================
  Your choice (1 / 2 / 3): 
```


## 📂 4. Cấu Trúc Dự Án

Dưới đây là sơ đồ cấu trúc thư mục chi tiết của dự án, giải thích chức năng cụ thể của từng tệp tin giúp bạn dễ dàng nắm bắt kiến trúc mã nguồn:

```text
24020220_23020024_23020646_CaroAI/
├── results/
│   └── experiment_results.csv     # File CSV lưu kết quả thực nghiệm tự động của Level 3
├── source_code/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── base_ai.py             # Lớp cơ sở trừu tượng BaseAI và định nghĩa cấu trúc kết quả SearchResult
│   │   ├── minimax.py             # Thuật toán tìm kiếm Minimax giới hạn độ sâu (Depth-limited)
│   │   ├── alphabeta.py           # Thuật toán tìm kiếm Alpha-Beta Pruning (Cắt tỉa Alpha-Beta)
│   │   ├── evaluation.py          # Hàm lượng hóa heuristic, quét bàn cờ đánh giá điểm các nước đi công/thủ
│   │   └── move_ordering.py       # Sắp xếp thứ tự nước đi ứng viên để gia tăng tỷ lệ cắt tỉa của Alpha-Beta
│   │
│   ├── game/
│   │   ├── __init__.py
│   │   ├── board.py               # Biểu diễn ma trận bàn cờ, kiểm tra ô trống, tính số quân cờ hiện tại
│   │   ├── rules.py               # Chứa các quy định chiến thắng (Win/Draw) dựa trên số quân liên tiếp
│   │   ├── game_state.py          # Quản lý lượt đi hiện tại, lịch sử nước đi, nhân bản (clone) trạng thái cờ
│   │   └── move_generator.py      # Tạo danh sách nước đi ứng viên trong phạm vi MAX_CANDIDATE_DISTANCE
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── console_ui.py          # Giao diện dòng lệnh vẽ bàn cờ ký tự và nhận tọa độ nước đi từ người chơi
│   │   └── pygame_ui.py           # Giao diện đồ họa sinh động viết bằng PyGame (vẽ X/O, nhận click chuột, hiển thị số nút duyệt)
│   │
│   ├── benchmark/
│   │   ├── __init__.py
│   │   ├── benchmark_runner.py    # Bộ công cụ chạy benchmark độc lập so sánh nhanh hai thuật toán
│   │   ├── test_states.py         # Định nghĩa 6 kịch bản thử nghiệm bàn cờ mẫu phục vụ so sánh khách quan
│   │   └── metrics.py             # Trình quản lý kết quả thực nghiệm, in bảng tabulate và kết xuất dữ liệu CSV
│   │
│   ├── levels/
│   │   ├── __init__.py
│   │   ├── ask_level.py           # Tiện ích hỏi người chơi về kích thước bàn cờ và độ sâu mong muốn
│   │   ├── level_1.py             # Trình khởi chạy trò chơi Level 1 (Human vs Minimax)
│   │   ├── level_2.py             # Trình khởi chạy Level 2 (Human vs Alpha-Beta và Compare Mode song song)
│   │   └── level_3.py             # Trình khởi chạy Level 3 (Kích hoạt bộ chạy thực nghiệm tự động)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── timer.py               # Context Manager và Decorator hỗ trợ đo đếm chính xác thời gian thực thi (wall-clock)
│   │
│   ├── config.py                  # Tệp cấu hình tập trung chứa hằng số (kích thước bàn, luật thắng, độ sâu mặc định)
│   ├── experiments.py             # Mã nguồn cốt lõi Level 3 thực hiện chạy scenarios × depths, lưu trữ CSV & in Automatic Analysis
│   └── main.py                    # Điểm xuất phát của toàn bộ ứng dụng, quản lý Menu chính 3 cấp độ
│
├── requirements.txt               # Danh sách các thư viện Python cần thiết cài đặt (pygame, tabulate, pytest)
└── README.md                      # Tệp tài liệu hướng dẫn sử dụng này
```

Chúc bạn có những giây phút đấu trí kịch tính và thú vị cùng với Caro AI! Nếu bạn muốn đóng góp cải tiến thuật toán hoặc giao diện đồ họa, hãy thoải mái thực hiện Pull Request hoặc thảo luận cùng nhóm phát triển.