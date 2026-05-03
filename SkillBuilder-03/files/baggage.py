import random
random.seed(123)

destinations = ['MIA', 'MDE', 'HND']
bag_tags = random.choices(destinations, cum_weights=[45, 95, 100], k = 450)