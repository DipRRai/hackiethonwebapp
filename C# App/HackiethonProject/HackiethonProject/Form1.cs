using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace HackiethonProject
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void btnSubmit_Click(object sender, EventArgs e)
        {
            string dataString = "http://127.0.0.1:5000/stats/" + txtData.Text;
            HttpWebRequest myRequest = (HttpWebRequest)WebRequest.Create(dataString);
            var resp = (HttpWebResponse)myRequest.GetResponse();
        }
    }
}
