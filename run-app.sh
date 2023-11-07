#!/bin/bash

sudo docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -it --rm -p 5000:5000 sommelier
