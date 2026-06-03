from utils.math_utils import randomTour, totalDistance, twoOptSwap

def tabuSearch(dist, max_iter=800, tabu_tenure=20):
    """
    Tabu Search cho TSP với lân cận 2-opt.

    Tham số:
        dist: ma trận khoảng cách
        max_iter: số vòng lặp tối đa
        tabu_tenure: thời gian cấm (số vòng lặp)
    Trả về:
        (best_tour, best_cost)
    """
    n = len(dist)
    curr_tour = randomTour(n)
    best_tour = curr_tour[:]
    best_cost = totalDistance(best_tour, dist)
    # tabu_list: key = (cặp cạnh bị xóa), value = vòng lặp hết hạn cấm
    tabu_list = {}

    for iter in range(max_iter):
        best_delta = float('inf')
        best_move = None

        # Duyệt toàn bộ lân cận 2-opt
        for i in range(n):
            for j in range(i + 1, n):
                a = curr_tour[i]
                b = curr_tour[(i + 1) % n]
                c = curr_tour[j]
                d = curr_tour[(j + 1) % n]

                # Công thức delta: d(a,c) + d(b,d) - d(a,b) - d(c,d)
                delta = dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]

                # Cặp cạnh bị xóa (sắp xếp để tránh trùng lặp)
                deleted_edge = (
                    (min(a, b), max(a, b)),
                    (min(c, d), max(c, d))
                )

                # Kiểm tra tabu
                is_tabu = (deleted_edge in tabu_list and tabu_list[deleted_edge] > iter)
                # Tiêu chuẩn khát vọng (aspiration)
                meets_aspiration = (totalDistance(curr_tour, dist) + delta < best_cost)

                if (not is_tabu) or meets_aspiration:
                    if delta < best_delta:
                        best_delta = delta
                        best_move = (i, j)

        if best_move is None:
            break

        i, j = best_move
        # Xác định lại các cạnh bị xóa sau khi đã chọn move
        a = curr_tour[i]
        b = curr_tour[(i + 1) % n]
        c = curr_tour[j]
        d = curr_tour[(j + 1) % n]
        deleted_edge = (
            (min(a, b), max(a, b)),
            (min(c, d), max(c, d))
        )
        tabu_list[deleted_edge] = iter + tabu_tenure

        curr_tour = twoOptSwap(curr_tour, i, j)
        curr_cost = totalDistance(curr_tour, dist)

        if curr_cost < best_cost:
            best_tour = curr_tour[:]
            best_cost = curr_cost

    return best_tour, best_cost

