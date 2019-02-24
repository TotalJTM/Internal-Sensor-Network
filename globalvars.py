
def init():
	global nodeList
	nodeList = []

def nodeListJSON():
	return json.dumps(nodeList,default=lambda o: o.__dict__,sort_keys=True, indent=4) # 