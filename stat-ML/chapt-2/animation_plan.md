# Scene-By-Scene Animation Plan

## Scene 01: The World Is Bigger Than The Dataset

Duration target: 0:00-1:00

Huge animated field of clustered dots. A small rectangular frame selects a tiny region, and those selected dots become a box labelled `Training Dataset`.

Key message: `Dataset << Real World`.

## Scene 02: Population

Duration target: 1:00-2:00

Large circle labelled `Population` with symbolic domains for customers, patients, roads, transactions, and factories.

Key message: `Population = all cases we want to understand`.

## Scene 03: Sample

Duration target: 2:00-3:00

Giant jar of colored balls. A scoop extracts a small subset that becomes a dataset grid.

Key equation: `Sample subset Population`, followed by `Sample -> Model -> Prediction`.

## Scene 04: Hidden Data-Generating Process

Duration target: 3:00-4:10

Inputs flow into a real-world process machine. Outputs emerge as images, transactions, medical records, and sensor signals. Only some outputs fall into the dataset.

Key message: `Reality -> Data -> Dataset`.

## Scene 05: Representative Sample vs Biased Sample

Duration target: 4:10-5:30

Split-screen comparison. Representative sample preserves population proportions and learns a balanced boundary. Biased sample misses subgroups and learns a distorted boundary.

Key message: `Large dataset != Good dataset`.

## Scene 06: Self-Driving Car In The Wrong World

Duration target: 5:30-6:50

Training road scenes are sunny and dry. Deployment scenes include rain, fog, night, snow, and glare. The model's confidence drops.

Key message: `Training World != Deployment World`.

## Scene 07: Training, Validation, And Test Sets

Duration target: 6:50-8:00

One dataset block splits into training, validation, and test containers with an approximate `70% / 15% / 15%` split.

Warning: all three must represent the future use case.

## Scene 08: IID

Duration target: 8:00-9:20

Identical dot clouds for training, validation, test, and deployment. Then break down IID into `Independent` and `Identically Distributed`, with video frames showing dependence and bell curves showing distribution match.

## Scene 09: Distribution Shift

Duration target: 9:20-10:50

Timeline from 2023 to 2026. Training distribution stays fixed while the real-world distribution shifts.

Key equation: `P_train(X) != P_real world(X)`.

## Scene 10: Final Question

Duration target: 10:50-12:30

Return to the ocean/bucket metaphor. The dataset feeds a model that predicts back into the population. The question changes from quantity to representativeness.

Final equation: `Model Generalization <= Quality of the Training Sample`.

## Scene 11: Subscribe Card

Duration target: about 17 seconds

A separate closing card with a channel call-to-action, next chapter teaser, and short tagline.

Key text:

- `THANK YOU FOR WATCHING`
- `SUBSCRIBE`
- `Mean, Median, Variance & Standard Deviation for ML`
- `Stay curious. Follow the math. Follow the data.`
