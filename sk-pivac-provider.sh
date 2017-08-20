#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COMMAND="python $DIR/sk-sensor-emit.py $@"

exec $DIR/sk-provider.sh $COMMAND
