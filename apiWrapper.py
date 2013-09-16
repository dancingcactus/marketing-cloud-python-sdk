import base64
import hashlib
import random
from datetime import datetime
import time
import requests

class AnalyticsAPI:
	"""
	Class to interact with the API for Adobe Analytics
	"""
	username = ""
	password = ""
	endpoint = ""
	defaultEndpoint = "https://api.omniture.com/admin/1.3/rest/"
	ENDPOINT_ERROR = "Invalid company specified."
	ENDPOINT_NO_COMPANY = "Company is a required parameter"

	def __init__(self,username,password):
		self.config(username,password)
	
	def getUsername (self):
		return self.username
		
	def setUsername (self, username):
		self.username = username
		endpoint = self.getEndpoint(username)
		
		
	def getPassword (self):
		return self.password
		
	def setPassword (self, password):
		self.password = password
		
	def config (self, username, password):
		self.setUsername(username)
		self.setPassword(password)
		
	def getEndpoint(self, username):
		company = username.partition(":")
		company = company[2]
		endpoint = self.invoke("Company.GetEndpoint",{"company":company})
		if endpoint.find(self.ENDPOINT_ERROR) > -1:	
			raise BadCompanyError(company)
		elif endpoint.find(self.ENDPOINT_NO_COMPANY) >-1:
			raise BadCompanyError("[Company Null]");
		else:
			return endpoint
			
		
	@staticmethod	
	
	def generateHeader(username, password):
		header = ""
		rand = int(random.random()*1000000000000)
		#print rand
		nonce = hashlib.md5(str(rand)).digest() #find a better random number generator
		created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		passwordDigest = base64.b64encode(hashlib.sha1(str(nonce)+str(created)+str(password)).digest())
		
		#print "Nonce"
		#print nonce
		
		header += 'UsernameToken Username="'+username+'", '
		header += 'PasswordDigest="' + passwordDigest + '", '
		header += 'Nonce="'+base64.b64encode(nonce)+'", '
		header += 'Created="'+created+'" '
		#print header
		return header	


	def invoke(self,method, params):
		if self.endpoint:
			endpoint = self.endpoint
		else:
			endpoint = self.defaultEndpoint
		
		endpoint += "?method="+str(method)
		headers = {"X-WSSE":AnalyticsAPI.generateHeader(self.getUsername(), self.getPassword())}
			
		r = requests.post(endpoint,data=params, headers=headers)			
		
		return r.text
	
class BadCompanyError(Exception):
	def __init__(self, company):
		self.company = company
	
	def __str__(self):
		return repr(self.company) + " Doesn't appear to be valid"
