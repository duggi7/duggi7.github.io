"""Train and evaluate a tabular policy in a custom inventory environment."""
import json
import random
from statistics import mean


class InventoryEnv:
    capacity = 12
    actions = (0, 2, 4, 6)
    horizon = 30

    def reset(self, seed):
        self.rng = random.Random(seed)
        self.stock = 5
        self.day = 0
        return self.state

    @property
    def state(self):
        return self.stock, self.day % 7 in (5, 6)

    def step(self, order):
        if self.day >= self.horizon or order not in self.actions:
            raise ValueError("Episode ended or order is outside the action space")
        received = min(self.capacity, self.stock + order)
        demand = self.rng.randint(2, 6) if self.state[1] else self.rng.randint(0, 4)
        sold = min(received, demand)
        self.stock = received - sold
        reward = 5 * sold - 2 * order - self.stock - 4 * (demand - sold)
        self.day += 1
        return self.state, reward, self.day == self.horizon


def train(episodes=4000):
    env = InventoryEnv()
    rng = random.Random(42)
    q = {(stock, weekend): [0.0] * len(env.actions)
         for stock in range(env.capacity + 1) for weekend in (False, True)}
    for episode in range(episodes):
        state = env.reset(episode)
        epsilon = max(.08, .8 * (1 - episode / episodes))
        done = False
        while not done:
            action = (rng.randrange(len(env.actions)) if rng.random() < epsilon
                      else max(range(len(env.actions)), key=q[state].__getitem__))
            next_state, reward, done = env.step(env.actions[action])
            target = reward if done else reward + .95 * max(q[next_state])
            q[state][action] += .08 * (target - q[state][action])
            state = next_state
    return lambda state: env.actions[max(range(len(env.actions)), key=q[state].__getitem__)]


def evaluate(policy, seeds=range(10000, 10200)):
    returns = []
    env = InventoryEnv()
    for seed in seeds:
        state = env.reset(seed)
        done = False
        total = 0
        while not done:
            state, reward, done = env.step(policy(state))
            total += reward
        returns.append(total)
    return round(mean(returns), 2)


if __name__ == "__main__":
    print(json.dumps({
        "mean_episode_reward": {
            "q_learning": evaluate(train()),
            "fixed_order_4": evaluate(lambda _: 4),
            "no_order": evaluate(lambda _: 0),
        },
        "held_out_episodes_per_policy": 200,
    }, indent=2))
