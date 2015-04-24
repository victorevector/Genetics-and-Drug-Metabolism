from django import forms
from api.models import DrugsAndSNP

drug_choices = []
all_entries = DrugsAndSNP.objects.all()
for entry in all_entries:
    drug_choices.append((entry.drug, entry.drug) )

class QueryForm(forms.Form):
    drug =  forms.ChoiceField(choices = drug_choices, required = True)
    # profile_name = FIELD WILL BE APPENDED IN VIEW in SUBCLASS 