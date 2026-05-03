import pandas as pd
import os

def initialize():
    # current_path = os.getcwd()
    # print("Current Working Directory:", current_path)

    df = pd.read_csv('datasets/headspace_data.csv')
    df['user_id'] = df['user_id'].astype(int)
    
    free_members = df[df['membership_type']=='free'].copy()
    
    free_members.dropna(subset=['trial_length'],inplace=True)
    cols_i_want = ['user_id',
                  'registration_date',
                  'registration_platform',
                   'acquisition_type',
                  'first_free_trial_start_date',
                  'first_free_trial_end_date',
                   'trial_length', 
                  ]
    
    free_members = free_members[cols_i_want]
    
    premium_members = df[df['membership_type']=='paid'].copy()
    cols_i_want = ['user_id',
                  'registration_date',
                  'registration_platform',
                   'acquisition_type',
                  'first_free_trial_start_date',
                  'first_free_trial_end_date',
                     'start_date',
                     'end_date',
                     'subscription_type',
                     'payment_platform',
                     'subscription_term_months',
                     'country',
                   'trial_length', 
                  ]
    #drop if trial length is nan tho...
    premium_members.dropna(subset=['trial_length'],inplace=True)
    premium_members = premium_members[cols_i_want]
    
    free_members['membership_type'] = 'free'
    premium_members['membership_type'] = 'paid'
    
    all_members = pd.concat([free_members,premium_members])
    all_members = all_members.sample(all_members.shape[0])
    all_members_dict = {}
    
    for idx, row in all_members.iterrows():
        user_id = row['user_id']

        if row['membership_type'] == 'free': 
            all_members_dict[user_id] = {'account_plan' : 'free',
                'registration_date' : row['registration_date'],
                                          'registration_platform' : row['registration_platform'],
                                          'acquisition_type' : row['acquisition_type'],
                                          'trial_length' : row['trial_length']}
        else:
            all_members_dict[user_id] = {'account_plan' : 'premium',
                'registration_date' : row['registration_date'],
                                      'registration_platform' : row['registration_platform'],
                                      'acquisition_type' : row['acquisition_type'],
                                      'trial_length' : row['trial_length'],
                                      'start_date' : row['start_date'],
                     'end_date' : row['end_date'],
                     'subscription_type' : row['subscription_type'],
                     'payment_platform' : row['payment_platform'],
                     'subscription_term_months' : row['subscription_term_months'],
                     'country' : row['country']}
    

    free_members = free_members.to_dict('list')
    premium_members = premium_members.to_dict('list')
    all_members = all_members_dict
    
    return free_members, premium_members, all_members