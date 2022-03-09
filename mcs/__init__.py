# This file defines that this is a package
# This file has no uses besides generating documentation for Doxygen

## @package mcs
# The top level package for the MCS 
#
# This package is top level package that has three system controllers
# The system controllers are defined as programs/process that loads and runs the controllers.
# 
# The first system controller is the Mowbot Controller.
# This starts the other system controllers in different threads so the system controllers can run in parallel.
#
# The second system controller is the Drive system controller.