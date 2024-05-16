
from src.processEvents import InputEvent
from src.processSDFluents import InputSDF


def readAppDynamicData(csv_file, initTime: int, queryTime: int, clock: int, declarations: dict, previous_rows=None):

	kept_rows = []

	if previous_rows:

		for row in previous_rows:

			time = int(row[1])
			if initTime < time <= queryTime:
				returned_row = assertInputEvents(time, row, declarations, queryTime, clock)
				if returned_row:
					kept_rows += [returned_row]
			else:
				kept_rows += [row]

	for row in csv_file:

		time = int(row[1])

		if initTime < time <= queryTime:

			returned_row = assertInputEvents(time, row, declarations, queryTime, clock)
			if returned_row:
				kept_rows += [returned_row]

		elif time > queryTime:
			kept_rows += [row]
			previous_rows = kept_rows
			break

	return previous_rows


def assertInputEvents(time: int, row: list, declarations: dict, queryTime: int, clock: int):

	event = (row[0],)
	returned_row = None

	if event in declarations:
		type_event = declarations[event]['type']
		event_dim = declarations[event]['Ndim']
		if event_dim == 1:
			index = (row[declarations[event]['index'][0]],)
		else:
			index = ()
			for i in declarations[event]['index']:
				index += ((row[i],),)

		if type_event == InputEvent:

			assertSimpleEvent(event, time, index, event_dim)

		else:
			interval = tuple([int(row[i]) for i in declarations[event]['interval']])
			if interval[-1] > queryTime:
				returned_row = row
				returned_row[declarations[event]['interval'][0]] = queryTime + clock
			event += (row[declarations[event]['value']],)
			assertInputSDF(event, interval, index, event_dim)

	return returned_row


def assertSimpleEvent(event, time, index, dim):

	if event in InputEvent.instances:

		InputEvent.instances[event].__update__(index, time)

	else:
		InputEvent(event, index, dim, time)


def assertInputSDF(fluent, interval, index, dim):

	if fluent in InputSDF.instances:

		InputSDF.instances[fluent].__update__(index, interval)

	else:
		InputSDF(fluent, index, interval, dim)



