import sys
sys.path
sys.path.append('..')

import gym
import universe

from utils.env import create_slither_env

from schedule import LinearExploration, LinearSchedule
from model import DeepQ

from configs.RattLe import config

"""
Use deep Q network for the Atari game. Please report the final result.
Feel free to change the configurations (in the configs/ folder). 
If so, please report your hyperparameters.

You'll find the results, log and video recordings of your agent every 250k under
the corresponding file in the results folder. A good way to monitor the progress
of the training is to use Tensorboard. The starter code writes summaries of different
variables.

To launch tensorboard, open a Terminal window and run 
tensorboard --logdir=results/
Then, connect remotely to 
address-ip-of-the-server:6006 
6006 is the default port used by tensorboard.
"""
if __name__ == '__main__':
	# make env
	env = create_slither_env()
	env.configure(fps=5.0, remotes=1, start_timeout=15 * 60, vnc_driver='go', vnc_kwargs={'encoding': 'tight', 'compress_level': 0, 'fine_quality_level': 50})

	record_env = create_slither_env()
	gym.wrappers.Monitor(record_env, config.record_path, video_callable=lambda x: True, resume=True)
	record_env.configure(fps=5.0, remotes=1, start_timeout=15 * 60, vnc_driver='go', vnc_kwargs={'encoding': 'tight', 'compress_level': 0, 'fine_quality_level': 50})

	# exploration strategy
	exp_schedule = LinearExploration(env, config.eps_begin, config.eps_end, config.eps_nsteps)

	# learning rate schedule
	lr_schedule  = LinearSchedule(config.lr_begin, config.lr_end, config.lr_nsteps)

	# train model
	model = DeepQ(env, record_env, config)
	model.run(exp_schedule, lr_schedule)
