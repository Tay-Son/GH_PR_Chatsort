

def worker(id, number, q):
    increased_number = 0

    for _ in range(number):
        increased_number += 1

    # 결과를 q에 저장
    q.put(increased_number)
    return





