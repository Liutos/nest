# -*- coding: utf8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nest",
    version="0.0.1",
    author="Liutos",
    author_email="mat.liutos@gmail.com",
    description="Nest of tasks and plans.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Liutos/nest",
    project_urls={
        "Bug Tracker": "https://github.com/Liutos/nest/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "click",
        "croniter==2.0.5",
        "DBUtils",
        "Flask",
        "PyMySQL==1.0.2",
        "PyPika",
        "redis",
        "webargs",
    ],
)
