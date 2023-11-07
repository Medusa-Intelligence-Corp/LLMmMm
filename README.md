# The Universal ML-Template

---

## Adapted from "The Universal Machine Learning Workflow" 🔄
> Chapter 6 of "Deep Learning with Python" 
> [O'Reilly Source](https://www.oreilly.com/library/view/deep-learning-with/9781617296864/Text/06.xhtml)

---

# How to install? FAQ.
> See [INSTALL.md](./INSTALL.md):

---

# Step 1: Define the Task 🎯
```You can’t do good work without a deep understanding of the context of
what you’re doing. Why is your customer trying to solve this particular
problem? What value will they derive from the solution—how will your
model be used, and how will it fit into your customer’s business pro-
cesses? What kind of data is available, or could be collected? What kind of
machine learning task can be mapped to the business problem?
```
> This repository won't help you do this, if you need inspiration check out [Kaggle](https://www.kaggle.com/code?page=2&types=competitions)

---

## Collect a Dataset 📦
- Simply download a csv from kaggle
- OR write a sophisticated downloader, see the [downloaders folder](./downloaders) 
```python
import pandas as pd
data = pd.read_csv('dataset.csv')
```

---

## Understand Your Data 🕵️
- Visualize, summarize, and explore
```python
data.head()
data.describe()
```
- At the very least, or go all out and do something like [this](https://www.kaggle.com/code/aleksandradeis/nfl-injury-analysis)
---

## Choose a Measure of Success 📏
- Define metrics to evaluate model performance
```python
from sklearn.metrics import accuracy_score
# ...
accuracy = accuracy_score(y_true, y_pred)
```

---

# Step 2: Develop a Model 🛠️

---

## Prepare the Data 🔄
- Preprocess and split the data
```python
from sklearn.model_selection import train_test_split
# ...
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

---

## Choose an Evaluation Protocol 📋
- K-fold validation, split validation, etc.

---

## Beat a Baseline 📈
- Compare with a random or simple model
```python
# Assume baseline_model is a simple model
baseline_accuracy = accuracy_score(y_test, baseline_model.predict(X_test))
```

---

## Overfit, Then Regularize and Tune 🔄
- Address overfitting with regularization techniques
```python
from sklearn.linear_model import Ridge
# ...
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
```

---

# Step 3: Deploy the Model 🚀

---

## Communicate with Stakeholders 🗣️
- Explain model, set expectations

---

## Ship an Inference Model 🚢
- Deploy model to production
```bash
docker run -p 5000:5000 my_ml_model
```

---

## Monitor and Maintain 🛠️
- Track model performance, update as necessary
