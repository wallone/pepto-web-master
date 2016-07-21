
import os

from web import app


def islocal():
    return os.environ["SERVER_NAME"] in ("localhost")

# FIXME this needs to be moved to a private file
app.secret_key = "b'\xdb\xe2\x14c\xee!\xb7F\x9c\xc8x\x8b\x04b\xbf\xad(\xc5(\x9f\x9az\xd6\x92'"

if __name__ == '__main__':
    extra_dirs = ['.']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)

    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port, debug=True, extra_files=extra_files)
