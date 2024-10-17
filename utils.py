import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def plot(t, ticker1, ticker2, res_mean , overval_cutoff, underval_cutoff):
    '''
        Function to plot the prices of the pairs, their residuals and the trade signals.
    '''

    t['date'] = pd.to_datetime(t['date'])

    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(30, 10), sharex=True)

    # Plot for residuals
    axs[0].plot(t['date'], t['residual'], label='Test Residuals', color='purple')
    axs[0].axhline(res_mean, color='black', linestyle='--', lw=1, label='Mean Residual')
    axs[0].axhline(overval_cutoff, color='black', linestyle='--', lw=1, label='Overval Cutoff')
    axs[0].axhline(underval_cutoff, color='black', linestyle='--', lw=1, label='Underval Cutoff')
    axs[0].set_ylabel('Residuals')
    axs[0].legend()
    axs[0].set_title('Residuals Plot')

    # Plot for ticker1
    axs[1].plot(t['date'], t[ticker1], label=ticker1, color='orange')
    axs[1].set_ylabel(f'{ticker1} Price')
    axs[1].legend()
    axs[1].set_title(f'{ticker1} Price Plot')

    # Plot for ticker2
    axs[2].plot(t['date'], t[ticker2], label=ticker2, color='blue')
    axs[2].set_ylabel(f'{ticker2} Price')
    axs[2].legend()
    axs[2].set_title(f'{ticker2} Price Plot')

    # Set common X label
    axs[2].set_xlabel('Date')

    for index, row in t.iterrows():
        date = row['date']
        signal = row['signal']
        
        # Add annotations based on the signal conditions
        if signal == 'enter overval':
            axs[2].annotate('Sell', xy=(date, row[ticker2]), xytext=(date, row[ticker2] + 50),
                            arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')
            axs[1].annotate('Buy', xy=(date, row[ticker1]), xytext=(date, row[ticker1] + 50),
                            arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, color='green')
        elif signal == 'exit overval':
            axs[1].annotate('Sell', xy=(date, row[ticker1]), xytext=(date, row[ticker1] + 50),
                            arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')
            axs[2].annotate('Buy', xy=(date, row[ticker2]), xytext=(date, row[ticker2] + 50),
                            arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, color='green')
        elif signal == 'enter underval':
            axs[1].annotate('Sell', xy=(date, row[ticker1]), xytext=(date, row[ticker1] + 50),
                            arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')
            axs[2].annotate('Buy', xy=(date, row[ticker2]), xytext=(date, row[ticker2] + 50),
                            arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, color='green')
        elif signal == 'exit underval':
            axs[2].annotate('Sell', xy=(date, row[ticker2]), xytext=(date, row[ticker2] + 50),
                            arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')
            axs[1].annotate('Buy', xy=(date, row[ticker1]), xytext=(date, row[ticker1] + 50),
                            arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, color='green')



    plt.tight_layout()
    plt.show()

def passes_adfuller_test(residuals, alpha):
    '''
        Function to check if the residuals of a pair pass the adfuller test.
    '''
    p_value = adfuller(residuals)[1]
    if p_value < alpha:
        return True
    return False

def get_regression_model(stock1, stock2):
    '''
     Function to regress a pair and retrieve the fitted model.
    '''
    X = sm.add_constant(stock1) 
    model = sm.OLS(stock2, X).fit()
    return model