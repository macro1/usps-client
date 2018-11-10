import setuptools


setuptools.setup(
    name="usps_client",
    version="0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=["urllib3[secure]"],
)
