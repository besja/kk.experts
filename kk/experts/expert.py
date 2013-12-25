from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText

from plone.namedfile.field import NamedBlobFile


from kk.experts import MessageFactory as _

from Products.CMFCore.utils import getToolByName

from Products.ATVocabularyManager import NamedVocabulary

from zope.interface import Invalid


def at_to_voc(atvocabulary):

     terms = []
     for i in atvocabulary:
         terms.append(SimpleTerm(value=i, title=atvocabulary.getValue(i)))
     return SimpleVocabulary(terms)

### AT VOCABS ###
#@grok.provider(IContextSourceBinder)
#def professional_experience(context):
#     atvocabulary = NamedVocabulary("""professional-experience""").getDisplayList(context) 
#     return at_to_voc(atvocabulary)
     
#@grok.provider(IContextSourceBinder)
#def functional_criteria(context):
#     atvocabulary = NamedVocabulary("""professional-experience""").getDisplayList(context) 
#     return at_to_voc(atvocabulary)
     
#@grok.provider(IContextSourceBinder)
#def subject_criteria(context):
#     atvocabulary = NamedVocabulary("""professional-experience""").getDisplayList(context) 
#     return at_to_voc(atvocabulary)

def list_to_voc(name):
    vocs = get_vocabs();
    voc = vocs[name]
    terms = []
    for i in voc:
        terms.append(SimpleTerm(value=i[0], title=i[1]))
    return SimpleVocabulary(terms)
    

### STATIC VOCAV ### 
from kk.experts.config import get_vocabs 
@grok.provider(IContextSourceBinder)
def professional_experience(context):
    return list_to_voc('professional-experience')
     
@grok.provider(IContextSourceBinder)
def functional_criteria(context):
    return list_to_voc('functional-criteria')
     
@grok.provider(IContextSourceBinder)
def subject_criteria(context):
    return list_to_voc('subject-criteria')

#professional_experience = NamedVocabulary("""professional-experience""")    
# Interface class; used to define content-type schema.

def checkMimeType(value):
    # ??? why fdf ??? 
    if not (value.contentType == "application/fdf"):
        raise Invalid(_(u"Invalid file type"))
    return True
    
class IExpert(form.Schema, IImageScaleTraversable):
    """
    Expert info
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/expert.xml to define the content type.
    title = schema.TextLine(title=_(u'Title'), required=True)
    desc = RichText(title=_(u'Description'), required=True)
    ProfExp = schema.List(title=_(u'Professional experience'), required=True,  value_type=schema.Choice(source=professional_experience))
    
    FunctCrit = schema.List(title=_(u'Functional criteria'), required=True,  value_type=schema.Choice(source=functional_criteria))
    
    SubCrit = schema.List(title=_(u'Subject criteria'), required=True,  value_type=schema.Choice(source=subject_criteria))   
    
    text = RichText(title=_(u'Body text'), required=False)
	
	# todo: restrict 'application/pdf' 
	
    PdfFile = NamedBlobFile(title=_(u"CV-PDF Upload"), required=False, constraint=checkMimeType)
    

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Expert(Container):
    grok.implements(IExpert)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# expert_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(IExpert)
    grok.require('zope2.View')

    # grok.name('view')


    def getFunctCrit(self):
  
        voc = functional_criteria(self.context)
        terms = self.context.FunctCrit
        result = []
        for i in voc:
           if i.value in terms:
               result.append(i.title)
        return ", ".join(result)
        
    def getProfExp(self):
  
        voc = professional_experience(self.context)
        terms = self.context.ProfExp
        result = []
        for i in voc:
           if i.value in terms:
               result.append(i.title)
        return ", ".join(result)    
            
    def getSubCrit(self):
  
        voc = subject_criteria(self.context)
        terms = self.context.SubCrit
        result = []
        for i in voc:
           if i.value in terms:
               result.append(i.title)
        return ", ".join(result)        
