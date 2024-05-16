
from src.processEvents import InputEvent, ComplexEvent
from src.processSimpleFluents import SimpleFluent
from src.processSDFluents import InputSDF, ComplexSDF
from src.eventRecognition import EventRecognition


def dynamicGrounding():

	for fluent in SimpleFluent.instances:
		sf = SimpleFluent.instances[fluent]
		for entity in sf.open_interval:
			EventRecognition.__updateEntities__(entity)

	for fluent in ComplexSDF.instances:
		sdf = ComplexSDF.instances[fluent]
		for entity in sdf.open_interval:
			EventRecognition.__updateEntities__(entity)


'''
def dynamicGrounding(entities):

	vessels = []
	# vesselPairs = []

	vessels = findNewVessels(vessels)
	vessels = addVesselsFromPW(vessels, entities)

	# vesselPairs = findNewPairs(vesselPairs)

	entities['vessel'] = vessels
	# entities['vesselPair'] = vesselPairs


def findNewVessels(vessels):

	if ('coord',) in InputEvent.instances:
		for index in InputEvent.instances[('coord',)]:
			vessels.append(index[0])

	return list(set(vessels))


def addVesselsFromPW(vessels, entities):

	if 'vessel' in entities:
		for obj in entities['vessel']:
			found = False
			for fluent in SimpleFluent.instances:
				if (obj,) in SimpleFluent.instances[fluent]:
					vessels.append(obj)
					found = True
					break
			if found:
				continue
			for fluent in ComplexSDF.instances:
				if (obj,) in ComplexSDF.instances[fluent]:
					vessels.append(obj)
					found = True
					break
			if found:
				continue
			for event in ComplexEvent.instances:
				if (obj,) in ComplexEvent.instances[event]:
					vessels.append(obj)
					break

	return list(set(vessels))


def findNewPairs(vesselPairs):

	fluent = ('proximity', 'true')

	if fluent in InputSDF.instances:
		for index in InputSDF.instances[fluent]:
			vesselPairs.append(index)

	fluent = ('rendezVous', 'true')

	if fluent in ComplexSDF.instances:
		for vp in ComplexSDF.instances[fluent]:
			vesselPairs.append(vp)

	return list(set(vesselPairs))
'''
