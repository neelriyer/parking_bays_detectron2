from setuptools import find_packages, setup

setup(
    name='airtron',
    version='0.0.1',
    author="Joseph Daniel",
    author_email="joseph@spotparking.com.au",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask',],
)