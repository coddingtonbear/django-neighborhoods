from distutils.core import setup

setup(
    name='django-neighborhoods',
    version='2.0',
    url='http://github.com/latestrevision/django-neighborhoods/',
    description='Get neighborhood information for your coordinates.',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    install_requires=[
        'django-localflavor>=1.0',
    ],
    packages=[
        'neighborhoods', 
        'neighborhoods.management',
        'neighborhoods.management.commands',
        'neighborhoods.migrations',
        ],
)
