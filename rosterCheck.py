from bs4 import BeautifulSoup
import time
import requests
import smtplib
from email.mime.text import MIMEText

URL1 = "https://estore.skifalls.com.au/WebAdmin/"
URL2 = "https://estore.skifalls.com.au/WebAdmin/instructorTools/processLogin.do"


liftpassNumber = "HFC" + input("Enter lift pass number : HFC")
GMAILusername = input("Enter Gmail username (without @gmail.com): ")
GMAILpassword = input("Enter Gmail password: ")

fromAddress = GMAILusername + "@gmail.com"
toAdress = fromAddress

def sendEmail(sitecontent):
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(GMAILusername, GMAILpassword)
	server.sendmail(fromAddress, toAdress, str(sitecontent))
	server.quit()
	
def getSoup():
	payload = {
			"passNumber": liftpassNumber,
			"password": "moab"
			}
			
	s = requests.session()
	s.get(URL1)
	r1 = s.post(URL2, data = payload)
	soup = BeautifulSoup(r1.text, "html.parser")
	
	if "error" in r1.text:
		print("ERROR")
		soup = "error"
	return soup
	
def changed(sitecontent):
	print("Website Changed")
	sendEmail(sitecontent)
	
	
def mainUpdateCheck():
	siteChanged = False
	gotSiteContent = False
	while siteChanged == False:
		print("Refreshing roster")
	
		newsitecontent = getSoup()
		
		if gotSiteContent == False:
			sitecontent = newsitecontent
			print("Loaded new site content")
			gotSiteContent = True
			print(sitecontent)
			print()
			
		elif newsitecontent != sitecontent:
				print("Connection error")
				if "error" == sitecontent:
					print("Site content changed!")
					siteChanged = True
					changed(newsitecontent)
		else:
			print("Waiting 5 minutes until next refresh.")
			time.sleep(600)
			print()
			
mainUpdateCheck()