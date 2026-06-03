# TSP-Metaheuristics: Giải bài toán Người giao hàng bằng Tabu Search, Simulated Annealing và Guided Local Search

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Dự án này cài đặt ba thuật toán metaheuristic kinh điển để giải **bài toán Người giao hàng đối xứng (Symmetric Traveling Salesman Problem - TSP)**:

- **Tabu Search (TS)**
- **Simulated Annealing (SA)**
- **Guided Local Search (GLS)**

Các thuật toán đều sử dụng phép biến đổi **2-opt** để sinh lân cận và được đánh giá trên các bộ dữ liệu chuẩn từ TSPLIB.

---

## Mục lục

- [Mô hình bài toán TSP](#mô-hình-bài-toán-tsp)
- [Toán tử 2-opt](#toán-tử-2-opt)
- [Các thuật toán](#các-thuật-toán)
  - [Tabu Search](#1-tabu-search-ts)
  - [Simulated Annealing](#2-simulated-annealing-sa)
  - [Guided Local Search](#3-guided-local-search-gls)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cài đặt và sử dụng](#cài-đặt-và-sử-dụng)
- [Kết quả thực nghiệm](#kết-quả-thực-nghiệm)
- [Giấy phép](#giấy-phép)

---

# Mô hình bài toán TSP

Cho tập thành phố:

```math
N=\{1,2,\dots,n\}
```

và ma trận khoảng cách đối xứng:

```math
D=[d_{ij}]
```

thỏa mãn:

```math
d_{ij}=d_{ji}\ge 0,\qquad d_{ii}=0
```

Một hành trình (tour) được biểu diễn bởi hoán vị vòng:

```math
\pi=(\pi_1,\pi_2,\dots,\pi_n)
```

với:

```math
\pi_{n+1}=\pi_1
```

Tổng chiều dài hành trình là:

```math
f(\pi)=\sum_{k=1}^{n}d_{\pi_k,\pi_{k+1}}
```

Mục tiêu của bài toán là tìm hành trình tối ưu:

```math
\pi^*=\arg\min_{\pi\in\Pi_N}f(\pi)
```

trong đó:

```math
\Pi_N
```

là tập tất cả các hành trình hợp lệ.

---

# Toán tử 2-opt

2-opt là phép biến đổi phổ biến trong các thuật toán tìm kiếm cục bộ cho TSP.

Cho hai vị trí:

```math
1\le i<j\le n
```

toán tử 2-opt:

1. Loại bỏ hai cạnh:

```math
(\pi_i,\pi_{i+1})
```

và

```math
(\pi_j,\pi_{j+1})
```

2. Thêm hai cạnh mới:

```math
(\pi_i,\pi_j)
```

và

```math
(\pi_{i+1},\pi_{j+1})
```

3. Đảo ngược đoạn nằm giữa hai vị trí.

Độ thay đổi chi phí được tính nhanh bởi:

```math
\Delta=
d_{\pi_i,\pi_j}
+d_{\pi_{i+1},\pi_{j+1}}
-d_{\pi_i,\pi_{i+1}}
-d_{\pi_j,\pi_{j+1}}
```

Nếu:

```math
\Delta<0
```

thì hành trình mới tốt hơn hành trình hiện tại.

---

# Các thuật toán

## 1. Tabu Search (TS)

Tabu Search là phương pháp tìm kiếm cục bộ có sử dụng bộ nhớ ngắn hạn nhằm tránh quay lại các trạng thái đã thăm và thoát khỏi cực trị địa phương.

Gọi:

```math
N(\pi)
```

là tập lân cận của lời giải hiện tại.

Thuật toán duy trì một danh sách cấm:

```math
\mathcal T
```

chứa các cặp cạnh vừa bị loại bỏ trong những bước gần đây.

Mỗi bước di chuyển được xác định bởi cặp chỉ số:

```math
(i,j)
```

và có độ thay đổi chi phí:

```math
\Delta(i,j)
```

Thuật toán chọn bước tốt nhất không nằm trong danh sách tabu.

Một bước tabu vẫn có thể được chấp nhận nếu thỏa mãn tiêu chuẩn khát vọng:

```math
f(\pi)+\Delta(m)<f(\pi^*)
```

trong đó:

```math
\pi^*
```

là lời giải tốt nhất đã tìm được.

### Tham số sử dụng

| Tham số | Giá trị |
|----------|----------|
| max_iter | 800 |
| tabu_tenure | 20 |

---

## 2. Simulated Annealing (SA)

Simulated Annealing mô phỏng quá trình ủ kim loại trong vật lý.

Cho:

```math
\Delta=f(\pi')-f(\pi)
```

là độ thay đổi chi phí khi chuyển từ lời giải hiện tại sang lời giải mới.

Xác suất chấp nhận bước di chuyển được xác định bởi quy tắc Metropolis:

```math
P(\text{accept})=
\begin{cases}
1,&\Delta\le0\\
\exp(-\Delta/T),&\Delta>0
\end{cases}
```

với:

```math
T
```

là nhiệt độ hiện tại.

Lịch giảm nhiệt sử dụng mô hình hình học:

```math
T_{k+1}=\alpha T_k
```

với:

```math
0<\alpha<1
```

Thuật toán dừng khi:

```math
T<T_{\mathrm{final}}
```

### Tham số sử dụng

| Tham số | Giá trị |
|----------|----------|
| init_temp | 2000 |
| final_temp | 0.1 |
| cooling_rate | 0.999 |
| inner_iter | 150 |

---

## 3. Guided Local Search (GLS)

Guided Local Search mở rộng hàm mục tiêu bằng cách đưa thêm các khoản phạt nhằm định hướng quá trình tìm kiếm.

Mỗi cạnh:

```math
e=(u,v)
```

được gán một giá trị phạt:

```math
p_e
```

ban đầu bằng 0.

Hàm mục tiêu mở rộng:

```math
h(\pi)=f(\pi)+\lambda\sum_{e\in\pi}p_e
```

Khi tìm kiếm rơi vào cực trị địa phương của:

```math
h(\pi)
```

thuật toán tính utility của từng cạnh:

```math
\operatorname{util}(e)=\frac{d_e}{1+p_e}
```

Các cạnh có utility lớn nhất sẽ bị tăng phạt:

```math
p_e\leftarrow p_e+1
```

Nhờ đó thuật toán có xu hướng loại bỏ các cạnh dài xuất hiện nhiều lần trong các lời giải.

Hệ số phạt được xác định bởi:

```math
\lambda=\text{lambda_factor}\cdot\bar d
```

trong đó:

```math
\bar d=
\frac{\sum_{i<j}d_{ij}}
{\binom{n}{2}}
```

là khoảng cách trung bình giữa các cặp thành phố.

### Tham số sử dụng

| Tham số | Giá trị |
|----------|----------|
| max_iter | 500 |
| lambda_factor | 0.4 |

---

# Cấu trúc dự án

```text
.
├── main.py
├── algorithms/
│   ├── tabu_search.py
│   ├── simulated_annealing.py
│   └── guided_local_search.py
├── utils/
│   ├── math_utils.py
│   └── data_loader.py
└── data/
```

| Tệp | Chức năng |
|------|-----------|
| main.py | Chạy thực nghiệm và tổng hợp kết quả |
| tabu_search.py | Cài đặt Tabu Search |
| simulated_annealing.py | Cài đặt Simulated Annealing |
| guided_local_search.py | Cài đặt Guided Local Search |
| math_utils.py | Các hàm xử lý tour và 2-opt |
| data_loader.py | Đọc dữ liệu TSPLIB (EUC_2D) |

---

# Cài đặt và sử dụng

## Yêu cầu

- Python 3.10 trở lên
- Không sử dụng thư viện ngoài

## Tải mã nguồn

```bash
git clone https://github.com/yourusername/TSP-Metaheuristics.git
cd TSP-Metaheuristics
```

## Chạy chương trình

```bash
python main.py
```

Đảm bảo các tệp `.tsp` được đặt trong thư mục `data/`.

## Tùy chỉnh

Có thể thay đổi:

- Danh sách bộ dữ liệu
- Số lần chạy (`NUM_RUNS`)
- Các tham số thuật toán

trực tiếp trong mã nguồn.

---

# Kết quả thực nghiệm

Mỗi thuật toán được chạy độc lập **5 lần** trên 6 bộ dữ liệu chuẩn của TSPLIB.

Sai số được tính theo:

```math
\text{Gap(\%)}=
\frac{\text{Best}-\text{Optimal}}
{\text{Optimal}}
\times100
```

| Instance | Optimal | TS Best | SA Best | GLS Best | TS Avg (Std) | SA Avg (Std) | GLS Avg (Std) | TS Gap | SA Gap | GLS Gap |
|----------|---------|---------|---------|----------|--------------|--------------|---------------|--------|--------|---------|
| eil51 | 426 | 442 | 430 | 428 | 456.4 (10.2) | 435.2 (4.4) | 429.6 (1.1) | 3.76% | 0.94% | 0.47% |
| st70 | 675 | 694 | **675** | 679 | 716.0 (23.4) | 682.6 (4.6) | 680.4 (0.9) | 2.81% | **0.00%** | 0.59% |
| kroA100 | 21282 | 22479 | 21346 | 21424 | 23224.2 (727) | 21465.8 (94.7) | 21523.4 (88.2) | 5.62% | 0.30% | 0.67% |
| pr144 | 58537 | 59168 | **58554** | 59356 | 59619.0 (451) | 58690.0 (102) | 59832.8 (425) | 1.08% | **0.03%** | 1.40% |
| d198 | 15780 | 16306 | 16139 | 16197 | 16450.0 (172) | 16235.8 (62.3) | 16293.2 (82.5) | 3.33% | 2.28% | 2.64% |
| lin318 | 42029 | 44415 | 44267 | 44418 | 44950.4 (746) | 44919.4 (586) | 44810.2 (311) | 5.68% | 5.32% | 5.68% |

**Giá trị in đậm là kết quả tốt nhất trên từng bộ dữ liệu.**

---

# Giấy phép

Dự án được phát hành theo giấy phép MIT.

Xem tệp `LICENSE` để biết thêm chi tiết.
