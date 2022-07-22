# MLOps com dados do Airbnb: primeiros passos

<img src="images/pipeline.png" alt="mlops pipeline">

Projeto da disciplina de MLOps da UFRN que tem como objetivo principal colocar em prática o conteúdo referente a Semana 08 da matéria, com o objetivo de construir um pipeline MLOps completo para implementar um modelo AirBnb House Price Prediction (AHPP) em produção

## Requisitos

Certifique-se de atender aos seguintes requisitos:

* Ter instalado `conda 4.8.2 | Python 3.7 ou maior`.
* Ter uma máquina com `Windows | Linux | Mac`.
* Possuir uma conta [wandb](https://wandb.ai/site).

Este projeto usa a ferramenta [wandb](https://wandb.ai/site) que possibilita acompanhar e visualizar todas as partes do seu pipeline de aprendizado de máquina, de conjuntos de dados a modelos de produção.

## Instalando

Criar ambiente do projeto:
```
conda env create -f environment.yml
```

Ativando o ambiente criado:
```
conda activate mlops_exercise
```

## Utilizando o projeto

Para executar todo o projeto, é necessário executar o seguinte comando:

```bash
mlflow run .
```

Dê uma olhada no arquivo `config.yaml` e veja se os parâmetros do projeto são bons para você.
