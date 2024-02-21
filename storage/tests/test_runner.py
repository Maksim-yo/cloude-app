from django.test.runner import DiscoverRunner
from django.conf import settings


class CustomTestRunner(DiscoverRunner):

    def setup_test_environment(self, **kwargs):
        settings.IS_TEST_MODE = True
        super().setup_test_environment(**kwargs)
