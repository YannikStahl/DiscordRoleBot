import os, re, discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


@tree.command(name="setpayout",
             description="This command gives you a Role.")
async def setpayout(interaction: discord.Interaction, role: discord.Role):
  member = interaction.user
  try:
    await member.add_roles(role)
  except Exception as e:
    print(f"Error {e}  occurd while trying to add that Role.")
  await interaction.response.send_message(
    f"Successfully added Role '{role.name}' to User {interaction.user.mention}!",
    ephemeral=True)


@tree.command(name="resetpayout",
             description="This command removes a Role from you.")
async def resetpayout(interaction: discord.Interaction, role: discord.Role):
  member = interaction.user
  try:
    await member.remove_roles(role)
  except Exception as e:
    print(f"Error {e}  occurd while trying to remove that Role.")
  await interaction.response.send_message(
    f"Successfully removed Role '{role.name}' from User {interaction.user.mention}!",
    ephemeral=True)


@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")
  try:
    await tree.sync()    
    print(f"Synced successfully!")
  except Exception as e:
    print(f"Error syncing commands: {e}")


client.run(DISCORD_TOKEN)
