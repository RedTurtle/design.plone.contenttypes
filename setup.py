# -*- coding: utf-8 -*-
"""Installer for the design.plone.contenttypes package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="design.plone.contenttypes",
    version="1.0.8",
    description="DesignItalia contenty types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="RedTurtle",
    author_email="sviluppoplone@redturtle.it",
    url="https://github.com/collective/design.plone.contenttypes",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/design.plone.contenttypes",
        "Source": "https://github.com/collective/design.plone.contenttypes",
        "Tracker": "https://github.com/collective/design.plone.contenttypes/issues",
        # 'Documentation': 'https://design.plone.contenttypes.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["design", "design.plone"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.app.dexterity",
        "collective.dexteritytextindexer",
        "collective.venue[geolocation]",
        "plone.formwidget.geolocation",
        "redturtle.volto",
        "redturtle.bandi",
        "z3c.unconfigure",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
            "collective.MockMailHost",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = design.plone.contenttypes.locales.update:update_locale
    """,
)
