from setuptools import setup
import image_optimizer

setup(
    name='image_optimizer',
    version=image_optimizer.__version__,

    description='PIL image optimizer',
    long_description='PIL based image optimizer',

    url='https://pypi.python.org/pypi/image_optimizer',
    download_url='https://pypi.python.org/pypi/image_optimizer',

    author=image_optimizer.__author__,
    author_email='mr.bobsans@gmail.com',

    license='BSD',

    classifiers=[
        'Development Status :: 4 - Beta',
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

    keywords='PIL image development',

    py_modules=['image_optimizer'],

    install_requires=['Pillow'],

    entry_points={
        'console_scripts': ['image_optimizer=image_optimizer:main']
    }
)
