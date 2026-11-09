# Terminal Config Bench

A Python benchmark inspired by terminal-based agent evaluation. It creates three synthetic deployment configuration failures covering invalid ports, readiness paths, and retry values. Each case gets a fresh temporary workspace.

Run with Python 3.10 or newer:

```sh
python benchmark.py
```

The harness runs a no-op baseline and a reference repair as subprocesses with a timeout. It checks the repaired configuration, preservation of the service field, and an unrelated sentinel file. The expected result is 0/3 for the no-op and 3/3 for the repair. The tasks and commands are local fixtures supplied by this project.
