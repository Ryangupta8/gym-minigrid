from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from operator import add
import numpy as np


class PersonFindingEnv(MiniGridEnv):
    """
    Single-room square grid environment with static obstacles, static people
    """

    def __init__(self, size=5, agent_start_pos=(1, 1), agent_start_dir=0, n_obstacles=4):


        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        # Reduce obstacles if there are too many
        if n_obstacles <= size/2 + 1:
            self.n_obstacles = int(n_obstacles)
        else:
            self.n_obstacles = int(size/2)
        super().__init__(
            grid_size=size,
            max_steps=4 * size * size,
            # Set this to True for maximum speed
            see_through_walls=False,
        )
        # Allow 3 actions : left, right, forward
        self.action_space = spaces.Discrete(self.actions.forward + 1)
        self.reward_range = (-10, 30)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        # Place obstacles
        self.obstacles = []
        self.obs_initpos= []
        
        for i_obst in range(self.n_obstacles):
            self.obstacles.append(Ball())
            init_pos =self.place_obj(self.obstacles[i_obst], max_tries=100)
            self.obs_initpos.append(init_pos)

        self.mission = (
            "avoid the obstacles and get to the green goal square"
        )


    def step(self, action):
        # Invalid action
        if action >= self.action_space.n:
            action = 0

        print 

        # Check if there is an obstacle in front of the agent
        front_cell = self.grid.get(*self.front_pos)
        not_clear = front_cell and front_cell.type != 'goal'

        obs, reward, done, info = MiniGridEnv.step(self, action)

        # If the agent tries to walk over an obstacle
        if action == self.actions.forward and not_clear:
            reward = -100
            done = True
            print("collision with objects")
            return obs, reward, done, info

        # If we touch target we get 1000 points
        if done and self.step_count >= self.max_steps:
            reward = -10
        elif done == True :
            reward = 30

        return obs, reward, done, info
        
        """ TODO     
        # If we Identify (touch) the wrong person but correct shirt color, we get 10
       	if front_cell != None and front_cell.type == 'wrong_target' and action == self.actions.forward:
       		reward = 10    
       	# If we touch someone with wrong color, we lose 5 points        
       	# If we identify the correct color t shirt then we get points
       	"""


        """ 
		Here is where when replacing with HSR/Turtlebot I get obstacle information from a camera
		# Update obstacle positions
        ObsinFOV=True
        num_obs = len(self.obstacles)
        # Test
        # print("object i:",i_obst)
        # Note I removed this functionality for now
		"""
     

        


class PersonFindingEnv5x5(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=5, n_obstacles=1)

class PersonFindingRandomEnv5x5(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=5, agent_start_pos=None, n_obstacles=1)

class PersonFindingEnv6x6(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=6, n_obstacles=3)

class PersonFindingRandomEnv6x6(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=6, agent_start_pos=None, n_obstacles=1)

class PersonFindingEnv8x8(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=8, agent_start_pos=None, n_obstacles=3)

class PersonFindingEnv12x12(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=12, agent_start_pos=None, n_obstacles=2)

class PersonFindingEnv12x12x4(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=12, agent_start_pos=None, n_obstacles=4)


class PersonFindingEnv16x16(PersonFindingEnv):
    def __init__(self):
        super().__init__(size=16, n_obstacles=3)

register(
    id='MiniGrid-Person-Finding-5x5-v0',
    entry_point='gym_minigrid.envs:PersonFindingEnv5x5'
)

register(
    id='MiniGrid-Person-Finding-Random-5x5-v0',
    entry_point='gym_minigrid.envs:PersonFindingRandomEnv5x5'
)

register(
    id='MiniGrid-Person-Finding-6x6-v0',
    entry_point='gym_minigrid.envs:PersonFindingEnv6x6'
)

register(
    id='MiniGrid-Person-Finding-Random-6x6-v0',
    entry_point='gym_minigrid.envs:PersonFindingRandomEnv6x6'
)

register(
    id='MiniGrid-Person-Finding-8x8-v0',
    entry_point='gym_minigrid.envs:PersonFindingEnv8x8'
)

register(
    id='MiniGrid-Person-Finding-12x12-v0',
    entry_point='gym_minigrid.envs:PersonFindingEnv12x12'
)

register(
    id='MiniGrid-Person-Finding-12x12x4-v0',
    entry_point='gym_minigrid.envs:PersonFindingEnv12x12x4'
)


register(
    id='MiniGrid-Person-Finding-16x16-v0',
    entry_point='gym_minigrid.envs:PersonFindingEnv16x16'
)


