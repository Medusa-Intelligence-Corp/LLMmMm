# LLMmMm 😋

A free and open source LLM-powered Sommelier. Try it now at [LLMmMm.com](https://llmmmm.com). Made via a simple flask API and static webpage that connects to [OpenRouter](https://openrouter.ai/).

# Server Installation

* debian or ubuntu bases are recommended
* save your ```OPENROUTER_API_KEY``` as an environment variable
* run ```apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-dev libssl-dev```
* clone this repository
* ```cd``` to the project directory
* ```pip install -r requirements.txt```
* SETUP LETS ENCRYPT ETC...
* run ```gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app```

# TODO
* Setup letsencrypt on debian server
* Support https everywhere
* Deploy
