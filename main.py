import os, re, discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
roles = ["UTC-1AM", "UTC-2AM", "UTC-3AM", "UTC-4AM", "UTC-5AM", "UTC-6AM", "UTC-7AM", "UTC-8AM", "UTC-9AM", "UTC-10AM", "UTC-11AM", "UTC-12AM", 
         "UTC-1PM", "UTC-2PM", "UTC-3PM", "UTC-4PM", "UTC-5PM", "UTC-6PM", "UTC-7PM", "UTC-8PM", "UTC-9PM", "UTC-10PM", "UTC-11PM", "UTC-12PM"]


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


@tree.command(name="schedule", description="Returns a Schedule of the Fleet Arena Shard.")
async def schedule(interaction: discord.Interaction):
  schedule_text = f"Schedule for Fleet Arena Shard:\n\n"
  for r in roles:
    role = discord.utils.get(interaction.guild.roles, name=r)
    members = role.members
    users = []
    for member in members:
      if member.nick:
        users.append(member.nick)
      else:
        users.append(member.name)
    schedule_text += f"{r} - {', '.join(users)}\n"
  await interaction.response.send_message(schedule_text)


@tree.command(name="convertlocaltime", description="Converts the time you enter from your timezone to UTC.")
@app_commands.choices(hour=[
    app_commands.Choice(name=str(hour)+"AM", value=hour) for hour in range(1,13) ] + [
    app_commands.Choice(name=str(hour)+"PM", value=hour+12) for hour in range(1, 13)
])
async def convertlocaltime(interaction : discord.Interaction, hour: app_commands.Choice[int]):
  timestamp = interaction.created_at
  utc_time = datetime.now(ZoneInfo("UTC")).hour
  print("UTC: " + str(utc_time))
  local_time = timestamp.astimezone().hour
  print("local: " + str(local_time))
  time_difference = local_time - utc_time
  converted_time = (hour.value - time_difference) % 24
  is_pm = converted_time > 12
  if is_pm:
    converted_time -= 12
    await interaction.response.send_message(f"The Time you entered converts to {converted_time} PM in UTC time.")
  else:
    await interaction.response.send_message(f"The Time you entered converts to {converted_time} AM in UTC time.")


@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")
  try:
    await tree.sync()    
    print(f"Synced successfully!")
  except Exception as e:
    print(f"Error syncing commands: {e}")


client.run(DISCORD_TOKEN)
