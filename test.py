import os
import discord
from datetime import date, timezone
import requests
import json
import datetime
from keep_alive import keep_alive

'''
To get today's date
'''
yesterday = date.today() - datetime.timedelta(days=1)
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")
year = yesterday.strftime("%y")
print(month, day, year)


intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)

def get_data():
  details = []
  game = []
  return (year,month,day)
  # response = requests.get(f"https://api.sportradar.com/nba/trial/v7/en/games/{year}/{month}/{day}/schedule.json?api_key={os.environ['API_KEY']}")
  # print(response)
  # json_data = json.loads(response.text)
  # for i in json_data['games']:
  #   d = datetime.fromisoformat(i['scheduled'][:-1]).astimezone(timezone.utc)
  #   game.append(d.strftime('%Y-%m-%d %H:%M'))
  #   game.append("@"+i['venue']['name'])
  #   game.append(i['home']['name'] + " vs " + i['away']['name'])
  #   game.append(i['id'])
  #   details.append(game)
  #   game = []
  # return details

def get_summary(game_id):
  data = ''
  response = requests.get(f"https://api.sportradar.com/nba/trial/v7/en/games/{game_id}/summary.json?api_key={os.environ['API_KEY']}")
  json_data = json.loads(response.text)
  data = f'''
    Status: {json_data["status"]}
    Q{json_data["quarter"]} - {json_data["clock"]}
    {json_data["home"]["name"]}: {json_data["home"]["points"]}
    {json_data["away"]["name"]}: {json_data["away"]["points"]}'''
  return data
  
class MyView(discord.ui.View):
    value = get_data()
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Game!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label=i[2],
                emoji = "🏀",
                description= f"Held at {i[1]} Time: {i[0]}",
                value= i[3]
            ) for i in value
        ]
    )
  
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
      summary = get_summary(select.values[0])
      await interaction.response.send_message(f"Awesome! Match Summary is {summary}")

@client.event
async def on_message(message):
  if message.author == client.user:
    return 
    
  await message.channel.send("The scheduled NBA games are", view=MyView())

print(get_data())
# client.run(os.environ['TOKEN'])