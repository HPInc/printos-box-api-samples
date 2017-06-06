# © Copyright 2016 HP Development Company, L.P.
# SPDX-License-Identifier: MIT

#!/usr/bin/python

__author__ = 'printos'

import requests, json, hmac, hashlib, datetime, base64, string, random

#access credentials
#baseUrl = "https://printos.api.hp.com/box" 					#use for production server account
#baseUrl = "https://stage.printos.api.hp.com/box"				#use for staging server account

key = ''
secret = ''

#amazon fetch and upload urls
amazon_fetch_url  = ""
amazon_upload_url = ""

fileToUpload = "C:\\FilePath\\FileName.pdf"

#--------------------------------------------------------------#


'''
Creates a folder with the given folder and recipient information

Params:
  fname - Folder name
  recipient - Name of recipient
  sender - sender of the folder
'''
def create_folder(fname, recipient, sender):
	print("In create_folder() function")
	print(" Creating folder: ", fname, "\n Recipient: ", recipient, "\n Sender: ", sender)
	payload = {'name':fname, 'from':sender, 'to':recipient}
	body = json.JSONEncoder().encode(payload)
	print(" Body: ", body)
	return request_post('/api/partner/folder', body)


'''
Creates a folder with the given folder and recipient/sender information and
uploads the specified files into the newly created folder

Params:
  fname - Folder name
  recipient - Name of recipient
  sender - sender of the folder
'''
def create_folder_with_files(fname, recipient, sender):
	print("In create_folder_with_files() function")
	print(" Creating folder: ", fname, "\n Recipient: ", recipient, "\n Sender: ", sender)
	payload = {
		'name': fname,
		'from': sender,
		'to': recipient,
		'files': [{
			'name': 'Python_File1.pdf',
			'copies': 1,
			'notes': 'Python_File1 was uploaded using Python',
			'url': "file_url1",
		}, {
			'name': 'Python_File2.pdf',
			'copies': 1,
			'notes': 'Python_File2 was uploaded using Python',
			'url': "file_url2",
		}]
	}
	body = json.JSONEncoder().encode(payload)
	print(" Body: ", body)
	return request_post('/api/partner/folder', body)


'''
Creates the header using the key/secret which
allows you to make the API calls

Params:
  method - type of method (POST, GET, PUT, etc)
  path - api path (excluding the base url)
  timestamp - current time in specified format
'''
def create_headers(method, path, timestamp):
	string_to_sign = method + ' ' + path + timestamp
	local_secret = secret.encode('utf-8')
	string_to_sign = string_to_sign.encode('utf-8')
	signature = hmac.new(local_secret, string_to_sign, hashlib.sha1).hexdigest()
	auth = key + ':' + signature
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
	print("In get_file() function")
	print(" Getting file with ID: ", file_id)
	path = '/api/partner/file/' + file_id
	return request_get(path)


'''
Return flows set up within Box
'''
def get_flows():
	print("In get_flows() function")
	print(" Getting flows")
	path = '/api/partner/flow'
	return request_get(path)	


'''
Returns information about a folder with the given ID

Params:
  folder_id - ID of folder to get information on
'''
def get_folder(folder_id):
	print("In get_folder() function")
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
	print("In get_uploadUrls() function")
	timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	path = '/api/partner/file/uploadurls'
	url = baseUrl + path
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
  path - api path (excluding the base url)
'''
def request_get(path):
	print("In request_get() function")
	timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	print(" Timestamp: ", timestamp)
	url = baseUrl + path
	headers = create_headers("GET", path, timestamp)
	result = requests.get(url, headers=headers)
	return result


'''
POST call

Params:
  path - api path (excluding the base url)
  data - data to be posted
'''
def request_post(path, data):
	print("In request_post() function")
	timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	print(" Timestamp: ", timestamp)
	url = baseUrl + path
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
	payload = { 
		'url': file_url,
		'name': 'Python_File.pdf', 
		'notes': 'File was uploaded using Python', 
		'folderId': folder_id, 
		'copies': 1, 
		# 'flow': "588fc7ab1e46861100dd7f42" # The flow value is either the easy submit name of the flow or the _id property from get_flows()
	}
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

def test_create_folder(fname, recipient, sender):
	print("In test_create_folder() function")
	result = create_folder(fname, recipient, sender)
	print_json(result)

def test_create_folder_with_files(fname, recipient, sender):
	print("In test_create_folder_with_files() function")
	result = create_folder_with_files(fname, recipient, sender)
	print_json(result)

def test_get_file(file_id):
	print("In test_get_file() function")
	result = get_file(file_id)
	print_json(result)

def test_get_flows():
	print("In test_get_flow() function")
	result = get_flows()
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


test_create_folder('Python_Folder', 'Python_Receiver', 'Python_Sender')
#test_create_folder_with_files('Python_Folder', 'Python_Receiver', 'Python_Sender')
#test_get_folder("FolderId")
test_get_substrates()
test_get_flows()
test_get_uploadUrls("application/pdf")
#test_upload_file_to_aws(amazon_upload_url, fileToUpload, "application/pdf")
#test_upload_file("FolderId", amazon_fetch_url)
#test_get_file("FileId")