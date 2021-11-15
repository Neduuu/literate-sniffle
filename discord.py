#from webscr import *
import discord
import os
from dotenv import load_dotenv
from courses import *
from discord.ext import commands
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
    ComponentsBot
)
load_dotenv()
bot = ComponentsBot('!')
def button_components():
  #--------------After course selection --------------------------------
  post_coursebuttons = [[Button(label="Display grades", custom_id="button1"),Button(label = 'Predict grades', custom_id = 'button2')],Button(label='Progress report', custom_id = 'button3')]
  #--------------Assessment buttons --------------------------------------
  assessment_buttons = [[Button(label="", custom_id="button1"),Button(label = 'Predict grades', custom_id = 'button2')],Button(label='Progress report', custom_id = 'button3')]
  

@bot.event
async def on_message(message):
    msg = message.content
    if msg == "hello" or 'hey':
    	await message.channel.send("pies are better than cakes. change my mind.")   
    await bot.process_commands(message)

@bot.command()
async def courses(ctx):
  await ctx.send(
        'Yes but for which course?',
        components = [
            Select(
                placeholder = "Select a course!",
                options = [
                    SelectOption(label = "Linear programming (MATH 3801)", value = "MATH3801"),
                    SelectOption(label = "Mathematical methods I (MATH 3705)", value = "MATH3705"),
                    SelectOption(label = 'Intro to statistics (STAT 2507)', value = 'STAT2507'),
                    SelectOption(label = 'Intro to computer science (COMP 1005)', value = 'COMP1005')
                ]
            )
        ]
    )
      
  interaction = await bot.wait_for("select_option")
  sel_course =  interaction.values[0]
  await interaction.send(content = f"{sel_course} selected!", components = [[Button(label="Display grades", custom_id="button1", style= 1),
                                                              Button(label = 'Predict grades', custom_id = 'button2',style= 1)],
                                                              Button(label='Progress report', custom_id = 'button3',style= 1)])

  course_display = await bot.wait_for(
        "button_click", check=lambda i: i.custom_id == "button1" or 'button2' or 'button3'
    )
  print(course_display.values)
  course_display.component
  print(course_display.message)
  option = course_display.custom_id
  for course in grade_list:
    if sel_course == course.name:
      if option == 'button1':
        await course_display.send(content=f"{option} selected", components = [Button(label= i, custom_id = i) for i in course.assessments])
      elif option == 'button2':
        pass


@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
    
    

while True:
  bot.run(os.getenv('D_TOKEN'))