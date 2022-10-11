from snowcrows import *
from equipment import *
from api import API


def compare_equipment(player_equipment: Equipment, sc_equipment: Equipment):
    exotic = Rarity("Exotic")

    for slot, sc_item in sc_equipment.items.items():
        player_item: Item = player_equipment.items[slot]
        #print(f"{slot}:\n\tP: {player_item}\n\tS: {sc_item}")
        # Skip aquatic gear
        if "Aquatic" in slot:
            continue
        # Check stats
        if player_item.stats.name != sc_item.stats.name:
            print(f"{player_item.stats} {player_item.name}: Should be {sc_item.stats.name}")

        if player_item.rarity < exotic:
            print(f"{player_item.name}: Rarity too low")

        sc_upgrades = sc_item.upgrades.copy()
        player_upgrades = player_item.upgrades.copy()
        for player_upgrade in player_upgrades:
            for sc_upgrade in sc_upgrades:
                if int(sc_upgrade.id) == int(player_upgrade.id):
                    sc_upgrades.remove(sc_upgrade)
                    player_upgrades.remove(player_upgrade)
        if len(sc_upgrades) != 0 or len(player_upgrades) != 0:
            print(f"{player_item.name}: Wrong upgrade ({', '.join(f'{upgrade}' for upgrade in player_upgrades)} instead of {', '.join(f'{upgrade}' for upgrade in sc_upgrades)})")


if __name__ == "__main__":
    api = API("API_KEY")
    url = "https://snowcrows.com/builds/mesmer/virtuoso/power-virtuoso"
    sc_equipment = get_sc_equipment(api, url)
    player_equipment = get_equipment(api, "Chamaki", 1)
    print(sc_equipment,"\n", player_equipment)
    print("----------------------------------------\nFeedback:")
    compare_equipment(player_equipment, sc_equipment)