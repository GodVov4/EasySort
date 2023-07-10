from setuptools import setup, find_namespace_packages


setup(
    name='EasySort',
    version='1.0.1',
    description='EasySort will help you to sort files in your folder',
    long_description='Many people have a folder on their desktop called something like "Disassemble". /'
                     'As a rule, hands never manage to disassemble this folder. EasySort will help you',
    url='https://github.com/GodVov4/EasySort',
    author='Volodymyr Martyn',
    author_email='martin.volodya@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=['pyfiglet'],
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)
