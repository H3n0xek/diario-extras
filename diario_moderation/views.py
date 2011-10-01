from django.conf import settings
from django.http import HttpResponse, Http404
from diario.models import Entry
from diario_moderation.models import EntryStatus, MODERATION_STATUS, \
                                     STATUS_QUEUED

from django import forms
from django.views.generic.edit import UpdateView, ListView



class EntryModerateForm(forms.ModelForm):
    status = forms.ChoiceField(choices=MODERATION_STATUS)

    class Meta:
        model = Entry
        fields = ('title', 'slug', 'body_source', 'tags')

    def save(self, **kwargs):
        s = EntryStatus.objects.get(entry=self.instance)
        s.status = self.cleaned_data['status']
        s.save()
        return super(EntryModerateForm, self).save(**kwargs)
        


class ModerateEntry(UpdateView):
    form_class = EntryModerateForm
    model = Entry
    template_name = 'diario/moderate_entry.html'
    
    def dispatch(self, request, *args, **kwargs):
        perm_checker_func = getattr(settings, 'DIARIO_MODERATION_PERMISSION_CHECKER', None)
        if perm_checker_func:
            result = perm_checker_func(request.user)
        else:
            result = request.user.has_perm('diario_moderation.moderate_entries')
        if not result:
            return HttpResponse(status=403)
        return super(ModerateEntry, self).dispatch(request, *args, **kwargs)


class ModerateEntryList(ListView):
    queryset = None
    template_name = 'diario/moderate_entry_list.html'
    
    def get_queryset(self):
        u = self.request.user
        if u.has_perm('diario_moderation.moderate_entries'):
            return Entry.objects.filter(entrystatus__status=STATUS_QUEUED)
        raise Http404
