<?php
# © Copyright 2022 HP Development Company, L.P.
# SPDX-License-Identifier: MIT

#Access credentials
$baseUrl = 'https://printos.api.hp.com/box'; #use for a production account
#$baseUrl = 'https://stage.printos.api.hp.com/box'; #use for a staging account
$key = '';
$secret = '';

#amazon fetch and upload urls
$amazon_fetch_url  = "";
$amazon_upload_url = "";

$fileToUpload = 'C:\\FilePath\\FileName.pdf';

#Function Calls 
#--------------------------------------------------------------#

#createFolder('PHP_Folder', 'PHP_Receiver', 'PHP_Sender');
#createFolderWithFiles('PHP_Folder', 'PHP_Receiver', 'PHP_Sender');
#getFolder('FolderId');
getSubstrates();
getFlows();
getUploadUrls("application/pdf");
#uploadFileToAws($fileToUpload, "application/pdf");
#uploadFile('FolderId', $amazon_fetch_url);
#getFile('FileId');


#Box APIs
#--------------------------------------------------------------#

/**
 * Create a folder in Box.
 * 
 * @param $folderName - name of the created folder
 * @param $recipient - name of the receiver
 * @param $sender - name of the sender
 */
function createFolder($folderName, $recipient, $sender) {
	echo "Creating Folder: " . $folderName . "</br>";
	$arr = array(
		'name' => $folderName, 
		'to' => $recipient, 
		'from' => $sender
	);
	$data = json_encode($arr);
	$response = postRequest('/api/partner/folder', $data);
	printInfo($response);
}

/**
 * Creates a folder with the given folder and recipient/sender information and
 * uploads the specified files into the newly created folder.
 * 
 * @param $folderName - name of the created folder
 * @param $recipient - name of the receiver
 * @param $sender - name of the sender
 */
function createFolderWithFiles($folderName, $recipient, $sender) {
	echo "Creating folder with files. </br>";

	$files = array();
    array_push($files, new File("PHP_File1.pdf", 1, "PHP_File1 was uploaded using PHP", "fileUrl1"));
    array_push($files, new File("PHP_File2.pdf", 1, "PHP_File2 was uploaded using PHP", "fileUrl2"));

	$arr = array(
		'name' => $folderName,
		'to' => $recipient, 
		'from' => $sender,
		'files' => $files
	);

	$data = json_encode($arr);
	$response = postRequest('/api/partner/folder', $data);
	printInfo($response);
}

/**
 * Gets information about a file in Box.
 * 
 * @param $fileId - Id of the file
 */
function getFile($fileId) {
	echo "Getting File: " . $fileId . "</br>";
	$response = getRequest('/api/partner/file/' . $fileId);
	printInfo($response);
}

/**
 * Gets flows set up within Box
 */
function getFlows() {
	echo "Getting Flows </br>";
	$response = getRequest('/api/partner/flow');
	printInfo($response);
}

/**
 * Gets information about a folder in Box.
 * 
 * @param $folderId - Id of the folder
 */
function getFolder($folderId) {
	echo "Getting Folder: " . $folderId . "</br>";
	$response = getRequest('/api/partner/folder/' . $folderId);
	printInfo($response);
}

/**
 * Gets the list of available substrates set in Box.
 */
function getSubstrates() {
	echo "Getting substrates </br>";
	$response = getRequest('/api/partner/substrate');
	printInfo($response);
}

/**
 * Gets the amazon aws upload urls for a file.
 *
 * @param $mimeType - MIME type of the file to upload
 */
function getUploadUrls($mimeType) {
	echo "Getting AWS urls for mimeType: " . $mimeType . "</br>";
	$mimeParam = "?mimeType=" . $mimeType;
	$response = getRequestWithParam('/api/partner/file/uploadurls', $mimeParam);
	printInfo($response);
}

/**
 * Upload a file to a specified folder in Box.
 *
 * @param $folderId - Id of the folder to upload to
 * @param $fileUrl - Url of the file to upload (not a local path)
 */
function uploadFile($folderId, $fileUrl) {
	echo "Uploading file: " . $fileUrl . " to folder: " . $folderId . "</br>";
	$arr = array(
		'url' => $fileUrl, 
		'name' => "PHP_File.pdf", 
		'notes' => 'File was uploaded using PHP', 
		'copies' => '1', 
		'folderId' => $folderId,
		# 'flow' => 'Flow ezName' # The flow value is either the easy submit name of the flow or the _id property from getFlows()
	);
	$data = json_encode($arr);
	$response = postRequest('/api/partner/file', $data);
	printInfo($response);
}

/**
 * Uploads a file to an amazon aws url.
 *
 * @param $file - local file to upload to amazon
 * @param $contentType - MIME type of the file (should be same as mimeType used to getUploadUrls)
 */
function uploadFileToAws($file, $contentType) {
	echo "Uploading file: " . $file . " to amazonaws </br>";
	$response = putRequest($file, $contentType);
	printInfo($response);
}


#Helper functions
#--------------------------------------------------------------#

/**
 * Creates the HMAC header to authenticate the API calls.
 *
 * @param $method - type of http method (GET, POST, PUT)
 * @param $path - api path
 * @param $timestamp - time in utc format 
 */
function createHmacAuth($method, $path, $timestamp) {
	global $key, $secret;
	$str = $method . ' ' . $path . $timestamp;
	$hash = hash_hmac('sha256', $str, $secret);
	return $key . ':' . $hash;
}

/**
 * Prints the responses in a "pretty" format, majority of the responses are in JSON format.
 *
 * @param $response - http response of the requests
 */
function printInfo($response) {
	// Check for errors
	if($response === FALSE){
		echo $response . "</br>";
		die($response);
	}

	$responseData = json_decode($response, TRUE);
	echo "<pre>"; print_r($responseData); echo "</pre>";
}


#GET, POST, and PUT
#--------------------------------------------------------------#

/**
 * HTTP GET request 
 *
 * @global $baseUrl - base url/path for the apis
 * @param $path - api path
 *
 * Note: $baseUrl . $path will be the full url to call a certain api.
 */
function getRequest($path) {
	global $baseUrl;
	
	$t = microtime(true);
	$micro = sprintf("%03d",($t - floor($t)) * 1000);
	$time = gmdate('Y-m-d\TH:i:s.', $t).$micro.'Z';
	$auth = createHmacAuth('GET', $path, $time);

	$options = array(
		'http' => array(
			'header'=>  "Content-Type: application/json\r\n" .
						"x-hp-hmac-date: " . $time . "\r\n" .
						"x-hp-hmac-authentication: " . $auth . "\r\n" .
						"x-hp-hmac-algorithm: SHA256\r\n",
			'method'  => 'GET',
		),
	); 

	$context = stream_context_create($options);
	return file_get_contents($baseUrl . $path, false, $context);
}

/**
 * HTTP GET request with a mimeType parameter
 *
 * @global $baseUrl - base url/path for the apis
 * @param $path - api path
 * @param $mimeParam - MIME type to be added to end of $path
 *
 * Note: $baseUrl . $path . $mimeParam will be the full url to get the aws urls specific to the MIME type.
 */
function getRequestWithParam($path, $mimeParam) {
	global $baseUrl;
	
	$t = microtime(true);
	$micro = sprintf("%03d",($t - floor($t)) * 1000);
	$time = gmdate('Y-m-d\TH:i:s.', $t).$micro.'Z';
	$auth = createHmacAuth('GET', $path, $time);

	$options = array(
		'http' => array(
			'header'=>  "Content-Type: application/json\r\n" .
						"x-hp-hmac-date: " . $time . "\r\n" .
						"x-hp-hmac-authentication: " . $auth . "\r\n" .
						"x-hp-hmac-algorithm: SHA256\r\n",
			'method'  => 'GET',
		),
	); 

	$context = stream_context_create($options);
	return file_get_contents($baseUrl . $path . $mimeParam, false, $context);
}

/**
 * HTTP POST request 
 *
 * @global $baseUrl - base url/path for the apis
 * @param $path - api path
 * @param $data - json data to post
 *
 * Note: $baseUrl . $path will be the full url to call a certain api.
 */
function postRequest($path, $data) {
	global $baseUrl;
	
	$t = microtime(true);
	$micro = sprintf("%03d",($t - floor($t)) * 1000);
	$time = gmdate('Y-m-d\TH:i:s.', $t).$micro.'Z';
	$auth = createHmacAuth('POST', $path, $time);

	$options = array(
		'http' => array(
			'header'=>  "Content-Type: application/json\r\n" .
						"x-hp-hmac-date: " . $time . "\r\n" .
						"x-hp-hmac-authentication: " . $auth . "\r\n" .
						"x-hp-hmac-algorithm: SHA256\r\n",
			'method'  => 'POST',
			'content' => $data
		),
	); 

	$context = stream_context_create($options);
	return file_get_contents($baseUrl . $path, false, $context);
}

/**
 * HTTP PUT request 
 *
 * @global $amazon_upload_url - amazon url to upload a local file to
 * @param $file - local file to upload
 * @param contentType - MIME type of the local file (should match amazon upload urls)
 */
function putRequest($file, $contentType) {
	global $amazon_upload_url;

	$postData = file_get_contents($file);

	$options = array(
		'http' => array(
			'header'=>  "Content-Type: " . $contentType . "\r\n",
			'method'  => 'PUT',
			'content' => $postData
		),
	); 

	$context = stream_context_create($options);
	return file_get_contents($amazon_upload_url, false, $context);
}

# Classes
#--------------------------------------------------------------#

class File {
	public $name;
	public $copies;
	public $notes;
	public $url;

	function __construct($name, $copies, $notes, $url) {
		$this->name = $name;
		$this->copies = $copies;
		$this->notes = $notes;
		$this->url = $url;
	}
}

?>