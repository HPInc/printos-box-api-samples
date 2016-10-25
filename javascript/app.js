// © Copyright 2016 HP Development Company, L.P.
// SPDX-License-Identifier: MIT

var BoxApi = require('./boxApi');

var key = '';
var secret = '';
var proxy = parseArgs();

new BoxApiTest().testAll();

function BoxApiTest() {

	//var baseUrl = 'https://printos.api.hp.com/box'; //use for account on production server
	//var baseUrl = 'https://stage.printos.api.hp.com/box'; //use for account on staging server
	var boxApi = new BoxApi(baseUrl, key, secret, proxy);

	this.testCreateFolder = function(fname, recipient, sender) {
		boxApi.createFolder(fname, recipient, sender)
		.then(success, failure);
	}

	this.testCreateFile = function(url, name, folder_id, copies, notes) {
		boxApi.createFile(url, name, folder_id, copies, notes)
		.then(success, failure);
	}

	this.testGetFolder = function (id) {
		boxApi.getFolder(id)
		.then(success, failure);
	}

	this.testGetFile = function(id) {
		boxApi.getFile(id)
		.then(success, failure);
	}

	this.testGetUploadUrls = function(mime_type) {
		boxApi.getUploadUrls(mime_type)
		.then(success, failure);
	}

	this.testGetSubstrates = function() {
		boxApi.getSubstrates()
		.then(success, failure);
	}

	this.testAll = function() {
		this.testCreateFolder('JavaScript_Folder', 'JavaScript_Receiver', 'JavaScript_Sender');	
		// this.testGetFolder('folder_id');
		// this.testCreateFile('http://www.w3schools.com/html/pic_mountain.jpg', 'JavaScript_File.jpg', 'folder_id', copies='3', notes='File was uploaded using JavaScript');
		// this.testGetFile('file_id');
		// this.testGetUploadUrls('application/pdf');
		// this.testGetSubstrates(); 
	}
}

//Handle 'proxy' cmd line arg: -p=<proxy>
function parseArgs() {
	var args = process.argv.slice(2);
	for (var i = 0; i < args.length; i++) {
		var arg = args[i];
		if (arg.startsWith('-p')) {
			var strs = arg.split('=');
			if (strs[1].length > 0) {
				proxy = strs[1];
				return proxy;
			}
		}
	}
	return undefined;
}

function success(response) {
	console.log(JSON.stringify({status: response.statusCode, body: response.body}, null, "  "));
}

function failure(error)	{
	console.log(JSON.stringify({error: error}, null, "  "));
}
