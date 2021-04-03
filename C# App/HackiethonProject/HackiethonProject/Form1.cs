using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Web.Script.Serialization;
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

        private async void btnLogin_Click(object sender, EventArgs e)
        {
            var values = new Dictionary<string, string>
            {
                {"username",  txtUsername.Text },
                { "password", txtPassword.Text}
            };


            var content = new FormUrlEncodedContent(values);
            var response = await client.PostAsync("http://127.0.0.1:5000/login_client", content);
            var responseString = await response.Content.ReadAsStringAsync();
            if (responseString == "success")
            {
                lblLoginStatus.Text = "Welcome, " + txtUsername.Text;
                MessageBox.Show("Successfully logged in");
            }
            else
            {
                MessageBox.Show("Failed to login ");
            }
            
        }
    }
}
