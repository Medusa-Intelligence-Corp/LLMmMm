# LLMmMm 😋

A free and open source LLM-powered Sommelier. Try it now at [LLMmMm.com](https://llmmmm.com). Made via a simple flask API and static webpage that connects to [OpenRouter](https://openrouter.ai/).

# Testing

* install docker
* get an ```OPENROUTER_API_KEY``` saved as an environment variable (look it up)
* clone this repository
* ```cd``` to the project directory
* ```bash build.sh```
* ```bash run.sh```

# Production Setup Guide

This guide will walk you through the steps to set up your Flask server with SSL using Nginx on a Debian or Ubuntu-based system.

## Prerequisites

- Debian or Ubuntu-based operating system
- ```OPENROUTER_API_KEY``` saved as an environment variable
- Docker installed

## Installation

1. Update the package list and install the required packages:
   ```
   sudo apt-get update
   sudo apt-get install -y --no-install-recommends certbot nginx
   ```

1. Open ports 80 and 443 for http and https
   ```
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

2. Stop the Nginx service temporarily:
   ```
   sudo systemctl stop nginx
   ```

3. Obtain an SSL certificate using Certbot:
   ```
   sudo certbot certonly --standalone -d api.llmmmm.com
   ```

## Nginx Configuration

1. Create a new Nginx configuration file for your domain:
   ```
   sudo nano /etc/nginx/sites-available/api.llmmmm.com
   ```

2. Add the following configuration to the file:
   ```
    server {
        listen 80;
        server_name api.llmmmm.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name api.llmmmm.com;

        ssl_certificate /etc/letsencrypt/live/api.llmmmm.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.llmmmm.com/privkey.pem;

        location / {
            proxy_pass http://localhost:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;

            # Add the following lines to include CORS headers
            proxy_set_header Access-Control-Allow-Origin "https://llmmmm.com";
            proxy_set_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
            proxy_set_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range";
            proxy_set_header Access-Control-Expose-Headers "Content-Length,Content-Range";
        }
    }
    ```

3. Save the file and exit the editor.

4. Enable the Nginx configuration by creating a symbolic link:
   ```
   sudo ln -s /etc/nginx/sites-available/api.llmmmm.com /etc/nginx/sites-enabled/
   ```

5. Test the Nginx configuration for any errors:
   ```
   sudo nginx -t
   ```

6. If there are no errors, restart the Nginx service:
   ```
   sudo service nginx restart
   ```

## Application Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repository.git
   ```

2. Change to the project directory:
   ```
   cd your-repository
   ```

3. Build the Docker image:
   ```
   bash build.sh
   ```

4. Edit the ```run.sh``` script for produciton, replace the ```-it``` flag with a ```-d``` flag. 

4. Run the Docker container:
   ```
   bash run.sh
   ```

Your Flask server should now be up and running with SSL enabled, accessible at ```https://api.llmmmm.com```.


