"""
Django admin page for grades models
"""
from django.contrib import admin

from config_models.admin import ConfigurationModelAdmin

from lms.djangoapps.grades.models import CoursePersistentGradesFlag, PersistentGradesEnabledFlag
from lms.djangoapps.grades.forms import CoursePersistentGradesAdminForm


class CourseAuthorizationAdmin(admin.ModelAdmin):
    """Admin for enabling subsection grades on a course-by-course basis."""
    form = CoursePersistentGradesAdminForm
    fieldsets = (
        (None, {
            'fields': ('course_id', 'enabled'),
            'description': '''
Enter a valid course id. If it is invalid, an error message will display.
'''
        }),
    )

admin.site.register(CoursePersistentGradesFlag, CourseAuthorizationAdmin)
admin.site.register(PersistentGradesEnabledFlag, ConfigurationModelAdmin)
