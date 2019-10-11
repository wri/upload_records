from copy import deepcopy

_glad = {
    "keyword": [
        "iso",
        "is__confirmed_alert",
        "is__regional_primary_forest",
        "wdpa_protected_area__iucn_cat",
        "is__alliance_for_zero_extinction_site",
        "is__key_biodiversity_area",
        "is__landmark",
        "gfw_plantation__type",
        "is__gfw_mining",
        "is__gfw_logging",
        "rspo_oil_palm__certification_status",
        "is__gfw_wood_fiber",
        "is__peat_land",
        "is__idn_forest_moratorium",
        "is__gfw_oil_palm",
        "idn_forest_area__type",
        "per_forest_concession__type",
        "is__gfw_oil_gas",
        "is__mangroves_2016",
        "intact_forest_landscapes_2016",
        "bra_biome__name",
    ]
}

_glad_change = deepcopy(_glad)
_glad_change["double"] = ["alert_area__ha", "aboveground_co2_emissions__Mg"]
_glad_change["integer"] = ["alert__count"]

_glad_summary = deepcopy(_glad)
_glad_summary["double"] = ["area__ha"]

glad_summary_iso = deepcopy(_glad_summary)

glad_summary_adm1 = deepcopy(_glad_summary)
glad_summary_adm1["keyword"].append("adm1")

glad_summary_adm2 = deepcopy(glad_summary_adm1)
glad_summary_adm2["keyword"].append("adm2")

glad_summary_wdpa = deepcopy(_glad_summary)
glad_summary_wdpa["keyword"].append("wdpa_id")
glad_summary_wdpa["keyword"].append("name")
glad_summary_wdpa["keyword"].append("iucn_cat")
glad_summary_wdpa["keyword"].append("status")

glad_change_daily_adm2 = deepcopy(_glad_change)
glad_change_daily_adm2["keyword"].append("alert__date")
glad_change_daily_adm2["keyword"].append("adm1")
glad_change_daily_adm2["keyword"].append("adm2")

glad_change_weekly_iso = deepcopy(_glad_change)
glad_change_weekly_iso["keyword"].append("alert__year")
glad_change_weekly_iso["keyword"].append("alert__week")

glad_change_weekly_adm1 = deepcopy(glad_change_weekly_iso)
glad_change_weekly_adm1["keyword"].append("adm1")

glad_change_weekly_adm2 = deepcopy(glad_change_weekly_adm1)
glad_change_weekly_adm2["keyword"].append("adm2")

glad_change_daily_wdpa = deepcopy(_glad_change)
glad_change_daily_wdpa["keyword"].append("alert__date")
glad_change_daily_wdpa["keyword"].append("wdpa_id")
glad_change_daily_wdpa["keyword"].append("name")
glad_change_daily_wdpa["keyword"].append("iucn_cat")
glad_change_daily_wdpa["keyword"].append("status")

glad_change_weekly_wdpa = deepcopy(_glad_change)
glad_change_weekly_wdpa["keyword"].append("alert__year")
glad_change_weekly_wdpa["keyword"].append("alert__week")
glad_change_weekly_wdpa["keyword"].append("wdpa_id")
glad_change_weekly_wdpa["keyword"].append("name")
glad_change_weekly_wdpa["keyword"].append("iucn_cat")
glad_change_weekly_wdpa["keyword"].append("status")
