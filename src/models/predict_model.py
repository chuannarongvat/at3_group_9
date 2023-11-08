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

def permutation_importance(df, target_feature, model, X, y, set_name=None, model_name=None):
    from sklearn.inspection import permutation_importance
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    r = permutation_importance(model, X, y, n_repeats=30, random_state=42)
    
    permu_imp = []
    
    for i in r.importances_mean.argsort()[::-1]:
        feature_name = df.columns[i]
        feature_imp = r.importances_mean[i]
        
        if str(feature_name) == str(target_feature):
            pass
        else:
            permu_imp.append({'feature': feature_name, 'importance': feature_imp})
    
    permu_imp_df =  pd.DataFrame(permu_imp).sort_values(by='importance', ascending=False)
    
    plot_importances(permu_imp_df, title_name=f'{model_name} Permutation Importance on {set_name} Set')
    return permu_imp_df