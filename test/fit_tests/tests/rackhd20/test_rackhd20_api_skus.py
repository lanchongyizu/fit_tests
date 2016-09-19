'''
Copyright 2016, EMC, Inc.

Author(s):
George Paulos

'''

import os
import sys
import time
import subprocess
# set path to common libraries
sys.path.append(subprocess.check_output("git rev-parse --show-toplevel", shell=True).rstrip("\n") + "/test/fit_tests/common")
import fit_common

# Select test group here using @attr
from nose.plugins.attrib import attr
@attr(all=True, regression=True, smoke=True)
class rackhd20_api_skus(fit_common.unittest.TestCase):
    def print_obms(self):
	#return
        api_data = fit_common.rackhdapi("/api/2.0/obms")
	print api_data['json']

    def check_obms_user(self):
	#return
	api_data = fit_common.rackhdapi("/api/2.0/obms")
	#print api_data['json']
	for item in api_data['json']:
 	    self.assertIn('user', item['config'], 'Obm not include user after post or delete sku')
	
    def setUp(self):
	print "----------setUp---------------"
	self.print_obms()
        # delete test skus if present
        api_data = fit_common.rackhdapi("/api/2.0/skus")
        for item in api_data['json']:
            if "test" in item['name']:
                fit_common.rackhdapi("/api/2.0/skus/" + item['id'], action="delete")
	#return
        api_data = fit_common.rackhdapi("/api/2.0/obms")
        for item in api_data['json']:
	    if "user" not in item['config']:
		data_payload = {
				"service": item['service'],
				"config": {
					"host": item['config']['host'],
					"user": "root",
					"password": "1234567"
				},
				"nodeId": item['node'].split('/')[4]
		}
                fit_common.rackhdapi("/api/2.0/obms", action="put", payload=data_payload)
	self.print_obms()
	#time.sleep(30)

    def test_api_20_none(self):
	print "---------test_api_20_none--------------"
	self.print_obms()
	self.check_obms_user()

    def test_api_20_sku(self):
	print "----------test_api_20_sku---------------"
	self.print_obms()
        api_data = fit_common.rackhdapi("/api/2.0/skus")
        self.assertEqual(api_data['status'], 200, 'Incorrect HTTP return code, expected 200, got:' + str(api_data['status']))
        for item in api_data['json']:
            self.assertEqual(fit_common.rackhdapi("/api/2.0/skus/" + item['id'])['status'],
                             200, 'Incorrect HTTP return code, expected 200, got:' + str(api_data['status']))
	self.print_obms()
	self.check_obms_user()

    def test_api_20_sku_post_get_delete(self):
	print "----test_api_20_sku_post_get_delete------"
	self.print_obms()
        data_payload = {
                        "name": "test1",
                        "rules": [
                            {
                                "contains": "test",
                                "path": "ohai.dmi.base_board.manufacturer"
                            }
                        ]
                        }
        api_data = fit_common.rackhdapi("/api/2.0/skus", action="post", payload=data_payload)
        self.assertEqual(api_data['status'], 201, 'Incorrect HTTP return code, expected 201, got:' + str(api_data['status']))
        #api_data = fit_common.rackhdapi("/api/2.0/skus/" + api_data['json']['id'])
        #self.assertEqual(api_data['status'], 200, 'Incorrect HTTP return code, expected 200, got:' + str(api_data['status']))
        #api_data = fit_common.rackhdapi("/api/2.0/skus/" + api_data['json']['id'],
        #                                   action="delete")
        #self.assertEqual(api_data['status'], 204, 'Incorrect HTTP return code, expected 204, got:' + str(api_data['status']))
	self.print_obms()
	self.check_obms_user()

    def test_api_20_sku_post_patch_delete(self):
	print "----test_api_20_sku_post_patch_delete----"
	self.print_obms()
        data_payload = {
                        "name": "test2",
                        "rules": [
                            {
                                "contains": "test",
                                "path": "ohai.dmi.base_board.manufacturer"
                            }
                        ]
                        }
        api_data = fit_common.rackhdapi("/api/2.0/skus", action="post", payload=data_payload)
        self.assertEqual(api_data['status'], 201, 'Incorrect HTTP return code, expected 201, got:' + str(api_data['status']))
        patch_payload ={"name": "test3"}
        api_data = fit_common.rackhdapi("/api/2.0/skus/" + api_data['json']['id'], action="patch", payload=patch_payload)
        self.assertEqual(api_data['status'], 200, 'Incorrect HTTP return code, expected 200, got:' + str(api_data['status']))
        self.assertEqual(api_data['json']['name'], "test3", "SKU patch failed")
	self.print_obms()
	self.check_obms_user()

if __name__ == '__main__':
    fit_common.unittest.main()
