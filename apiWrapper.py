#!/usr/bin/python
from apiCredentials import ApiCredentials
import base64
import hashlib
import random
from datetime import datetime
import time
import requests

class AnalyticsAPI(ApiCredentials):
    """
    Class to interact with the API for Adobe Analytics
    """
    def __init__(self, config_file):
        ApiCredentials.__init__(self, config_file)
        self.ENDPOINT_ERROR = "Invalid company specified."
        self.ENDPOINT_NO_COMPANY = "Company is a required parameter"

    def getEndpoint(self):
        company = self.webServicesUsername.split(":")[1]
        endpoint = self.invoke("Company.GetEndpoint", {"company": company})
        if endpoint.find(self.ENDPOINT_ERROR) > -1:
            raise BadCompanyError(company)
        elif endpoint.find(self.ENDPOINT_NO_COMPANY) > -1:
            raise BadCompanyError("[Company Null]")
        else:
            return endpoint

    @staticmethod
    def generateHeader(self, username, shared_secret):
        header = ""
        rand = int(random.random()*1000000000000)
        #print rand
        nonce = hashlib.md5(str(rand)).digest() #find a better random number generator
        created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        passwordDigest = base64.b64encode(hashlib.sha1(str(nonce)+str(created)+str(shared_secret)).digest())
        header += 'UsernameToken Username="'+username+'", '
        header += 'PasswordDigest="' + passwordDigest + '", '
        header += 'Nonce="'+base64.b64encode(nonce)+'", '
        header += 'Created="'+created+'" '
        #print header
        return header

    def invoke(self, method, params, api_end_point_label=None):
        if api_end_point_label:
            endpoint = self.getApiEndPoint(api_end_point_label)
        else:
            endpoint = self.default_api_end_point
        endpoint += "?method="+str(method)
        headers = {"X-WSSE": self.generateHeader(self, self.webServicesUsername, self.webServicesSharedSecret)}
        r = requests.post(endpoint, data=params, headers=headers)
        return r.text

class BadCompanyError(Exception):
    def __init__(self, company):
        self.company = company

    def __str__(self):
        return repr(self.company) + " Doesn't appear to be valid"
