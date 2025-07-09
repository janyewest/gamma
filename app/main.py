import json
import os
from pathlib import Path

from dotenv import load_dotenv
from ligo.gracedb.rest import GraceDb
import pandas as pd
from supabase import Client, create_client

def get_data(url: str, query_ct: str, query_events: str, orderby: list[str]):
    """get GraceDB query response data"""

    print('Gathering GraceDB results...')
    g = GraceDb()

    # retrieve total count
    count = 0
    events_count = g.superevents(query=query_ct)
    for _ in events_count:
        count += 1
    print(f'Total events since Jan 1, 2025: {count}')

    # retrieve filtered events
    events = g.superevents(query=query_events, orderby=orderby)
    gw_events = []
    for event in events:
        gw_events.append(event)

    return count, gw_events


def events_to_json(f_out: str, flat_data):
    """to JSON file"""

    with open(f_out, 'w') as f:
        json.dump(flat_data, f, indent=2)

    print(f'JSON file created at: {f_out}')


def flatten_data(count, list_gw):
    """flatten response data"""

    print('Flattening data...')

    flat_data = []
    for e in list_gw:
        instruments_raw = e.get('preferred_event_data', {}).get('instruments')
        flat_data.append(
            {
                'superevent_id': e.get('superevent_id'),
                'grace_id': e.get('preferred_event_data', {}).get('graceid'),
                'created': e.get('preferred_event_data', {}).get('created'),
                'n_events': int(e.get('preferred_event_data', {}).get('nevents') or 0),
                't_start': e.get('t_start'),
                't_0': e.get('t_0'),
                't_end': e.get('t_end'),
                't_dur': e.get('t_end') - e.get('t_start'),
                't_latency': e.get('preferred_event_data', {}).get('reporting_latency'),
                'far': e.get('preferred_event_data', {}).get('far'),
                'likelihood': e.get('preferred_event_data', {}).get('likelihood'),
                'group': e.get('preferred_event_data', {}).get('group'),
                'instruments': e.get('preferred_event_data', {}).get('instruments'),
                'pipeline': e.get('preferred_event_data', {}).get('pipeline'),
                'total_count': count,
            }
        )

    return flat_data


def to_df(flat_data):
    """to Pandas dataframe"""

    print('Preparing DF...')
    df_gw = pd.DataFrame(flat_data)
    df_gw['created'] = pd.to_datetime(df_gw['created']).dt.tz_localize(None)

    return df_gw


def to_supabase_db(outfile: str, url: str, account: str, key: str, table: str, flat_data):
    """to Supabase database table"""

    print('\nConnecting to Supabase...')

    supabase: Client = create_client(url, key)
    response_fetch = supabase.table(table).select('id').execute()
    print('Deleting table...')
    for ele in response_fetch.data:
        response_delete = supabase.table(table).delete().eq('id', ele['id']).execute()
    print('Writing to table...')
    response_insert = supabase.table(table).insert(flat_data, count='exact').execute()
    count_insert = response_insert.count
    print(f'{count_insert} rows written to Supabase table: {table}.')


if __name__ == '__main__':

    config_path = '../../config/.env'
    output_file_json = 'superevents.json'
    gracedb_url = 'https://gracedb.ligo.org/api/superevents'
    load_dotenv(dotenv_path=Path(config_path))
    supabase_table = 'ligo_gravity_waves'
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
    supabase_account = os.getenv('SUPABASE_ACCOUNT')

    # query info
    query_count = 'gpstime: 1419724818 .. 9999999999'
    query_gw = 'gpstime: 1419724818 .. 9999999999 far < 2e-6 label: EM_READY | RAVEN_ALERT | HIGH_PROFILE & ~INJ & ~DQV'
    orderby_gw = ['-gpstime']

    # get data
    count_gw, events_gw = get_data(gracedb_url, query_count, query_gw, orderby_gw)

    # flatten data
    flat_events_gw = flatten_data(count_gw, events_gw)

    # events to JSON
    events_to_json(output_file_json, flat_events_gw)

    # display all to console
    # pd.set_option('display.max_columns', None)  # Show all columns
    # pd.set_option('display.max_rows', None)  # Show all rows (careful if it's a big df)
    # pd.set_option('display.width', 0)  # Auto-detect width of the terminal
    # pd.set_option('display.expand_frame_repr', False)  # Prevent multi-line wrapping

    # to pandas DF
    df = to_df(flat_events_gw)
    df.sort_values(by=['created'], inplace=True, ignore_index=True)
    # print('\n', df)
    print(f'\n{len(df)} rows')

    # to Supabase table
    to_supabase_db(output_file_json, supabase_url, supabase_account, supabase_key, supabase_table, flat_events_gw)
