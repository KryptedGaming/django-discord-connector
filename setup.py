import os, sys
from setuptools import find_packages, setup
from setuptools.command.test import test

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-discord-connector',
    version=__import__('django_discord_connector').__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple Django application that adds Discord entities and SSO handling',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/KryptedGaming/django-discord-connector',
    author='porowns',
    author_email='porowns@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=2.2.13',
        'django-singleton-admin-2>=1.1.0',
        'discord>=1.0.1',
        'requests>=2.22.0',
        'requests_oauthlib>=1.2.0',
        'celery>=4.0.2',
    ],
    test_suite='runtests.runtests',
)
