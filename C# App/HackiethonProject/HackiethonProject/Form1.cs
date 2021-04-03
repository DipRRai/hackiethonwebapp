using System;
using System.Collections.Generic;
using System.Diagnostics;
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

                //App time collection

                Dictionary<string, float> appDict = new Dictionary<string, float> { };

                var content_app = new FormUrlEncodedContent(values);
                var response_app = await client.PostAsync("http://127.0.0.1:5000/get_appstats", content_app);
                var responseString_app = await response_app.Content.ReadAsStringAsync();
                string[] entries = responseString_app.Split('|');
                string[] firstEntry = entries[0].Split('~');

                if (firstEntry[0] != "datetime")
                {
                    string appString = "datetime~" + dateString+ "|" + responseString_app;

                    var values_app = new Dictionary<string, string>
                    {
                        {"appstats", appString}
                    };

                    content_app = new FormUrlEncodedContent(values_app);
                    response_app = await client.PostAsync("http://127.0.0.1:5000/stats/", content_app);
                    responseString_app = await response_app.Content.ReadAsStringAsync();
                }
                else
                {
                    int count = 0;
                    bool isNewDay = false;
                    richTextBox1.Text += string.Join(",", entries) + '\n';
                    foreach (string entry in entries)
                    {
                        if (entry.Length == 0)
                        {
                            continue;
                        }

                        if (count == 0)
                        {
                            string serverDate = entry.Split('~')[1];
                            //MessageBox.Show(serverDate + " " + dateString);
                            if (serverDate != dateString)
                            {
                                isNewDay = true;
                            }
                        }
                        else
                        {
                            if (isNewDay)
                            {
                                string[] pair = entry.Split('~');
                                string appName = pair[0];
                                float timeCount = 0;
                                appDict[appName] = 0;
                            }
                            else
                            {
                                string[] pair = entry.Split('~');
                                string appName = pair[0];
                                float timeCount = float.Parse(pair[1]);
                                appDict[appName] = timeCount;
                                foreach (Process p in Process.GetProcesses())
                                {
                                    if (p.ProcessName.ToLower() == appName.ToLower())
                                    {
                                        appDict[appName] += 1;
                                        break;
                                    }
                                }
                            }
                        }
                        count++;
                    }

                    string userAppStat = "datetime~" + dateString + "|";
                    foreach (KeyValuePair<string, float> kvp in appDict)
                    {
                        userAppStat = userAppStat + kvp.Key.ToString() + "~" + kvp.Value.ToString() + "|";
                    }

                    //MessageBox.Show(userAppStat);

                    var values_app = new Dictionary<string, string>
                    {
                        {"appstats", userAppStat}
                    };

                    content_app = new FormUrlEncodedContent(values_app);
                    response_app = await client.PostAsync("http://127.0.0.1:5000/stats/", content_app);
                    responseString_app = await response_app.Content.ReadAsStringAsync();
                }
            }
        }
    }
}
