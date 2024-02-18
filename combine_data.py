import pandas as pd
import os

def combine_data(drop_incognito=True):
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

    df = pd.concat(all_data, ignore_index=True).drop(['username', 'ip_addr_decrypted', 'user_agent_decrypted', 'platform', 'conn_country', 'offline_timestamp', 'offline', 'shuffle', 'reason_start', 'reason_end', 'skipped'], axis=1) # might do things with columns like conn_country or skipped later, but for now just drop them

    # drop incognito mode
    if drop_incognito:
        df = df[df['incognito_mode'] == False]
    df = df.drop('incognito_mode', axis=1)

    # as far as I can tell, missing spotify_track_uri only happens when a personal/local file was played

    # drop podcasts
    df = df[df['spotify_episode_uri'].isna()].drop(['spotify_episode_uri', 'episode_name', 'episode_show_name'], axis=1)
    print("Data combined\n")

    # add columns for time in minutes and hours
    df['minutes_played'] = df['ms_played'] / 1000 / 60
    df['hours_played'] = df['ms_played'] / 1000 / 60 / 60

    print("Data stats:")
    # print(df.head())
    print(f'\tNumber of tracks: {df.shape[0]}')
    # print(df.columns)
    print(f'\tMost recent track: {df["ts"].max()}')
    print(f'\tTotal time played: {round(df["minutes_played"].sum(), 1)} minutes')
    print(f'\t                   {round(df["hours_played"].sum(), 1)} hours')
    print(f'\t                   {round(df["hours_played"].sum() / 24, 1)} days')

    # save the dataframe to a csv
    print("\nSaving data")
    df.to_csv('all_data.csv', index=False)
    print("Data saved to all_data.csv")

if __name__ == '__main__':
    combine_data(drop_incognito=False)