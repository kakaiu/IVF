import pymongo, orientdb
import json
import os 

def store(data, output_path='data.ivf'):
    with open(output_path, 'w') as json_file:
        json_file.write(json.dumps(data))

def getDesc(ID):
	if ID%10==1:
		for result in tmp_repo_desc_mongo.find({'id':int(ID/10)}):
			return '{}<br>language: {}<br>forks: {}'.format(result['full_name'],result['language'],result['forks'])
		return str(ID)
	else:
		return 'Vertex ID: ' + str(ID) + '<br>You can add remote resource for it'

posCache = dict()
def getPos(ID):
	if posCache.has_key(ID):
		return posCache[ID]

	for tmp in tmp_layout:
		if tmp['id']==ID:
			posCache[ID] = [tmp['x'], tmp['y'], tmp['z']]
			return [tmp['x'], tmp['y'], tmp['z']]

	posCache[ID] = None
	return None

def getLineList(ID):
	if ID%10==0:
		return []

	neighbors = orientdb.orientOperator().getNeighbors(ID)
	if neighbors==None:
		return []
	else:
		lines = []
		for neighbor in neighbors:
			tmp1 = getPos(neighbor)
			tmp2 = getPos(ID)
			if tmp1!=None and tmp2!=None:
				lineID = ID*1000000000+neighbor
				result['object'].append([1, 0, [lineID, tmp1, tmp2]]) #type 1 is line; 0 is not presented
				lines.append(lineID)
		return lines

result = dict()
result['object'] = []
result['interaction'] = []
result['operationTable'] = dict()
result['reactionTable'] = dict()
result['shapeTable'] = {0: 'line'}

tmp_layout = []
color_table = dict()

tmp_id_list = []
tmp_desc_dict = dict()

tmp_repo_desc_mongo = pymongo.MongoClient('localhost', 27017)['reposGithub']['reposInfo']
for instance in pymongo.MongoClient('localhost', 27017)['layout']['layout'].find({'timestamp':1499598783232}):
	tmp_layout = instance['layout']
	break

for item in tmp_layout:
	if item['graphID']%10==1:
		item['color'] = '0x00ffff'
	else:
		item['color'] = '0x0000ff'

colorID = 0
for item in tmp_layout:
	if not color_table.has_key(item['color']):
		color_table[item['color']] = colorID
		colorID = colorID + 1

for item in tmp_layout:
	item['id'] = item['graphID']
	item.pop('graphID')
	item['w'] = pow((item['size']), 0.5)*10*0.2
	item['x'] = item['x']*0.2
	item['y'] = item['y']*0.2
	item['z'] = item['z']*0.2
	item.pop('size')
	item['colorID'] = color_table[item['color']]
	item.pop('color')
	result['object'].append([0, 1, item]) #type 0 is particle; 1 is presented
	tmp_id_list.append(item['id'])
	tmp_desc_dict[item['id']] = getDesc(item['id'])

result['colorTable'] = dict(zip(color_table.values(),color_table.keys()))

for tmp_id in tmp_id_list:
	lines = getLineList(tmp_id)
	if len(lines)>0:
		result['interaction'].append([tmp_id, [1,[[1,tmp_desc_dict[tmp_id]],[2,3],[3,[]],[4,lines]]] ]) #{'pick':[dowhat[1, 2]]}
	else:
		result['interaction'].append([tmp_id, [1,[[1,tmp_desc_dict[tmp_id]],[2,3]]] ])

result['operationTable'][1] = 'pick'
result['reactionTable'][1] = 'infoDisplay'
result['reactionTable'][2] = 'enlarge'
result['reactionTable'][3] = 'keepLine'
result['reactionTable'][4] = 'appearLine'

store(result, 'compass.ivf')