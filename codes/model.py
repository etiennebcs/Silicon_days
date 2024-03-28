from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import pandas as pd
import joblib



# save filepath to variable for easier access
file_path = "../src/articles.csv"

# read the data and store data in DataFrame
data = pd.read_csv(file_path)


# select prediction target
y = data.isFakeNews

# choose features
features = ['publish_date', 'nb_title_found']
X = data[features]

# split to 2 part
train_X, val_X, train_y, val_y = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state = 0)

# Impute missing values
    # make copy
X_train_plus = train_X.copy()
X_valid_plus = val_X.copy()
    # add colomns
X_train_plus['publish_date_was_missing'] = X_train_plus['publish_date'].isnull()
X_valid_plus['publish_date_was_missing'] = X_valid_plus['publish_date'].isnull()
    # imputation
my_imputer = SimpleImputer()
imputed_X_train_plus = pd.DataFrame(my_imputer.fit_transform(X_train_plus))
imputed_X_valid_plus = pd.DataFrame(my_imputer.transform(X_valid_plus))
    # Imputation removed column names; put them back
imputed_X_train_plus.columns = X_train_plus.columns
imputed_X_valid_plus.columns = X_valid_plus.columns

print(imputed_X_valid_plus.columns)
# build model

RF_model = RandomForestClassifier(n_estimators=50, random_state=1)        # n_estimators=50 gives the optimal mae
RF_model.fit(imputed_X_train_plus, train_y)

# predictio normal
pred = RF_model.predict(imputed_X_valid_plus)
print(pred)

# Prédiction with proba
proba_preds = RF_model.predict_proba(imputed_X_valid_plus)
continuous_preds = proba_preds[:, 1]

# show result
print(continuous_preds)

# calculate error by MAE
mae = mean_absolute_error(val_y, continuous_preds)
print("Mean Absolute Error (MAE): ",mae)


# Save model
#joblib.dump(RF_model, '../src/model.pkl')


"""
# save model
joblib.dump(model, 'model.pkl')

# load model
loaded_model = joblib.load('model.pkl')

# use model
predictions = loaded_model.predict(X)
"""