# File to use in T-Swift LL 

import pandas as pd
df = pd.read_csv('datasets/taylor-swift-all-songs.csv')

def recommend_song(mood_contributor, taylor_preference, swift_lyric):
    # filter songs based on mood contributor
    # allow for plural or singular Friend/Friends
    if ('friend' in mood_contributor.lower()) and ('ex' not in mood_contributor.lower()):
        mood_contributor = 'friend(s)'

    if mood_contributor.lower() in [x.lower() for x in df['mood_contributor'].unique()]:
        filtered_songs = df[df['mood_contributor'].str.lower() == mood_contributor.lower()]
    else:
        print('''Double check mood_contributor is one of:
          -'Love Interest'
          -'Ex-Partner'
          -'Myself'
          -'Friend(s)'
          -'Family'
          -'Ex-Friend'
          -'Other' ''')
        # so that we don't throw an error:
        return '', '0'

    # filter songs based on Taylor Swift lyric
    if len(swift_lyric) > 0:
        filter = filtered_songs['lyrics'].str.lower().str.contains(swift_lyric.lower(), case=False)
        if filter.sum() == 0:
            print(f'There are no songs available with your chosen lyric. Please choose a different lyric')
            return '', ''
        else:
            print(f'There are {filter.sum()} songs that include your lyric')
            filtered_songs = filtered_songs[filter]

    # filter songs based on Taylor preference
    if 'old' in taylor_preference:
        filter = filtered_songs['old_taylor'] == 'old_taylor'
    elif 'new' in taylor_preference:
        filter = filtered_songs['old_taylor'] == 'new_taylor'
    else:
        print('''old_taylor needs to be either:\n
          -'old'\n
          -'new' ''')
        return '', ''

    if filter.sum() > 0:
        filtered_songs = filtered_songs[filter]

    # Return recommended song (possibly randomly selected)
    recommended_song = filtered_songs.sample()
    return recommended_song.iloc[0,0], recommended_song.iloc[0,2]