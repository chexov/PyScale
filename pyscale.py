import urllib, urllib2, base64
import httplib

class RightScale(object):
	
	def __init__(self, username, password, account):
		self.username = username
		self.password = password
		self.account = str(account)
		self.resource_url = '/api/acct/%s/%s/%s'
		self.collection_url = '/api/acct/%s/%s'
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
		servers_url = self.build_url('servers')
		
		response = self.http_auth_request(servers_url)
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
	 
	def _DELETE_resource(self, resource, resource_id):
		url = self.build_url(resource, str(resource_id))
		
		self.conn.request('DELETE', url, body=None, headers=self.headers)
		response = self.conn.getresponse()
		
		return response
	


def cleanUpDelploymnets():
	DEPLOYMENTS_TO_SAVE = [3201, 12228, 8610, 15852]
	right = RightScale(sys.argv[1], sys.argv[2], 2951)
		
	index = right.deployments_index()
	xmldoc = minidom.parseString(index.read())
		
	for deployment in xmldoc.getElementsByTagName('deployment'):
		href = deployment.getElementsByTagName('href')[0]
		
		deployment_id = int(href.firstChild.data.split('/')[-1])
		if not deployment_id in DEPLOYMENTS_TO_SAVE:
			print "Deleting deployment: %d" % deployment_id
			right.deployments_delete(deployment_id)


def cleanUpServerTemplates():
	SERVERTEMPLATES_TO_SAVE = [13792, 919, 13788, 13745, 13791, 13088, 13793, 13777, 16962, 15507, 18060, 20483, 20484]
	index = right.servertemplates_index()
	xmldoc = minidom.parseString(index.read())
		
	for template in xmldoc.getElementsByTagName('href'):
		template_id = int(template.firstChild.data.split('/')[-1])
		
		if not template_id in SERVERTEMPLATES_TO_SAVE:
			print "Deleting server template: %d" % template_id
			right.servertemplates_delete(template_id)
	
	
def cleanUpRightScripts():
	SCRIPTS_TO_SAVE = [25089, 26558, 26524, 26463, 26525, 34457, 34458, 33928, 34462, 29978, 29974, 24565, 28164, 5508, 26559, 26522, 21020, 26560, 26523, 24577, 26706, 24578, 28031, 27733, 27726, 26702, 24570, 27948, 26716, 26717, 26528, 26552, 26561, 26553, 26556, 26956, 27727, 27593, 26957, 26557, 26527, 26554, 26466, 39356, 39358, 39391]
	index = right.rightscripts_index()
	xmldoc = minidom.parseString(index.read())
	
	for script in xmldoc.getElementsByTagName('href'):
		script_id = int(script.firstChild.data.split('/')[-1])
		
		if not script_id in SCRIPTS_TO_SAVE:
			print "Deleting rightscript: %d" % script_id
			right.rightscripts_delete(script_id)




if __name__ == '__main__':
	import sys
	from xml.dom import minidom
	
	cleanUpDeployments()
	#cleanUpServerTemplates()
	#cleanUpRightScripts()