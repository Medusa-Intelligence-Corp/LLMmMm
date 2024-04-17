#!/bin/bash

#NOTE: If you are running in production remove the -it flag and add a -d flag instead
sudo docker run -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY -it --rm -p 5000:5000 sommelier
