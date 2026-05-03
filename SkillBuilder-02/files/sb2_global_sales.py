import numpy as np

# generation parameters
market_names = ['NA', 'EU', 'APAC']
market_sales = [141, 183, 95]
means = [150, 120, 110]
stdevs = [30, 24, 20]
np.random.seed(42)

# storage for main data
markets = np.array([])
sales = np.array([])

# generate data
for i in range(3):
    
    # grab parameters
    market = market_names[i]
    n_sales = market_sales[i]
    mean = means[i]
    stdev = stdevs[i]
    
    # generate regional data
    new_markets = np.repeat([market], n_sales)
    markets = np.hstack((markets, new_markets))
    new_sales = np.random.normal(mean, stdev, n_sales).round(2)
    sales = np.hstack((sales, new_sales))
    
# shuffle the data
n_sales = sales.size
shuffled_idxs = np.random.permutation(n_sales)
markets = markets[shuffled_idxs]
sales = sales[shuffled_idxs]
    
# generate helper lists with indices of each region's sales
sales_idx_na = np.argwhere(markets == 'NA')
sales_idx_eu = np.argwhere(markets == 'EU')
sales_idx_apac = np.argwhere(markets == 'APAC')

markets = markets.tolist()
sales = sales.tolist()
sales_idx_na = sum(sales_idx_na.tolist(), [])
sales_idx_eu = sum(sales_idx_eu.tolist(), [])
sales_idx_apac = sum(sales_idx_apac.tolist(), [])