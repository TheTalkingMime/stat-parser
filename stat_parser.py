import os
import json
import csv
import requests
from collections import defaultdict

json_files = [pos_json for pos_json in os.listdir('stats_jsons') if pos_json.endswith('.json')]
data_list = {}

for json_file in json_files:
    full_path = os.path.join('stats_jsons/', json_file)
    with open(full_path, 'r') as f:
        data = json.load(f)
        data_list[json_file[:-5]] = data

# https://minecraft.wiki/w/Statistics

bac_columns = ['UUID', 'Name', 'Time', 'Distance By Elytra', 'Fireworks Used', 'Deaths', 'Totems Used', 'Shulkers Opened', 'Diamond Pickaxe Uses', 'Diamond Shovel Uses', 'Diamond Axe Uses', 'Diamond Hoe Uses']
bac_stats = [
    ["stats", "minecraft:custom", "minecraft:play_time"],
    ["stats", "minecraft:custom", "minecraft:aviate_one_cm"],
    ["stats", "minecraft:used", "minecraft:firework_rocket"],
    ["stats", "minecraft:custom", "minecraft:deaths"],
    ["stats", "minecraft:used", "minecraft:totem_of_undying"],
    ["stats", "minecraft:custom", "minecraft:open_shulker_box"],
    ["stats", "minecraft:used", "minecraft:diamond_pickaxe"],
    ["stats", "minecraft:used", "minecraft:diamond_shovel"],
    ["stats", "minecraft:used", "minecraft:diamond_axe"],
    ["stats", "minecraft:used", "minecraft:diamond_hoe"],
]

melon_columns = ['UUID', 'Name', 'Melons', 'Time', 'Dirt Mined', 'Grass Mined', 'Dirt Used', 'Grass Used', 'Moss Used', 'Distance By Elytra', 'Fireworks Used', 'Melon Seeds Used']
melon_stats = [
    ["stats", "minecraft:picked_up", "minecraft:melon_slice"],
    ["stats", "minecraft:custom", "minecraft:play_time"],
    ["stats", "minecraft:mined", "minecraft:dirt"],
    ["stats", "minecraft:mined", "minecraft:grass_block"],
    ["stats", "minecraft:used", "minecraft:dirt"],
    ["stats", "minecraft:used", "minecraft:grass_block"],
    ["stats", "minecraft:used", "minecraft:moss_block"],
    ["stats", "minecraft:custom", "minecraft:aviate_one_cm"],
    ["stats", "minecraft:used", "minecraft:firework_rocket"],
    ["stats", "minecraft:used", "minecraft:melon_seeds"],
]

columns = bac_columns
interesting_stats = bac_stats

indiv_counts = defaultdict(list)
count = 0
for uuid in data_list:
    stats_file = data_list[uuid]

    # Mojang API Request - UUID to IGN
    r = requests.get('https://sessionserver.mojang.com/session/minecraft/profile/' + uuid)
    indiv_counts[uuid].append(r.json()['name'])

    for stat in interesting_stats:
        if stat[0] in stats_file and stat[1] in stats_file[stat[0]] and stat[2] in stats_file[stat[0]][stat[1]]:
            stat_count = stats_file[stat[0]][stat[1]][stat[2]]
            indiv_counts[uuid].append(stat_count)
        else:
            indiv_counts[uuid].append(0)

with open('stats.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    for key, values in indiv_counts.items():
        writer.writerow([key] + values)

print(count)
print(indiv_counts)