#!/usr/bin/python

import urllib, urllib2, base64
import httplib2


class RightScale(object):
	
	def __init__(self, username, password, account):
		self.username = username
		self.password = password
		self.account = account
		self.resource_url = 'https://my.rightscale.com/api/acct/%s/%s/%s'
		self.collection_url = 'https://my.rightscale.com/api/acct/%s/%s'
		self.credentials = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
		
		self._init_urls()
	
	def _init_urls(self):
		self.resource_url = self.resource_url % (self.account, '%s', '%s')
		self.collection_url = self.collection_url % (self.account, '%s')
	
		
	def build_url(self, resource, resource_id=None):
		if resource_id == None:
			url = self.collection_url % resource
		else:
			url = self.resource_url % (resource, resource_id)
		return url
	
	def http_auth_request(self, url):
		request = urllib2.Request(url)
		request.add_header('Authorization', 'Basic %s' % self.credentials)
		request.add_header('X-API-VERSION', '1.0')
		return urllib2.urlopen(request)
	
	def servers_index(self):
		servers_url = self.build_url('servers.js')
		
		response = self.http_auth_request(servers_url)
		return response
	
	def DELETE_resource(self, resource, resource_id):
		url = self.build_url(resource, resource_id)
		
		response = self.http_auth_request(url)
		return response
	





if __name__ == '__main__':
	pass