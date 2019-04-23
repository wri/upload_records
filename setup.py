from setuptools import setup, find_packages

setup(
    name="upload_records",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click", "boto3", "retrying", "requests"

    ],
    entry_points="""
        [console_scripts]
        concatenate_record=upload_records.concatenate_record:cli
    """,
)