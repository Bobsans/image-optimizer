from setuptools import setup
from image_optimizer import optimizer

setup(
    name='image_optimizer',
    version=optimizer.__version__,
    description='PIL based image optimizer',
    long_description='PIL based image optimizer',
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
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    keywords=['PIL', 'optimize', 'image'],
    platforms=['Any'],
    packages=['image_optimizer'],
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': ['image_optimizer=image_optimizer.optimizer:main']
    }
)
