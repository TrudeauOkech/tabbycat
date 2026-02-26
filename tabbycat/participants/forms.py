from django import forms
from django.utils.translation import gettext_lazy as _

from privateurls.utils import populate_url_keys
from registration.form_utils import CustomQuestionsFormMixin

from .models import Speaker


class AdminSpeakerForm(CustomQuestionsFormMixin, forms.ModelForm):

    class Meta:
        model = Speaker
        fields = ('name', 'last_name', 'email', 'phone', 'gender', 'categories')

    def __init__(self, *args, **kwargs):
        self.tournament = kwargs.pop('tournament')
        self.team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)

        self.fields['categories'].queryset = self.tournament.speakercategory_set.all()
        self.add_question_fields()

    def save(self, commit=True):
        if self.team:
            self.instance.team = self.team
        obj = super().save(commit=commit)
        if commit:
            populate_url_keys([obj])
            self.save_answers(obj, replace_existing=bool(self.instance.pk))
        return obj
