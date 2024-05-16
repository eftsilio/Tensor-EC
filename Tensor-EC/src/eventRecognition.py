from time import process_time

import numpy as np
from scipy import sparse as sp

from operator import itemgetter
import itertools as it
from collections import defaultdict


class EventRecognition:

	shape: int = None
	step: int = None
	clock: int = None
	dynamic_grounding: bool = False
	format_of_sparse: str = None

	initTime: int = None
	qt: int = None

	dim1 = None
	dim2 = None
	eye = None
	empty = None
	termAtQt = None

	map_entities = {}
	inv_map_entities = {}
	n_entities = 0

	def __init__(self, window, step, clock, dynamic_grounding, fos):

		EventRecognition.shape = int(window / clock) + 2
		EventRecognition.step = step
		EventRecognition.clock = clock
		EventRecognition.dynamic_grounding = dynamic_grounding
		EventRecognition.format_of_sparse = fos

	@staticmethod
	def __run__(cachingOrder: list, declarations: dict, definitions: dict, linear: bool):

		for ce_str in cachingOrder:

			complex_event_type = declarations[ce_str]['type']
			complex_event_dim = declarations[ce_str]['Ndim']
			complex_event_rule = definitions[ce_str]

			complex_event = complex_event_type.__createNewInstance__(ce_str, complex_event_dim)

			# er_start = process_time()
			complex_event.__execute__(complex_event_rule, linear)
			# er_end = process_time()
			# print(ce_str, int(round(((er_end - er_start) * 1000))))

	@classmethod
	def __windowParams__(cls, initTime, qt):

		cls.initTime = initTime
		cls.qt = qt
		if cls.dynamic_grounding:
			cls.map_entities = {}
			cls.inv_map_entities = {}
			cls.n_entities = 0

	@classmethod
	def __updateParams__(cls, tensors_dim):

		cls.dim1 = cls.n_entities
		cls.dim2 = cls.shape
		cls.eye = np.ones((cls.dim1**0, cls.dim2**0))
		cls.termAtQt = {}
		cls.empty = {}
		if not cls.dim1:
			for dim in tensors_dim:
				cls.empty[dim] = sp.csr_matrix((0, 0))
			return

		cls.U = sp.diags([1.0], 1, (cls.dim2, cls.dim2))
		cls.upper = sp.csr_matrix(np.triu(np.ones((cls.dim2, cls.dim2)), k=1))
		for dim in tensors_dim:
			cls.empty[dim] = sp.csr_matrix((cls.dim1 ** dim, cls.dim2))
			termAtQt = np.zeros((cls.dim1 ** dim, cls.dim2))
			termAtQt[:, -1] = 1.0
			cls.termAtQt[dim] = sp.csr_matrix(termAtQt)
			# non-sparse
			# cls.empty[dim] = np.empty((cls.dim1 ** dim, cls.dim2))
			# if dim > 1:
			# 	cls.ones[dim] = np.ones((cls.dim1 ** (dim - 1), 1))

	@classmethod
	def __updateEntities__(cls, index: tuple):

		for entity in index:
			if len(index) == 1:
				entity = (entity,)
			if entity not in cls.map_entities:
				cls.map_entities[entity] = cls.n_entities
				cls.inv_map_entities[cls.n_entities] = entity
				cls.n_entities += 1

	@staticmethod
	def __transformToTypeofSparse__(matrix, format_of_sparse: str):

		if format_of_sparse == 'csr':
			return matrix.tocsr()
		elif format_of_sparse == 'csc':
			return matrix.tocsc()
		else:
			return matrix.todia()
