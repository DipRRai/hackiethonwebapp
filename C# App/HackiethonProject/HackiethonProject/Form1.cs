using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace HackiethonProject
{
    public partial class Form1 : Form
    {
        private static readonly HttpClient client = new HttpClient();
        public Form1()
        {
            InitializeComponent();
        }

        private async void btnSubmit_Click(object sender, EventArgs e)
        {
            
            var values = new Dictionary<string, string>
            {
                {"hours",  txtHours.Text },
                { "days", txtDays.Text}
            };


            var content = new FormUrlEncodedContent(values);
            var response = await client.PostAsync("http://127.0.0.1:5000/stats/", content);
            var responseString = await response.Content.ReadAsStringAsync();
            MessageBox.Show(responseString);
        }
    }
}
