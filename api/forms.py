from django import forms

DRUGS = [ ('fluc', 'flucloxacillin'),]
class QueryForm(forms.Form):
    drug =  forms.ChoiceField(choices = DRUGS, required = True)
    # profile_name = FIELD WILL BE APPENDED IN VIEW in SUBCLASS, because the 