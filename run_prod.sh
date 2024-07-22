#!/bin/bash

sudo podman run -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY -d --rm -p 5000:5000 sommelier
