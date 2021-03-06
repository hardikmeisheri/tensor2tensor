# coding=utf-8
# Copyright 2018 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for tensor2tensor.rl.gym_utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gym
from gym import spaces
import numpy as np
from tensor2tensor.rl import gym_utils
import tensorflow as tf


class SimpleEnv(gym.Env):
  """A simple environment with a 3x3 observation space, is done on action=1."""

  def __init__(self):
    self.reward_range = (-1.0, 1.0)
    self.action_space = spaces.Discrete(2)
    self.observation_space = spaces.Box(low=0, high=255, shape=(3, 3))

  def reset(self):
    return self.observation_space.low

  def step(self, action):
    if action == 0:
      return self.reset(), -1.0, False, {}
    else:
      return self.observation_space.high, +1.0, True, {}


class GymUtilsTest(tf.test.TestCase):

  # Just make an environment and expect to get one.
  def test_making_simple_env(self):
    env = gym_utils.make_gym_env("CartPole-v0")
    self.assertTrue(isinstance(env, gym.Env))

  # Make a time-wrapped environment and expect to get one.
  def test_making_timewrapped_env(self):
    env = gym_utils.make_gym_env("CartPole-v0", rl_env_max_episode_steps=1000)
    self.assertTrue(isinstance(env, gym.Env))
    self.assertTrue(isinstance(env, gym.wrappers.TimeLimit))
    self.assertEquals(1000, env._max_episode_steps)

  # Make a time-wrapped environment with unlimited limit.
  def test_unlimited_env(self):
    env = gym_utils.make_gym_env("CartPole-v0", rl_env_max_episode_steps=None)
    self.assertTrue(isinstance(env, gym.Env))
    self.assertTrue(isinstance(env, gym.wrappers.TimeLimit))
    self.assertTrue(env._max_episode_steps is None)

  def test_gym_registration(self):
    env = gym_utils.register_gym_env(
        "tensor2tensor.rl.gym_utils_test:SimpleEnv")

    # Most basic check.
    self.assertTrue(isinstance(env, gym.Env))

    # Just make sure we got the same environment.
    self.assertTrue(np.allclose(env.reset(),
                                np.zeros(shape=(3, 3), dtype=np.uint8)))

    _, _, done, _ = env.step(1)
    self.assertTrue(done)


if __name__ == "__main__":
  tf.test.main()
