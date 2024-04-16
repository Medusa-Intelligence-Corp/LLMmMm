#!/bin/bash

sudo docker run -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY -it --rm -p 5000:5000 sommelier
