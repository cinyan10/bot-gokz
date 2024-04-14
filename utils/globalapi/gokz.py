from utils.configs.gokz import LJ_COLOR_RANGE, MAP_TIERS


def lj_color(distance: float) -> str:
    for threshold in sorted(LJ_COLOR_RANGE.keys(), reverse=True):
        if distance >= threshold:
            return LJ_COLOR_RANGE[threshold]

    return "meh"


def get_maps_in_tier_range(min_tier, max_tier):
    return {
        map_name: tier
        for map_name, tier in MAP_TIERS.items()
        if min_tier <= tier <= max_tier
    }
