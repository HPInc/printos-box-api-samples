#!/usr/bin/python

__author__ = 'printos'

import requests, json, hmac, hashlib, datetime, base64, string, random

#access credentials
token = ''
secret = ''
endpoint = "https://stage.printos.api.hp.com/box"				#change depending on if you are using staging or production

#amazon fetch and upload urls
amazon_fetch_url  = ""
amazon_upload_url = ""

fileToUpload = ""

#--------------------------------------------------------------#


'''
Creates a folder with the given folder and recipient name

Params:
  fname - Folder name
  recipient - Name of recipient
  sender - sender of the folder
'''
def create_folder(fname, recipient, sender='PythonSender'):
	print("In create_folder function()")
	print(" Creating folder: ", fname, "\n Recipient: ", recipient, "\n Sender: ", sender)
	payload = {'name':fname, 'from':sender, 'to':recipient}
	body = json.JSONEncoder().encode(payload)
	print(" Body: ", body)
	return request_post('/api/partner/folder', body)


'''
Creates the header using the token/secret which
allows you to make the API calls

Params:
  method - type of method (POST, GET, PUT, etc)
  path - api path (excluding the base endpoint)
  timestamp - current time in specified format
'''
def create_headers(method, path, timestamp):
	string_to_sign = method + ' ' + path + timestamp
	local_secret = secret.encode('utf-8')
	string_to_sign = string_to_sign.encode('utf-8')
	signature = hmac.new(local_secret, string_to_sign, hashlib.sha1).hexdigest()
	auth = token + ':' + signature
	return {
		'content-type': 'application/json',
		'x-hp-hmac-authentication': auth,
		'x-hp-hmac-date': timestamp,
		'x-hp-hmac-algorithm' : 'SHA1'
	}


'''
Return information about a file with the given ID

Params:
  file_id - ID of file to get information on
'''
def get_file(file_id):
	print("In get_file function()")
	print(" Getting file with ID: ", file_id)
	path = '/api/partner/file/' + file_id
	return request_get(path)


'''
Returns information about a folder with the given ID

Params:
  folder_id - ID of folder to get information on
'''
def get_folder(folder_id):
	print("In get_folder function()")
	print(" Getting folder with ID: ", folder_id)
	path = '/api/partner/folder/' + folder_id
	return request_get(path)


'''
Returns the available substrates
'''
def get_substrates():
	print("In get_substrates() function")
	return request_get('/api/partner/substrate')


'''
Returns the upload URLs to aws with the matching MIME type

Params:
  mimeType - MIME type of file that will be uploaded (application/pdf, image/jpeg, etc)
'''
def get_uploadUrls(mimeType):
	print("In get_uploadUrls function()")
	timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	path = '/api/partner/file/uploadurls'
	url = endpoint + path
	headers = create_headers("GET", path, timestamp)
	result = requests.get(url, headers=headers, params={'mimeType':mimeType})
	return result


'''
Prints the data into a cleaner JSON format

Params:
  data - data that needs to be printed into JSON format
'''
def print_json(data):
	print(json.dumps(data.json(), indent=4, sort_keys=True))


'''
GET call

Params:
  path - api path (excluding the base endpoint)
'''
def request_get(path):
	print("In request_get() function")
	timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	print(" Timestamp: ", timestamp)
	url = endpoint + path
	headers = create_headers("GET", path, timestamp)
	result = requests.get(url, headers=headers)
	return result


'''
POST call

Params:
  path - api path (excluding the base endpoint)
  data - data to be posted
'''
def request_post(path, data):
	print("In request_post() function")
	timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	print(" Timestamp: ", timestamp)
	url = endpoint + path
	headers = create_headers("POST", path, timestamp)
	result = requests.post(url, data, headers=headers)
	return result


'''
Uploads a file to the specified folder

Params:
  folder_id - ID of folder to upload file to
  file_url - url of file you would like to upload
'''
def upload_file(folder_id, file_url):
	print("In upload_file() function")
	payload = { 'url': file_url, 'name': 'File.pdf', 'notes': 'Please work, I\'ll give cookies', 'folderId': folder_id, 'copies': 1 }
	body = json.JSONEncoder().encode(payload)
	return request_post('/api/partner/file', body)


'''
Uploads a file to the amazon aws url

Params:
  amazonUrl - amazon upload url (obtained from get_uploadUrls())
  fileToUpload - local file you would like to upload to the amazon url
  contentType - type of file (application/pdf, image/jpeg, etc)
'''
def upload_file_to_aws(amazonUrl, fileToUpload, contentType):
	print("In upload_file_to_aws() function")
	print("Uploading file: ", fileToUpload)
	file = open(fileToUpload, 'rb')
	data = file.read()
	return requests.put(amazonUrl, data=data, params={'file':fileToUpload}, headers={'Content-Type': contentType})


#--------------------------------------------------------------#

'''
Test functions to test out each part of the Box API
'''

def test_create_folder(fname, recipient):
	print("In test_create_folder() function")
	result = create_folder(fname, recipient)
	print_json(result)

def test_get_file(file_id):
	print("In test_get_file() function")
	result = get_file(file_id)
	print_json(result)

def test_get_folder(folder_id):
	print("In test_get_folder() function")
	result = get_folder(folder_id)
	print_json(result)

def test_get_substrates():
	print("In test_substrates() function")
	result = get_substrates()
	print_json(result)

def test_get_uploadUrls(mimeType):
	print("In test_get_uploadUrls() function")
	result = get_uploadUrls(mimeType)											
	print_json(result)

def test_upload_file(folder_id, file_url):
	print("In test_upload_file() function")
	result = upload_file(folder_id, file_url)
	print_json(result)

def test_upload_file_to_aws(amazonUrl, fileToUpload, contentType):
	print("In test_upload_file_to_aws() function")
	result = upload_file_to_aws(amazonUrl, fileToUpload, contentType)
	print(result)


#--------------------------------------------------------------#


test_create_folder('PythonFolderName', 'PythonRecipient') 										#uncomment out if folder needs to be created
#test_get_folder("") 																	#pass in ID of the folder from the result of test_create_folder
#test_get_substrates()																	#list of available substrates to add when uploading file
#test_get_uploadUrls("application/pdf")													#comment out if you already have the upload URLs, change MIME type depending on file you need to upload
#test_upload_file_to_aws(amazon_upload_url, fileToUpload, "application/pdf")				#<Response [200]> is the response you want to see					
#test_upload_file("57bc9a7144e4f91100e61485", amazon_fetch_url)							#provide own file url or upload file to amazon aws url and then provide fetch url
#test_get_file("57bcafb044e4f91100e6179e")												#pass in ID of the file from the result of test_upload_file