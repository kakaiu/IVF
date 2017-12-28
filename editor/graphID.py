class IDConverter:
	def __init__(self):
		pass

	def getGraphID(self, vID, vType):
		if vType=='user':
			return vID*10
		elif vType=='repo':
			return vID*10+1

	def getIDandType(self, graphID):
		if graphID%10==0:
			return [graphID/10, 'user']
		elif graphID%10==1:
			return [graphID/10, 'repo']