from setuptools import setup, find_packages


def get_requirements(file_path:str) -> list[str]:
    """
    #### params:
        - file_path: path of the file
#### returns: It returns list of packages names recieved from file.
    """
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()

        requirements = [req.strip("\n") for req in requirements]
        if "-e ." in requirements:
            requirements.remove("-e .")
            
        return requirements


setup(
    name="mlproject",
    version="0.0.1",
    author="Hasan",
    author_email="hasanraza768001@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
