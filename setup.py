import os
import setuptools

if "requirements.txt" in os.listdir("."):
    with open("requirements.txt", encoding="utf-8") as r:
        requires = [i.strip() for i in r]  # Зависимости
else:
    requires = []


with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


name = "aio_crystal_pay"
author = "alteralt"


setuptools.setup(
    name=name,
    version="1.0.4",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    author=author,
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: Russian",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={"Source": "https://github.com/{}/{}".format(author, name)},
)
