import discord
import os

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)

class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
  
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
      await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

@client.event
async def on_message(message):
  if message.author == client.user:
    return 
    
  await message.channel.send("Choose a flavor!", view=MyView())
  
client.run(os.environ['TOKEN'])