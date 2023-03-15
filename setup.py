from setuptools import setup

setup(
    name='lightningRegister',
    version='1.0',
    entry_points={
    'console_scripts': [
        'lightningRegister.mqttClient:main',
        ],
    }
)