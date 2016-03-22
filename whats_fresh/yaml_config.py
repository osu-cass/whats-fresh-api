from yaml import load
import os

print("getting yaml config")

DEFAULT_CONFIG_DIR = './'
CONFIG_DIR = os.environ.get('WF_CONFIG_DIR', DEFAULT_CONFIG_DIR)

print(CONFIG_DIR)

CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yml')

# Open our yaml config and override settings values with it's config
try:
    config_file = open(CONFIG_PATH)
    for key, value in load(config_file.read()).items():
        globals()[key] = value
    config_file.close()
except Exception, e:
    print "Could not find, or open config located at %s" % CONFIG_PATH
    print "The error occured was: %s" % e
