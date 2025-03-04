import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Sample training dataset for rent prediction
data = pd.DataFrame({
    'size': [750, 1000, 1200, 1500, 1800],
    'bedrooms': [1, 2, 2, 3, 3],
    'location_encoded': [1, 2, 2, 3, 3],
    'rent': [1500, 2000, 2200, 3000, 3500]
})

# Train the model
X = data[['size', 'bedrooms', 'location_encoded']]
y = data['rent']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model to disk
with open('rent_predictor.pkl', 'wb') as file:
    pickle.dump(model, file)
