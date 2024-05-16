
from src.eventRecognition import *

inf = float('inf')


class SDFluent(EventRecognition):
	
	def __init__(self, fluent_str: tuple, dim: int):

		self.fluent_str = fluent_str
		self.matrix = None
		self.ndim = dim
		self.intervals = {}

	def __getString__(self):
		sym_str = ''

		for i in self.intervals:
			entity = self.inv_map_entities[i][0]

			sym_str += '(%s(%s)=%s, [' % (self.fluent_str[0], entity, self.fluent_str[-1])
			sym_str += ','.join(map(str, self.intervals[i])) + ']).\n'

		return sym_str
	

class InputSDF(SDFluent):

	instances = {}

	def __init__(self, fluent_str: tuple, index: tuple, interval: tuple, dim: int):

		super().__init__(fluent_str, dim)

		if self.dynamic_grounding:
			EventRecognition.__updateEntities__(index)

		if interval[0] <= self.initTime:
			start_t = 1
		else:
			start_t = int((interval[0] - self.initTime) / self.clock)

		if interval[-1] > self.qt:
			end_t = int((self.qt - self.initTime) / self.clock)
		else:
			end_t = int((interval[-1] - self.initTime) / self.clock)

		pos = range(start_t, end_t)

		x = itemgetter(*index)(self.map_entities)
		self.init_matrix = defaultdict()
		for t in pos:
			self.init_matrix[x, t] = 1.0

		InputSDF.instances[fluent_str] = self

	def __update__(self, index: tuple, interval: tuple):

		if self.dynamic_grounding:
			EventRecognition.__updateEntities__(index)

		if interval[0] <= self.initTime:
			start_t = 1
		else:
			start_t = interval[0] - self.initTime

		if interval[-1] > self.qt:
			end_t = int((self.qt - self.initTime) / self.clock)
		else:
			end_t = int((interval[-1] - self.initTime) / self.clock)

		pos = range(start_t, end_t)

		x = itemgetter(*index)(self.map_entities)
		for t in pos:
			self.init_matrix[x, t] = 1.0

	@staticmethod
	def __getTimeMatrix__(fluent: tuple, dim: int = 1, negative: bool = False):

		if fluent in InputSDF.instances:

			matrix = InputSDF.instances[fluent].matrix

		else:
			matrix = InputSDF.empty[dim]

		if negative:
			return InputSDF.eye - matrix

		return matrix
	
	@classmethod
	def __finalize__(cls):

		for sdf in cls.instances:
			instance = cls.instances[sdf]
			matrix = sp.dok_matrix((cls.dim1 ** instance.ndim, cls.dim2))
			if instance.ndim > 1:
				new_dict = defaultdict()
				for key in instance.init_matrix:
					i = 0
					for d in range(instance.ndim, 0, -1):
						i += key[0][d-1] * (cls.dim1 ** (instance.ndim - d))
					new_key = (i, key[-1])
					new_dict[new_key] = 1.0
				instance.init_matrix = new_dict
			dict.update(matrix, instance.init_matrix)
			instance.matrix = matrix.tocsr()

			del instance.init_matrix

	@classmethod
	def __forget__(cls):

		for sdf in cls.instances:
			instance = cls.instances[sdf]
			del instance

		cls.instances = {}


class ComplexSDF(SDFluent):

	instances = {}

	def __init__(self, fluent_str: tuple):

		super().__init__(fluent_str)
		self.intervals = []

		ComplexSDF.instances[fluent_str] = self

	def __execute__(self, definition):

		self.matrix = definition()

		points = self.matrix.nonzero()[0]

		if points.size:
			self.__getIntervals__(points)
		elif self.open_interval:
			self.intervals = [self.open_interval]
			self.open_interval = None
		else:
			del ComplexSDF.instances[self.fluent_str]
			del self

	def __getIntervals__(self, points):

		intervals = []

		for _, group in it.groupby(enumerate(points), lambda t: t[1] - t[0]):
			group = list(group)
			intervals.append((self.initTime + group[0][-1], self.initTime + group[-1][1] + 1))

		if self.open_interval:
			if self.open_interval[-1] == intervals[0][0]:
				intervals[0] = (self.open_interval[0], intervals[0][1])
			else:
				intervals = [self.open_interval] + intervals

		self.open_interval = None

		if intervals[-1][1] > self.qt >= intervals[-1][0]:
			self.open_interval = (intervals[-1][0], self.qt + 1)
		if intervals[-1][1] > self.qt + 1:
			intervals[-1] = (intervals[-1][0], inf)

		self.intervals = intervals

	@staticmethod
	def __getTimeMatrix__(fluent: tuple, negative: bool = False):

		if fluent in ComplexSDF.instances:

			matrix = ComplexSDF.instances[fluent].matrix

		else:
			matrix = ComplexSDF.empty

		if negative:
			return ComplexSDF.eye - matrix

		return matrix

	@classmethod
	def __createNewInstance__(cls, fluent_str: tuple):

		if fluent_str not in cls.instances:

			ComplexSDF(fluent_str)

		return cls.instances[fluent_str]
