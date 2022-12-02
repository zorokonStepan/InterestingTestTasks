import sys
import json

from typing import Union


def get_unique_elements_json(data: Union[list, dict], result=None):
	"""
	The function allows you to get all the unique elements in a json file
	param: data - data in json format
	param: result - an object in which unique values will be collected.
	it is created the python set inside the function at the start of work
	return: list of unique values of a json file
	"""
	if result is None:
		result = set()

	# if the json dictionary == python dictionary, you need to iterate over both keys and values
	if isinstance(data, dict):
		for k, v in data.items():
			result.add(k)
			if type(v) in (list, dict):
				get_unique_elements_json(v, result)
			else:
				result.add(v)
	# if the json array == python list, you need to iterate over the elements of this structure
	elif isinstance(data, list):
		for el in data:
			if type(el) in (list, dict):
				get_unique_elements_json(el, result)
			else:
				result.add(el)
	# there shouldn't be any other data structures in json,
	# but if it's not a dictionary or an array, then something is wrong here
	else:
		return None

	return list(result)


if __name__ == "__main__":
	# read the data from the json file the link to which is specified in the command line parameter
	with open(sys.argv[1]) as json_file:
		data = json.load(json_file)
	# get unique values from the json file
	result = get_unique_elements_json(data)
	# combining unique values from the json file into a string to write to a file
	result_str = ', '.join([str(i) for i in result])
	# writing unique values from the json file to a new file
	with open("out.txt", "w") as file:
		file.write(f'[{result_str}]')

