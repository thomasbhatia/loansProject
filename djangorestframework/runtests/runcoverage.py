"""
Useful tool to run the test suite for djangorestframework and generate a coverage report.
"""

# http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/
# http://www.travisswicegood.com/2010/01/17/django-virtualenv-pip-and-fabric/
# http://code.djangoproject.com/svn/django/trunk/tests/runtests.py
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangorestframework.runtests.settings'

from django.conf import settings
from django.test.utils import get_runner
from coverage import coverage
from itertools import chain
import djangorestframework

def main():
    """Run the tests for djangorestframework and generate a coverage report."""
    
    # Discover the list of all modules that we should test coverage for
    project_dir = os.path.dirname(djangorestframework.__file__)
    cov_files = []
    for (path, dirs, files) in os.walk(project_dir):
        # Drop tests and runtests directories from the test coverage report
        if os.path.basename(path) == 'tests' or os.path.basename(path) == 'runtests':
            continue
        cov_files.extend([os.path.join(path, file) for file in files if file.endswith('.py')])

    cov = coverage()
    cov.erase()
    cov.start()
    TestRunner = get_runner(settings)

    if hasattr(TestRunner, 'func_name'):
        # Pre 1.2 test runners were just functions,
        # and did not support the 'failfast' option.
        import warnings
        warnings.warn(
            'Function-based test runners are deprecated. Test runners should be classes with a run_tests() method.',
            DeprecationWarning
        )
        failures = TestRunner(['djangorestframework'])
    else:
        test_runner = TestRunner()
        failures = test_runner.run_tests(['djangorestframework'])

    cov.stop()
    cov.report(cov_files)
    cov.xml_report(cov_files)
    sys.exit(failures)

if __name__ == '__main__':
    main()
