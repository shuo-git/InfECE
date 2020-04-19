# On the Inference Calibration of Neural Machine Translation

## Contents

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Contact](#contact)

## Introduction

This is the implementation of our work 'On the Inference Calibration of Neural Machine Translation' (ACL 2020).

## Prerequisites

**TER COMpute Java code**

Download the TER tool from http://www.cs.umd.edu/%7Esnover/tercom/. We use TER label to calculate the inference ECE.

## Usage

1) Set the necessary paths in `run.sh`

```shell
CODE=Path_to_InfECE
TER=Path_to_tercom-0.7.25
ref=Path_to_reference
hyp=Path_to_hypothesis
vocab=Path_to_target_side_vocabulary
```

2) Run `run.sh`

```shell
./run.sh
```


## Contact

If you have questions, suggestions and bug reports, please email [wangshuo18@mails.tsinghua.edu.cn](mailto:wangshuo18@mails.tsinghua.edu.cn).