import json, os

class ivf_writer:
	__data_structure = None
	__currentID = -1
	__currentIDFreeCache = []
	__idTable = dict()

	def init(self):
		self.__data_structure = dict()
		self.__data_structure['object'] = []
		self.__data_structure['interaction'] = []
		self.__data_structure['operationTable'] = dict()
		self.__data_structure['reactionTable'] = dict()
		self.__data_structure['colorTable'] = dict()

	def setObject(self, groupID, object): #id, [type 0 is particle, if immediately appear, {w,x,y,z, colorID}]
		self.__currentID = self.__currentID + 1
		self.__data_structure['object'].append([self.__currentID].extend(object))
		if self.__idTable.has_key(groupID):
			self.__idTable[groupID].append(self.__currentID)
		else:
			self.__idTable[groupID] = [self.__currentID]
		return self.__currentID

	def modifyObject(self, groupID, newObject):
		modifiedList = []
		if self.__idTable.has_key(groupID):
			tmpIDs = self.__idTable[groupID]
			for i in range(0, len(self.__data_structure['object'])):
				for tmpID in tmpIDs:
					if len(modifiedList)==len(tmpIDs):
						return tmpIDs

					if self.__data_structure['object'][i][0]==tmpID:
						self.__data_structure['object'][i] = [tmpID].extend(newObject)
						modifiedList.append(self.__data_structure['object'][i][0])
		return modifiedList

	def setInteraction(self, groupID, interactions): #groupID means interaction group
		if self.__idTable.has_key(groupID): #tmpID1 != (group1 && group2)
			tmpIDs = self.__idTable[groupID]
			for tmpID in tmpIDs:
				self.__data_structure['interaction'].append([tmpID].append(interactions))

	def modifyInteraction(self, groupID, newInteractions):
		modifiedList = []
		if self.__idTable.has_key(groupID):
			tmpIDs = self.__idTable[groupID]
			for i in range(0, len(self.__data_structure['interaction'])):
				for tmpID in tmpIDs:
					if len(modifiedList)==len(tmpIDs):
						return tmpIDs

					if self.__data_structure['interaction'][i][0]==tmpID:
						self.__data_structure['interaction'][i] = [tmpID].append(newInteractions)
						modifiedList.append(self.__data_structure['interaction'][i][0])

	def setOperationTable(self, operationTable):
		self.__data_structure['operationTable'] = operationTable

	def setReactionTable(self, reactionTable):
		self.__data_structure['reactionTable'] = reactionTable

	def setColorTable(self, colorTable):
		self.__data_structure['colorTable'] = colorTable

	def write(self, output_path='data.ivf'):
		with open(output_path, 'w') as json_file:
        	json_file.write(json.dumps(self.__data_structure))