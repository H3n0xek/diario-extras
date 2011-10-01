try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import user_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    
    
setup(
    name = 'diario-extras',
    version = '0.1.0',
    description = 'Extra features for django-diario weblog application',
    long_description = ('This app contains additional views and some features, like a moderation and entry statuses'),
    keywords = 'django diario apps weblog blog',
    install_requires = [ 'django-diario', ],
    author = 'H3n0xek and others (see AUTHORS file)',
    author_email = 'H3n0xek@blackhat.cc',
    url = 'http://github.com/H3n0xek/diario-extras',
    license = 'GNU Lesser General Public License (LGPL), Version 3',
    classifiers = [
        'Environment :: Plugins',
        'Framework :: Django',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,    
)    

    