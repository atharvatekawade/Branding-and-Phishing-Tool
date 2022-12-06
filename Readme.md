# Branding and Phishing Tool

This was a project as part of our Design Practises course CSP 290 under guide Dr. Gaurav Varhsney. This is a fullstack app built in react and django. It consists various modules listed below:
1) Monitoring: This module is used to watch out for competitor brands which try to copy your brand. Begin by entering the website you wish to monitor. The algorithm will extract the domain name and generate similar looking domain names using techniques such as: Vowel swapping, Letter Replacement, Bitsquatting, etc. Then depending on the threshold for similarity entered, it will show all websites with similar domain and content atleast similar as threshold set. You can leave the threshold blank, it will use the default value. The similarity is calculated using TfIDF method.

![Picture1](https://user-images.githubusercontent.com/64606981/205916254-d4598ce1-ca35-43dc-aad1-728fc1ffd73a.jpeg)

2) Phishing Detection: This module is used to detect if a particular website is phishing or not. I use a two-layer approach to efficiently detect if the webiste is phishing or not.
a) Search Engine: First a Search Engine based scheme to check if the site is indexed by popular search engines like Google, Bing. If this is the case, based on the trust we have on them, we flag the website as not phishing.
b) Machine Learning Based: It may be the case that some new genuine sites yet not indexed by search engines are not phishing. Flagging them phishing only based on search engine indexing is inaacurate. For them, I used Random Forest Classifier based certain features extracted from the web site such as HTML src attributes, domain name, SSL certificate details, etc. If the prediction is phishing, only then the website is flagged as phishing. In this case, alternate URLS are suggested with similar domain and co-doamin names. The similar names are generated by the technique used for monitoring sites described above.

## References

I used the following two papers for my study:
1) A survey and classification of web phishing detection schemes by Gaurav Varshney, Manoj Misra, Pradeep K. Atrey: https://onlinelibrary.wiley.com/doi/abs/10.1002/sec.1674
2) Phishing Websites Features by Rami M. Mohammad, Fadi Thabtah, Lee McCluskey: https://ieeexplore.ieee.org/abstract/document/6470857
