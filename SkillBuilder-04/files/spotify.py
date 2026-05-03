import random
random.seed(42)
membership_types = ['free', 'individual', 'duo', 'family', 'student']

memberships = random.choices(membership_types, cum_weights=[60, 88, 91, 95, 100], k=2394)