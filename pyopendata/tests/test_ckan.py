import pyopendata as pyod

print(pyod)
import urllib2
import urllib
import json
import pprint


# cstore = pyod.base.CKANStore('http://catalog.data.gov/')

cstore = pyod.base.CKANStore('http://demo.ckan.org/')
print(cstore.packages)
# print('groups', len(cstore.groups))
# print('tags', len(cstore.tags))
print(cstore.get_package_from_id('1234567890'))
print(cstore.get_resources_from_tag('gold'))
print(cstore.get_packages_from_group('data-explorer'))

quit()

for c in cstore.packages:
    print(c)

for c in cstore.packages:
    try:
        # df = c.read()
        # print(df)
        quit()
    except Exception as e:
        print(e)
        pass
"""
request = urllib2.Request('http://catalog.data.gov/api/action/package_show?id={0}'.format('DOC-5570'))
response = urllib2.urlopen(request)
response_dict = json.loads(response.read())
print(response_dict)
"""
