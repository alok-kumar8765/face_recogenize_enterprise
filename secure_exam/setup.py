from setuptools import setup, find_packages

setup(
    name="secure_exam",
    version="1.0.0",
    description="AI-based exam proctoring with face & liveness detection",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django",
        "opencv-python",
        "face-recognition",
        "numpy"
    ],
)
