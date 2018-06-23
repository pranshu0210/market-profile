from setuptools import setup

setup(
    name='mktProfile',
    version='0.1.0',
    author='Pranshu Dave',
    author_email='pranshudave@gmail.com',
    packages=['mktProfile'],
    url='https://github.com/pranshu0210/mktProfile',
    license='MIT license',
    description='A library that generates Market Profile from OHLC data',
    long_description="",
    install_requires=[
        "numpy >= 1.13.0",
        "pandas >= 0.20.3",
    ],
    keywords=['python', 'finance', 'market profile', 'quant', 'stock', 'crypto'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)
