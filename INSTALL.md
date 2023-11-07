# INSTALLATION

a template project for machine learning experiments, using dockerized pytorch environments and data downloaders

# Requirements

* [docker](https://www.docker.com/)
* a bash shell



# Optional Dependencies
* OpenAI key if you are using scikit-llm
* for GPU users [nvidia container toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)

# Setting up your openAI api key

* get your API key from openai.com [see video](https://www.youtube.com/watch?v=lnQsO-2MwXM)

Setting up an environment variable for your OpenAI API key across different operating systems requires a slightly different approach for each OS. Here's a step-by-step guide to setting up the `OPENAI_API_KEY` environment variable on Linux, Windows, and macOS.

### Linux
1. **Edit the `~/.bashrc` or `~/.bash_profile` file**:
   - Open a terminal.
   - Use a text editor to open the `~/.bashrc` or `~/.bash_profile` file, e.g., `nano ~/.bashrc`.
2. **Add the following line** to the end of the file:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
3. **Save and close** the file.
4. **Apply the changes** by either:
   - Closing and re-opening the terminal, or,
   - Running the command `source ~/.bashrc` or `source ~/.bash_profile`.

### Windows
1. **Open the System Properties**:
   - Press `Win` + `Pause|Break` keys together or right-click on 'This PC' on the desktop or in File Explorer, and choose Properties.
   - Click on "Advanced system settings" on the left.
2. **Open Environment Variables**:
   - Click on the "Environment Variables" button near the bottom right.
3. **Create a new System Variable**:
   - Under the System Variables section, click "New".
   - Enter `OPENAI_API_KEY` as the Variable name and your API key as the Variable value.
   - Click OK on all dialogs to save.

### macOS
1. **Edit the `~/.zshenv` or `~/.bash_profile` file**:
   - Open a terminal.
   - macOS 10.15 (Catalina) and later uses the Z shell by default, so you would typically use `nano ~/.zshenv`. For earlier versions, use `nano ~/.bash_profile`.
2. **Add the following line** to the end of the file:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
3. **Save and close** the file.
4. **Apply the changes** by either:
   - Closing and re-opening the terminal, or,
   - Running the command `source ~/.zshenv` or `source ~/.bash_profile`.

Remember to replace `'your-api-key-here'` with your actual OpenAI API key in each of the steps above.


# Getting Started

* Build the docker image by using ```sh build-docker-image.sh```
* start your training environment by running ```sh run-training-environment.sh``` or ```sh gpu-environment.sh``` and follow the link to the jupyter server
* Use a [downloader](./downloader/) to download a dataset into the [data](./data/) folder
* Run a [training notebook](./training_notebooks) to fit your model
* Export your model to the [saved models](./saved_models) folder
* Shrink, optimize, and deploy your model, see [deploy](./deploy) for examples 

# Frequently Asked Questions

### Will this run on Windows or macOS?

Not really, but you can try if you must. Specifically the pytorch docker image has known issues on M1 macs, if you want a less fancy environment that you might be able to run on your mac change ```pytorch:latest``` to ```ubuntu:latest``` in the dockerfile, and add ```pip install scikitlearn``` or something like that.

I asked ChatGPT to rewrite the dockerfile so it is less fancy and here's what it said, if you are on a mac you can use the text below as your dockerfile instead:

```
# Start from the latest Ubuntu image
FROM ubuntu:latest

# Set the non-interactive mode for tzdata (prevents the interactive timezone query)
ENV DEBIAN_FRONTEND=noninteractive

# Update the system and install necessary software
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Install Jupyter Notebook, openai, scikit-learn, matplotlib and other useful stuff.
RUN pip install jupyter openai scikit-llm scikit-learn matplotlib numpy pandas seaborn

# Set up the working directory
RUN mkdir /workspace
WORKDIR /workspace

# Change the ownership and permissions of /.local and /workspace
RUN mkdir /.local /.jupyter
RUN chmod -R 777 /.local /.jupyter /workspace

# When the container launches, start a Jupyter Notebook server
CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser"]
```

### How to I shut down the notebook?

Go to the terminal where you ran the ```run-training....sh``` and press ```CTRL+C```, [WTF](https://medium.com/@aantipov/what-happens-when-you-ctrl-c-in-the-terminal-36b093443e06)

### What the hell is this notebook stuff?

Try this tutorial to learn more [tutorial](https://jupyter.org/try)

### Can I deploy this in a cloud environment via Docker? or run it on my big ML rig with many nvidia GPUs?

Hell yes you can! I'll eventually write a more detailed guide here on how to do that, but the setup is almost identical to running locally.
