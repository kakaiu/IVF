from orientSchema import Node, Relationship, Contribution
from pyorient.ogm.exceptions import MultipleResultsFound, NoResultFound
from pyorient import PyOrientORecordDuplicatedException,PyOrientNullRecordException
from pyorient.ogm import Graph, Config
from pyorient.ogm.property import String
from pyorient.ogm.what import expand, out, in_

import json
import os 

def loadConfig():
	filename = r'/compassConfig/globalConfig.json'
	if os.path.exists(filename):
		with open(filename) as json_file:
			return json.load(json_file)
	else:
		print 'Config is not existed!'
		print 'Please make sure the config.json is located as src/dataModule/config/config.json'
		os._exit(0)

c = loadConfig()
ORIENT_ADDR = c['orient_address']
ORIENT_PORT = c['orient_port']
ORIENT_USERNAME = c['orient_username']
ORIENT_PASSWORD = c['orient_password']
ORIENT_DB = c['orient_db']

class orientWapper:
	__orient = None
	__isValid = None

	def __init__(self):
		self.__orient = Graph(Config.from_url(ORIENT_ADDR+'/'+ORIENT_DB,
							ORIENT_USERNAME,ORIENT_PASSWORD)) #initial_drop=False, this param is dangerous!
		try:
			self.__orient.create_all(Node.registry)
			self.__orient.create_all(Relationship.registry)
			self.__isValid = True
		except:
			self.__isValid = False

	def buildIndex(self):
		if self.__isValid:
			try:
				self.__orient.client.command("CREATE INDEX user.id UNIQUE")
			except:
				pass
			try:
				self.__orient.client.command("CREATE INDEX repo.id UNIQUE")
			except:
				pass
			try:
				self.__orient.client.command("CREATE PROPERTY contribution.out LINK")
			except:
				pass
			try:
				self.__orient.client.command("CREATE PROPERTY contribution.in LINK")
			except:
				pass
			try:
				self.__orient.client.command("CREATE INDEX UniqueContributesEdges ON contribution(in,out) UNIQUE")
			except:
				pass
		else:
			print 'build index failed!'

	def database(self):
		if self.__isValid:
			return self.__orient
		else:
			return None

	def isValid(self):
		return self.__isValid

class orientOperator:
	__graph = None
	__isValid = None

	def __init__(self):
		self.__graph = orientWapper()
		if self.__graph.isValid():
			self.__isValid = True
		else:
			self.__isValid = False

	def buildIndex(self): #for only once time
		if self.__isValid:
			self.__graph.buildIndex()

	def parseGraphID(self, graphID):
		if self.__isValid:
			if graphID%10==0:
				return [graphID/10, 'user']
			elif graphID%10==1:
				return [graphID/10, 'repo']
			else:
				print 'GRAPHID ERROR!', graphID
				return None
		else:
			return None

	def addUser(self, id):
		if self.__isValid:
			try:
				return self.__graph.database().users.create(id=id)
			except  Exception, e:
				pass
			try:
				tmp = self.__graph.database().users.query(id=id).all()
				if len(tmp)==1:
					return tmp[0]
				else:
					print 'GRAPH ERROR!'
					return None

			except Exception, e:
				print type(e), 'add user'
				return None
		else:
			return None

	def addRepo(self, id, language):
		if self.__isValid:
			try:
				return self.__graph.database().repos.create(id=id, type=language)
			except  Exception, e:
				pass

			try:
				tmp = self.__graph.database().repos.query(id=id).all()
				if len(tmp)==1:
					return tmp[0]
				else:
					print 'GRAPH ERROR!'
					return None

			except Exception, e:
				print type(e), 'add repo'
				return None
		else:
			return None
		
	def addContribution(self, user, repo):
		if self.__isValid:
			try:
				self.__graph.database().contribution.create(user,repo)
				return True
			except PyOrientORecordDuplicatedException, e:
				return True
			except Exception, e:
				return False
		else:
			return False

	def getNeighbors(self, graphID):
		v = self.parseGraphID(graphID)
		if v==None:
			return None

		vID = v[0]
		vType = v[1]

		if self.__isValid:
			if vType=='user':
				result = []
				try:
					tmp = self.__graph.database().users.query(id=vID).what(expand(out(Contribution))).all()
					for item in tmp:
						result.append(item.graphID())
					return result
				except:
					return None

			elif vType=='repo':
				result = []
				try:
					tmp = self.__graph.database().repos.query(id=vID).what(expand(in_(Contribution))).all()
					for item in tmp:
						result.append(item.graphID())
					return result
				except:
					None

			else:
				print 'vType ERROR!'
				return None
		else:
			return None