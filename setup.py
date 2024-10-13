from setuptools import setup
import os

about = {}

with open("minds_cli/__about__.py") as fp:
    exec(fp.read(), about)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")) as req_file:
    requirements = req_file.read().splitlines()

def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name=about['__package_name__'],
    description=about['__description__'],
    long_description=get_long_description(),
    download_url=about['__pypi__'],
    keywords="minds mindsdb ai",
    long_description_content_type="text/markdown",
    author=about['__author__'],
    url=about['__github__'],
    project_urls={
        "Issues": about['__github__'] + "/issues",
        "CI": about['__github__'] + "/actions",
        "Changelog": about['__github__'] + "/releases",
    },
    license="Apache License, Version 2.0",
    version=about['__version__'],
    packages=["minds_cli"],
    entry_points="""
        [console_scripts]
        minds=minds_cli.cli:main
    """,
    install_requires=requirements,
    extras_require={"test": ["pytest", "pytest-mock"]},
    python_requires=">=3.7",
)