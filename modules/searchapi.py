import os
import urllib2

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

import requests
import re

def get_datasets_from_html(root, dataversename):
    query = ''
    url = root + "/dataverse/" + dataversename + "?types=datasets"
    response = urllib2.urlopen(url)

    html = response.read()
    pattern = re.compile(r'>http\:\/\/hdl.handle.net\/\d+\/(\S+)<', re.IGNORECASE)
    match = pattern.findall(html)
    for q in match:
        query+=q + ' '
    return query

def search_by_handles(self, searchquery):
    (searchhandles, metadata, pids) = ('', [], [])
    if ' ' in searchquery['q']:
	pids = searchquery['q'].split()
    if ',' in searchquery['q']:
        pids = searchquery['q'].split(",")

    if not pids:
        return metadata

    for handle in pids:
        ids = re.search(r'hdl\:\d+\/(\w+)', handle, re.M|re.I)
        if ids:
	    identificator = ids.group(1)
	    searchhandles = searchhandles + identificator + ' '

    if searchhandles:
 	searchquery['q'] = searchhandles
	metadata = search_by_keyword(self, searchquery)

    return metadata

def search_by_keyword(self, searchquery):
    if searchquery:
        url = '{0}/search'.format(
            self.native_base_url
        )

 	options = ['q', 'type', 'subtree', 'sort', 'order', 'per_page', 'start', 'show_relevance', 'show_facets', 'fq']

	# Form parameters URI
  	params = {'key': self.token}
	for opt in options:
	    if opt in searchquery:
		params[opt] = searchquery[opt]

	resp = requests.get(url, params)

        if resp.status_code == 404:
            raise self.VersionJsonNotFoundError(
                'JSON metadata could not be found for this version.'
            )
        elif resp.status_code != 200:
            raise self.ConnectionError('JSON metadata could not be retrieved.')

        metadata = resp.json()['data']

        return metadata

