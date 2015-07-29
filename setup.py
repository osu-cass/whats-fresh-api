from distutils.core import setup
from setuptools import find_packages

dependencies = [
    'Django==1.7.1',
    'Jinja2==2.7.3',
    'MarkupSafe==0.23',
    'Pillow==2.5.1',
    'PyYAML==3.11',
    'Pygments==1.6',
    'Sphinx==1.2.2',
    'argparse==1.2.1',
    'django-phonenumber-field==0.6',
    'docutils==0.12',
    'mock==1.0.1',
    'pep8==1.5.7',
    'phonenumbers==6.2.0',
    'psycopg2==2.5.3',
    'requests==2.3.0',
    'wsgiref==0.1.2',
    'fig==1.0.1'
]

setup(
    name='whats-fresh',
    version='1.0.3',
    install_requires=dependencies,
    author=u'OSU Center for Applied Systems and Software',
    author_email='support@osuosl.org',
    packages=find_packages(),
    url='https://github.com/osu-cass/whats-fresh-api',
    license='',
    zip_safe=False,
    package_data={
        'whats_fresh.whats_fresh_api.tests.testdata': ['*.json', 'media/*'],
        'whats_fresh.whats_fresh_api': ['templates/*', 'static/*.png', 'static/css/*']},
    description="What's Fresh API implementation",
    long_description=open('README.rst').read()
)
