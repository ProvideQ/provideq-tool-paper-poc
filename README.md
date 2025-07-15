# provideq-tool-paper-poc
Proof of Concept implementation for the ProvideQ Tool Paper:
```bibtex
@article{eichhorn2025provideq,
  title = {ProvideQ: A Quantum Optimization Toolbox},
  author = {Eichhorn, Domenik and Poser, Nick and Schweikart, Maximilian and Schaefer, Ina},
  journal = {arXiv preprint arXiv:2507.07649},
  year = {2025}
}
```

This repository contains the problem instances for the vehicle routing problem and the knapsack problem, as well as a script to solve the problems with the [ProvideQ Toolbox Api](https://github.com/ProvideQ/toolbox-python-api).

The vrp instances were taken from the [CVRPLIB website](http://vrp.galgos.inf.puc-rio.br/index.php/en), and the knapsack instances were generated using a [custom script](./problems/knapsack/generate.sh) that invokes a [knapsack generator](https://github.com/JorikJooken/knapsackProblemInstances).

## How to use
Configure [run_solvers.py](./run_solvers.py) to your liking.
- Set a custom `base_url` to use a different toolbox backend.
- Comment out any test method calls that you don't want to run

Make sure you have Python installed run the script via the console
```sh
python ./run_solvers.py
```
