"""
Defines a form for providing validation of CourseEmail templates.
"""
import logging

from django import forms

from lms.djangoapps.grades.models import CourseAuthorization

from opaque_keys import InvalidKeyError
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import CourseKey
from opaque_keys.edx.locations import SlashSeparatedCourseKey

log = logging.getLogger(__name__)


class CourseAuthorizationAdminForm(forms.ModelForm):
    """Input form for subsection grade enabling, allowing us to verify data."""

    class Meta(object):
        model = CourseAuthorization
        fields = '__all__'

    def clean_course_id(self):
        """Validate the course id"""
        cleaned_id = self.cleaned_data["course_id"]
        try:
            course_key = CourseKey.from_string(cleaned_id)
        except InvalidKeyError:
            try:
                course_key = SlashSeparatedCourseKey.from_deprecated_string(cleaned_id)
            except InvalidKeyError:
                msg = u'Course id invalid.'
                msg += u' --- Entered course id was: "{0}". '.format(cleaned_id)
                msg += 'Please recheck that you have supplied a valid course id.'
                raise forms.ValidationError(msg)

        if not modulestore().has_course(course_key):
            msg = u'COURSE NOT FOUND'
            msg += u' --- Entered course id was: "{0}". '.format(course_key.to_deprecated_string())
            msg += 'Please recheck that you have supplied a valid course id.'
            raise forms.ValidationError(msg)

        return course_key
