from setuptools import setup, find_packages

setup(
    name='data_catalog',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'dash',
        'plotly',
        'dash-bootstrap-components', 
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'data-catalog = data_catalog.dash_app:run_server'
        ]
    },
    author='Nic Herfel',
    author_email='nsherfel@gmail.com',
    description='An interactive data cataloging tool for internal use.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nsherfel/tds-datsci-data-catalog.git',
)
