from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import RedirectView
from django import forms
from django.contrib import messages

from diario.models import Entry
from diario_moderation.models import EntryStatus, STATUS_ACCEPTED, \
                                     STATUS_DRAFT, STATUS_QUEUED, \
                                     STATUS_REJECTED, STATUS_REWRITE
from diario.views.entries import EntryList


class ListByStatus(EntryList):
    '''Semi-generic view that return entry list depend on it's status'''
    queryset = None
    status = None
    
    def get_queryset(self):
        return Entry.objects.filter(entrystatus__status=self.status,
                                    author=self.request.user)

class ListDrafts(ListByStatus):
    '''Return a list of current user's drafts'''
    status = STATUS_DRAFT    
    template_name = 'diario/list_drafts.html'
    allow_empty = True
    

class ListQueued(ListByStatus):
    '''Return a list of current user's queued entries'''
    status = STATUS_QUEUED
    template_name = 'diario/list_queued.html'

class ListRejected(ListByStatus):
    '''Return a list of current user's rejected entries'''
    status = STATUS_REJECTED
    template_name = 'diario/list_rejected.html'

class ListRewrite(ListByStatus):
    '''Return a lisf of current user's entries that must be rewrited'''
    status = STATUS_REWRITE
    template_name = 'diario/list_rewrite.html'
 
 
class EntryCreationForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'body_source')
    

class CreateDraft(CreateView):
    model = Entry
    form_class = EntryCreationForm
    template_name = 'diario/create_draft.html'
    context_object_name = 'form'
    
    def get_initial(self):
        initial = super(CreateDraft, self).get_initial()
        initial['author'] = self.request.user
        return initial
        
    def get_success_url(self):
        return reverse('edit-draft', kwargs={'pk': self.object.pk})



class EditDraft(UpdateView):
    model = Entry
    form_class = EntryCreationForm
    template_name = 'diario/edit_draft.html'
    context_object_name = 'form'
    queryset = None    
        
    def get_success_url(self):
        return reverse('edit-draft', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        user = self.request.user
        queryset = Entry.objects.filter(entrystatus__status=STATUS_DRAFT)
        if user.has_perm('diario_moderation.moderate_entry'):
            return queryset
        return queryset.filter(author=user)
  

def QueueDraft(RedirectView):
    queryset = EntryStatus.objects.filter(status=STATUS_DRAFT)    

    def get_redirect_url(self, **kwargs):
        return reverse('list-drafts')

    def get_queryset(self):
        return self.queryset

    def get_status(self, pk, user):
        try:
            return self.get_queryset().get(entry__author__id=user, pk=pk)
        except EntryStatus.DoesNotExist:
            raise Http404

    def queue_entry(self, status):
        EntryStatus.objects.filter(pk=status.pk).update(status=STATUS_QUEUED)
        messages.add_message(self.request, messages.INFO,
                            u'Your article has been sent to moderators')
        return True
             

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)        
        if not pk:
            raise Http404
        status = self.get_status(pk, request.user)
        if self.queue_entry(status):
            return super(QueueDraft, self).get(request, *args, **kwargs)
        return HttpResponse(status=403)
   
