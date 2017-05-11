// © Copyright 2016 HP Development Company, L.P.
// SPDX-License-Identifier: MIT

import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.ParseException;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

public class Box_Example {

	//Access Credentials
	private static String key = "";
	private static String secret = "";
	private static Box box;

	//amazon urls 
	private static String amazonUpload = "";
    private static String amazonFetch = "";

    private static String fileToUpload = "C:\\FilePath\\FileName.pdf";
    private static String fileUrl = "http://www.w3schools.com/html/pic_mountain.jpg";
	
	public static void main(String[] args) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		box = new Box(key, secret, "HmacSHA1");

		printInfo( box.CreateFolder("Java_Folder", "Java_Receiver", "Java_Sender"), true );
//		printInfo( box.CreateFolderWithFiles("Java_Folder", "Java_Receiver", "Java_Sender"), true);
//		printInfo( box.GetFolder("FolderId"), true );
		printInfo( box.GetSubstrates(), false );
		printInfo( box.GetUploadUrls("application/pdf"), true );
//		printInfo( box.UploadFileToAws(amazonUpload, fileToUpload, "application/pdf"), false);
//		printInfo( box.UploadFile("FolderId", fileUrl), true );
//		printInfo( box.GetFile("FileId"), true);
	}

	/**
	 * Prints the body of a HttpResponse in a "pretty" format. Information printed is determined
	 * on whether the body is expected to be JSON or regular format.
	 * 
	 * @param response - Response with information to output
	 * @param JsonResponse - Determines if response entity is expected to have JSON output 
	 * @throws ParseException
	 * @throws IOException
	 */
	private static void printInfo(HttpResponse response, boolean JsonResponse) throws ParseException, IOException {
		System.out.println(response.getStatusLine().getStatusCode() + " : " + response.getStatusLine().getReasonPhrase());
		HttpEntity entity = response.getEntity();
		String body = EntityUtils.toString(entity, "UTF-8");
		if(JsonResponse) {
			JSONObject formatted = new JSONObject(body);
			System.out.print("RESPONSE: ");
			System.out.println(formatted.toString(4));
		} else {
			System.out.println(body);
		}
	}

}
