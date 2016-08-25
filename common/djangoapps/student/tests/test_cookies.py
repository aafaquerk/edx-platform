# pylint: disable=missing-docstring
from __future__ import unicode_literals

import six
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from student.cookies import get_user_info_cookie_data
from student.tests.factories import UserFactory, CourseEnrollmentFactory


class CookieTests(SharedModuleStoreTestCase):
    @classmethod
    def setUpClass(cls):
        super(CookieTests, cls).setUpClass()
        cls.course = CourseFactory()

    def setUp(self):
        super(CookieTests, self).setUp()
        self.user = UserFactory.create()

    def _get_expected_header_urls(self, request):
        expected_header_urls = {
            'logout': reverse('logout'),
        }

        # Studio (CMS) does not have the URLs below
        if settings.ROOT_URLCONF == 'lms.urls':
            expected_header_urls.update({
                'account_settings': reverse('account_settings'),
                'learner_profile': reverse('learner_profile', kwargs={'username': self.user.username}),
            })

        # Convert relative URL paths to absolute URIs
        for url_name, url_path in six.iteritems(expected_header_urls):
            expected_header_urls[url_name] = request.build_absolute_uri(url_path)

        return expected_header_urls

    def test_get_user_info_cookie_data(self):
        """ Verify the function returns data that """
        request = RequestFactory().get('/')
        request.user = self.user

        enrollment_mode = 'verified'
        course_id = self.course.id  # pylint: disable=no-member
        CourseEnrollmentFactory.create(user=self.user, course_id=course_id, mode=enrollment_mode)

        actual = get_user_info_cookie_data(request, self.user)

        expected_enrollments = [{
            'course_run_id': six.text_type(course_id),
            'seat_type': enrollment_mode,
        }]

        expected = {
            'version': settings.EDXMKTG_USER_INFO_COOKIE_VERSION,
            'username': self.user.username,
            'email': self.user.email,
            'header_urls': self._get_expected_header_urls(request),
            'enrollments': expected_enrollments,
        }

        self.assertDictEqual(actual, expected)
