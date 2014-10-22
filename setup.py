from distutils.core import setup
from pip.req import parse_requirements
from setuptools import find_packages

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='whats-fresh',
    version='0.1.0',
    install_requires=reqs,
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
