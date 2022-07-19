import sys
try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False


# Build setuptools-specific options (if installed).
if not has_setuptools:
    print("WARNING: setuptools/distribute not available. Console scripts will not be installed.")
    setuptools_options = {}
else:
    setuptools_options = {
        'entry_points': {
            'console_scripts': [
                'couchpy = couchdb.view:main',
                'couchdb-dump = couchdb.tools.dump:main',
                'couchdb-load = couchdb.tools.load:main',
                'couchdb-replicate = couchdb.tools.replicate:main',
                'couchdb-load-design-doc = couchdb.loader:main',
            ],
        },
        'install_requires': [],
        'test_suite': 'couchdb.tests.__main__.suite',
        'zip_safe': True,
    }


setup(
    name = 'CouchDB-CRUD',
    version = '1.0.1',
    description = 'Python library for working with CouchDB CRUD',
    author = 'Tai Nguyen',
    author_email = 'tainp@viettel.com.vn',
    license = 'BSD',
    url = 'https://github.com/tainp98/couchdb_crud',
    packages = ['couchdb_query', 'couchdb_query.model', 'couchdb_query.doc'],
    **setuptools_options
)