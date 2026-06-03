import math
import random
from utils.math_utils import randomTour, totalDistance, twoOptSwap


def simulatedAnnealing(dist, init_temp=2000, final_temp=0.1,
                       cooling_rate=0.999, inner_iter=150):
    """
    Simulated Annealing cho TSP với lân cận 2-opt.

    Tham số:
        dist: ma trận khoảng cách
        init_temp: nhiệt độ khởi tạo
        final_temp: nhiệt độ kết thúc
        cooling_rate: hệ số làm lạnh (alpha)
        inner_iter: số bước lặp trong mỗi mức nhiệt
    Trả về:
        (best_tour, best_cost)
    """
    n = len(dist)
    curr_tour = randomTour(n)
    best_tour = curr_tour[:]
    best_cost = totalDistance(best_tour, dist)
    temp = init_temp

    while temp > final_temp:
        for _ in range(inner_iter):
            # Chọn ngẫu nhiên i, j để thực hiện 2-opt
            i = random.randint(0, n - 2)        
            j = random.randint(i + 1, n - 1)    
            nei_tour = twoOptSwap(curr_tour, i, j)

            delta = totalDistance(nei_tour, dist) - totalDistance(curr_tour, dist)

            # Tiêu chí chấp nhận Metropolis
            if delta < 0 or random.random() < math.exp(-delta / temp):
                curr_tour = nei_tour
                curr_cost = totalDistance(curr_tour, dist)
                if curr_cost < best_cost:
                    best_tour = curr_tour[:]
                    best_cost = curr_cost

        # Giảm nhiệt độ theo lịch làm lạnh hình học
        temp *= cooling_rate

    return best_tour, best_cost