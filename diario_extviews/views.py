from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from django import forms

from diario.models import Entry
from diario_moderation.models import EntryStatus, STATUS_ACCEPTED, STATUS_DRAFT

from diario.views.entries import EntryList


class ListDrafts(EntryList):
    queryset = None    
    template_name = 'diario/list_drafts.html'
    
    def get_queryset(self):
        return Entry.objects.filter(entrystatus__status=STATUS_DRAFT,
                                    author=self.request.user)
 
 
class EntryCreationForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'body_source')
    

class CreateDraft(CreateView):
    model = Entry
    form_class = EntryCreationForm
    
    def get_initial(self):
        initial = super(CreateDraft, self).get_initial()
        initial['author'] = self.request.user
        return initial
        
    # TODO: finish me!