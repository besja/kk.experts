# -*- coding: utf-8 -*-
import cStringIO # *much* faster than StringIO
import urllib
import transaction
from AccessControl.SecurityManagement import newSecurityManager
import os
import json
from plone.dexterity.utils import createContentInContainer
from zope.component.hooks import setSite
from Testing.makerequest import makerequest
from plone import namedfile
from plone.app.textfield.value import RichTextValue

plone_site_id = 'Plone' # Adjust as needed.

app = makerequest(app)
site = app[plone_site_id]
setSite(site)
user = app.acl_users.getUser('admin').__of__(site.acl_users)
newSecurityManager(None, user)



source_path = os.path.join(os.path.dirname(sys.modules['kk.experts'].__file__),'import','source.json')
source = open(source_path)
data = json.loads(source.read())

f = app.Plone.expertsearch

for i in data:
    id = i['title']
    item = createContentInContainer(f, "kk.experts.expert", title=i['title'])
    item.text = RichTextValue(raw = i['text'], mimeType='text/html',outputMimeType='text/x-html-safe', encoding='utf-8')
    item.desc = RichTextValue(raw = i['description'], mimeType='text/html',outputMimeType='text/x-html-safe', encoding='utf-8')
    item.ProfExp = i['ProfExp']
    item.FunctCrit = i['FunctCrit']
    item.SubCrit = i['SubCrit']
    file_data= urllib.urlopen(i['file'])
    item.PdfFile = namedfile.NamedBlobFile(file_data.read(), filename = u'PdfFile', contentType = 'application/pdf')


    
#file = urllib.urlopen('http://consulting.androschin.com/expertensuche/102/at_download/PdfFile')




#f.invokeFactory("File", "test", file = file )

transaction.commit()
app._p_jar.sync()



