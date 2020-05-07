from random import choice


n = 20
rooms = n**2
graph = [set() for i in range(rooms)]
mark = []


def is_cyclic():
	global mark
	mark = [False for v in range(rooms)]
	for v in range(0, rooms):
		if not mark[v] and dfs(v, -1):
			return True
	return False


def dfs(v, prev):
	if mark[v]:
		return True
	mark[v] = True
	for adjacent in graph[v]: 
		if adjacent != prev and dfs(adjacent, v):
			return True
	return False


def random_room():
	return choice(range(0, rooms))


def random_neighbor(v):
	neighbors = []
	if v % n != 0:
		neighbors.append(v - 1)
	if v % n != n - 1:
		neighbors.append(v + 1)
	if v // n != 0:
		neighbors.append(v - n)
	if v // n != n - 1:
		neighbors.append(v + n)
	return choice(neighbors)


def add_edge():
	while True:
		v = random_room()
		u = random_neighbor(v)
		if u in graph[v]:
			continue
		graph[v].add(u)
		graph[u].add(v)
		if not is_cyclic():
			break
		graph[v].discard(u)
		graph[u].discard(v)


def build_maze():
	for i in range(rooms - 1):
		add_edge()


def get_room(i, j):
	return (i // 2 - 1) * n + (j // 2 - 1)


def to_string():
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


build_maze()
to_string()


def shift():
	v = random_room()
	u = random_neighbor(v)
	graph[v].discard(u)
	graph[u].discard(v)
	add_edge()


def burn():
	t = 1000