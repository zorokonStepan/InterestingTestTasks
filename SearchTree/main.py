class TreeStore:
	def __init__(self, array):
		self.array = array
		self.items = {item['id']: item for item in self.array}

	def getAll(self):
		return self.array

	def getItem(self, id):
		return self.items[id]

	def getChildren(self, id):
		return [item for item in self.array if item['parent'] == id]

	def getAllParents(self, id):
		result = []
		while True:
			tmp_id = self.items[id]['parent']
			if tmp_id != 'root':
				result.append(self.items[tmp_id])
			else:
				break
			id = self.items[id]['parent']
		return result


if __name__ == "__main__":

	items = [
		{"id": 1, "parent": "root"},
		{"id": 2, "parent": 1, "type": "test"},
		{"id": 3, "parent": 1, "type": "test"},
		{"id": 4, "parent": 2, "type": "test"},
		{"id": 5, "parent": 2, "type": "test"},
		{"id": 6, "parent": 2, "type": "test"},
		{"id": 7, "parent": 4, "type": None},
		{"id": 8, "parent": 4, "type": None}
	]

	ts = TreeStore(items)

	assert ts.getAll() == items
	assert ts.getItem(7) == {"id": 7, "parent": 4, "type": None}
	assert ts.getChildren(4) == [{"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]
	assert ts.getChildren(5) == []
	assert ts.getAllParents(7) == [{"id": 4, "parent": 2, "type": "test"},
								   {"id": 2, "parent": 1, "type": "test"},
								   {"id": 1, "parent": "root"}]
