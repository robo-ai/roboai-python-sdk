import setuptools
from setuptools import setup
from robo_sdk import __version__


setup(
    name='robo-python-sdk',
    description='ROBO-AI SDK',
    version=__version__,
    author='ROBO-AI',
    author_email='info@robo-ai.com',
    url='https://robo-ai.com/',
    download_url='',
    py_modules=['robo_ai','robo_nlu'],
    packages=setuptools.find_packages(),
    setup_requires=['attrs', 'cattrs', 'requests','requests-toolbelt','pyyaml','pydantic'],
    install_requires=['attrs', 'cattrs', 'requests','requests-toolbelt','pyyaml','pydantic'],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
