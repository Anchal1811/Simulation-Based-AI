import numpy as np
import pandas as pd

def generate_data(n=1000):
    np.random.seed(42)
    age = np.random.normal(50, 15, n)
    treatment = np.where(age > 50, 1, 0)
    recovery = (10 * treatment) - (0.1 * age) + np.random.normal(0, 5, n)
    return pd.DataFrame({'Age': age, 'Treatment': treatment, 'Recovery': recovery})