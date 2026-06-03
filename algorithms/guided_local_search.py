from utils.math_utils import randomTour, totalDistance, twoOptSwap


def guidedLocalSearch(dist, max_iter=500, lambda_factor=0.4):
    """
    Guided Local Search cho TSP (dùng 2-opt, phạt cạnh dài).

    Tham số:
        dist: ma trận khoảng cách
        max_iter: số lần gọi Local Search
        lambda_factor: hệ số điều chỉnh lambda
    Trả về:
        (best_tour, best_cost)
    """
    n = len(dist)
    # Ma trận phạt (đối xứng)
    penalty = [[0] * n for _ in range(n)]

    # Tính lambda ≈ a * avg_edge
    sum_edge = sum(dist[i][j] for i in range(n) for j in range(i + 1, n))
    avg_edge = sum_edge / (n * (n - 1) / 2)
    lam = lambda_factor * avg_edge       # λ = a * (chi phí trung bình cạnh)

    curr_tour = randomTour(n)
    best_tour = curr_tour[:]
    best_cost = totalDistance(best_tour, dist)

    for _ in range(max_iter):
        # Local Search (2-opt) tối ưu hàm augmented cost 
        improved = True
        while improved:
            improved = False
            best_delta_aug = 0
            best_move = None

            for i in range(n):
                for j in range(i + 1, n):
                    a, b = curr_tour[i], curr_tour[(i + 1) % n]
                    c, d = curr_tour[j], curr_tour[(j + 1) % n]

                    # delta chiều dài thật
                    delta = dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]
                    # delta phần phạt: penalty(a,c) + penalty(b,d) - penalty(a,b) - penalty(c,d)
                    delta_pen = (penalty[a][c] + penalty[b][d] -
                                 penalty[a][b] - penalty[c][d])
                    delta_aug = delta + lam * delta_pen

                    if delta_aug < best_delta_aug:
                        best_delta_aug = delta_aug
                        best_move = (i, j)

            if best_move and best_delta_aug < 0:
                i, j = best_move
                curr_tour = twoOptSwap(curr_tour, i, j)
                improved = True

        # Cập nhật best solution
        curr_cost = totalDistance(curr_tour, dist)
        if curr_cost < best_cost:
            best_tour = curr_tour[:]
            best_cost = curr_cost

        # Phạt các cạnh có utility cực đại 
        # Utility của cạnh e = chiều dài / (1 + số lần bị phạt)
        max_utility = -1
        edges_to_pen = []
        for k in range(n):
            u, v = curr_tour[k], curr_tour[(k + 1) % n]
            utility = dist[u][v] / (1 + penalty[u][v])

            if utility > max_utility:
                max_utility = utility
                edges_to_pen = [(u, v)]
            elif abs(utility - max_utility) < 1e-9:
                edges_to_pen.append((u, v))

        for u, v in edges_to_pen:
            penalty[u][v] += 1
            penalty[v][u] += 1

    return best_tour, best_cost