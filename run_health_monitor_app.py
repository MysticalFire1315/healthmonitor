
import os
import sys

sys.path.append(os.path.dirname(__name__))

from healthmonitor_app import create_app

# create an app instance
app = create_app("app_config.toml")

app.run(debug=True)
