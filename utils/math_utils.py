import random
# Tổng độ dài tuor
def totalDistance(tour, dist):
    n = len(tour)
    cost = 0
    for i in range(n):
        cost += dist[tour[i-1]][tour[i]]
    return cost
# Hàm 2-opt
def twoOptSwap(tour,i,j):
  rev_tour = tour[:]
  rev_tour[i+1:j+1] = reversed(tour[i+1:j+1])
  return rev_tour

# Khởi tạo tour ngẫu nhiên
def randomTour(n):
  tour = list(range(n))
  random.shuffle(tour)
  return tour