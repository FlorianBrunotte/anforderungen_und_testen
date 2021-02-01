from django import forms
from .models import requirement, testcase, projekt
#import der Choices damit die überall verwendbar sind
from .choices import *

#Nur hier müssen die Sachen angepasst werden
class RequirementForm(forms.Form):
    #Felder die verändert werden können
    req_form_name = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 100}), max_length=100, required=False)
    req_form_beschreibung = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 100}), max_length=300, required=False)
    req_form_kommentar = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 100}), max_length=300, required=False)

    #TestCases
    req_form_fk_testcase = forms.ModelMultipleChoiceField(queryset=None ,widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        tecs = kwargs.pop('tecs')
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields["req_form_fk_testcase"].queryset = tecs

class TestCaseForm(forms.Form):
    #Felder die verändert werden können
    testc_form_name = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 100}), max_length=100, required=False)
    testc_form_beschreibung = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 80}), max_length=300, required=False)
    testc_form_kommentar = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 80}), max_length=300, required=False)
    testc_form_vorbedingung = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 80}), max_length=300, required=False)

    testc_form_fk_requirement = forms.ModelMultipleChoiceField(queryset=None ,widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        reqs = kwargs.pop('reqs')
        super(TestCaseForm, self).__init__(*args, **kwargs)
        self.fields["testc_form_fk_requirement"].queryset = reqs

class TestCase_Schritt_Form(forms.Form):
    #Felder die verändert werden können
    schritt_form_schritt = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}))
    schritt_form_erwartetesergebnis = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}))

class TestCase_Schritt_Form2(forms.Form):
    #Felder die verändert werden können
    schritt_form_tatsaechlichesergebnis = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 40}))
    schritt_ergebnis = forms.CharField(label='ergebnis', widget=forms.RadioSelect(choices=RUN_STATUS))


class TestRunForm(forms.Form):
    # Felder die verändert werden können
    testr_form_name = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 80}), max_length=100, required=False)
    testr_form_beschreibung = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 80}), max_length=300, required=False)
    testr_form_kommentar = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 80}), max_length=300, required=False)

    testr_form_fk_testcase = forms.ModelChoiceField(queryset=None ,widget=forms.RadioSelect, required=False)

    def __init__(self, *args, **kwargs):
        tecs = kwargs.pop('tecs')
        super(TestRunForm, self).__init__(*args, **kwargs)
        self.fields["testr_form_fk_testcase"].queryset = tecs


class GroupForm(forms.Form):
    # Felder die verändert werden können
    group_form_group = forms.ChoiceField(choices=projekt.objects.all(), widget=forms.Select(attrs={'onchange': 'submit();'}))


class TestCase_Schritte_Form(forms.Form):
    #Felder die verändert werden können
    schritt_form_schritt = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}), max_length=300, required=False)
    schritt_form_erwartetesergebnis = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}), max_length=300, required=False)
    schritt_form_tatsaechlichesergebnis = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 40}), max_length=300, required=False)
    schritt_ergebnis = forms.CharField(label='ergebnis', widget=forms.RadioSelect(choices=RUN_STATUS))


class Note_Form(forms.Form):
    # Felder die verändert werden können
    note_form = forms.CharField(required=False, label="",widget=forms.Textarea(attrs={"rows": 5, "cols": 60}))


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
