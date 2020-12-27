import streamlit as st
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score

def main():
    st.title('Binary Classification Web App')
    st.sidebar.title('Binary Cassification Web App')
    st.sidebar.markdown('Is masroom is good or poisonous')

    @st.cache(persist=True)
    def load_data():
        data = pd.read_csv('C:\\Users\\hp\\Desktop\\All in One\\Masrooms Dataset\\mush.csv')
        label = LabelEncoder()
        for col in data.columns:
            data[col] = label.fit_transform(data[col])
        return data

    
    
    @st.cache(persist=True)
    
    def split(df):
        y = df.target
        x = df.drop(columns=['target'])
        x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3,random_state=0)
        return x_train, x_test, y_train, y_test
    
    def plot_matrics(metrics_list):
        if 'Confusion Matrix' in metrics_list:
            st.subheader('Confusion Matrix')
            plot_confusion_matrix(model, x_test, y_test, display_labels=class_names)
            st.pyplot()

        if 'ROC Curve' in metrics_list:
            st.subheader('ROC Curve')
            plot_roc_curve(model, x_test, y_test)
            st.pyplot()

        if 'Precision-Recall Curve' in metrics_list:
            st.subheader('Precision-Recall Curve')
            plot_precision_recall_curve(model, x_test, y_test)
            st.pyplot()



    df = load_data()

    x_train, x_test, y_train, y_test = split(df)
    class_names = ['edible','poisonous']
    st.sidebar.subheader('Chosse Classifier')
    classifier = st.sidebar.selectbox('Classifier',('Support Vector Machine','Logistics Regression','Random Forests Classifier'))

    if classifier == 'Support Vector Machine':
        st.sidebar.subheader('Model Hyperparameters')
        C = st.sidebar.number_input('C (Regularization parameter)',0.01,10.0, step=0.01, key='C')
        kernel = st.sidebar.radio('kernel',('rbf','linear'),key='kernel')
        gamma = st.sidebar.radio('Gamma (kernel coefficient)',('scale','auto'),key = 'gamma')
        

        metrics = st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Support Vector Machine Results')
            model = SVC(C=C, kernel=kernel, gamma=gamma)
            model.fit(x_train,y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)

            st.write('Accuracy', accuracy.round(2))
            st.write('precision',precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write('Recall', recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_matrics(metrics)


    if classifier == 'Logistics Regression':
        st.sidebar.subheader('Model Hyperparameters')
        C = st.sidebar.number_input('C (Regularization parameter)',0.01,10.0, step=0.01, key='C')
        max_iter = st.sidebar.slider('Maximum number of iterations', 100, 500, key='max_iter')
        metrics = st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Logistics Regression Results')
            model = LogisticRegression(C=C, max_iter=max_iter)
            model.fit(x_train,y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)

            st.write('Accuracy', accuracy.round(2))
            st.write('precision',precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write('Recall', recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_matrics(metrics)



    if classifier == 'Random Forests Classifier':
        st.sidebar.subheader('Model Hyperparameters')
        n_estimators = st.sidebar.number_input('The number of trees in the forest.',100, 5000, step=10, key='n_estimators')
        max_depth = st.sidebar.number_input('The maximum depth of the tree',1, 20, step=1, key='max_depth')
        bootstrap = st.sidebar.radio('Bootstrap samples when building trees', ('True','False'))
        metrics = st.sidebar.multiselect('What metrics to plot?',('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button('Classify',key='classify'):
            st.subheader('Random Forests Classifier Results')
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap=bootstrap, n_jobs=1)
            model.fit(x_train,y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)

            st.write('Accuracy', accuracy.round(2))
            st.write('precision',precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write('Recall', recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_matrics(metrics)

    if st.sidebar.checkbox('Show raw data', False):
        st.subheader('Mushrooms Data Set (Classification)')
        sh = df.shape

        st.subheader('the shape of data is '+str(sh))
        st.write(df)



if __name__ == "__main__":
    main()   