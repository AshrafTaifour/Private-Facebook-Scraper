# Automated Social Media Spear-Phisher 
## Authors: 
- Abdullah Arif
- Abdullah Chattha
- Ashraf Taifour
- Mohamad Elchami
- Steve Pham

## Supervisor
    Dr. Sherif Saad Ahmed

## Adding packages
	Don't forget to `pip3 freeze > requirements.txt` - after installing packages in virtual environment

## How to run
Program has been tested on Linux

1. Setup
* Make sure you have gecko driver installed: https://github.com/mozilla/geckodriver/releases
* Also, install TOR: https://www.torproject.org/download/ 
* Extract TorFolder to program directory
2. Putting in login information
* Navigate to the secretDirectory/secret.py file and put in your email, password and username
3. Recommended step: use virtual environment
```
python3 -m venv facebookEnv
source facebookEnv/bin/activate
```
4. Install dependencies 
`pip3 install -r requirements.txt`

5. Run program
    `python3 main.py`

# What is this? 🤔
This repository is a subsection of our automated spear-phishing project, the full project scope can be viewed at https://github.com/Abdullah-chattha/Fb-Twitter-gui. The focus of this repository is the Facebook webscraping component of the project. This program logins to a Facebook account, views the friend's list of the Facebook account and saves all the URLs of those friends. It then iterates through each friend's URL and obtains their "likes" page. This "likes" pages is then parsed for interests (the nature of the liked page) and the name of the liked page itself. This will be data that can be stored in multiple formats (HTML or CSV) which will be used to create a phishing message that can be sent to the victim with a URL to click, the URL will be a link to educate the victim about spear-phishing attacks.

# General Scope of the Project

Phishing attacks accounted for 80% of security incidents [[2](https://www.csoonline.com/article/3153707/top-cybersecurity-facts-figures-and-statistics.html)]. And the pandemic has increased the number of cyber attacks[[5](https://www.who.int/news-room/detail/23-04-2020-who-reports-fivefold-increase-in-cyber-attacks-urges-vigilance)]. So, it is imperative that we study different social attacks. There is a more potent type of phishing called “spear-phishing”, where an attacker gathers information about a user and uses that to craft a more persuasive message. This technique has a much higher click through rate than average phishing attacks. Fortunately, this method is time-consuming and so the attacker cannot target as many people. However, we believe that you can use machine learning to automate this process. If this process becomes widespread, it would have disastrous consequences.

Our project will be to create this automated spear-phishing tool. We will then use our tool to analyze them to determine the effectiveness of various algorithms and the vulnerability on different platforms. We also hope to show the potency of this attack. So, we will compare it to normal phishing attacks and compare the results. We hope the results from our study will help future developers and cybersecurity researchers to create more effective safeguards against social attacks.

Most malware comes from email. However, there is a rising trend for phishing attacks conducted on social media. This is because social media contains a plethora of personal information which makes it possible to launch this type of automated spear-phishing attack.

Rather than creating a defensive tool like a phishing detector using machine learning, we have created an offensive tool. This is because when people are trying to break things, they look for the easiest ways to get the job done. The principle of easiest penetration states that a security system is as strong as its weakest link. So by thinking like an attacker, we can become better defenders.

# Potential improvements to this project
Our main goal for improvement is to create an NLP model for the creation of phishing messages using a user's interests as input. The interests can be expanded to include various pages that include important information about a user's behavior. This includes but is not limited to, Check-ins, Sports, Music, Movies, Books, Games, Posts by a user, etc.

[1]: https://www.fundera.com/resources/small-business-cyber-security-statistics \
[2]: https://www.csoonline.com/article/3153707/top-cybersecurity-facts-figures-and-statistics.html \
[3]: https://enterprise.verizon.com/resources/reports/dbir/2020/results-and-analysis/ \
[4]: https://www.phishingbox.com/news/phishing-news/internet-security-threat-report-irst-2019. \
[5]: https://www.who.int/news-room/detail/23-04-2020-who-reports-fivefold-increase-in-cyber-attacks-urges-vigilance 
