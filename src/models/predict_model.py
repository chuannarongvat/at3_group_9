import numpy as np
class NullRegressor:
    def __init__(self):
        self.y = None
        self.pred_value = None
        self.preds = None

    def fit(self, y):
        self.y = y
        self.pred_value = y.mean()

    def predict(self, y):
        self.preds = np.full((len(y), 1), self.pred_value)
        return self.preds

    def fit_predict(self, y):
        self.fit(y)
        return self.predict(self.y)
    
def print_regressor_scores(y_preds, y_actuals, set_name=None):
    from sklearn.metrics import mean_squared_error as mse
    from sklearn.metrics import mean_absolute_error as mae

    print(f"RMSE {set_name}: {mse(y_actuals, y_preds, squared=False)}")
    print(f"MAE {set_name}: {mae(y_actuals, y_preds)}")

def assess_regressor_set(model, features, target, set_name=''):
    preds = model.predict(features)
    print_regressor_scores(y_preds=preds, y_actuals=target, set_name=set_name)
    
def plot_actual_vs_predicted(y_actual, y_predicted, title=None):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(y_actual, y_predicted, 'o', color='orange', label='Predictions')
    ax.plot(y_actual, y_actual, '-', color='red', label='Actual')
    
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    
    if title:
        ax.set_title(title)
    
    ax.legend()
    plt.show()

def fit_assess_regressor(model, X_train, y_train, X_val, y_val):
    model.fit(X_train, y_train)
    assess_regressor_set(model, X_train, y_train, set_name='Training')
    assess_regressor_set(model, X_val, y_val, set_name='Testing')
    #plot_actual_vs_predicted(y_val, model.predict(X_val), title='Comparison of Actual vs. Predicted Target (Testing)')
    
    return model

def plot_importances(df, title_name=None):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    sns.barplot(data=df, x='feature', y='importance', palette='ch:.25')
    
    if title_name is not None:
        plt.title(title_name)
    else:
        plt.title('Feature Importance')
    
    sns.barplot(data=df, x='feature', y='importance', palette='ch:.25')
    plt.xticks(rotation=90)
    plt.show()

def permutation_importance(model, X, y, set_name=None, model_name=None):
    from sklearn.inspection import permutation_importance
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    
    r = permutation_importance(model, X, y, n_repeats=30, random_state=42)
    
    permu_imp = []
    
    for i in r.importances_mean.argsort()[::-1]:
        feature_name = X.columns[i]
        feature_imp = r.importances_mean[i]
        
        permu_imp.append({'feature': feature_name, 'importance': feature_imp})
    
    permu_imp_df = pd.DataFrame(permu_imp).sort_values(by='importance', ascending=False)
    
    title_name = f'{model_name} Permutation Importance on {set_name} Set'
    plot_importances(permu_imp_df, title_name=title_name)
    return permu_imp_df
