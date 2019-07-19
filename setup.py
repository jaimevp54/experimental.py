from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='experimental',
    packages=['experimental'],
    version='0.0.1',
    description='Safe python experimenting.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jaime Vinas',
    author_email='jaimevp54@gmail.com',
    license="MIT",
    url='https://github.com/jaimevp54/experimental.py',
    download_url='https://github.com/jaimevp54/experimental.py/archive/0.0.1.tar.gz',
    keywords=['feature', 'experiments', 'testing', 'rollback'],
    python_requires='>=2.7',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
