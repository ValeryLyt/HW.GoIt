from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.0',
    description='Folder parser',
    author='Valeriia Lytvynova',
    author_email='lyt.valery3340@gmail.com',
    url='https://github.com/ValeryLyt/HW.GoIt/blob/main/HW_7/clean_folder/setup.py',
    license='',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']},
)