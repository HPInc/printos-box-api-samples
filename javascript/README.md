# JavaScript

## General Information

Tested and run with Node.js version 16.13.0 

The modules that the code requires can be installed using npm. You can download Nodejs which comes with npm together with it.

Modules required:
* superagent 
* superagent-proxy

Install modules using:
> npm install {module name}

## How To Run / Program Information

Run on the command line using:
> node app.js

Before you can run the code, you need to provide the Key/Secret in app.js. There are two baseUrls provided. Uncomment the one that your Key/Secret was created/provided in (by default this is https://printos.api.hp.com ).

If you are running behind a web proxy you should run the program with a -p={web proxy}:{port} argument like this:
> node app.js -p=http://web-proxy:8080

Comment or un-comment function calls in app.js to make the API calls you want

The fetch and upload urls obtained from GetUploadUrls will be used to upload a local file to amazon which can then be uploaded to box. If you already have your file hosted yourself, you will not need to use this function.
