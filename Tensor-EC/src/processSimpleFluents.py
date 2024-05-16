
from src.eventRecognition import *

from time import process_time
from scipy.sparse import linalg as lg
# lg.use_solver(useUmfpack=True, assumeSortedIndices=True)
from itertools import groupby

inf = float('inf')
linear_equation = False


class SimpleFluent(EventRecognition):
	instances = {}

	def __init__(self, fluent_str: tuple, ndim: int):

		self.fluent_str = fluent_str
		self.ndim = ndim

		self.intervals = {}
		self.open_interval = None
		self.matrix = None

		SimpleFluent.instances[fluent_str] = self

	def __getString__(self):

		sym_str = ''
		arg = ()
		if len(self.fluent_str) > 2:
			arg = self.fluent_str[1:-1]

		if not self.intervals:
			indices = groupby(zip(*self.matrix.nonzero()), lambda t: t[0])
			for en_pos, group in indices:
				if self.ndim > 1:
					rem = en_pos
					en_get = ()
					for d in range(self.ndim, 0, -1):
						temp = int(rem / (self.dim1 ** (d - 1)))
						rem = rem - temp * (self.dim1 ** (d - 1))
						en_get += (temp,)
				else:
					en_get = (en_pos,)
				entity = itemgetter(*en_get)(self.inv_map_entities)
				start_i = next(group)[-1]
				temp = start_i
				intervals = []
				for r in group:
					if r[1] - temp == 1:
						temp = r[-1]
					else:
						dist = temp - start_i + 1
						start_i = self.initTime + start_i * self.clock
						end_i = start_i + dist * self.clock
						intervals.append((start_i, end_i))
						start_i = r[1]
						temp = start_i

				dist = temp - start_i + 1
				start_i = self.initTime + start_i * self.clock
				end_i = start_i + dist * self.clock
				if end_i > self.qt + self.clock:
					end_i = inf
				intervals.append((start_i, end_i))
				self.intervals[entity] = intervals

		for i in self.intervals:
			if self.ndim == 1:
				entity = i
			else:
				entity = ()
				for en in i:
					entity += en

			entity = ','.join(entity + arg)

			sym_str += '(%s(%s)=%s, [' % (self.fluent_str[0], entity, self.fluent_str[-1])
			sym_str += ','.join(map(str, self.intervals[i])) + ']).\n'

		return sym_str

	def __execute__(self, definition: dict, linear: bool = False):

		initiations = definition['initiatedAt']()

		if linear:
			if self.open_interval:
				pos = defaultdict()
				for entity in self.open_interval:
					if self.ndim == 1:
						i = self.map_entities[entity]
					else:
						x = itemgetter(*entity)(self.map_entities)
						i = 0
						for d in range(len(x)):
							i += x[d] * (self.dim1 ** (self.ndim - d - 1))
					pos[i, 0] = 1.0

				open_matrix = sp.dok_matrix((self.dim1 ** self.ndim, self.dim2))
				dict.update(open_matrix, pos)
				initiations = initiations + open_matrix.tocsr()

		if initiations.size or self.open_interval:
			if linear:
				terminations = self.termAtQt[self.ndim] + definition['terminatedAt']()
			else:
				terminations = definition['terminatedAt']()
		else:
			if linear:
				terminations = self.termAtQt[self.ndim]
			else:
				terminations = self.empty[self.ndim]

		self.__holdsAtMatrix__(initiations, terminations, linear)

		if not self.matrix.size:
			del SimpleFluent.instances[self.fluent_str]
			del self

	def __holdsAtMatrix__(self, initiations, terminations, linear_method: bool = False):

		if not linear_method:
			if self.ndim == 1:
				holdsAt = np.zeros((self.dim1, self.dim2,))
			else:
				holdsAt = sp.dok_matrix((self.dim1 ** self.ndim, self.dim2))

		self.intervals = {}

		if linear_method:

			initiations[initiations > 1] = 1.0
			terminations[terminations > 1] = 1.0

			if linear_equation:

				shape = ((self.dim1 ** self.ndim) * self.dim2, 1)
				vector_b = ((initiations - initiations.multiply(terminations)) @ self.U)
				vector_b = vector_b.reshape(shape, order='C').A
				vector_t = np.reshape(terminations.A, newshape=(shape[0],), order='C')
				vector_t = -1.0 + vector_t[1:]

				matrix_G = sp.diags([[1.0], vector_t], offsets=[0, -1], shape=(shape[0], shape[0]), format='csc')

				vector_h = lg.spsolve(matrix_G, vector_b, use_umfpack=True)
				
				holdsAt = vector_h.reshape((self.dim1 ** self.ndim, self.dim2), order='C')
				holdsAt[holdsAt > 1.0] = 1.0

			else:

				holdsAt = sp.csr_matrix((self.dim1 ** self.ndim, self.dim2))
				initiations = initiations - initiations.multiply(terminations)

				while initiations.size:
					Su = initiations @ self.upper
					Su[Su > 1] = 1.0
					terminations = terminations.multiply(Su)
					Tu = terminations @ self.upper
					Tu[Tu > 1] = 1.0
					holdsAt = holdsAt + (Su - Tu)
					initiations = initiations.multiply(Tu)

			if self.ndim > 1:

				indices = holdsAt[:, -1].nonzero()[0]
				self.open_interval = []

				for en_pos in indices:
					rem = en_pos
					en_get = ()
					for d in range(self.ndim, 0, -1):
						temp = int(rem / (self.dim1 ** (d - 1)))
						rem = rem - temp * (self.dim1 ** (d - 1))
						en_get += (temp,)
					entity = itemgetter(*en_get)(self.inv_map_entities)
					self.open_interval.append(entity)
			else:
				self.open_interval = [self.inv_map_entities[x] for x in holdsAt[:, -1].nonzero()[0] if x in self.inv_map_entities]

		else:

			s_indices = initiations.nonzero()
			start_points = defaultdict(list)

			if self.open_interval:
				for entity in self.open_interval:
					if self.ndim == 1:
						i = self.map_entities[entity]
					else:
						x = itemgetter(*entity)(self.map_entities)
						i = 0
						for d in range(len(x)):
							i += x[d] * (self.dim1 ** (self.ndim - d - 1))
					start_points[(i,)] = [0]

			self.open_interval = []

			for r in zip(*s_indices):
				start_points[r[0:1]].append(r[-1])

			if start_points:

				t_indices = terminations.nonzero()
				end_points = defaultdict(list)

				for r in zip(*t_indices):
					end_points[r[0:1]].append(r[-1])

				for en_pos in start_points:

					current_start_points = iter(start_points[en_pos])
					current_sp = next(current_start_points)
					if en_pos not in end_points:
						end_points[en_pos] = [self.dim2 - 1]
					else:
						end_points[en_pos] += [self.dim2 - 1]
					current_end_points = iter(end_points[en_pos])
					current_tp = next(current_end_points)

					while current_tp < current_sp:
						current_tp = next(current_end_points)

					if current_sp != current_tp:

						if self.ndim > 1:
							idx = (*en_pos, slice(current_sp + 1, current_tp + 1))
							holdsAt[idx] = 1.0
							rem = en_pos[0]
							en_get = ()
							for d in range(self.ndim, 0, -1):
								temp = int(rem / (self.dim1 ** (d - 1)))
								rem = rem - temp * (self.dim1 ** (d - 1))
								en_get += (temp,)
						else:
							idx = (*en_pos, slice(current_sp + 1, current_tp + 1))
							holdsAt[idx] = 1.0
							en_get = en_pos

						entity = itemgetter(*en_get)(self.inv_map_entities)
						start_i = self.initTime + (current_sp + 1) * self.clock
						end_i = start_i + (current_tp - current_sp) * self.clock
						if end_i > self.qt + self.clock:
							end_i = inf
							self.open_interval.append(entity)
						self.intervals[entity] = [(start_i, end_i)]

					for ip in current_start_points:
						if ip > current_tp:
							while current_tp < ip:
								current_tp = next(current_end_points)
							if ip != current_tp:
								if self.ndim > 1:
									idx = (*en_pos, slice(ip + 1, current_tp + 1))
									holdsAt[idx] = 1.0
									rem = en_pos[0]
									en_get = ()
									for d in range(self.ndim, 0, -1):
										temp = int(rem / (self.dim1 ** (d - 1)))
										rem = rem - temp * (self.dim1 ** (d - 1))
										en_get += (temp,)
								else:
									idx = (*en_pos, slice(ip + 1, current_tp + 1))
									holdsAt[idx] = 1.0
									en_get = en_pos
								entity = itemgetter(*en_get)(self.inv_map_entities)
								start_i = self.initTime + (ip + 1) * self.clock
								end_i = start_i + (current_tp - ip) * self.clock
								if end_i > self.qt + self.clock:
									end_i = inf
									self.open_interval.append(entity)
								if entity not in self.intervals:
									self.intervals[entity] = [(start_i, end_i)]
								else:
									self.intervals[entity].append((start_i, end_i))

		self.matrix = sp.csr_matrix(holdsAt)

	@staticmethod
	def __getHoldsAtMatrix__(fluent: tuple, dim: int = 1, negative: bool = False):

		if fluent in SimpleFluent.instances:

			matrix = SimpleFluent.instances[fluent].matrix

		else:
			matrix = SimpleFluent.empty[dim]

		if negative:
			return SimpleFluent.eye - matrix

		return matrix

	@classmethod
	def __forget__(cls):

		for fluent in cls.instances:
			instance = cls.instances[fluent]
			del instance

		cls.instances = {}

	@classmethod
	def __createNewInstance__(cls, fluent: tuple, dim: int):

		if fluent not in cls.instances:
			SimpleFluent(fluent, dim)

		return cls.instances[fluent]
