from webscr import *
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
def ass_button(course):
  #--------------Assessment buttons --------------------------------------
  assessment_buttons = [[Button(label= i, custom_id = i,style= 1) for i in course.assessments],Button(label= 'All', custom_id = 'All',style=3)]
  return assessment_buttons

def pcourse_button():
  #--------------After course selection --------------------------------
  post_coursebuttons = [[Button(label="Display grades", custom_id="button1"),Button(label = 'Predict grades', custom_id = 'button2')],Button(label='Progress report', custom_id = 'button3')]
  return post_coursebuttons

@bot.event
async def on_message(message):
    msg = message.content
    if msg == "hello":
    	await message.channel.send("pies are better than cakes. change my mind.")   
    await bot.process_commands(message)

@bot.command()
async def courses(ctx):
  channel = ctx.channel
  await ctx.send(
        'Which course do you want to see?',
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
  p_b = pcourse_button()
  await interaction.send(content = f"{sel_course} selected!", components = p_b)

  course_display = await bot.wait_for(
        "button_click", check=lambda i: i.custom_id == "button1" or 'button2' or 'button3'
    )
  print(course_display.message)
  option = course_display.custom_id
  for course in grade_list:

    if sel_course == course.name:
      a_b = ass_button(course)
      if option == 'button1':
        await course_display.send(content=f"{option} selected", components = a_b)
        dec = await bot.wait_for('button_click', check= lambda i: i != None)
        if dec.custom_id == 'All':
          pass
        else:
          ass = dec.custom_id
          text = f'{ass} scores for {course.name}'
          for i,v in enumerate(course.assessments[ass]):       
            text += f'{ass[:-1]} {i+1}: {v}%\n'
          ave_score = course.average_score(ass)
          text += ave_score
          await channel.send(content = text)
              
        
      elif option == 'button2':
        await course_display.send(content=f"{option} selected", components = a_b)
   
      elif option == 'button3':
        await course_display.send(content=f"{option} selected",components = [Button(label = 'View plot', custom_id = 'viewplot')])
        report = await bot.wait_for('button_click', check = lambda i: i.custom_id == 'viewplot')
        await report.send(content='Which assessments?', components = a_b)
        dec = await bot.wait_for('button_click', check= lambda i: i != None)
        
        if dec.custom_id == 'All':
            await channel.send(file=discord.File(f'{course.name}_plots.png'))
        else:
          course.course_plots(dec.custom_id)
          await channel.send(file=discord.File(f'{course.name}{dec.custom_id.upper()}_plots.png'))
          


@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
    
    

while True:
  bot.run(os.getenv('D_TOKEN'))