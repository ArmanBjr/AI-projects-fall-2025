# Supervised Learning

Three notebooks moving from classical models to a neural network written by hand.

## `decision-trees/`

Binary classification on the **Adult census income** dataset (`adult.csv`) — predicting
whether income exceeds \$50K/year from demographic and employment attributes.

Covers categorical encoding, train/test splitting, tree depth versus overfitting, and
evaluation beyond raw accuracy on an imbalanced target.

```bash
jupyter notebook adult.ipynb
```

## `linear-regression/`

Regression on the **Auto MPG** dataset (`mpg.csv`) — predicting fuel efficiency from engine
displacement, weight, horsepower and model year.

Covers exploratory correlation analysis, feature scaling, fitting, and residual inspection.

```bash
jupyter notebook regression.ipynb
```

## `neural-networks/`

A **multi-layer perceptron implemented from scratch in NumPy**, trained on Fashion-MNIST.

No TensorFlow or PyTorch — forward propagation, backpropagation and the gradient updates
are all written out explicitly. `scikit-learn` appears only to fetch the dataset, split it
and scale the features.

- Activation functions (ReLU, sigmoid, softmax) and their derivatives, hand-derived
- Cross-entropy loss
- Mini-batch gradient descent
- Per-class evaluation, with sample predictions in `images/`

```bash
jupyter notebook mlp_fashion_mnist.ipynb
```

`report.pdf` documents the architecture and results.

> First run downloads Fashion-MNIST from OpenML and needs a network connection.
