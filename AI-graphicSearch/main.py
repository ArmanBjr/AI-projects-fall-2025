from datetime import datetime

from Board import Board
from Problem import Problem
from Solution import Solution
from State import State
from Search import Search
import ast

if __name__ == '__main__':

    # config base on your system and task
    test_case_number = 1

    test_path = f'./tests/{test_case_number}.txt'
    start_time = datetime.now()
    file = open(test_path, 'r')
    p = ''
    for i in file.readlines():
        a = i.replace('\n', '')
        a = a.replace(' ', '')
        p += a
    lst = ast.literal_eval(p)
    s = Search.dfs_by_explore(
        Problem(State(Board(len(lst), len(lst[0]), lst), None, 0, None, None)))
    if s is None:
        s = Solution(None, None, start_time)
    s.print_path()