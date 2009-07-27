import urllib, urllib2, base64
import httplib

class RightScale(object):
	
	def __init__(self, username, password, account):
		self.username = username
		self.password = password
		self.account = str(account)
		self.resource_url = '/api/acct/%s/%s/%s'
		self.collection_url = '/api/acct/%s/%s'
		self.action_url = '/api/acct/%s/%s/%s/%s'
		self.credentials = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
		self.headers = {
						'Authorization': 'Basic %s' % self.credentials,
						'X-API-VERSION': '1.0' 
		}
		self.conn = httplib.HTTPSConnection('my.rightscale.com')
		
		self._init_urls()
	
	def _init_urls(self):
		self.resource_url = self.resource_url % (self.account, '%s', '%s')
		self.collection_url = self.collection_url % (self.account, '%s')
		self.action_url = self.action_url % (self.account, '%s', '%s', '%s')
	
	def build_url(self, resource, resource_id=None, action=None):
		if resource_id == None:
			url = self.collection_url % resource
		else:
			if action == None:
				url = self.resource_url % (resource, resource_id)
			else:
				url = self.action_url % (resource, resource_id, action)
		return url
	
	def http_auth_request(self, url):
		request = urllib2.Request(url)
		request.add_header('Authorization', 'Basic %s' % self.credentials)
		request.add_header('X-API-VERSION', '1.0')
		return urllib2.urlopen(request)
	
	def servers_index(self):
		servers_url = self.build_url('servers')
		
		self.conn.request('GET', servers_url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	
	def servers_stop(self, resource_id):
		server_url = self.build_url('servers', str(resource_id), action='stop')
		
		self.conn.request('POST', server_url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	
	def servers_delete(self, resource_id):
		self._DELETE_resource('servers', resource_id)
	
	def deployments_index(self):
		deployments_url = self.build_url('deployments')
		
		self.conn.request('GET', deployments_url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	
	def deployments_delete(self, resource_id):
		self._DELETE_resource('deployments', str(resource_id))
	
	def servertemplates_index(self):
		st_url = self.build_url('server_templates')
		
		self.conn.request('GET', st_url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	
	def servertemplates_delete(self, resource_id):
		self._DELETE_resource('server_templates', str(resource_id))
	
	def rightscripts_index(self):
		rightscript_url = self.build_url('right_scripts')
		
		self.conn.request('GET', rightscript_url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	
	def rightscripts_delete(self, resource_id):
		self._DELETE_resource('right_scripts', resource_id)
	
	def arrays_index(self):
		arrays_url = self.build_url('server_arrays')
		
		self.conn.request('GET', arrays_url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	
	def arrays_delete(self, resource_id):
		self._DELETE_resource('server_arrays', resource_id)
	
	def _DELETE_resource(self, resource, resource_id):
		url = self.build_url(resource, str(resource_id))
		
		self.conn.request('DELETE', url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	


