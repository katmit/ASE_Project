import yaml
import Tests

from Utils import cli
import Repgrid

import os

SCRIPTDIR = os.path.dirname(__file__)
YAMLFILE = os.path.join(SCRIPTDIR, 'config.yml')

##
# Loads a YAML configuration file "config.yml" into a Python dictionary
# "configs" using the yaml library.
#
# Prints usage information for the script and the options it supports.
#
# Runs an infinite loop (run_csv = True) to allow the user to input various
# options/arguments and update the configuration file "config.yml".
#
# If the 'help' field in the configuration file is set to True, it will
# print help text for the script's options.
#
# The "cli" function from the Utils module is used to process the user's
# input (stored in "csv_args") and update the "configs" dictionary
# accordingly.
#
# The updated "configs" dictionary is then written back to the "config.yml"
# file.
#
# The "Tests.ALL()" method is called, which runs a suite of tests
# for the script.
#
# The script allows the user to run a series of tests with
# different options/arguments and store the configuration in a YAML file.
##
with open(YAMLFILE, "r") as config_file:
    configs = yaml.safe_load(config_file)

help_string = """USAGE: xpln.py [OPTIONS] [-g ACTION] \n OPTIONS:\n"
      "-b  --bins       initial number of bins           = 16\n"
      "-c  --cliffs     cliff's delta threshold          = 0.147\n"
      "-d  --d          different is over sd*d           = 0.35\n"
      "-f   --file      name of file                     = ../etc/data/auto93.cs\n"
      "-F   --Far       distance to \"faraway\"          = .95\n"
      "-g  --go         start-up action                  = run all tests\n"
      "-h  --help       show help                        = false\n"
      "-H  --Halves     search space for clustering      = 512\n"
      "-m  --min        smallest cluster                 = .5\n"
      "-M  --max        numbers                          = 512\n"
      "-p  --p          distance coefficient             = 2\n"
      "-r  --rest       how many of rest to sample       = 4\n"
      "-s  --seed       random number seed               = 937162211 \n"
      "-R  --Reuse      child splits reuse a parent pole = true\n"
      "-q  --quit  exit \n"""

print("xpln.py : multi-goal semi-supervised explanation\nenter -h/--help for help.\n")

run_csv = True

while run_csv:
    csv_args = input("Select an option/s \n")
    new_configs = cli(csv_args, configs)

    with open(YAMLFILE, "w") as config_file:
        config_file.write(yaml.dump(new_configs))

    if new_configs['the']['help']:
        print(help_string)

    if new_configs['the']['quit']:
        quit()

    if new_configs['the']['go']:
        Tests.ALL()
