from numpy import random
import secrets

n_customers = 5000
customer_data = {}
rng = random.default_rng(64490759)

for _ in range(n_customers):
    customer_id = secrets.token_hex(4)
    n_purchases = rng.poisson(20)
    total_spend = rng.choice([39, 49, 59], n_purchases).sum()
    state = rng.choice(['OR', 'CA', 'WA', 'NV', 'AZ', 'UT', 'ID', 'MT',], 1,
                       p=[0.40, 0.25, 0.15, 0.08, 0.04, 0.04, 0.02, 0.02,])[0]
    
    customer_data[customer_id] = [total_spend, state]
    
