# C Sharp

## General Information

Code was written in Visual Studios 2015

NuGet package used
 * Newtonsoft.json 

Package restore should take care of this, but if something occurs and the package doesn't get restored. The version that was used is 9.0.1

## How To Run / Program Information

Program is a Console Application so F5 or clicking Start on the menu bar should build and run the program.

Before you can run the code, you need to provide the Key/Secret. There are two baseUrls provided. Uncomment the one that your Key/Secret was created/provided in.

The initial functions will create a folder, get available substrates and print out the amazon upload/fetch urls. The fetch and upload urls will be used to upload a local file to amazon which can then be uploaded to box. If you already have your file hosted yourself, you will not need to use this function.

The folder id that is needed for the GetFolder() function is obtained from the CreateFolder output. A sample output can be found in [../sample_output/create_folder_output.txt](https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/create_folder_output.txt) where the id you will use is on line 11.

Uploading a file requires the folder id it will upload to and the url where the file is being hosted on. It is currently defaulted to a jpeg url so you will need to change that to your file url or the amazon urls. The output for a sample file upload to box can be found in [../sample_output/upload_file_output.txt](https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/upload_file_output.txt) where the file id you need for GetFile() is on line 7.

Note: The sample output is in python so the initial print statements will be different, but the structure of the JSON should be the same.