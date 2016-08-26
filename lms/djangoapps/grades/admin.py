"""
Django admin page for grades models
"""
from django.contrib import admin

from config_models.admin import ConfigurationModelAdmin

from lms.djangoapps.grades.models import CourseAuthorization, SubsectionGradesEnabledFlag
from lms.djangoapps.grades.forms import CourseAuthorizationAdminForm


class CourseAuthorizationAdmin(admin.ModelAdmin):
    """Admin for enabling subsection grades on a course-by-course basis."""
    form = CourseAuthorizationAdminForm
    fieldsets = (
        (None, {
            'fields': ('course_id', 'enabled'),
            'description': '''
Enter a course id in the following form: Org/Course/CourseRun, eg MITx/6.002x/2012_Fall
Do not enter leading or trailing slashes. There is no need to surround the course ID with quotes.
Validation will be performed on the course name, and if it is invalid, an error message will display.
'''
        }),
    )

admin.site.register(CourseAuthorization, CourseAuthorizationAdmin)
admin.site.register(SubsectionGradesEnabledFlag, ConfigurationModelAdmin)
