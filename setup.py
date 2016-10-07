#!/usr/bin/env python

import setuptools


setuptools.setup(
        name='python-pyng',
        version='0.1.0',
        description='Utility for sending asynchronous ping messages',
        license='GPLv2',
        long_description=(open('README.rst').read()),
        author='Joshua Downer',
        author_email='joshua.downer@gmail.com',
        url='http://github.com/jdowner/pyng',
        keywords='ping ICMP asyncio',
        packages=['pyng'],
        package_data={
          '': ['*.rst', 'LICENSE'],
        },
        scripts=['bin/pyng'],
        install_requires=[
            'docopt',
            ],
        platforms=['Unix'],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Communications",
            "Topic :: Internet",
            "Topic :: System",
            "Topic :: System :: Monitoring",
            "Topic :: System :: Networking",
            "Topic :: System :: Networking :: Monitoring",
            "Topic :: System :: Systems Administration",
            "Topic :: Utilities",
            ]
        )
