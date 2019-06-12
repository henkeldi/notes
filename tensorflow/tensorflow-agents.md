
# TF-Agents

*A robust, scalable and easy to use Reinforcement Learning Library*

### Motivation

* Greate for Learning RL: Colabs, examples, documentation
* Well suited for solving complex problems with RL
* Develop new RL algorithms quickly
* Well tested and easy to configure with gin-config

### Installation

```bash
pip install tf-agents-nightly
```

### Example: Cart Pole

```python
class CartPole(tf_agents.py_environment.PyEnvironment):
    
    def observation_spec(self): 
        """Defines the Observations"""
    
    def action_spec(self):
        """Defines the Actions"""
    
    def _reset(self):
        """Reset the environment and return an initial time_step(reward, observation)."""
        
    def _step(self, action):
        """Apply the action an return the next time_step(reward, observation)."""
```

Trying to balance the Pole:

```python
# Load the environment
env = suite_gym.load("CartPole-V1")

# Define a Policy
policy = ActorPolicy(...)

time_step = env.reset()
episode_return = 0.0

# Start playing
while not time_step.is_last():
  policy_step = policy.action(time_step)
  time_step = env.step(policy_step.action)
  episode_return += time_step.reward
```

* Actor Policy: Takes in observations and emits probability over the actions

Prepare to Train with TF Agents

```python
# Create the Environment
tf_env = tf_py_environment.TFPyEnvironment(suite_gym.load("CartPole-V1"))

# Create the Network
action_net = actor_distribution_network.ActorDistributionNetwork(
   tf_env.observation_spec(), tf_env.action_spec(),
   fc_layer_params=[32, 64])

# Create the Agent
tf_agent = reinforce_agent.ReinforceAgent(
    tf_env.time_step_spec(),
    tf_env.action_spec(),
    actor_network=actor_net,
    optimizer=AdamOptimizer(learning_rate=learning_rate))
```

Collect Experience and Train with TF Agents

```python
replay_buffer = TFUniformReplayBuffer()
driver = DynamicEpisodicDriver(
    tf_env, agent.collect_policy,
    observers=[replay_buffer.add_batck],
    num_episodes=1)

for _ in range(num_iterations):
    # Get experience
    driver.run()
    # train the Agent
    experience = replay_buffer.gather_all()
    agent.train(experience)
    replay_buffer.clear()
```


### Useful links

[TF-Agent @ Google IO 2019](https://www.youtube.com/watch?v=tAOApRQAgpc&t=1138s)

[TF-Agent @ TF Summit](https://www.youtube.com/watch?v=-TTziY7EmUA)

[TF-Agents Github repository](https://www.github.com/tensorflow/agents)

[TF-Agents Colabs](https://github.com/tensorflow/agents/tree/master/tf_agents/colabs)