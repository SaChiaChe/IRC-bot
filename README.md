# IRC Robot
A simple IRC robot that has 5 simple functions.

## How to run

Start the program
```
python bot.py
```

Input the Host IP
```
Host IP: *INPUT HERE*
```

Input the Port
```
Port: *INPUT HERE*
```

Then the bot would try to connect to the server.
If it fails, then the program would end.

Input the Nickname
```
Nickname: *INPUT HERE*
```

Input the Username
```
Username: *INPUT HERE*
```

Input the Channel
```
Channel: *INPUT HERE*
```

The bot would now join the Channel and introduct it self

```
PRIVMSG #*Channel* :I'm *Username*
```

And continuously receive message and reply to it.

To close the bot, just input QUIT
```
QUIT
```

## Description

An simple IRC robot running on a IRC server made by alexyoung (https://github.com/alexyoung/ircd.js)
It has 5 functions:

### 1. Connection to Channel & Automatic Introduction Message:

Connect to the desired channel and Introduct itself
```
PRIVMSG #*Channel* :I'm *Username*
```

### 2. Daily horoscope:

When recieve a message:
```
<constellation>
```

The bot will reply with a daily horoscope
```
今天在你的專業領域上會有好機會降臨
```

### 3. Guess Number

When recieve a message:
```
!guess
```

The bot would start a number guessing game, 
the user have to guess a number between 1 and 10, 
if the number is illegal, the bot will ignore it,
and the bot would give hints if the user guessed a legal number.
The user can't quit the game before he guessed the correct answer.

### 4. Music bot

When recieve a message:
```
!song <song_name>
```

The bot will go to youtube and find a song that is related to the song_name.

### 5. Chat

When recieve a message:
```
!chat
```

The bot will start receiving user input,
and both the user's and the bot's message will be displayed simultaniously.
User may send or receive message continuously.

If the user wants to end the chat, 
just send !bye
```
!bye
```

and the chat will end.

## Built With

* Python 3.6.0 :: Anaconda custom (64-bit)

## Authors

* **SaKaTetsu** - *Initial work* - [SaKaTetsu](https://github.com/SaKaTetsu)
