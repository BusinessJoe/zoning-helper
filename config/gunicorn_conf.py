from pathlib import Path

bind = 'unix:/tmp/nginx.socket'
Path('/tmp/app-initialized').touch()
