# Java

## General Information

Code was written in Eclipse Neon

External libraries used:
 * Apache HttpComponents (last tested with version 4.5.13)
 * org.json  (last tested with version 20140107)

The JAR files to the libraries are not included. You will need to download and configure the jars to your build path to compile and run the project. You may also use different libraries to create the needed JSON strings and Http requests.

## How To Run / Program Information

The Box_Example.java class is the one that you will run.

Before you can run the code, you need to provide the Key/Secret. The Box.java class has two baseUrls. The production URL is used by default and should be used for most PrintOS customers.  If you were provided a development account in the staging environment then use the staging URL.

The initial methods will create a folder, get available substrates and print out the amazon upload/fetch urls. The fetch and upload urls will be used to upload a local file to amazon which can then be uploaded to box. If you already have your file hosted yourself, you will not need to use this method.

The folder id that is needed for the GetFolder() method is obtained from the CreateFolder output. A sample output can be found in [../sample_output/create_folder_output.txt](https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/create_folder_output.txt) where the id you will use is on line 11.

Uploading a file requires the folder id it will upload to and the url where the file is being hosted on. It is currently defaulted to a jpeg url so you will need to change that to your file url or the amazon urls. The output for a sample file upload to box can be found in [../sample_output/upload_file_output.txt](https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/upload_file_output.txt) where the file id you need for GetFile() is on line 7.

Note: The sample output is in python so the initial print statements will be different, but the structure of the JSON should be the same.
