from django.conf import settings
from django.http import HttpResponse
from diario.models import Entry
from diario_moderation.models import EntryStatus, MODERATION_STATUS

from django import forms
from django.views.generic.edit import UpdateView

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
    
    def dispatch(self, request, *args, **kwargs):
        perm_checker_func = getattr(settings, 'DIARIO_MODERATION_PERMISSION_CHECKER', None)
        if perm_checker_func:
            result = perm_checker_func(request.user)
        else:
            result = request.user.has_perm('diario_moderation.can_moderate_entries')
        if not result:
            return HttpResponse(status=403)
        return super(ModerateEntry, self).dispatch(request, *args, **kwargs)
