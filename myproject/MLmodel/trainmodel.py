import pandas as pd;
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Importing the dataset
fakedf=pd.read_csv("data/fake.csv")
truedf=pd.read_csv('data/true.csv')

#adding lable to determine weather fake or not to help after concat
fakedf['label']=0
truedf['label']=1

#concat and reset the index
df=pd.concat([fakedf,truedf]).reset_index(drop=True)

#shuffling the df
df=df.sample(frac=1).reset_index(drop=True)

df['content']=df['title']+" "+df['text']

x=df['content']
y=df['label']

#d ataset split into train-test

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

# vectorization of the data

vectorizer=TfidfVectorizer(stop_words='english',max_df=0.7)

# vectorization of training data

x_train_vec=vectorizer.fit_transform(x_train)

#vectorization of testing data

x_test_vec=vectorizer.transform(x_test)

# training of data

model=LogisticRegression()
model.fit(x_train_vec,y_train)

# Evaluate

y_pred=model.predict(x_test_vec)
# print("Accuracy: ",accuracy_score(y_test,y_pred))
# print("Classification report:\n",classification_report(y_test,y_pred))

import joblib
# Save the model and vectorizer
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
