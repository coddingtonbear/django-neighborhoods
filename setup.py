from distutils.core import setup

setup(
    name='django-neighborhoods',
    version='2.0',
    url='http://bitbucket.org/latestrevision/django-neighborhoods/',
    description='Get neighborhood information for your coordinates.',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    packages=[
        'neighborhoods', 
        'neighborhoods.management',
        'neighborhoods.management.commands',
        'neighborhoods.migrations',
        ],
)
