# -*- coding: utf-8 -*-
"""SI_CP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CQ7XCRTWQdOBf8bIgGss01JJ8MT7tHCY
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold, StratifiedKFold, RepeatedStratifiedKFold, ShuffleSplit
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from imblearn.combine import SMOTETomek
from sklearn.model_selection import cross_val_score,cross_val_predict, train_test_split
from sklearn.preprocessing import OneHotEncoder,StandardScaler,PowerTransformer,LabelEncoder
from sklearn.metrics import accuracy_score,classification_report, recall_score,confusion_matrix, roc_auc_score, precision_score, f1_score, roc_curve

import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv("dataset.csv")
df.head()

print(df['stroke'].value_counts())
print('***'*30)
print(df.shape)
print('***'*30)
print(df.isna().sum())

# Value counts of the 'stroke' column
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='stroke')
plt.title('Distribution of Stroke (Target Variable)')
plt.xlabel('Stroke')
plt.ylabel('Count')
plt.show()

print("percentage of missing values in bmi :: ",round(df['bmi'].isna().sum()/len(df['bmi'])*100,2))
print("percentage of missing values in Smoking Status :: ",round(df['smoking_status'].isna().sum()/len(df['smoking_status'])*100,2))

# we will drop smoking status as huge no.of values are missing , even if we fill it may  effect
# the integrity of the data

df.drop(columns=['smoking_status'],axis=1,inplace=True)
print(df.shape)

sns.distplot(df['bmi'])
plt.show()
print(df['bmi'].skew())

df['bmi'].fillna(df['bmi'].median(),inplace=True)
print(df['bmi'].isna().sum())

print(df.columns)
print('***'*20)
print(df.describe())

f,ax=plt.subplots(1,3,figsize=(15,5))
sns.boxplot(df['age'],color='red',ax=ax[0])
sns.boxplot(df['avg_glucose_level'],color='yellow',ax=ax[1])
sns.boxplot(df['bmi'],color='blue',ax=ax[2])
plt.show()

df.columns

q1=df['avg_glucose_level'].quantile(0.25)
q3=df['avg_glucose_level'].quantile(0.75)
iqr=q3-q1
lower=q1-3*iqr
upper=q3+3*iqr

print(q1," ",iqr)

# no of extreemmmme outliers
print(df[(df['avg_glucose_level']<lower) | (df['avg_glucose_level']>upper)].shape)
print("before removing Outliers",df.shape)

print('***'*20)


# removing extremmme outliers
df=df[(df['avg_glucose_level']>=lower) & (df['avg_glucose_level']<=upper)]
print("after removing Outliers",df.shape)

# removing mild + extremmme outliers
new_df=df[(df['avg_glucose_level']>=q1-1.5*iqr) & (df['avg_glucose_level']<=q1+1.5*iqr)]

q1=df['bmi'].quantile(0.25)
q3=df['bmi'].quantile(0.75)
iqr=q3-q1
lower=q1-3*iqr
upper=q3+3*iqr

print(q1," ",iqr)

# no of extreemmmme outliers
print(df[(df['bmi']<lower) | (df['bmi']>upper)].shape)

df=df[(df['bmi']>=lower)&(df['bmi']<=upper)]

# removing mild + extremmme outliers
new_df=new_df[(new_df['bmi']>=q1-1.5*iqr) & (new_df['bmi']<=q1+1.5*iqr)]

fig,ax=plt.subplots(1,2,figsize=(15,5),sharey=True)
sns.boxplot(df['avg_glucose_level'],color='yellow',ax=ax[0])
sns.boxplot(df['bmi'],color='blue',ax=ax[1])
plt.show()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
label_encoded_df = df.copy()

print(label_encoded_df.select_dtypes(include='O').columns)

for col in label_encoded_df.select_dtypes(include='O').columns:
    label_encoded_df[col]=le.fit_transform(label_encoded_df[col])
label_encoded_df.head()

df.head()

correlation=df.corr()
sns.heatmap(correlation,annot=True,cmap='PuBu',fmt=".2g",)
plt.show()

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

# separate independent & dependent variables
X = label_encoded_df.iloc[:,0:11]  #independent columns
y = label_encoded_df.iloc[:,-1]    #target column i.e price range

# # apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=chi2, k=10)
fit = bestfeatures.fit(X,y)
dfscores = pd.DataFrame(fit.scores_)
cols=pd.DataFrame(X.columns[fit.get_support()])
pval=pd.DataFrame(np.round(fit.pvalues_,3))
k=pd.concat([dfscores,cols,pval],axis=1)
k.columns=['Fscore','features','p_values']
print(k)
# print(k.sort_values(by='Fscore',ascending=False))
dfscores = pd.DataFrame
print(X.columns[fit.get_support()])
print(type(fit))

df.head()

# K-Fold
kf = KFold(n_splits=5)

for fold, (train_index, test_index) in enumerate(kf.split(X, y), 1):
    x_train, x_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Plot histograms for features in x_train and x_test
    plt.figure(figsize=(12, 4))
    for i, feature in enumerate(X.columns):
        plt.subplot(1, len(X.columns), i+1)
        plt.hist(x_train[feature], alpha=0.5, label='Train')
        plt.hist(x_test[feature], alpha=0.5, label='Test')
        plt.title(feature)
        plt.legend()
    plt.suptitle(f'K-Fold - Fold {fold}')
    plt.show()

# Stratified K-Fold
ss = StratifiedKFold(n_splits=5)

for fold, (train_index, test_index) in enumerate(ss.split(X, y), 1):
    x_train, x_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Plot histograms for features in x_train and x_test
    plt.figure(figsize=(12, 4))
    for i, feature in enumerate(X.columns):
        plt.subplot(1, len(X.columns), i+1)
        plt.hist(x_train[feature], alpha=0.5, label='Train')
        plt.hist(x_test[feature], alpha=0.5, label='Test')
        plt.title(feature)
        plt.legend()
    plt.suptitle(f'Stratified K-Fold - Fold {fold}')
    plt.show()

classifiers = {
    '1': LogisticRegression(),
    '2': KNeighborsClassifier()
}

num_splits = None
while num_splits is None:
    try:
        num_splits = int(input("Enter the number of splits for cross-validation: "))
    except ValueError:
        print("Invalid input. Please enter a valid number of splits.")

accuracy_results = {}

for classifier_choice, classifier in classifiers.items():
    print(f"Classifier: {classifier.__class__.__name__}")
    classifier_metrics = {}


    sm = SMOTETomek(random_state=42)
    X_resampled, y_resampled = sm.fit_resample(X, y)

    cv_techniques = {
        'KFold': KFold(n_splits=num_splits),
        'StratifiedKFold': StratifiedKFold(n_splits=num_splits),
    }

    metrics_results = {technique: [] for technique in cv_techniques}

    for technique, cv in cv_techniques.items():
        accuracy_scores = []
        recall_scores = []
        precision_scores = []

        for train_index, test_index in cv.split(X_resampled, y_resampled):
            X_train, X_test = X_resampled.iloc[train_index], X_resampled.iloc[test_index]
            y_train, y_test = y_resampled.iloc[train_index], y_resampled.iloc[test_index]

            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)

            accuracy_scores.append(accuracy)
            recall_scores.append(recall)
            precision_scores.append(precision)


        average_accuracy = sum(accuracy_scores) / len(accuracy_scores)
        average_recall = sum(recall_scores) / len(recall_scores)
        average_precision = sum(precision_scores) / len(precision_scores)

        metrics_results[technique] = {
            'Accuracy': average_accuracy,
            'Recall': average_recall,
            'Precision': average_precision
        }

    classifier_metrics[classifier.__class__.__name__] = metrics_results
    accuracy_results[classifier.__class__.__name__] = metrics_results


for classifier, techniques in accuracy_results.items():
    print(f"\nClassifier: {classifier}")
    for technique, metrics in techniques.items():
        print(f"{technique} - Accuracy: {metrics['Accuracy']:.2f}, Recall: {metrics['Recall']:.2f}, Precision: {metrics['Precision']:.2f}")

fold_accuracies = {technique: [] for technique in cv_techniques}
classifiers = {
    '1': LogisticRegression(),
    '2': KNeighborsClassifier()
}

for technique, cv in cv_techniques.items():
    for train_index, test_index in cv.split(X_resampled, y_resampled):
        X_train, X_test = X_resampled.iloc[train_index], X_resampled.iloc[test_index]
        y_train, y_test = y_resampled.iloc[train_index], y_resampled.iloc[test_index]

        for classifier_choice, classifier in classifiers.items():
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            fold_accuracies[technique].append(accuracy)


plt.figure(figsize=(10, 6))
sns.boxplot(data=pd.DataFrame(fold_accuracies), orient='v')
plt.xlabel('Cross-Validation Technique')
plt.ylabel('Accuracy')
plt.title('Accuracy Distribution for Each Fold in KFold and StratifiedKFold')
plt.xticks(rotation=45)
plt.show()

classifiers = list(accuracy_results.keys())
techniques = list(cv_techniques.keys())

accuracy_values = np.array([[accuracy_results[classifier][technique]['Accuracy'] for technique in techniques] for classifier in classifiers])

fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.2
index = np.arange(len(techniques))

for i, classifier in enumerate(classifiers):
    ax.bar(index + i * bar_width, accuracy_values[i], bar_width, label=f'Classifier {classifier}')

ax.set_xlabel('Cross-Validation Technique')
ax.set_ylabel('Average Accuracy')
ax.set_title('Average Accuracy Comparison of Cross-Validation Techniques')
ax.set_xticks(index + bar_width * len(classifiers) / 2)
ax.set_xticklabels(techniques)
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()