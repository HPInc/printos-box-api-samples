// © Copyright 2016 HP Development Company, L.P.
// SPDX-License-Identifier: MIT

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Box
{
    class Folder
    {
        public string name { get; set; }
        public string from { get; set; }
        public string to { get; set; }
        public List<BoxFile> files { get; set; }

        public Folder() {
            files = new List<BoxFile>();
        }
    }
}
