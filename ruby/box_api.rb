# © Copyright 2016 HP Development Company, L.P.
# SPDX-License-Identifier: MIT

require 'json'
require 'net/http'
require 'openssl'
require 'time'

#access credentials
#$baseUrl = "https://printos.api.hp.com/box"		#use for production account
#$baseUrl = "https://stage.printos.api.hp.com/box"	#use for staging account
$key = ""
$secret = ""

#amazon fetch and upload urls
$amazon_fetch_url  = ""
$amazon_upload_url = ""

$file_to_upload = "C:\\FilePath\\FileName.pdf"

#Box APIs
#--------------------------------------------------------------#

# Creates a Folder in Box
#
# Param: 
#   folder_name - name of the created folder
#   recipient - name of the receiver
#   sender - name of the sender
def create_folder(folder_name, recipient, sender)
	puts "Creating folder: " + folder_name
	folder = {:name => folder_name, :to => recipient, :from => sender}
	data = JSON.generate(folder)
	response = request_post('/api/partner/folder', data)
	puts response.body
end

# Creates a folder with the given folder and recipient/sender information and
# uploads the specified files into the newly created folder
#
# Params:
#   folder_name - Folder name
#   recipient - Name of recipient
#   sender - sender of the folder
def create_folder_with_files(folder_name, recipient, sender) 
	puts "Creating folder with files."
	data = {
		"name" => folder_name,
		"from" => sender,
		"to" => recipient,
		"files" => [{
			"name" => "Ruby_File1.pdf",
			"copies" => 1,
			"notes" => "Ruby_File1 was uploaded using Ruby",
			"url" => "file_url1"
		}, {
			"name" => "Ruby_File2.pdf",
			"copies" => 1,
			"notes" => "Ruby_File2 was uploaded using Ruby",
			"url" => "file_url2"
		}]
	}.to_json()
	puts data
	response = request_post('/api/partner/folder', data)
	puts response.body
end

# Gets information about a file in Box.
#
# Param: 
#   file_id - Id of the file
def get_file(file_id)
	puts "Getting file: " + file_id
	response = request_get('/api/partner/file/' + file_id)
	puts response.body
end

# Gets flows set up within Box
def get_flows()
	puts "Getting flows"
	response = request_get('/api/partner/flow')
	puts response.body
end

# Gets information about a folder in Box.
#
# Param: 
#   file_id - Id of the folder
def get_folder(folder_id)
	puts "Getting folder: " + folder_id
	response = request_get('/api/partner/folder/' + folder_id)
	puts response.body
end

# Gets the list of available substrates set in Box.
def get_substrates()
	puts "Getting list of substrates."
	response = request_get('/api/partner/substrate')
	puts response.body
end

# Gets the amazon aws upload urls for a file.
#
# Param: 
#   mime_type - MIME type of the file to upload
def get_upload_urls(mime_type)
	puts "Getting aws urls for MIME type: " + mime_type
	response = request_get_with_param('/api/partner/file/uploadurls', mime_type)
	puts response.body
end

# Upload a file to a specified folder in Box.
#
# Param: 
#   folder_id - Id of the folder to upload to
#   file_url - Url of the file to upload (not a local path)
def upload_file(folder_id, file_url) 
	puts "Uploading file: " + file_url + " to folder: " + folder_id
	file = {
		:url => file_url, 
		:name => "Ruby_File.pdf", 
		:notes => "This was uploaded using Ruby", 
		:copies => 1, 
		:folderId => folder_id,
		# :flow => "Flow ezName" # The flow value is either the easy submit name of the flow or the _id property from get_flows()
	}
	data = JSON.generate(file)
	response = request_post('/api/partner/file', data)
	puts response.body
end

# Upload a file to an amazon aws url.
#
# Param: 
#   file_to_upload - local file to upload to amazon
#   content_type - MIME type of the file (should be the same as the mime_type used to get_upload_urls)
def upload_file_to_aws(file_to_upload, content_type)
	puts "Uploading file: " + file_to_upload + " to aws"
	response = request_put(file_to_upload, content_type)
	puts response
end


#Helper functions
#--------------------------------------------------------------#

# Creates the HMAC header to authenticate the API calls.
#
# Param: 
#   method - type of http method (GET, POST, PUT)
#   path - api path
#   timestamp - time in utc format
def create_hmac_auth(method, path, timestamp)
	str = method + ' ' + path + timestamp;
	sha1 = OpenSSL::Digest.new('sha1')
	hash = OpenSSL::HMAC.hexdigest(sha1, $secret, str)
	return $key + ":" + hash
end


#GET, POST, and PUT
#--------------------------------------------------------------#

# HTTP GET request
#
# Param: 
#   path - api path
#
# Note: baseUrl + path will be the full url to call a certain api
def request_get(path)
	timestamp = Time.now.utc.iso8601
	auth = create_hmac_auth("GET", path, timestamp)
	
	uri = URI($baseUrl + path)

	request = Net::HTTP::Get.new(uri)
	request.add_field("x-hp-hmac-authentication", auth)
	request.add_field("x-hp-hmac-date", timestamp)

	response = Net::HTTP.start(uri.host, uri.port,
		:use_ssl => uri.scheme == 'https',
		:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		http.request(request)
	end

	return response
end

# HTTP GET request with a mime_type parameter
#
# Param: 
#   path - api path
#   param - MIME type to be added to the end of path
#
# Note: +baseUrl + path + param will be the full url to get the aws urls specific to the MIME type.
def request_get_with_param(path, param)
	timestamp = Time.now.utc.iso8601
	auth = create_hmac_auth("GET", path, timestamp)
	
	uri = URI($baseUrl + path + "?mimeType=" + param)

	request = Net::HTTP::Get.new(uri)
	request.add_field("x-hp-hmac-authentication", auth)
	request.add_field("x-hp-hmac-date", timestamp)

	response = Net::HTTP.start(uri.host, uri.port,
		:use_ssl => uri.scheme == 'https',
		:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		http.request(request)
	end
end

# HTTP POST request
#
# Param: 
#   path - api path
#   data - json data to post
#
# Note: baseUrl + path will be the full url to call a certain api
def request_post(path, data)
	timestamp = Time.now.utc.iso8601
	auth = create_hmac_auth("POST", path, timestamp)
	
	uri = URI($baseUrl + path)

	request = Net::HTTP::Post.new(uri)
	request.add_field("Content-Type", "application/json")
	request.add_field("x-hp-hmac-authentication", auth)
	request.add_field("x-hp-hmac-date", timestamp)
	request.body = data

	response = Net::HTTP.start(uri.host, uri.port,
		:use_ssl => uri.scheme == 'https',
		:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		http.request(request)
	end

	return response
end

# HTTP PUT request
#
# Param: 
#   file - local file to upload
#   content_type - MIME type of the local file (should match amazon upload urls)
def request_put(file, content_type)
	uri = URI($amazon_upload_url)

	request = Net::HTTP::Put.new(uri)
	request.body_stream = File.open(file)
	request.add_field("Content-Type", content_type)
	request.add_field('Content-Length', File.size(file))

	response = Net::HTTP.start(uri.host, uri.port,
		:use_ssl => uri.scheme == 'https',
		:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		http.request(request)
	end

	return response
end


#Function Calls 
#--------------------------------------------------------------#

create_folder("Ruby_Folder", "Ruby_Receiver", "Ruby_Sender")
#create_folder_with_files("Ruby_Folder", "Ruby_Receiver", "Ruby_Sender")
#get_folder("FolderId")
get_substrates()
get_flows()
get_upload_urls("application/pdf")
#upload_file_to_aws($file_to_upload, "application/pdf")
#upload_file("FolderId", $amazon_fetch_url)
#get_file("FileId")