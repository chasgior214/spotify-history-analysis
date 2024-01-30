import pandas as pd
import os

def combine_data():
    # Determine the names of all the files in the directory 'Spotify Extended Streaming History' which start with 'Streaming_History_Audio'
    filenames = os.listdir('Spotify Extended Streaming History')
    filenames = [filename for filename in filenames if filename.startswith('Streaming_History_Audio')]
    print(f"{len(filenames)} files found")

    # Read the jsons
    print("Combining data...")
    all_data = []
    count = 0
    for filename in filenames:
        count += 1
        print(f"Combining file {count} of {len(filenames)}")
        all_data.append(pd.read_json('Spotify Extended Streaming History/' + filename))

    df = pd.concat(all_data, ignore_index=True).drop(['username', 'ip_addr_decrypted', 'user_agent_decrypted', 'platform', 'conn_country', 'spotify_track_uri', 'episode_name', 'episode_show_name', 'spotify_episode_uri'], axis=1) # might do things with columns like conn_country later, but for now just drop them
    print("Data combined")
    # might want to drop podcasts

    print("Data stats:")
    # print(df.head())
    print(f'\tNumber of tracks: {df.shape[0]}')
    # print(df.columns)
    print(f'\tMost recent track: {df["ts"].max()}')

    # save the dataframe to a csv
    print("Saving data")
    df.to_csv('all_data.csv', index=False)
    print("Data saved to all_data.csv")