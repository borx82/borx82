!pip install pandas sklearn matplotlib
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

test_df = pd.read_sql("SELECT * FROM StockSentimentData", con=engine)
print(test_df)
test_df.plot(x="Sentiment", y="StockAVGDifference", kind="scatter")
X_train, X_test, y_train, y_test = train_test_split(test_df.Sentiment, test_df.StockAVGDifference)
plt.scatter(X_train, y_train, label = 'Training Data', color = "r", alpha = 0.7)
plt.scatter(X_train, y_train, label = 'Testing Data', color = "g", alpha = 0.7)
plt.legend()
plt.title("Test Train Split")
plt.show()

LR = LinearRegression()
LR.fit(X_train.values.reshape(-1,1),y_train.values)

prediction = LR.predict(X_test.values.reshape(-1,1))

plt.plot(X_test, prediction, label = "Linear Regression" , color = 'b')
plt.scatter(X_test, y_test, label="Actual Test Data", color = 'g', alpha= .7)
plt.legend()
plt.show()

LR.predict(np.array([[0.5]]))[0]

LR.score (X_test.values.reshape(-1,1), y_test.values)