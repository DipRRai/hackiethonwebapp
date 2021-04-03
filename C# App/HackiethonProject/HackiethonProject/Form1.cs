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

        public Dictionary<string, float> timeDict = new Dictionary<string, float> { };
        public float globalTimeCount = 0;
        public bool isLoggedIn = false;

        
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
                isLoggedIn = true;
                //btnUpdate.Enabled = true;

                var values_time = new Dictionary<string, string>
                {
                    {"placeholder",  "placeholder"},
                };


                var content_time = new FormUrlEncodedContent(values_time);
                var response_time = await client.PostAsync("http://127.0.0.1:5000/get_timestats", content_time);
                var responseString_time = await response_time.Content.ReadAsStringAsync();
                string[] entries = responseString_time.Split('|');
                Dictionary<string, float> temp = new Dictionary<string, float> { };
                foreach (string entry in entries)
                {
                    if (entry.Length == 0)
                    {
                        continue;
                    }
                    else
                    {
                        string[] pair = entry.Split('~');
                        string day = pair[0];
                        float timeCount = float.Parse(pair[1]);
                        temp[day] = timeCount;
                    }
                }
                timeDict = temp;
            }
            else
            {
                MessageBox.Show("Failed to login ");
            }
            
        }

        private async void Form1_Load(object sender, EventArgs e)
        {
            //btnUpdate.Enabled = false;
        }

        private async void tmrCounter_Tick(object sender, EventArgs e)
        {
            globalTimeCount += 1;
            if (isLoggedIn)
            {
                DateTime localDate = DateTime.Now;
                string dateString = localDate.Day + ":" + localDate.Month + ":" + localDate.Year;
                if (timeDict.ContainsKey(dateString))
                {
                    timeDict[dateString] += globalTimeCount;
                }
                else
                {
                    timeDict[dateString] = globalTimeCount;
                }

                string userTimeStat = "";

                foreach (KeyValuePair<string, float> kvp in timeDict)
                {
                    userTimeStat = userTimeStat + kvp.Key.ToString() + "~" + kvp.Value.ToString() + "|";
                }

                var values = new Dictionary<string, string>
                {
                    {"stats",  userTimeStat}
                };


                var content = new FormUrlEncodedContent(values);
                var response = await client.PostAsync("http://127.0.0.1:5000/stats/", content);
                var responseString = await response.Content.ReadAsStringAsync();
                //MessageBox.Show(responseString);
                
            }
        }
    }
}
