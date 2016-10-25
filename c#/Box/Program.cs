// © Copyright 2016 HP Development Company, L.P.
// SPDX-License-Identifier: MIT

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace Box
{
    class Program
    {
        //Access Credentials
        //private static string baseUrl = "https://printos.api.hp.com/box"; //use for production server account
        //private static string baseUrl = "https://stage.printos.api.hp.com/box"; // use for staging server account
        private static string key = "";
        private static string secret = "";

        //amazon urls 
        private static string amazonFetch = "";
        private static string amazonUpload = "";
        private static string fileUrl = "http://www.w3schools.com/html/pic_mountain.jpg"; 

        private static string fileToUpload = "C:\\FilePath\\FileName.pdf"; //your local file to upload to the amazon upload url

        static void Main(string[] args)
        {
            RunAsync().Wait();

            Console.WriteLine("All Tasks Complete. Press any key to stop...");
            Console.ReadKey();
        }

        static async Task RunAsync()
        {
            await CreateFolder("CSharp_Folder", "CSharp_Receiver", "CSharp_Sender"); WaitBeforeProceeding();
            //await GetFolder("FolderId"); WaitBeforeProceeding();
            await GetSubstrates(); WaitBeforeProceeding();
            await GetUploadUrls("application/pdf"); WaitBeforeProceeding();
            //await UploadFileToAWS(fileToUpload, "application/pdf"); WaitBeforeProceeding();
            //await UploadFileToBox("FolderId", fileUrl); WaitBeforeProceeding();
            //await GetFile("FileId"); WaitBeforeProceeding();
        }

        //Helper methods below
        /*------------------------------------------------------------------------------------*/

        /// <summary>
        /// Creates and adds the Hmac headers to a client
        /// </summary>
        /// <param name="method">Type of Http method (GET, POST, PUT)</param>
        /// <param name="path">Endpoint which the method will hit</param>
        /// <param name="client">HttpClient to have the headers added to</param>
        private static void CreateHmacHeaders(string method, string path, HttpClient client)
        {
            string timeStamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");

            string stringToSign = method + " " + path + timeStamp;
            HMACSHA1 hmac = new HMACSHA1(Encoding.UTF8.GetBytes(secret));
            byte[] bytes = hmac.ComputeHash(Encoding.UTF8.GetBytes(stringToSign));
            string signature = BitConverter.ToString(bytes).Replace("-", string.Empty).ToLower();
            string auth = key + ":" + signature;

            client.DefaultRequestHeaders.Add("x-hp-hmac-authentication", auth);
            client.DefaultRequestHeaders.Add("x-hp-hmac-date", timeStamp);
            client.DefaultRequestHeaders.Add("x-hp-hmac-algorithm", "SHA1");
        }

        private static void WaitBeforeProceeding()
        {
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

        //Methods for APIs Below
        /*------------------------------------------------------------------------------------*/

        /// <summary>
        /// Creates a folder within the Box application
        /// </summary>
        /// <param name="folderName">Name of the folder</param>
        /// <param name="recipient">Name of receiver</param>
        /// <param name="sender">Name of sender</param>
        /// <returns></returns>
        private static async Task CreateFolder(string folderName, string recipient, string sender)
        {
            Console.WriteLine("Creating folder with name: "  + folderName);
            using (var client = new HttpClient())
            {
                CreateHmacHeaders("POST", "/api/partner/folder", client);
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                Folder folder = new Folder();
                folder.name = folderName;
                folder.to = recipient;
                folder.from = sender;

                string folderJson = JsonConvert.SerializeObject(folder);
                HttpResponseMessage response = await client.PostAsync(baseUrl + "/api/partner/folder", new StringContent(folderJson, Encoding.UTF8, "application/json"));
                
                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("\nSuccess. Folder was created.\n");
                    string info = await response.Content.ReadAsStringAsync();
                    JObject json = JObject.Parse(info);
                    string infoFormatted = json.ToString();
                    Console.WriteLine(infoFormatted);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to create folder");
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }

        /// <summary>
        /// Gets information about a file in Box
        /// </summary>
        /// <param name="fileId">Id of the file</param>
        /// <returns></returns>
        private static async Task GetFile(string fileId)
        {
            Console.WriteLine("Getting file with ID: " + fileId);
            using (var client = new HttpClient())
            {
                CreateHmacHeaders("GET", "/api/partner/file/" + fileId, client);

                HttpResponseMessage response = await client.GetAsync(baseUrl + "/api/partner/file/" + fileId);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("\nSuccess. File was found.\n");
                    string info = await response.Content.ReadAsStringAsync();
                    JObject json = JObject.Parse(info);
                    string infoFormatted = json.ToString();
                    Console.WriteLine(infoFormatted);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to find File " + fileId);
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }

        /// <summary>
        /// Gets information about a folder in Box
        /// </summary>
        /// <param name="folderId">Id of the folder</param>
        /// <returns></returns>
        private static async Task GetFolder(string folderId)
        {
            Console.WriteLine("Getting folder with ID: " + folderId);
            using (var client = new HttpClient())
            {
                CreateHmacHeaders("GET", "/api/partner/folder/" + folderId, client);

                HttpResponseMessage response = await client.GetAsync(baseUrl + "/api/partner/folder/" + folderId);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("\nSuccess. Folder was found.\n");
                    string info = await response.Content.ReadAsStringAsync();
                    JObject json = JObject.Parse(info);
                    string infoFormatted = json.ToString();
                    Console.WriteLine(infoFormatted);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to get folder " + folderId);
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }

        /// <summary>
        /// Gets the list of available substrates set in Box
        /// </summary>
        /// <returns></returns>
        private static async Task GetSubstrates()
        {
            Console.WriteLine("Getting list of substrates");
            using (var client = new HttpClient())
            {
                CreateHmacHeaders("GET", "/api/partner/substrate", client);

                HttpResponseMessage response = await client.GetAsync(baseUrl + "/api/partner/substrate");

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Success. Substrates found.");
                    string info = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(info);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to get list of substrates.");
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }

        /// <summary>
        /// Gets the amazon aws upload urls for a certain filetyple
        /// </summary>
        /// <param name="mimeType">MIME type of the file to upload</param>
        /// <returns></returns>
        private static async Task GetUploadUrls(string mimeType)
        {
            Console.WriteLine("Getting upload urls");
            using (var client = new HttpClient())
            {
                CreateHmacHeaders("GET", "/api/partner/file/uploadurls", client);
                string mimeTypeQuery = "?mimeType=" + mimeType;

                HttpResponseMessage response = await client.GetAsync(baseUrl + "/api/partner/file/uploadurls" + mimeTypeQuery);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("\nSuccess. Upload urls obtained.\n");
                    string info = await response.Content.ReadAsStringAsync();
                    JObject json = JObject.Parse(info);
                    string infoFormatted = json.ToString();
                    Console.WriteLine(infoFormatted);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to obtain upload urls.");
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }

        /// <summary>
        /// Uploads a file to an amazon aws upload url
        /// </summary>
        /// <param name="file">local file to upload</param>
        /// <param name="contentType">Content-Type of file (should be same as mimetype you passed in to get uploadurls)</param>
        /// <returns></returns>
        private static async Task UploadFileToAWS(string file, string contentType)
        {
            Console.WriteLine("Uploading file: " + file + " to AWS.");

            using (var client = new HttpClient())
            {
                HttpContent content = new StreamContent(File.OpenRead(file));
                content.Headers.Add("Content-Type", contentType);

                HttpResponseMessage response = await client.PutAsync(amazonUpload, content);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Success. File was uploaded to AWS.");
                    Console.WriteLine(response.StatusCode);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to upload file to AWS.");
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }

        /// <summary>
        /// Upload a file to a specified folder in Box
        /// </summary>
        /// <param name="folderId">Id of the folder to upload to</param>
        /// <param name="fileUrl">Url of the file (not a local path)</param>
        /// <returns></returns>
        private static async Task UploadFileToBox(string folderId, string fileUrl)
        {
            Console.WriteLine("Uploading file: " + fileUrl + " to Box.");

            using (var client = new HttpClient())
            {
                CreateHmacHeaders("POST", "/api/partner/file", client);
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                BoxFile file = new BoxFile(fileUrl, "CSharp_File.pdf", folderId, "10");
                file.notes = "File was uploaded using CSharp";

                string fileJson = JsonConvert.SerializeObject(file);
                HttpResponseMessage response = await client.PostAsync(baseUrl + "/api/partner/file", new StringContent(fileJson, Encoding.UTF8, "application/json"));

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("\nSuccess. File was uploaded to Box.\n");
                    string info = await response.Content.ReadAsStringAsync();
                    JObject json = JObject.Parse(info);
                    string infoFormatted = json.ToString();
                    Console.WriteLine(infoFormatted);
                }
                else
                {
                    Console.WriteLine("Failure. Unable to upload file to Box.");
                    Console.WriteLine(response.ReasonPhrase);
                }
            }
        }
    }
}
