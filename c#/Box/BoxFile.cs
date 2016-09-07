using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Box
{
    class BoxFile
    {
        public string url { get; set; }
        public string name { get; set; }
        public string notes { get; set; }
        public string folderId { get; set; }
        public string copies { get; set; }
        public string substrate { get; set; }

        public BoxFile(string fileUrl, string fileName, string fId, string numCopies)
        {
            url = fileUrl;
            name = fileName;
            folderId = fId;
            copies = numCopies;
        }
    }
}
