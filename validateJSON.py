'''
JSON Validator Script: Validate a JSON data instance (or set of instances) against JSON schemas
Created 26-Aug-2016  M. Kouremetis (MITRE)
'''
import getopt
import os
import jsonmerge
import jsonschema
import simplejson
import sys
import traceback


'''TODO:
	-Hardcoded to draft 4 json schemas

'''

HELP_OUTPUT = "validateJSON.py -d <json data file or directory name> -s <json schema file> \n\n " \
			  "Usage: \n" \
			  "-d <json data directory> will attempt to validate every json file in directory against the schema \n\n" \
			  "Notes: \n" \
			  "(Supply absolute paths of parameters, if not in current directory) \n"  \
			  "(If json schema is in multiple files, place referenced files in same directory as the supplied schema file path \n" 

SCHEMA_DIR_ERROR_LOOP_CONT = "--> Since this a directory of schema files, will continue and try to merge the other schema files"


'''
utility exception function
'''
def generic_except(message):
	print(message)
	print(sys.exc_info()[0])
	traceback.print_exc()
	return False


'''
handle args passed from command line
'''
def handle_CL_param(main_args):

	try:
		opts, args = getopt.getopt(main_args,"d:hs:",["help", "data=","schema="])
	except getopt.GetoptError as err:
		print str(err)
		print(HELP_OUTPUT)
		sys.exit(2)

	param ={"data_dir": False}

	for opt, arg in opts:
		if opt in ("-d","--data"):
			param["json_data_fn"] = arg
			if os.path.isdir(arg):
				param["data_dir"] = True
		
		elif opt in ("-s","--schema"):
			param["json_schema_fn"] = arg
			if os.path.isdir(arg):
				print("Error: schema supplied is directory, should be single file")
				print(HELP_OUTPUT)
				sys.exit(1)

		elif opt in ("-h", "--help"):
			print(HELP_OUTPUT)
			sys.exit(1)

	#print(param)
	return param


'''
process a directory of json data files, against a schema
'''
def process_data_dir(data_fn, schema_fn):
	#grab all the json schema files from the provided directory (non-recursive)
	data_files = [f for f in os.listdir(data_fn) if os.path.isfile(f) if f.endswith('.json')]
	status = True
	#for each schema, check the json data against it
	for d in data_files:
		if not process_json_data(data_fn, schema_fn):
			status = False
	return status



'''
check json data file against json schema
'''	
def process_json_data(data_fn,schema_fn):
	with open(data_fn, "r") as d_file, open(schema_fn, "r") as schema_file:
		#Load json files
		try:
			data = simplejson.load(d_file)
			schema = simplejson.load(schema_file)
		except:
			return generic_except("Error loading json file:")
		
		#First, validate schema
		try:
			jsonschema.Draft4Validator.check_schema(schema)
		except jsonschema.exceptions.SchemaError as f:
			print("{} was found to not be a valid Draft4 JSON schema(s), error: {} ".format(schema_fn, f))
			return False

		#Validate JSON data against schema
		try:
			resolver = jsonschema.RefResolver("file:"+os.path.abspath(schema_fn), schema)
			jsonschema.validate(data, schema, resolver=resolver)
		except jsonschema.exceptions.ValidationError:
			print("{} did not validate against the schema(s): {}".format(data_fn.split("/")[-1], schema_fn))
			for error in sorted(jsonschema.Draft4Validator(schema, resolver = resolver).iter_errors(data), key=str):
				print (error.message)
			return False

	print("{} did successfully validate against the schema(s): {}".format(data_fn.split("/")[-1], schema_fn))

	return True


'''
main
'''
def main(argv):
	
	param = handle_CL_param(argv)
	#param = {"json_data_fn" : "/home/michael/Desktop/MAEC-JSONValidator/test_json_data.json", "json_schema_fn": "/home/michael/Desktop/MAEC-JSONValidator/Behavior.json", 'schema_dir': False ,}
	
	#Process a directory of json data files or a single json file
	if param['data_dir']:
		process_data_dir(param["json_data_fn"], param["json_schema_fn"])
	else:
		process_json_data(param["json_data_fn"],param["json_schema_fn"])
	return



if __name__ =="__main__":
	main(sys.argv[1:])