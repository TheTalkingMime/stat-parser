import os
import json
import csv
import requests
from pathlib import Path
from collections import defaultdict

CWD = Path(__file__).resolve().parent

# https://minecraft.wiki/w/Statistics
def main():
    all_player_stats = defaultdict(list)
    raw_stats = load_stat_files()
    data_format = load_data_format()

    for uuid in raw_stats:
        ign = get_ign(uuid)
        player_raw_stats = raw_stats[uuid]

        for root in data_format:
            if root == "stats":
                all_player_stats[ign] = get_stats(data_format[root], player_raw_stats[root])
    write_data(get_columns(data_format), all_player_stats)


def get_stats(data_format, stats_file):
    stats = []
    for stat_type in data_format:
        if stat_type not in stats_file:
            stats.append(0)
            continue
        for objective in data_format[stat_type]:
            if objective not in stats_file[stat_type]:
                stats.append(0)
                continue
            stats.append(stats_file[stat_type][objective])
    return stats


def get_columns(data_format):
    columns = ['ign']
    for root in data_format:
        for data_type in data_format[root]:
            for objective in data_format[root][data_type]:
                columns.append(data_format[root][data_type][objective])
    return columns


def stat_exists(stats_file, stat):
    try:
        return stats_file[stat[0]][stat[1]][stat[2]]
    except KeyError:
        return ""


def get_ign(uuid):
    # Mojang API Request - UUID to IGN
    r = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')
    return r.json()['name']


def load_data_format(filename='format.json'):
    filename = os.path.join(CWD, filename)
    with open(filename, 'r') as f:
        data_format = json.load(f)
    return data_format


def load_stat_files(filename='stats_jsons'):
    stats_folder = os.path.join(CWD, filename)
    json_files = [pos_json for pos_json in os.listdir(stats_folder) if pos_json.endswith('.json')]
    data_list = {}

    for json_file in json_files:
        full_path = os.path.join(stats_folder, json_file)
        with open(full_path, 'r') as f:
            data = json.load(f)
            data_list[json_file[:-5]] = data
    return data_list


def write_data(column_headers, rows):
    filename = os.path.join(CWD, 'stats.csv')
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(column_headers)
        for key, values in rows.items():
            writer.writerow([key] + values)


main()