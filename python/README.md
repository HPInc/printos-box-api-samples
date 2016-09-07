#Python

##General Information

Code was written in Python 3.5.2
Uses the "requests" module so that will need to be installed in order to run the code

Windows: Go to location of easy_install.exe

```easy_install.exe requests```

Linux/Mac:

```sudo easy_install requests```

It also uses json, hmac, hashlib, datetime, base64, string, random modules as well. If they aren't found, you may need to install these as well.

##How To Run / Program Information

Run on the command line using ```python box_api.py```

Before you can run the code, you need to provide the Key/Secret (Line 10/11). The initial functions will create a folder, get available substrates and print out the amazon upload/fetch urls. The fetch and upload urls will be used to upload a local file to amazon which can then be uploaded to box. If you already have your file hosted yourself, you will not need to use this function.

The folder id that is needed for the get_folder() function is obtained from the create_folder output. A sample output can be found in [../sample_output/create_folder_output.txt] (https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/create_folder_output.txt) where the id you will use is on line 11.

Uploading a file requires the folder id it will upload to and the url where the file is being hosted on. It is currently defaulted to the amazon fetch url so you will need to change that to your file url if you aren't using the amazon urls. The output for a sample file upload to box can be found in [../sample_output/upload_file_output.txt] (https://github.com/HPInc/printos-box-api-samples/blob/master/sample_output/upload_file_output.txt) where the file id you need for get_file() is on line 7.
