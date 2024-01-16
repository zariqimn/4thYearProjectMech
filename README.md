# 4thYearProjectMech
***
## author: Zariq Iman
---
This repo represents the work that I did in my final year project.
This project was on utilising **Multi-Objective Bayesian Optimisation** for a mechanical design.

This overview will undisclose any detailed information of the mechanical component, it serves as a guideline for the underlying algorithms used for optimisation.
---
## Project Overview
The whole idea of this project was to test and optimise a mechanical component for crash instances. Usually, this is done through parametric study which sequentially loops over every combination of parameters to find an optimal point that gives a max/min output response. In this project, we used a sampling algorithm that enables us to predict the relationship of output response vs parameter combination. This serves as a new way to craft a Design of Experiment.
This project was done by incorporating a CAD (ntopology), an FEA (abaqus), and Python

### Bayesian Optimisation
To read more on Multi-Objective Bayesian Optimisation architecture, click on link below. This is one of the libraries that was used to implement our project
[BoTorch](https://botorch.org/docs/multi_objective "BoTorch Documentation")
---
## File Directory
|filename|Description|
|---|---|
|MOBO_ANN.py|algorithm used to run Multi-Objective Bayesian Optimisation|
|abaqus|all scripts used to run simulation on CAD files generated on ntopology|
|ntopology|scripts used to generate CAD models based on inital samples, and new parameters to study|
|||
|||
|||


