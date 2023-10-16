"""A setup tools based setup module.
"""

import setuptools


setuptools.setup(
    name="log-highlighter",
    version="1.0",

    packages=[
        'highlight',
    ],

    entry_points={
        'console_scripts': [
            'highlight=highlight:main',
        ],
    },
)
