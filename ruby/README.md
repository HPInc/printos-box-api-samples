#Ruby

##General Information

Code was written in Ruby 2.3.1

The code uses Net::HTTP and sets the verify_mode to VERIFY_NONE. This is a easy and quick way to bypass verifying TLS certificates. You may want to change this if security is a priority.

##How To Run / Program Information

Run on the command line using ```ruby box_api.rb```

Before you can run the code, you need to provide the Key/Secret. There are two baseUrls provided. Uncomment the one that your Key/Secret was created/provided in.

The initial functions will create a folder.

The fetch and upload urls obtained from get_upload_urls will be used to upload a local file to amazon which can then be uploaded to box. If you already have your file hosted yourself, you will not need to use this function.

The folder id that is needed for the get_folder() function is obtained from the create_folder output. A sample output can be found in [../sample_output/create_folder_output.txt] (https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/create_folder_output.txt) where the id you will use is on line 11.

Uploading (Creating) a file requires the folder id it will upload to and the url where the file is being hosted on. You will need to change the upload url to your file url or the amazon fetch url after uploading your file to the amazon upload url. The output for a sample file upload to box can be found in [../sample_output/upload_file_output.txt] (https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/upload_file_output.txt) where the file id you need for get_file() is on line 7.

Note: The sample output is in python so the initial print statements will be different, but the structure of the JSON should be the same.
