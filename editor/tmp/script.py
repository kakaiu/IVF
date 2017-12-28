import json
import ivfWriter

def load(input_path):
    with open(input_path) as json_file:
        data = json.load(json_file)
        return data

def store(data, output_path='data.ivf'):
    with open(output_path, 'w') as json_file:
        json_file.write(json.dumps(data))



tmp = load("tsne_data.json")
result = dict()
result['object'] = []
result['interaction'] = []
result['operationTable'] = dict()
result['reactionTable'] = dict()
result['colorTable'] = {0:'0x00ffff', 1:'0xff00ff', 2:'0xffff00'}

x_min = 999999999
x_max = -999999999
for item in tmp:
	tmpX = float(item['x'].encode('utf-8'))
	if tmpX<x_min:
		x_min = tmpX
	if tmpX>x_max:
		x_max = tmpX

x_scope = x_max-x_min
x_sec = float(x_scope)/3
x_0 = x_min
x_1 = x_min+x_sec
x_2 = x_min+2*x_sec
x_3 = x_max

tmp_id_list = []
tmp_desc_dict = dict()
for item in tmp:
	item['id'] = int(filter(str.isdigit, item['pr_number'].encode('utf-8')))
	item.pop('pr_number')
	item['type']=0
	tmpX = float(item['x'].encode('utf-8'))
	if tmpX<x_1:
		item['colorID'] = 0
	elif tmpX<x_2:
		item['colorID'] = 1
	else:
		item['colorID'] = 2
	item.pop('label')
	item['w']=10
	item['x'] = float(item['x'])*10
	item['y'] = float(item['y'])*10
	item['z'] = float(item['z'])*10
	result['object'].append([0, 1, item]) #type 0 is particle; 1 is presented
	tmp_id_list.append(item['id'])
	tmp_desc_dict[item['id']] = item['description']
	item.pop('description')


for tmp_id in tmp_id_list:
	result['interaction'].append([tmp_id, [1,[[1,tmp_desc_dict[tmp_id]],[2,3]]] ]) #{'pick':[dowhat[1, 2]]}

result['operationTable'][1] = 'pick'
result['reactionTable'][1] = 'infoDisplay'
result['reactionTable'][2] = 'enlarge'

store(result, 'sample.ivf')