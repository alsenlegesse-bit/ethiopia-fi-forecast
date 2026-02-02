import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from datetime import datetime

class FinancialInclusionForecaster:
    def __init__(self):
        self.models = {}
        
    def fit_trend_model(self, historical_data, indicator):
        """Fit linear trend model to historical data"""
        X = np.array(historical_data['year']).reshape(-1, 1)
        y = historical_data[indicator].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        self.models[indicator] = model
        return model
    
    def forecast(self, indicator, years):
        """Generate forecasts for future years"""
        if indicator not in self.models:
            raise ValueError(f"No model trained for {indicator}")
        
        years_array = np.array(years).reshape(-1, 1)
        predictions = self.models[indicator].predict(years_array)
        
        # Add confidence intervals (simplified)
        std_error = 0.02  # 2% standard error for illustration
        lower_bound = predictions - 1.96 * std_error
        upper_bound = predictions + 1.96 * std_error
        
        forecasts = pd.DataFrame({
            'year': years,
            'prediction': predictions,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        })
        
        return forecasts
    
    def create_scenarios(self, baseline, events_model, events_list):
        """Create optimistic, baseline, and pessimistic scenarios"""
        scenarios = {}
        
        # Baseline scenario (trend only)
        scenarios['baseline'] = baseline
        
        # Optimistic scenario (with positive events)
        optimistic = baseline.copy()
        for year in [2025, 2026, 2027]:
            optimistic = events_model.apply_impacts(optimistic, events_list, year)
        scenarios['optimistic'] = optimistic
        
        # Pessimistic scenario (reduced growth)
        pessimistic = baseline * 0.8  # 20% lower growth
        scenarios['pessimistic'] = pessimistic
        
        return scenarios

if __name__ == "__main__":
    # Example usage
    forecaster = FinancialInclusionForecaster()
    
    # Historical data example
    historical = pd.DataFrame({
        'year': [2011, 2014, 2017, 2021, 2024],
        'ACC_OWNERSHIP': [0.14, 0.22, 0.35, 0.46, 0.49]
    })
    
    # Fit model
    model = forecaster.fit_trend_model(historical, 'ACC_OWNERSHIP')
    
    # Forecast
    future_years = [2025, 2026, 2027]
    forecasts = forecaster.forecast('ACC_OWNERSHIP', future_years)
    
    print("Forecasts for Account Ownership:")
    print(forecasts)
