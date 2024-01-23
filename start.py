import pandas as pd
import os

# Importing the datasets
# import the jsons from all files starting with 'Streaming_History_Audio'

# Determine the names of all the files in the directory 'Spotify Extended Streaming History' which start with 'Streaming_History_Audio'
filenames = os.listdir('Spotify Extended Streaming History')
filenames = [filename for filename in filenames if filename.startswith('Streaming_History_Audio')]

# Read the jsons
all_data = []
for filename in filenames:
    all_data.append(pd.read_json('Spotify Extended Streaming History/' + filename))

df = pd.concat(all_data, ignore_index=True).drop(['username', 'ip_addr_decrypted', 'user_agent_decrypted'], axis=1)
print(df.head())
print(df.shape)
print(df.columns)

# Count the ms_played by artist
df_artist = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
df_artist = df_artist.sort_values('ms_played', ascending=False)
# convert ms_played to hours
df_artist['hours_played'] = df_artist['ms_played'] / 1000 / 60 / 60

print(df_artist.head())