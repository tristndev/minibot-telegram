# minibot-telegram

![PyPI pyversions](https://img.shields.io/badge/python-2.*%20%7C%203.*-blue)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Code Size](https://img.shields.io/github/languages/code-size/tristndev/minibot-telegram)

A (really) minimal framework for sending messages with a Telegram bot. 

## Intro & Motivation

`minibot-telegram` was developed as a very minimal framework for *unidirectionally sending messages to a single recipient with a Telegram bot*.

In my daily work developing Python code, I often encountered situations where scripts ran over a longer period of time on remote machines and I wanted to either

- be notified when the script execution finished (see `Mode A` below), or
- be updated on the go, how things are going (see `Mode B` below).

Originally created as a submodule of one of my projects, I decided to extract the `minibot-telegram` functionality as a modular part, mainly to facilitate refactoring and reuse in other projects. 

## Usage

### Installation

Simply `git clone` this repository into a subdirectory called `Minibot` of your project and install the required packages using pip:

```
$ git clone https://github.com/tristndev/minibot-telegram.git Minibot
$ pip install -r minibot
```

### Getting started

#### Creating a bot and finding out your `USER_ID`

Firstly, you will need to create a [Telegram bot](https://core.telegram.org/bots) by talking to the [Botfather](https://telegram.me/botfather). 
After choosing an adequate name, he will assign your bot a `TOKEN` which you will have to store somewhere safe.

Since we want the bot to basically talk to one person only, we need to find out that person's Telegram `USER_ID`.
This is achieved with the following steps:

1. Send an arbitrary message from the Telegram account you want to receive the updates to the bot you just created. You can find that bot by searching for its name in the standard Telegram search. 
2. Execute the `minibot.py` script with the flag `--userid`, so something like 

   ```bash
   $ python minibot.py --userid
   ```

3. The last user ID your bot received a message from will be printed to the console.

In summary, you now know your bot `TOKEN` as well as your personal `USER_ID`.

#### Setting up your `.env` file

The `minibot` script needs to know the bot to send messages from and the user to send messages to.
For this, the corresponding information is stored in a `.env` file that needs to be stored in the same directory as the `minibot.py` script.

> *Attention: Make sure to always exclude the `.env` file from your version control (git, etc.). We do not want other people to mess with your bot.*

The content of the `.env` file should look like this:

```yaml
TOKEN = "YourTokenHere"
USER_ID = 12345
```

### Mode A: Import the module in your code.

You can easily import the module into your code via `import minibot` (that is, if the `minibot.py` file is in the same directory). 

The usage then works as in [`example.py`](example.py):

```python
import time
try:
    import minibot # import minibot in your project
except:# You might have to use (when Minibot is in a subdirectory)
    from Minibot import minibot

if __name__ == '__main__':
    # 1. Do your work
    print("Let's do some work. Counting to 10...")
    for i in range(10):
        print(i)
        time.sleep(0.1)

    print("All work done. Calling minibot...")
    # 2. Handle the Telegram messaging
    mb = minibot.MiniBot() # create a minibot instance
    mb.send_message("All work done.") # send a notification
    print("Telegram message sent.")
```

#### Worker Functions

There are two main worker functions you can use to construct messages:

* `send_message(message)` sends the string `message` to the defined user ID

  *Example*:

  ```python
  import minibot
  mb = minibot.MiniBot
  mb.send_message("Your message here")
  ```

* `send_dictionary(dict, message=None)` creates a string of the following format, formatted as code:

  ```
  message (if specified)
  key1:	value1
  key2: 	value2
  ...
  ```

  *Example*:

  ```python
  import minibot
  mb = minibot.MiniBot()
  mb.send_dictionary({"key1": "value1", "key2": 123}, "Your intro message here")
  ```

### Mode B: Let a cron job trigger messages.

With Linux, you can simply schedule a cronjob to periodically execute the messaging task. 

#### 1. Set up the code

The cron job executes the `minibot.py` file as a main program (like we would with a terminal call `python minibot.py`). Accordingly, we need to define what to do once the script is called by the cron job.

Look for the function `collect_info_into_message` right above the line `if __name__=="__main__"`, and implement the logic you want to execute periodically:

```python
...
def collect_info_into_message():
    # Do your info collection here.
    # For example: Look for a log file and extract some info. 
    return "Your collected information."

if __name__ == '__main__':
    ...

```

#### 2. Create the cronjob

For the example: Execute *"every two hours between 8 and 23h"*, insert the following line in the crontab file (open with `crontab -e`):

```bash
0 8-23/2 * * * /usr/bin/python /home/user/<your_project>/minibot.py

```
>  A good tool to create crontab schedule expressions is [`crontab guru`](https://crontab.guru/).

## The `.env` file in Git

The `.env` file was initially added to the git repo, but changes are not tracked via

```bash
$ git update-index --skip-worktree .env
```

If changes should be tracked again, use:

```bash
$ git update-index --no-skip-worktree .env
```