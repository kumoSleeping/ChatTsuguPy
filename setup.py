from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='tsugu',
    version='3.1.1',
    author='kumoSleeping',
    author_email='zjr2992@outlook.com',
    license="MIT",
    description='Tsugu Python Frontend',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kumoSleeping/ChatTsuguPy',
    packages=find_packages(exclude=('test','test*')),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
            "loguru",
            "tsugu-api-python>=1.3.3",
            "arclet-alconna",
        ],
    python_requires='>=3.8',
    include_package_data=False,

)
