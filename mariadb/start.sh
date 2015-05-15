#!/bin/bash

touch 'finnotest'

__run_supervisor() {
echo "Running the run_supervisor function."
/usr/bin/supervisord
}

# Call all functions
__run_supervisor
