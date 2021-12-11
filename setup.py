from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


with open("basxconnect/__init__.py") as f:
    # magic n stuff
    version = (
        [i for i in f.readlines() if "__version__" in i][-1]
        .split("=", 1)[1]
        .strip()
        .strip('"')
    )

setup(
    name="basxconnect",
    version=version,
    description="CRM application for non-profit organizations",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/basxsoftwareassociation/basxconnect",
    author="basx Software Association",
    author_email="sam@basx.dev",
    license="New BSD License",
    install_requires=[
        "basx-bread",
        "django-phonenumber-field",
        "phonenumbers",
        "django-formtools",
        "djangorestframework",
        "chardet",
        "tablib",
    ],
    extras_require={
        "testing": ["basx-bread[testing]"],
        "mailer-integration": ["mailchimp_marketing"],
    },
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
