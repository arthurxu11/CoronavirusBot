# Arthur Xu
# April 8th, 2020
# CoronaVirus Case Monitor

import discord, random
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

client = commands.Bot(command_prefix = "!")

dailyTime = '11:00' #What time the daily message will be sent. Use 24hr format (7PM = 19:00)
defaultCountry = 'Enter country' # The default country for daily messages

@client.event
async def on_ready():
    # Updates when bot is online
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(Enter channel here) #Enter channel to send daily updates to 
    # Starts checking if it's time for the daily update
    await channel.send(dailyUpdates())

@client.event
async def on_message(message):
    # Ignores itself
    if message.author == client.user:
        return
    
    # When bot is called
    if message.content.startswith('!cases'): # Bot call
        msg = message.content
        # Gets the country name (Ignores !cases)
        country = msg[7:]
        country = country.lower()
        # Sends a request to the coronavirus statistics website
        url = "https://www.worldometers.info/coronavirus/country/"+country+"/"
        try:
            # Calls getStats method
            results = getStats(url)
            # Prints results
            await message.channel.send("Cases: "+results[0]+"\n Deaths: "+results[1]+"\n Recovered: "+results[2])
        except:
            # Does not work with invalid country
            await message.channel.send("Invalid Country!")

def getStats(url):
    # Requests for the stats from worldometers.com
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll(id="maincounter-wrap")
    result = []

    # Gets the relevant info
    for tabs in results:
        number = tabs.find('span')
        number = (number.text.strip())
        result.append(number)
        
    return(result)

def dailyUpdates():
    # Checks if the time is the time for the daily message
    now=datetime.strftime(datetime.now(),'%H:%M')
    while True:
        now=datetime.strftime(datetime.now(),'%H:%M')
        if now == dailyTime:
            # If it is time for the daily message, call getStats and send it to the channel
            dailyUrl = "https://www.worldometers.info/coronavirus/country/"+defaultCountry+"/"
            dailyResults = getStats(dailyUrl)
            message = str("Country: "+defaultCountry+"\n Cases: "+dailyResults[0]+"\n Deaths: "+dailyResults[1]+"\n Recovered: "+dailyResults[2])
            return message
            time.sleep(75)
        else:
            # Only checks every 15 seconds
            time.sleep(15)

client.run('Enter bot token here')
