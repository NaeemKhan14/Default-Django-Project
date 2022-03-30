from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from django import forms


class CustomFiltersForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(

        )

        for field_name, field in self.fields.items():
            self.helper.layout.append(HTML("<th>"))
            self.helper.layout.append(Field(field_name, placeholder=field.label))
            self.helper.layout.append(HTML("</th>"))