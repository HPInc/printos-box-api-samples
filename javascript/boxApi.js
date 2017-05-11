// © Copyright 2016 HP Development Company, L.P.
// SPDX-License-Identifier: MIT

var printOSClientPath = printOSClientPath || './printOSClient'; 
var PrintOSClient = require(printOSClientPath);

function BoxApi(baseUrl, key, secret, proxy) {

	var printOSClient = new PrintOSClient(baseUrl, key, secret, proxy);

	this.createFolder = function(fname, recipient, sender) {
		console.log("Creating folder ", fname);
		var payload = {'name':fname, 'from':sender, 'to':recipient};
		return printOSClient.post('/api/partner/folder', payload);
	}

	this.createFolderWithFiles = function(fname, recipient, sender) {
		console.log("Creating folder with files");
		var payload = {
			name: fname,
			from: sender,
			to: recipient,
			files: [{
				name: "JavaScript_File1.pdf",
				copies: 1,
				notes: "JavaScript_File1 was uploaded using JavaScript",
				url: "FileUrl1" 
			}, {
				name: "JavaScript_File2.pdf",
				copies: 1,
				notes: "JavaScript_File2 was uploaded using JavaScript",
				url: "FileUrl2" 
			}]
		}
		return printOSClient.post('/api/partner/folder', payload);
	}
	
	this.getFile = function(id) {
		console.log("Getting file " + id);
		return printOSClient.get('/api/partner/file/' + id);
	}

	this.getFolder = function(id) {
		console.log("Getting folder " + id);
		return printOSClient.get('/api/partner/folder/' + id);
	}

	this.getUploadUrls = function(mimeType) {
		console.log("Getting upload urls");
		return printOSClient.get('/api/partner/file/uploadurls', query_params = {'mimeType':mimeType});
	}
	
	this.getSubstrates = function() {
		console.log("Getting list of substrates");
		return printOSClient.get('/api/partner/substrate');
	}

	this.uploadFile = function(url, name, folderId, copies, notes) {
		console.log("Creating file", url);
		var payload = {'url':url, 'name':name, 'folderId':folderId, 'copies':copies, 'notes':notes }
		return printOSClient.post('/api/partner/file', payload);
	}
}

module.exports = BoxApi;