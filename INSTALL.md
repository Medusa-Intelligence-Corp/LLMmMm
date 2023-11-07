# INSTALLATION

# Requirements

* [docker](https://www.docker.com/)
* a bash shell
* An OpenAI API Key

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


