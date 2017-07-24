
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.interface import implements 
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.supermodel import model

from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText

from plone.namedfile.field import NamedBlobFile


from kk.experts import MessageFactory as _

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import Invalid


def at_to_voc(atvocabulary):

     terms = []
     for i in atvocabulary:
         terms.append(SimpleTerm(value=i, title=atvocabulary.getValue(i)))
     return SimpleVocabulary(terms)

def list_to_voc(name):
    vocs = get_vocabs();
    voc = vocs[name]
    terms = []
    for i in voc:
        terms.append(SimpleTerm(value=i[0], title=i[1]))
    return SimpleVocabulary(terms)
    

### STATIC VOCAV ### 
from kk.experts.config import get_vocabs 
professional_experience =  list_to_voc('professional-experience')
     
functional_criteria = list_to_voc('functional-criteria')
     
subject_criteria=list_to_voc('subject-criteria')


def checkMimeType(value):
    # ??? why fdf ??? 

    if not (value.contentType == "application/fdf" or value.contentType == "application/pdf") :
        raise Invalid(_(u"Invalid file type"))
    return True
    
class IExpert(model.Schema, IImageScaleTraversable):
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
    implements(IExpert)

class ExpertView(BrowserView):
    """ sample view class """
    __call__ = ViewPageTemplateFile('expert_templates/view.pt')


    def getFunctCrit(self):

        voc = functional_criteria
        terms = self.context.FunctCrit
        result = []
        for i in voc:
           if i.value in terms:
               result.append(i.title)
        return ", ".join(result)
        
    def getProfExp(self):
  
        voc = professional_experience
        terms = self.context.ProfExp
        result = []
        for i in voc:
           if i.value in terms:
               result.append(i.title)
        return ", ".join(result)    
            
    def getSubCrit(self):
  
        voc = subject_criteria
        terms = self.context.SubCrit
        result = []
        for i in voc:
           if i.value in terms:
               result.append(i.title)
        return ", ".join(result)        

