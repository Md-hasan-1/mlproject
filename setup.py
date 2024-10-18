from setuptools import find_packages, setup
from typing import List

# This function gets all the names of packages 
def get_requirements(file:str)->List[str]:
    """
    params:
        - file -> path of file for requirements.
RETURNS: List of names present inside file obj.
    """
    requirements = list()
    HED = "-e ."
    with open(file) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HED in requirements:
            requirements.remove(HED)

    return requirements


setup(
    name="mlproject",
    version="0.0.1",
    author="Hasan",
    author_email="hasanraza768001@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
