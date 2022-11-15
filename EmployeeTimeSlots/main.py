# def get_n_fib(position: int):
#     if position < 1:
#         return None
#
#     fib_lst = [0, 1]
#
#     while position > len(fib_lst):
#         fib_lst.append(fib_lst[-1] + fib_lst[-2])
#
#     return fib_lst[position - 1]

"""
Вот что я имел в виду, как можно к примеру улучшить поиск определенного числа Фибаначчи.
Список не нужно создавать и хранить не нужные значения.
По оперативной памяти так будет лучше
"""


def get_n_fib(position: int):
    if position < 1:
        return None

    if position == 1:
        return 0

    if position == 2:
        return 1

    pos1, pos2 = 0, 1
    cnt = 2

    while position > cnt:
        pos1, pos2 = pos2, pos1 + pos2
        cnt += 1

    return pos2


assert get_n_fib(0) is None
assert get_n_fib(1) == 0
assert get_n_fib(2) == 1
assert get_n_fib(3) == 1
assert get_n_fib(4) == 2
assert get_n_fib(5) == 3

assert get_n_fib(44) == 433494437
assert get_n_fib(77) == 3416454622906707
