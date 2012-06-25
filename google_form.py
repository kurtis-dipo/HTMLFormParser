# Test case for HTMLFormParser v0.1
# 
# This test should return Google's login form values
#
# (C) Kurtis Dipo aka Piotr Dusik 2012
# http://piotr.dusik.pl
# piotr@dusik.pl
#

import urllib2
import HTMLFormParser


req = urllib2.Request("https://accounts.google.com/ServiceLogin")
html = urllib2.urlopen(req).read()
form = HTMLFormParser.HTMLFormParser()
form.set_form_identifier({"id" : "gaia_loginform"})
form.parse(html)
items = form.items
print items
