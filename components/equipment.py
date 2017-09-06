from components.component import Component
from components.messages import QueryType
from managers.echo import EchoService
from stats.enums import StatsEnum
from util.decorators import cached, invalidate_cache


class Equipment(Component):
    NAME = "equipment"
    """
    This component attaches itself to anything with a bodies.
    It represents equipment worn or wielded
    """
    def __init__(self):
        super().__init__()
        self.host_body = None
        self.worn_equipment_map = {}
        self.wielded_equipment_map = {}

    def copy(self):
        # TODO Copying an equipment to another type of body would require some sort of validation.
        # TODO Removing or dropping invalid mappings.
        new_equipment = Equipment()
        new_equipment.host_body = self.host_body
        new_equipment.worn_equipment_map = self.__copy_all_items(self.worn_equipment_map)
        new_equipment.wielded_equipment_map = self.__copy_all_items(self.wielded_equipment_map)

        return new_equipment

    @staticmethod
    def __copy_all_items(collection):
        collection_copy = collection.copy()
        for index, item_list in enumerate(collection):
            collection_copy[index].clear()
            for item in item_list:
                collection_copy[index].append(item.copy())

        return collection_copy

    def on_register(self, host):
        super().on_register(host)
        self.host_body = host.body
        host.register_query_responder(self, QueryType.RemoveObject, self.remove_item)

    @invalidate_cache
    def remove_item(self, item):
        success = False
        for item_list in self.worn_equipment_map.values():
            if item in item_list:
                item_list.remove(item)
                success = True

        for key in self.wielded_equipment_map.copy().keys():
            if self.wielded_equipment_map[key] == item:
                del self.wielded_equipment_map[key]
                success = True

        return success

    @invalidate_cache
    def wear(self, item):
        # Wearing requires the bodypart to be compatible with the item
        if not self.host_body:
            self.host_body = self.host.body

        if item.armor:
            armor = item.armor
            if item.size == self.host.stats.size:
                for compatible_bodypart_uid in armor.wearable_body_parts_uid:
                    host_body_parts = self.host_body.get_body_parts(compatible_bodypart_uid)
                    for host_body_part in host_body_parts:
                        if host_body_part:
                            if host_body_part in self.worn_equipment_map:
                                if armor.worn_layer not in [item.armor.worn_layer for item in
                                                            self.worn_equipment_map[host_body_part]]:
                                    self.worn_equipment_map[host_body_part].append(item)
                                    return True
                            else:
                                self.worn_equipment_map[host_body_part] = [item]
                                return True

        return False

    @invalidate_cache
    def wield(self, item):
        if not self.host_body:
            self.host_body = self.host.body

        # Wielding requires bodyparts with GRASP
        grasp_able_body_parts = sorted(
            [free_body_part for free_body_part in
             self.host_body.get_grasp_able_body_parts()
             if free_body_part not in self.wielded_equipment_map],
            key=lambda x: x.relative_size, reverse=True
        )

        # Wielding with one hand gets priority
        wielding_body_parts = []
        total_size_held = 0
        while grasp_able_body_parts:
            free_body_part = grasp_able_body_parts.pop(0)
            wielding_body_parts.append(free_body_part)
            item_size = item.size.value
            # 10 is the normal relative_size for a hand
            relative_size_modifier = free_body_part.relative_size - 10
            relative_size_modifier = round(relative_size_modifier / 10) if relative_size_modifier else 0
            relative_size = self.host.stats.size.value + relative_size_modifier

            total_size_held += relative_size
            if total_size_held >= item_size:
                if item.weapon.two_handed and len(wielding_body_parts) >= 2 or not item.weapon.two_handed:
                    for body_part in wielding_body_parts:
                        self.wielded_equipment_map[body_part] = item
                    return True
        return False

    @cached
    def get_worn_items(self):
        return [item for item_list in self.worn_equipment_map.values() for item in item_list]

    @cached
    def get_load_of_worn_items(self):
        worn_items = self.get_worn_items()
        total_weight = 0.0
        for item in worn_items:
            item_weight = item.stats.get_current_value(StatsEnum.Weight)
            material_modifier = item.material.weight
            total_weight += item_weight * material_modifier

        return total_weight

    @cached
    def get_wielded_items(self):
        return [item for item in self.wielded_equipment_map.values()]
