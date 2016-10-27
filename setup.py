import os

from image_optimizer import __version__
from setuptools import setup, find_packages

base = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='image_optimizer',
    version=__version__,
    description='PIL based image optimizer',
    long_description=long_description,
    url='https://github.com/Bobsans/image-optimizer',
    download_url='https://pypi.python.org/pypi/image_optimizer',
    author='Bobsans',
    author_email='mr.bobsans@gmail.com',
    maintainer='Bobsans',
    maintainer_email='mr.bobsans@gmail.com',
    license='Freeware',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: Freeware',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities'
    ],
    keywords='PIL optimize image',
    platforms=['Any'],
    packages=find_packages(),
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': ['image_optimizer=image_optimizer.optimizer:main']
    }
)
