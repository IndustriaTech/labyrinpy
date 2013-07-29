from setuptools import setup, find_packages

setup(
    name='labyrinpy',
    version='0.1',
    description='Implementation of Labyrintti SMS Gateway API',
    author='Kiril Vladimiroff',
    author_email='kiril@vladimiroff.org',
    url='https://github.com/Vladimiroff/labyrinpy/',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['requests>=1.2.3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
