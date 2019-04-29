from setuptools import setup, find_packages

setup(
    name="upload_records",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "boto3", "retrying", "requests"],
    entry_points={
        "console_scripts": [
            "create_dataset=upload_records.create:cli",
            "concatenate_records=upload_records.concatenate:cli",
        ]
    },
)
