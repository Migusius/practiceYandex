from random import choice, sample, random
from collections import defaultdict, namedtuple
from math import log, exp


n = 50
rooms = n**2
graph = [set() for i in range(rooms)]
mark = []


def is_cyclic(graph):
	global mark
	mark = [False for v in range(rooms)]
	for v in range(0, rooms):
		if not mark[v] and dfs(v, -1, graph):
			return True
	return False


def dfs(v, prev, graph):
	if mark[v]:
		return True
	mark[v] = True
	for adjacent in graph[v]: 
		if adjacent != prev and dfs(adjacent, v, graph):
			return True
	return False


def random_room():
	return choice(range(0, rooms))


def get_neighbors(v):
	neighbors = []
	if v % n != 0:
		neighbors.append(v - 1)
	if v % n != n - 1:
		neighbors.append(v + 1)
	if v // n != 0:
		neighbors.append(v - n)
	if v // n != n - 1:
		neighbors.append(v + n)
	return neighbors


def random_neighbor(v):
	return choice(get_neighbors(v))


def add_edge(graph):
	while True:
		v = random_room()
		u = random_neighbor(v)
		if u in graph[v]:
			continue
		graph[v].add(u)
		graph[u].add(v)
		if not is_cyclic(graph):
			break
		graph[v].discard(u)
		graph[u].discard(v)


def build_maze(graph):
	for i in range(rooms - 1):
		add_edge(graph)


def get_room(i, j):
	return (i // 2 - 1) + (j // 2 - 1) * n


def to_string(graph):
	for i in range(1, 2*n + 2):
		for j in range(1, 2*n + 2):
			if i % 2 == 1:
				if j % 2 == 1:
					c = '+'
				else:
					if i != 2*n + 1 and get_room(i - 1, j) in graph[get_room(i + 1, j)]:
						c = '.'
					else:
						c = '-'
			else:
				if j % 2 == 1:
					if j != 2*n + 1 and get_room(i, j - 1) in graph[get_room(i, j + 1)]:
						c = '.'
					else:
						c = '|'
				else:
					c = '.'
			print(c, end='')
		print()


build_maze(graph)
to_string(graph)

def subgraph_to_frozenset(matrix, index, graph):
	key = set()
	for v in matrix:
		neighbors = set()
		for u in graph[v]:
			neighbors.add(u - index)
		key.add(frozenset(neighbors))
	return frozenset(key)


def rate(graph):
	count = defaultdict(int)
	metric = 0
	for j in range(n - 1):
		for i in range(n - 1):
			index = i + j *n
			subMatrix = [index, index + 1, index + n, index + n + 1]
			count[subgraph_to_frozenset(subMatrix, index, graph)] += 1

	for k in count.values():
		metric += 1 / (abs(20 - k) + 1)
	return metric
	return 1 + log(1 + metric)


start_metric = rate(graph)

def shift(graph):
	v = random_room()
	u = sample(graph[v], 1)[0]
	graph[v].discard(u)
	graph[u].discard(v)
	add_edge(graph)


def transition_probability(diff, t):
	print("prob : ", exp(1000000*diff / t))
	return exp(1000000*diff / t)


def should_keep_changes(p):
	if random() < p:
		return True
	return False


def annealing(graph):
	temp = 100
	eps = 0.0001
	k = 0.995
	times = 200

	prev = graph.copy()
	ans = graph.copy()
	prev_metric = ans_metric = rate(graph)

	for i in range(1, times):
		shift(graph)
		cur_metric = rate(graph)
		print("diff : ", cur_metric - prev_metric)
		if ans_metric < cur_metric:
			ans = graph.copy()
			ans_metric = cur_metric
		if should_keep_changes(transition_probability(cur_metric - prev_metric, temp)):
			prev = graph.copy()
			prev_metric = cur_metric
		else:
			graph = prev.copy()
		temp *= k

	to_string(ans)
	print(start_metric)
	print(ans_metric)
	print("-----")
	print(1 + log(1 + start_metric))
	print(1 + log(1 + ans_metric))

annealing(graph)