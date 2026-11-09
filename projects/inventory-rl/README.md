# Inventory Replenishment RL

A custom Python reinforcement-learning simulation for inventory decisions. The state contains stock and a weekend indicator. The action is the restock quantity. Reward accounts for sales, ordering, holding inventory, and unmet demand.

Run with Python 3.10 or newer:

```sh
python simulation.py
```

The script trains tabular Q-learning on 4,000 seeded episodes and compares it with fixed ordering and no ordering on 200 held-out demand seeds. All policies see the same evaluation seeds. The simulator uses synthetic demand and immediate restocking to isolate the decision problem.
