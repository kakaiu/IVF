import pymongo, orientdb, ivfWriter

def getDesc(ID):
	if ID%10==1:
		for result in tmp_repo_desc_mongo.find({'id':int(ID/10)}):
			return '{}<br>language: {}<br>forks: {}'.format(result['full_name'],result['language'],result['forks'])
		return str(ID)
	else:
		return 'Vertex ID: ' + str(ID) + '<br>You can add remote resource for it'

iw = ivfWriter.ivf_writer()

color_table = dict()
tmp_id_list = []
tmp_desc_dict = dict()

tmp_layout = pymongo.MongoClient('localhost', 27017)['layout']['universe']
tmp_repo_desc_mongo = pymongo.MongoClient('localhost', 27017)['reposGithub']['reposInfo']

colorID = 0
for item in tmp_layout.find():
	if not color_table.has_key(item['color']):
		color_table[item['color']] = colorID
		colorID = colorID + 1

for item in tmp_layout.find():
	iw.setObject(0, [0, 1, item['x']*0.1, item['y']*0.1, item['z']*0.1, item['size']*0.1, color_table[item['color']]])
	tmp_id_list.append(item['graphID'])
	tmp_desc_dict[item['graphID']] = getDesc(item['graphID'])


iw.setColorTable(dict(zip(color_table.values(),color_table.keys())))
iw.setInteraction(0, [1,[ [1,'I am repo'], [2,3]]])
iw.setOperationTable({1:'pick'})
iw.setReactionTable({1:'infoDisplay', 2:'enlarge'})

iw.write('compass_u.ivf')