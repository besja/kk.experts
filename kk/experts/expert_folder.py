from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import implements 
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText


from kk.experts import MessageFactory as _
from kk.experts.expert import functional_criteria, professional_experience, subject_criteria

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# Interface class; used to define content-type schema.

class IExpertFolder(model.Schema, IImageScaleTraversable):
    """
    Folder to store experts
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/expert_folder.xml to define the content type.
    model.load("models/expert_folder.xml")



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ExpertFolder(Container):
    implements(IExpertFolder)

    # Add your class methods and properties here
class ExpertFolderView(BrowserView):
    """ sample view class """
    __call__ = ViewPageTemplateFile('expert_folder_templates/view.pt')
    
    def getProfExp(self):
        return professional_experience
        
    def getFunctCrit(self):
        return functional_criteria

    def getSubCrit(self):
        return subject_criteria
          
    # Add view methods here

class ExpertSearchResultsView(BrowserView):

    __call__ = ViewPageTemplateFile('expert_folder_templates/expert_search_results.pt')
    
    def searchForExperts(self):

        request = self.request
        ProfExp = request.get('ProfExp', None)
        FunctCrit = request.get('FunctCrit', None)
        SubCrit = request.get('SubCrit', None)

        if not ProfExp:
            ProfExp = None
        if not FunctCrit:
            FunctCrit = None
        if not SubCrit:
            SubCrit = None

        experts = self.context.portal_catalog(portal_type="kk.experts.expert", path="/".join(self.context.getPhysicalPath()))

        results = []
        for expert in experts:
            exp = expert.getObject()
            res = {}
            labelBrk = False

            if ProfExp:
                inProfExp = list(exp.ProfExp)
                if isinstance(ProfExp, str):
                    if not(ProfExp in inProfExp):
                        continue
                else:
                    for raz in ProfExp:
                        if not(raz in inProfExp):
                            labelBrk = True
                            break
            
                if labelBrk:
                    continue

            if FunctCrit:
                inFunctCrit = list(exp.FunctCrit)
                if isinstance(FunctCrit, str):
                    if not(FunctCrit in inFunctCrit):
                       continue
                else:
                    for raz in FunctCrit:
                        if not(raz in inFunctCrit):
                            labelBrk = True
                            break
        
                if labelBrk:
                    continue

            if SubCrit:
                inSubCrit = list(exp.SubCrit)
                if isinstance(SubCrit, str):
                    if not(SubCrit in inSubCrit):
                        continue
                else:
                    for raz in SubCrit:
                        if not(raz in inSubCrit):
                            labelBrk = True
                            break
        
                if labelBrk:
                    continue

            if labelBrk:
                continue
            else:
                res['id'] = exp.getId()
                res['exp'] = expert

                results += [res]
    
        decorated = [(dict_["id"], dict_) for dict_ in results]
        decorated.sort(lambda a, b: cmp(a[0], b[0]))
        result = [dict_['exp'] for (key, dict_) in decorated]
        return result