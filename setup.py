from setuptools import setup, find_packages

setup(
    name = "python-redisdnsd",
    version = "0.2",
    packages = find_packages(),
    author = "3onyc",
    author_email = "3onyc@x3tech.com",
    description = "A DNS server using Redis as a storage backend and gevent networking",
    license = "MIT",
    keywords = "dns redis gevent",
    url = "http://github.com/x3tech/python-redisdnsd",
    install_requires = [
        'gevent>=1.0,<1.1',
        'cython',
        'redis',
        'dnslib'
    ],
    entry_points = {
        'console_scripts': [
            'python-redisdnsd = pyredisdnsd.main:main'
        ]
    }
)
