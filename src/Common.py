import yaml
from pathlib import Path

##
# Imports the yaml and Path modules.
#
# Determines the file path of the script using __file__ and resolve().
#
# Loads a YAML file (config.yml) located in the parent directory of the
# script file.
#
# Opens the YAML file and uses yaml.safe_load() to parse the contents into a Python object.
#
# Defines two variables eg and fails and initializes them to an empty
# dictionary and zero, respectively.
##
my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'config.yml'

with config_path.open() as config_file:
    cfg = yaml.safe_load(config_file)

eg = {}
fails = 0
