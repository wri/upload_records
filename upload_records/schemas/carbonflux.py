from copy import deepcopy

_carbonflux = {
    "keyword": [
        "iso",
        "is__treecover_gain_2000-2012",
        "is__mangrove",
        "tcs_driver__type",
        "ecozone__name",
        "is__gfw_land_right",
        "wdpa_protected_area__iucn_cat",
        "is__intact_forest_landscape",
        "gfw_plantation__type",
        "is__intact_primary_forest",
        "is__peatlands_flux",
    ],
    "integer": ["treecover_density__threshold"],
}


_carbonflux_summary = deepcopy(_carbonflux)
_carbonflux_summary["keyword"].append("is__treecover_loss_2000-2015")
_carbonflux_summary["double"] = [
    "treecover_extent_2000__ha",
    "area__ha",
    "aboveground_biomass_stock_2000__Mg",
    "gross_annual_biomass_removals_2001-2015__Mg",
    "gross_cumulative_co2_removals_2001-2015__Mg",
    "net_flux_co2_2001-2015__Mg",
    "aboveground_carbon_stock_2000__Mg",
    "belowground_carbon_stock_2000__Mg",
    "deadwood_carbon_stock_2000__Mg",
    "litter_carbon_stock_2000__Mg",
    "soil_carbon_stock_2000__Mg",
    "total_carbon_stock_2000__Mg",
    "treecover_loss_2001-2015__ha",
    "aboveground_biomass_loss_2001-2015__Mg",
    "gross_emissions_co2e_co2_only_2001-2015__Mg",
    "gross_emissions_co2e_non_co2_2001-2015__Mg",
    "gross_emissions_co2e_all_gases_2001-2015__Mg",
]


carbonflux_summary_iso = deepcopy(_carbonflux_summary)
carbonflux_summary_adm1 = deepcopy(carbonflux_summary_iso)
carbonflux_summary_adm1["keyword"].append("adm1")
carbonflux_summary_adm2 = deepcopy(carbonflux_summary_adm1)
carbonflux_summary_adm2["keyword"].append("adm2")

_carbonflux_change = deepcopy(_carbonflux)
_carbonflux_change["integer"].append("treecover_loss__year")
_carbonflux_change["double"] = [
    "treecover_loss__ha",
    "aboveground_biomass_loss__Mg",
    "gross_emissions_co2e_co2_only__Mg",
    "gross_emissions_co2e_non_co2__Mg",
    "gross_emissions_co2e_all_gases__Mg",
    "aboveground_carbon_stock_in_emissions_year__Mg",
    "belowground_carbon_stock_in_emissions_year__Mg",
    "deadwood_carbon_stock_in_emissions_year__Mg",
    "litter_carbon_stock_in_emissions_year__Mg",
    "soil_carbon_stock_in_emissions_year__Mg",
    "total_carbon_stock_in_emissions_year__Mg",
]

carbonflux_change_iso = deepcopy(_carbonflux_change)
carbonflux_change_adm1 = deepcopy(carbonflux_change_iso)
carbonflux_change_adm1["keyword"].append("adm1")
carbonflux_change_adm2 = deepcopy(carbonflux_change_adm1)
carbonflux_change_adm2["keyword"].append("adm2")