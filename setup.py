from distutils.core import setup

setup(
    name='django-neighborhoods',
    version='1.0',
    url='http://bitbucket.org/latestrevision/django-neighborhoods/',
    description='Use neighborhood boundaries provided by the Zillow',
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
        'neighborhoods.management.commands',
        ],
    zip_safe=False
)
