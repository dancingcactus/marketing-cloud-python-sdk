import unittest
from apiWrapper import *

creds = {};
execfile("credentials.conf",creds);

class apiWrapperUnitTest(unittest.TestCase):
	def setUp(self):
		self.api = AnalyticsAPI(creds['username'], creds['password']);
		self.fake_user = "foo:Justin Grover";
		self.fake_password = "bar";

	def test_getUsername(self):
		self.assertEqual(self.api.getUsername(),creds['username']);

	def test_setUsername(self):
		self.api.setUsername(self.fake_user);
		self.assertEqual(self.api.getUsername(),self.fake_user);
		self.api.setUsername(creds['username']);

	def test_getPassword(self):
		self.assertEqual(self.api.getPassword(), creds['password']);

	def test_setPassword(self):
		self.api.setPassword(self.fake_password);
		self.assertEqual(self.api.getPassword(),self.fake_password);
		self.api.setPassword(creds['password'])

	def test_config(self):
		self.api.config(self.fake_user,self.fake_password);
		self.assertEqual(self.api.getUsername(), self.fake_user)
		self.assertEqual(self.api.getPassword(), self.fake_password);
		self.api.config(creds['username'], creds['password']);

	def test_getEndpoint(self):
		self.assertTrue(isinstance(self.api.getEndpoint(creds['username']),unicode))
		self.assertRaises(BadCompanyError,self.api.getEndpoint,"foo")
		self.assertRaises(BadCompanyError,self.api.getEndpoint,"foo:foo")

	def test_invoke(self):
		self.assertTrue(self.api.invoke("Company.GetReportSuites",{}).find("error")<0)

if __name__ == '__main__':
	unittest.main();

