# Postman Collection

## General Information

This is an exported collection for the Postman application (exported as a v2.1 Collection).  It allows you to import a working set of API calls to test the functionality of the current APIs.  Before using this collection you will need to generate a Key/Secret for the Box API from within your PrintOS organization.   Details on this process can be found here: [API Authentication](https://developers.hp.com/printos-hp-indigo-integration-hub/doc/printos-api-authentication)

The Postman application can be downloaded here:  https://www.postman.com/downloads

## How To Run / Program Information

1. Import the "PrintOS Box.postman_collection.json" file through the file -> import dialog of Postman.
3. Import either the "Production Environment.postman_environment.json" or "Staging Environment.postman_environment.json" file through the Manage Environments dialog in the upper right settings menu
	- "Production Environment..." is used for standard PrintOS accounts in the main production environment (most common)
	- "Staging Environment..." is used if you were provided a development account for API development (less common)
3. In the Manage Environments dialog (typically and eye icon) edit the environment you just imported and replace the "key" and "secret" values with the key and secret from the PrintOS account you are using.  Click "Update" to save changes.
4. Select the Environment you just imported in the environment drop-down menu (should be named 'Production Environment' or 'Staging Environment').
5. In the PrintOS Box collection in the left pane select the API call you wish to make then click the "Send" button to send the API call.  

## About the Postman collection

- A Pre-request Script inside the collection uses the CryptoJS library to dynamically generate the authentication HMAC required for all API calls.  
- This Pre-request Script also sets the necessary environment variables which are used in the HTTP Headers section for each call.
- The response field can be used to capture response JSON messages from the Box API calls.

**NOTE:** Some of the API calls such as Box Upload File and Box Query File are dependant on earlier API calls.  You should create at least one Folder before uploading a file, and upload one file before querying a file.  This collection uses the Tests tabs to populate various environments based on the responses from the API calls.
