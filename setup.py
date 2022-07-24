import os
import setuptools

if "requirements.txt" in os.listdir("."):
    with open("requirements.txt", encoding="utf-8") as r:
        requires = [i.strip() for i in r]  # Зависимости
else:
    requires = []


name = "aio_crystal_pay"
author = "alteralt"

setuptools.setup(
    name=name,
    packages=setuptools.find_packages(),
    author=author,
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: Russian",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={"Source": "https://github.com/{}/{}".format(author, name)},
)
