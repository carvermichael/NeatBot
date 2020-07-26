# NeatBot

## Setup

1. Install Python 3.x.x (Discord claims a dep of > 3.5.3, it's working for me on 3.7.6)
2. Install discord.py 1.3.4
3. Create and fill out a properties.py file in the same directory as neatbot.py.
4. Add two properties to this file:
    ```
    neatbotToken={DiscordBotAPIToken}
    giphyToken={GiphyAPIToken}
    ```
5. Run neat_bot.py!


### If you like to copy commands:

```
pip3 install -r requirements.txt
```
```
echo "neatbotToken={DiscordBotAPIToken}
giphyToken={GiphyAPIToken}" >> properties.py
```
```
python neat_bot.py
```

### Testing

Run the tests
```
python -m unittest
```
```
python -m unittest tests/TestBookService.py 
```
