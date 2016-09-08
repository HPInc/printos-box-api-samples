import java.io.File;
import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.FileEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.json.JSONObject;


public class Box {

	//Access Credentials
	//private static String baseUrl = "https://printos.api.hp.com/box"; //use for account on production server
	//private static String baseUrl = "https://stage.printos.api.hp.com/box"; //use for account on staging server
	private static HmacAuth auth;

	public Box(String key, String secret, String algorithm) {
		auth = new HmacAuth(key, secret, algorithm);
	}

	/**
	 * Creates a folder with the specified information in Box
	 * 
	 * @param folderName - Name of folder to create
	 * @param recipient - Name of receiver
	 * @param sender - Name of sender
	 * @return HttpResponse of the POST request
	 * @throws IOException
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 */
	public HttpResponse CreateFolder(String folderName, String recipient, String sender) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		String path = "/api/partner/folder";
		CloseableHttpClient client = HttpClients.createDefault();
		HttpPost request = new HttpPost(baseUrl + path);

		addHeaders(request, "POST", path);

		JSONObject folder = new JSONObject();
		folder.put("name", folderName);
		folder.put("to", recipient);
		folder.put("from", sender);
		
		request.setEntity(new StringEntity(folder.toString(), "UTF-8"));
		
		System.out.println("Creating Folder: " + folderName);
		return client.execute(request);
	}
	
	/**
	 * Gets information about a file in Box
	 * 
	 * @param fileId - Id of the file 
	 * @return HttpResponse of the GET request
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 * @throws IOException
	 */
	public HttpResponse GetFile(String fileId) throws InvalidKeyException, NoSuchAlgorithmException, IOException {
		String path = "/api/partner/file/" + fileId;
		CloseableHttpClient client = HttpClients.createDefault();
		HttpGet request = new HttpGet(baseUrl + path);
		
		addHeaders(request, "GET", path);
		
		System.out.println("Getting File with ID: " + fileId);
		return client.execute(request);
	}
	
	/**
	 * Gets information about a folder in Box
	 * 
	 * @param folderId - Id of the folder
	 * @return HttpResponse of the GET request
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 * @throws IOException
	 */
	public HttpResponse GetFolder(String folderId) throws InvalidKeyException, NoSuchAlgorithmException, IOException {
		String path = "/api/partner/folder/" + folderId;
		CloseableHttpClient client = HttpClients.createDefault();
		HttpGet request = new HttpGet(baseUrl + path);
		
		addHeaders(request, "GET", path);
		
		System.out.println("Getting Folder with ID: " + folderId);
		return client.execute(request);
	}
	
	/**
	 * Gets the list of available substrates set in Box
	 * 
	 * @return HttpResponse of the GET request
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 * @throws IOException
	 */
	public HttpResponse GetSubstrates() throws InvalidKeyException, NoSuchAlgorithmException, IOException {
		String path = "/api/partner/substrate";
		CloseableHttpClient client = HttpClients.createDefault();
		HttpGet request = new HttpGet(baseUrl + path);
		
		addHeaders(request, "GET", path);
		
		System.out.println("Getting list of Substrates ");
		return client.execute(request);
	}
	
	/**
	 * Gets the amazon aws upload urls for a file
	 * 
	 * @param mimeType - MIME type of file to upload
	 * @return HttpResponse of the GET request
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 * @throws IOException
	 */
	public HttpResponse GetUploadUrls(String mimeType) throws InvalidKeyException, NoSuchAlgorithmException, IOException {
		String path = "/api/partner/file/uploadurls";
		CloseableHttpClient client = HttpClients.createDefault();
		String mimeParam = "?mimeType=" + mimeType;
		HttpGet request = new HttpGet(baseUrl + path + mimeParam);
		
		addHeaders(request, "GET", path);
		
		System.out.println("Getting AWS upload urls");
		return client.execute(request);
	}
	
	/**
	 * Upload a file to a specified folder in Box
	 * 
	 * @param folderId - Id of the folder to upload to
	 * @param fileUrl - Url of the file (not a local path)
	 * @return HttpResponse of the POST request
	 * @throws IOException
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 */
	public HttpResponse UploadFile(String folderId, String fileUrl) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		String path = "/api/partner/file";
		CloseableHttpClient client = HttpClients.createDefault();
		HttpPost request = new HttpPost(baseUrl + path);
		
		addHeaders(request, "POST", path);

		JSONObject file = new JSONObject();
		file.put("url", fileUrl);
		file.put("name", "Java_File.pdf");
		file.put("notes", "File was uploaded using Java");
		file.put("folderId", folderId);
		file.put("copies", 100);
		
		request.setEntity(new StringEntity(file.toString(), "UTF-8"));
		
		System.out.println("Uploading file: " + fileUrl);
		return client.execute(request);
	}
	
	/**
	 * Uploads a file to an amazon aws upload url
	 * 
	 * @param amazonUrl - amazon upload url
	 * @param file - local file to upload to amazon
	 * @param contentType - MIME type of the file
	 * @return HttpRequest of the PUT request
	 * @throws IOException
	 */
	public HttpResponse UploadFileToAws(String amazonUrl, String file, String contentType) throws IOException {
		CloseableHttpClient client = HttpClients.createDefault();
		HttpPut request = new HttpPut(amazonUrl);
		
		HttpEntity entity = new FileEntity(new File(file));
		request.setEntity(entity);
		request.addHeader("Content-Type", contentType);

		System.out.println("Upload file: " + file + " to amazon aws");
		return client.execute(request);
	}
	
	/**
	 * Adds the headers to an HttpRequest
	 * 
	 * @param request - request to add the headers to
	 * @param method - type of request (GET, POST, PUT)
	 * @param path - the path the request is sent to (doesn't include baseUrl)
	 * @throws InvalidKeyException
	 * @throws NoSuchAlgorithmException
	 */
	private void addHeaders(HttpRequest request, String method, String path) throws InvalidKeyException, NoSuchAlgorithmException {
		request.addHeader("Content-Type", "application/json");
		request.addHeader("x-hp-hmac-authentication", auth.getHmacAuthentication(method, path));
		request.addHeader("x-hp-hmac-date", auth.getTimestamp());
	}
}
