from django.contrib.auth.models import User
from django import forms

from Scholarship.models import TrackedUser, StudyHoursRecord, AcademicResource, LibraryItem

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name + " " + obj.last_name

class TrackedUserForm(forms.ModelForm):
  user = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))
  number_of_hours = forms.IntegerField(min_value=0)

  class Meta:
    model = TrackedUser
    fields=['user', 'number_of_hours']

class StudyHoursRecordForm(forms.ModelForm):
  date = forms.DateField()
  number_of_hours = forms.IntegerField(min_value=1)

  class Meta:
    model = StudyHoursRecord
    exclude=['user', 'time_stamp']


class AcademicResourceForm(forms.ModelForm):
  year = forms.IntegerField()

  class Meta:
    model = AcademicResource
    fields = ['resource_name', 'course_number', 'professor_name', 'resource_pdf', 'year', 'term']

class LibraryItemForm(forms.ModelForm):
  class Meta:
    model = LibraryItem
    fields = ['title', 'isbn_number', 'course', 'edition', 'item_pdf']
