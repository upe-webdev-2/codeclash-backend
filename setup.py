from setuptools import setup

setup(
    name = "codeclash_backend",
    packages = ['codeclash_backend'],
    include_package_data = True,
    install_requires = [
        'flask',
        'python-dotenv',
        'requests',
        'flask-socketio',
        'simple-websocket',
        'eventlet',
        'prisma',
        'coverage'
    ],
)