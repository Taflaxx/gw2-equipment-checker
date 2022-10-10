from api import *


def get_equipment(api: API, character: str, tab: int = 1):
    char_data = api.get_endpoint_v2(f"/characters?v=2021-07-24T00%3A00%3A00Z&id={character}")
    equipment_tab_items = None
    for equipment_tab in char_data["equipment_tabs"]:
        if equipment_tab["tab"] == tab:
            equipment_tab_items = equipment_tab

    if not equipment_tab_items:
        raise Exception("Equipment Tab not found")

    equipment = Equipment()
    equipment.name = equipment_tab_items["name"]
    for equipment_tab_item in equipment_tab_items["equipment"]:
        item = Item()
        item.id = equipment_tab_item["id"]
        item_data = api.get_endpoint_v2(f"items/{equipment_tab_item['id']}")
        item.name = item_data["name"]
        item.rarity = Rarity(item_data["rarity"])

        stats = Stats()
        if "stats" in equipment_tab_item:
            stats.id = equipment_tab_item["stats"]["id"]
            stats.attributes = equipment_tab_item["stats"]["attributes"]
        elif "infix_upgrade" in item_data["details"]:
            stats.id = item_data["details"]["infix_upgrade"]["id"]
            for stat in item_data["details"]["infix_upgrade"]["attributes"]:
                stats.attributes[stat["attribute"]] = stat["modifier"]
        else:
            for equipment_item in char_data["equipment"]:
                if item.id == equipment_item["id"] and equipment_tab_items["tab"] in equipment_item["tabs"]:
                    stats.id = equipment_item["stats"]["id"]
                    stats.attributes = equipment_item["stats"]["attributes"]
                    break
            else:
                raise Exception(f"Unable to get stats for item: {item}")

        stats_data = api.get_endpoint_v2(f"itemstats/{stats.id}")
        stats.name = stats_data["name"]
        item.stats = stats

        equipment.items[equipment_tab_item["slot"]] = item

    return equipment


class Equipment:
    name: str = None
    items: dict = {}

    def __str__(self):
        nl = "\n"
        return f"Equipment Tab: {self.name}:\n{nl.join(f'{slot}: {item}' for slot, item in self.items.items())}"


class Rarity:
    def __init__(self, rarity):
        self.name = rarity
        self.__value = ["Junk", "Basic", "Fine", "Masterwork", "Rare", "Exotic", "Ascended", "Legendary"].index(rarity)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.__value < other.__value

    def __le__(self, other):
        return self.__value <= other.__value

    def __eq__(self, other):
        return self.__value == other.__value

    def __ge__(self, other):
        return self.__value >= other.__value

    def __gt__(self, other):
        return self.__value > other.__value


class Stats:
    id: int = None
    name: str = None
    attributes: dict = {}

    def __str__(self):
        return f"{self.name}: {self.attributes}"


class Item:
    id: int = None
    name: str = "None"
    rarity: Rarity = None
    stats: Stats = None

    def __str__(self):
        return f"{self.id}, {self.name}, {self.rarity}, {self.stats}"


if __name__ == "__main__":
    api = API("API_KEY")
    print(get_equipment(api, "CHARACTER_NAME", 1))
