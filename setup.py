import re

from setuptools import setup
from setuptools import find_packages
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(
    join(CURDIR, "webhooks", "src", "__init__.py"), encoding="utf-8"
) as f:
    VERSION = re.search('\n__version__ = "(.*)"', f.read()).group(1)

setup(
    name="robotframework-webhooks",
    version=VERSION,
    author="M.Kherki(Alpha-Centauri-00)",
    author_email="alpha_Centauri@posteo.de",
    description="A listener that sends a Stack Trace to MS-Teams or Slack where the failure appears.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alpha-Centauri-00/robotframework-webhooks",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    install_requires=["robotframework >= 3.2"],
    python_requires=">=3.6",
)
