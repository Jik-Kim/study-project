from glob import glob
from setuptools import find_packages, setup


PACKAGE_NAME = "gesture_robot"


setup(
    name=PACKAGE_NAME,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/gesture_robot"]),
        (f"share/{PACKAGE_NAME}", ["package.xml"]),
        (f"share/{PACKAGE_NAME}/launch", glob("launch/*.launch.py")),
        (f"share/{PACKAGE_NAME}/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="gesture_robot team",
    maintainer_email="team@example.com",
    description="Python nodes for the gesture-controlled tracking robot.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
    'console_scripts': [
        'test_pub = gesture_robot.test_publisher:main',
        'test_sub = gesture_robot.test_subscriber:main',
    ],
},
)
