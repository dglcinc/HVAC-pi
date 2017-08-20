#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COMMAND="python $DIR/sk-sensor-emit.py $@"

exec -a sk_provider $DIR/sk-provider.sh $COMMAND &
