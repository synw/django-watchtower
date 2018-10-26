from setuptools import setup, find_packages

version = __import__('watchtower').__version__

setup(
    name='django-watchtower',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description='Collect metrics and events from Django',
    author='synw',
    author_email='synwe@yahoo.com',
    url='https://github.com/synw/django-watchtower',
    download_url='https://github.com/synw/django-watchtower/releases/tag/' + version,
    keywords=['django', 'monitoring'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "redis",
        "geoip2",
        "django-user-agents",
    ],
    zip_safe=False
)
