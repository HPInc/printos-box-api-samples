# PHP

## General Information

Code was written in PHP 5.6.24

## How To Run / Program Information

Installing XAMPP and adding the box_api.php file to the htdocs folder is a quick way to run the code.

Before you can run the code, you need to provide the Key/Secret. There are two baseUrls provided. Uncomment the one that your Key/Secret was created/provided in.

The initial functions will create a folder.

The fetch and upload urls obtained from getUploadUrls will be used to upload a local file to amazon which can then be uploaded to box. If you already have your file hosted yourself, you will not need to use this function.

The folder id that is needed for the getFolder() function is obtained from the createFolder output. A sample output can be found in [../sample_output/create_folder_output.txt](https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/create_folder_output.txt) where the id you will use is on line 11.

Uploading (Creating) a file requires the folder id it will upload to and the url where the file is being hosted on. You will need to change the upload url to your file url or the amazon fetch url after uploading your file to the amazon upload url. The output for a sample file upload to box can be found in [../sample_output/upload_file_output.txt](https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/upload_file_output.txt) where the file id you need for getFile() is on line 7.

Note: The sample output is in python so the initial print statements will be different, but the structure of the JSON should be the same.
