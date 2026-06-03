```markdown
# TSP-Metaheuristics: Giải bài toán Người giao hàng bằng Tabu Search, Simulated Annealing và Guided Local Search

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Dự án này cài đặt ba thuật toán metaheuristic kinh điển cho **bài toán người giao hàng đối xứng (Symmetric TSP)**:
- **Tabu Search (TS)**
- **Simulated Annealing (SA)**
- **Guided Local Search (GLS)**

Tất cả đều sử dụng phép hoán đổi **2-opt** và được đánh giá trên các bộ dữ liệu chuẩn từ TSPLIB. Dưới đây trình bày chi tiết mô hình toán học, cài đặt tham số và kết quả thực nghiệm.

## Mục lục
- [Mô hình toán học](#mô-hình-toán-học)
- [Các thuật toán và tham số](#các-thuật-toán-và-tham-số)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cài đặt và thực nghiệm](#cài-đặt-và-thực-nghiệm)
- [Kết quả thực nghiệm](#kết-quả-thực-nghiệm)
- [Giấy phép](#giấy-phép)

## Mô hình toán học

### Bài toán TSP
Cho tập hợp \(N = \{1, 2, \dots, n\}\) thành phố và ma trận khoảng cách đối xứng \(D = [d_{ij}]\) với \(d_{ij} = d_{ji} \ge 0\) và \(d_{ii} = 0\). Một hành trình (tour) là một hoán vị vòng quanh \(\pi = (\pi_1, \pi_2, \dots, \pi_n)\), trong đó \(\pi_{n+1} = \pi_1\). Chiều dài hành trình được xác định bởi:

\[
f(\pi) = \sum_{k=1}^{n} d_{\pi_k, \pi_{k+1}}
\]

Mục tiêu là tìm \(\pi^*\) sao cho:

\[
\pi^* = \arg\min_{\pi \in \Pi_N} f(\pi)
\]

với \(\Pi_N\) là tập tất cả các hoán vị vòng quanh.

### Toán tử 2-opt
Cho hai chỉ số \(i, j\) (\(1 \le i < j \le n\)), toán tử 2-opt đảo ngược đoạn từ \(i+1\) đến \(j\) và thay hai cạnh \((\pi_i, \pi_{i+1})\), \((\pi_j, \pi_{j+1})\) bằng \((\pi_i, \pi_j)\) và \((\pi_{i+1}, \pi_{j+1})\). Sự thay đổi độ dài (delta) được tính:

\[
\Delta = d_{\pi_i, \pi_j} + d_{\pi_{i+1}, \pi_{j+1}} - d_{\pi_i, \pi_{i+1}} - d_{\pi_j, \pi_{j+1}}
\]

Nếu \(\Delta < 0\), hành trình mới ngắn hơn.

## Các thuật toán và tham số

### 1. Tabu Search (TS)
- **Ý tưởng:** Duy trì danh sách cấm (tabu list) các cạnh vừa bị loại bỏ để tránh quay lại. Cho phép chấp nhận bước bị cấm nếu nó tạo ra lời giải tốt hơn lời giải tốt nhất đã biết (tiêu chuẩn khát vọng).
- **Tham số cài đặt:**
  - `max_iter = 800` – số vòng lặp tối đa.
  - `tabu_tenure = 20` – số vòng lặp một bước di chuyển bị cấm.
- **Lân cận:** Duyệt toàn bộ các cặp (i, j) để chọn bước tốt nhất.

### 2. Simulated Annealing (SA)
- **Ý tưởng:** Mô phỏng quá trình ủ kim loại: chấp nhận bước xấu với xác suất \( \exp(-\Delta / T) \) (Metropolis), nhiệt độ giảm dần theo lịch hình học.
- **Tham số cài đặt:**
  - `init_temp = 2000` – nhiệt độ ban đầu.
  - `final_temp = 0.1` – nhiệt độ kết thúc.
  - `cooling_rate = 0.999` – hệ số giảm nhiệt (\(\alpha\)).
  - `inner_iter = 150` – số bước lặp tại mỗi mức nhiệt.
- **Lân cận:** Chọn ngẫu nhiên một cặp (i, j) mỗi bước.

### 3. Guided Local Search (GLS)
- **ý tưởng:** Đưa các khoản phạt (penalty) vào hàm mục tiêu. Mỗi khi rơi vào cực trị địa phương, tăng phạt cho (các) cạnh có **utility** cao nhất: \( \text{util}(e) = \frac{d_e}{1+p_e} \). Hàm mục tiêu mở rộng: \( h(\pi) = f(\pi) + \lambda \sum_{e\in\pi} p_e \).
- **Tham số cài đặt:**
  - `max_iter = 500` – số lần gọi local search.
  - `lambda_factor = 0.4` – hệ số \(\lambda\) được tính bằng \( \lambda = \text{lambda\_factor} \times \text{avg\_edge} \), với avg_edge là độ dài trung bình của tất cả các cạnh trong đồ thị.
- **Lân cận:** Greedy 2-opt tối thiểu hóa hàm \(h(\pi)\).

## Cấu trúc dự án
```
.
├── main.py                  # Chạy thực nghiệm, in bảng kết quả
├── algorithms/
│   ├── tabu_search.py       # Cài đặt TS
│   ├── simulated_annealing.py # Cài đặt SA
│   └── guided_local_search.py # Cài đặt GLS
├── utils/
│   ├── math_utils.py        # totalDistance, twoOptSwap, randomTour
│   └── data_loader.py       # Đọc file TSPLIB (định dạng EUC_2D)
└── data/                    # Thư mục chứa các file .tsp
```

## Cài đặt và thực nghiệm

1. **Yêu cầu:** Python 3.10 trở lên, không cần thư viện ngoài.
2. **Clone dự án:**
   ```bash
   git clone https://github.com/yourusername/TSP-Metaheuristics.git
   cd TSP-Metaheuristics
   ```
3. **Chạy thực nghiệm:**
   ```bash
   python main.py
   ```
   (Đảm bảo các file .tsp nằm trong thư mục `data/` với tên như trong `main.py`)

4. **Tùy chỉnh:** Sửa số lần chạy (`NUM_RUNS`), danh sách instance hoặc tham số thuật toán trực tiếp trong các file tương ứng.

## Kết quả thực nghiệm

Thực hiện **5 lần chạy** cho mỗi thuật toán trên 6 instance TSPLIB. Các chỉ số: **Best** (tốt nhất), **Avg** (trung bình), **Std** (độ lệch chuẩn), **Time(s)** (thời gian trung bình), **Gap(%)** = (Best – Optimal)/Optimal × 100.

| Instance | Optimal | TS Best | SA Best | GLS Best | TS Avg (Std) | SA Avg (Std) | GLS Avg (Std) | TS Gap | SA Gap | GLS Gap |
|----------|---------|---------|---------|----------|--------------|--------------|---------------|--------|--------|---------|
| eil51    | 426     | 442     | 430     | 428      | 456.4 (10.2) | 435.2 (4.4)  | 429.6 (1.1)   | 3.76%  | 0.94%  | 0.47%   |
| st70     | 675     | 694     | **675** | 679      | 716.0 (23.4) | 682.6 (4.6)  | 680.4 (0.9)   | 2.81%  | **0.00%** | 0.59%   |
| kroA100  | 21282   | 22479   | 21346   | 21424    | 23224.2 (727) | 21465.8 (94.7) | 21523.4 (88.2)| 5.62%  | 0.30%  | 0.67%   |
| pr144    | 58537   | 59168   | **58554**| 59356    | 59619.0 (451) | 58690.0 (102) | 59832.8 (425) | 1.08%  | **0.03%** | 1.40%   |
| d198     | 15780   | 16306   | 16139   | 16197    | 16450.0 (172) | 16235.8 (62.3) | 16293.2 (82.5)| 3.33%  | 2.28%  | 2.64%   |
| lin318   | 42029   | 44415   | 44267   | 44418    | 44950.4 (746) | 44919.4 (586) | 44810.2 (311) | 5.68%  | 5.32%  | 5.68%   |

*Ghi chú:* Giá trị **in đậm** là kết quả tốt nhất cho instance đó.

## Giấy phép

Dự án được phân phối theo giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
```