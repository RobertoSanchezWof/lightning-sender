from setuptools import setup, find_packages

setup(
    name='lightning-sender',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'webSocketClient = webSocketClient:main',
        ],
    },
)