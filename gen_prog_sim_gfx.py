import time
import random
import json

import pyglet
from pyglet.gl import *

from simulation_environment import create
from simulation_environment import environment
from simulation_environment import event_handlers
from simulation_environment import active_actions
from simulation_environment import agent_behavior_base

from genetic_programming import lgp

# Set up graphical window
config = Config(double_buffer=True, depth_size=0, sample_buffers=1, samples=8)
window = pyglet.window.Window(width = 800, height = 600, config=config)
glClearColor(.8,.8,.8,1) # Set background color
glEnable(GL_BLEND) # Enable transparency / alpha blending
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

counter = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
	window.clear()
	env.draw()
	active_actions.draw()
	counter.draw()
	
def update(realtime_dt):
	if env.update() == "terminate":
		pyglet.app.exit()
	active_actions.update()
	
def behavior_from_json(fn):
	with open(fn, 'r') as infile:
		pop_data = json.load(infile)
	max_fit = float('-inf')
	elite_individual = None
	for i, individual_data in enumerate(pop_data):
		if individual_data['_fit'] > max_fit:
			max_fit = individual_data['_fit']
			elite_individual = lgp.Behavior()
			elite_individual.s_lgp.prog = individual_data['s_lgp']
			elite_individual.a_lgp.prog = individual_data['a_lgp']
	return elite_individual.behavior
	
# Genetic program loaded from json file
agent_behavior_function = behavior_from_json('test13_data.json')
#agent_behavior_function = agent_behavior_base.behavior

# Create and initialize environment
env = environment.Environment(agent_behavior_function, dt = .1, sim_time = 0, time_out = 100,
	hash_map_grid_size = 40, width = 800, height = 600, show_bins = False, run_max_speed = True)
env.create_perimeter_walls(location = 'inside', thickness = 5) # Walls
create.create_test_terrain(env) # Terrain
create.create_random_swarm(env, count = 10, radius = 20) # Swarm

# Create active action manager
active_actions = active_actions.ActiveActions(env)

pyglet.clock.schedule_interval(update, 1/120) # Update display 60 times per second

window.push_handlers(event_handlers.EventHandlers(env, window, active_actions))
pyglet.app.run() # Run pyglet


