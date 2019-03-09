
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

### Example: Learning to walk

```python
actor_net = ActorDistributionNetwork(action_spec)
critic_net = CriticNetwork((observation_spec, action_spec), ..)

tf_agent = sac_agent.SacAgent(
  critic_network=critic_network,
  actor_network=actor_network,
  actor_optimizer=AdamOptimizer(learning_rate=..),
  critic_optimizer=AdamOptimizer(learning_rate=..))

dataset = replay_buffer.as_dataset(num_steps=2).prefetch(3)
for batched_experience in dataset:
  tf_agent.train(batched_experience)
```

### Useful links
[TF-Agent @ TF Summit](https://www.youtube.com/watch?v=-TTziY7EmUA)

[TF-Agents Github repository](https://www.github.com/tensorflow/agents)

[TF-Agents Colabs](https://github.com/tensorflow/agents/tree/master/tf_agents/colabs)