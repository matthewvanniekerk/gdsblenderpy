from setuptools import setup,find_packages

with open('README.md', 'r') as f:
    readme = f.read()
dependencies = [
        'numpy',
        'gdspy',
        'matplotlib>=2.2.2',
        'phidl',
        'progressbar2'
]
setup(
    name='gdsblenderpy',
    version='0.0.2',
    description='GDS to Blender Python Translator',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Matthew van Niekerk',
    author_email='matthewvanniekerk@mac.com',
    url='https://github.com/matthewvanniekerk/gds-blender-py',
    packages=find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)