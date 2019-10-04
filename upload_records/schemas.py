from copy import deepcopy

_annualupdate_minimum = {
    "keyword": [
        "iso",
        "tcs_driver__type",
        "global_land_cover__class",
        "is__regional_primary_forest",
        "is__idn_primary_forest",
        "erosion_risk__level",
        "is__biodiversity_significance_top_10_perc",
        "is__biodiversity_intactness_top_10_perc",
        "wdpa_protected_area__iucn_cat",
        "is__alliance_for_zero_extinction_site",
        "gfw_plantation__type",
        "river_basin__name",
        "ecozone__name",
        "is__urban_water_intake",
        "is__mangroves_1996",
        "is__mangroves_2016",
        "baseline_water_stress__level",
        "is__intact_forest_landscape",
        "is__endemic_bird_area",
        "is__tiger_conservation_landscape",
        "is__landmark",
        "is__gfw_land_right",
        "is__key_biodiversity_area",
        "is__gfw_mining",
        "rspo_oil_palm__certification_status",
        "is__peat_land",
        "is__gfw_oil_palm",
        "is__idn_forest_moratorium",
        "idn_land_cover__class",
        "is__mex_protected_areas",
        "is__mex_psa",
        "mex_forest_zoning__zone",
        "is__per_permanent_production_forest",
        "is__per_protected_area",
        "per_forest_concession__type",
        "bra_biome__name",
        "is__gfw_wood_fiber",
        "is__gfw_resource_right",
        "is__gfw_logging",
    ],
    "integer": ["treecover_density__threshold"],
}

annualupdate_minimum_change_iso = deepcopy(_annualupdate_minimum)
annualupdate_minimum_change_iso["integer"].append("treecover_loss__year")
annualupdate_minimum_change_iso["double"] = [
    "treecover_loss__ha",
    "aboveground_biomass_loss__Mg",
    "aboveground_co2_emissions__Mg",
]

annualupdate_minimum_change_adm1 = deepcopy(annualupdate_minimum_change_iso)
annualupdate_minimum_change_adm1["keyword"].append("adm1")

annualupdate_minimum_change_adm2 = deepcopy(annualupdate_minimum_change_adm1)
annualupdate_minimum_change_adm2["keyword"].append("adm2")

annualupdate_minimum_summary_iso = deepcopy(_annualupdate_minimum)
annualupdate_minimum_summary_iso["double"] = [
    "treecover_extent_2000__ha",
    "treecover_extent_2010__ha",
    "area__ha",
    "treecover_gain_2000-2012__ha",
    "aboveground_biomass_stock_2000__Mg",
    "aboveground_co2_stock_2000__Mg",
    "treecover_loss_2001-2018__ha",
    "aboveground_biomass_loss_2001-2018__Mg",
    "aboveground_co2_emissions_2001-2018__Mg",
]

annualupdate_minimum_summary_adm1 = deepcopy(annualupdate_minimum_summary_iso)
annualupdate_minimum_summary_adm1["keyword"].append("adm1")

annualupdate_minimum_summary_adm2 = deepcopy(annualupdate_minimum_summary_adm1)
annualupdate_minimum_summary_adm2["keyword"].append("adm2")

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
