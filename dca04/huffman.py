import heapq


def huffman(symbol_probability_list):
    queue = [(prob, [(symbol, [])]) for symbol, prob in symbol_probability_list]
    if len(queue) < 2:
        raise ValueError("At least two elements must be passed for encoding")
    heapq.heapify(queue)
    while len(queue) >= 2:
        first = heapq.heappop(queue)
        second = heapq.heappop(queue)
        prob_sum = first[0] + second[0]
        for _, code in first[1]:
            code.append('1')
        for _, code in second[1]:
            code.append('0')
        heapq.heappush(queue, (prob_sum, first[1] + second[1]))
    return {symbol: "".join(reversed(code)) for symbol, code in queue[0][1]}


