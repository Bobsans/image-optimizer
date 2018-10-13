import os

from image_optimizer import __version__
from setuptools import setup, find_packages

base = os.path.abspath(os.path.dirname(__file__))

setup(
    name='image_optimizer',
    version=__version__,
    description='PIL based image optimizer',
    long_description='PIL based image optimizer.\nDetails: https://github.com/Bobsans/image-optimizer',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
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
