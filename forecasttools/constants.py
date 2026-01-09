"""
Constants for hubverse forecasting workflows. This module
provides standard constants used across CDC respiratory
disease forecast hubs including quantile levels, forecast
horizons, disease-specific column mappings, target
definitions, and hub location lists.

Location codes are derived programmatically from the
location_table.parquet file (Census data).
"""

import importlib.resources

import polars as pl


_location_table_path = importlib.resources.files(__package__).joinpath(
    "location_table.parquet"
)
location_table: pl.DataFrame = pl.read_parquet(_location_table_path)


# standard hubverse quantile levels (23 levels)
HUBVERSE_QUANTILE_LEVELS: list[float] = [
    0.01,
    0.025,
    0.05,
    0.1,
    0.15,
    0.2,
    0.25,
    0.3,
    0.35,
    0.4,
    0.45,
    0.5,
    0.55,
    0.6,
    0.65,
    0.7,
    0.75,
    0.8,
    0.85,
    0.9,
    0.95,
    0.975,
    0.99,
]

# standard forecast horizons for weekly submissions
# -1 = nowcast, 0 = current week, 1-3 = future weeks
STANDARD_HORIZONS: list[int] = [-1, 0, 1, 2, 3]


# valid disease identifiers
VALID_DISEASES: list[str] = ["flu", "covid", "rsv"]

# valid target types
VALID_TARGET_TYPES: list[str] = ["hosp", "ed"]

# NHSN dataset column names for each disease; these map to
# columns in the NHSN hospitalization reporting data
DISEASE_NHSN_COLUMNS: dict[str, str] = {
    "flu": "totalconfflunewadm",
    "covid": "totalconfc19newadm",
    "rsv": "totalconfrsvnewadm",
}

# hubverse target names by disease and target type
# hosp = NHSN hospitalization data, ed = NSSP ED visit
# proportion data
DISEASE_TARGETS: dict[str, dict[str, str]] = {
    "flu": {
        "hosp": "wk inc flu hosp",
        "ed": "wk inc flu prop ed visits",
    },
    "covid": {
        "hosp": "wk inc covid hosp",
        "ed": "wk inc covid prop ed visits",
    },
    "rsv": {
        "hosp": "wk inc rsv hosp",
        "ed": "wk inc rsv prop ed visits",
    },
}

# hubverse submission column order
HUBVERSE_SUBMISSION_COLUMNS: list[str] = [
    "reference_date",
    "target",
    "horizon",
    "target_end_date",
    "location",
    "output_type",
    "output_type_id",
    "value",
]

# official CDC forecast hub repositories
HUB_URLS: dict[str, str] = {
    "flusight": "https://github.com/cdcepi/FluSight-forecast-hub",
    "covid": "https://github.com/CDCgov/COVID-19-Forecast-Hub",
    "rsv": "https://github.com/CDCgov/rsv-forecast-hub",
}

# hub tasks.json URLs (authoritative source for location requirements)
HUB_TASKS_JSON_URLS: dict[str, str] = {
    "flusight": "https://github.com/cdcepi/FluSight-forecast-hub/blob/main/hub-config/tasks.json",
    "covid": "https://github.com/CDCgov/COVID-19-Forecast-Hub/blob/main/hub-config/tasks.json",
    "rsv": "https://github.com/CDCgov/rsv-forecast-hub/blob/main/hub-config/tasks.json",
}

# all location codes from Census data
ALL_LOCATION_CODES: list[str] = location_table.get_column("location_code").to_list()

# 50 US state FIPS codes (is_state=True in location_table)
STATE_LOCATION_CODES: list[str] = (
    location_table.filter(pl.col("is_state"))
    .sort("location_code")
    .get_column("location_code")
    .to_list()
)

# DC and territory FIPS codes (is_state=False, excluding US)
TERRITORY_LOCATION_CODES: list[str] = (
    location_table.filter(~pl.col("is_state") & (pl.col("location_code") != "US"))
    .sort("location_code")
    .get_column("location_code")
    .to_list()
)

# individual territory codes for convenience
DC_FIPS: str = "11"
PR_FIPS: str = "72"


# hub locations are built from location_table data
# all three hubs currently accept: US + 50 states + DC + PR (53 locations)
# locations are sorted in FIPS order with US first
def _build_hub_locations() -> list[str]:
    """Build hub location list: US + states + DC + PR in FIPS order."""
    # get states + DC + PR, sorted by FIPS code
    hub_codes = (
        location_table.filter(
            pl.col("is_state")  # 50 states
            | (pl.col("location_code") == DC_FIPS)  # DC
            | (pl.col("location_code") == PR_FIPS)  # PR
        )
        .sort("location_code")
        .get_column("location_code")
        .to_list()
    )
    return ["US"] + hub_codes


# all three hubs currently have the same 53 locations
FLUSIGHT_LOCATIONS: list[str] = _build_hub_locations()
COVID_HUB_LOCATIONS: list[str] = _build_hub_locations()
RSV_HUB_LOCATIONS: list[str] = _build_hub_locations()

# mapping from hub name to location list
HUB_LOCATIONS: dict[str, list[str]] = {
    "flusight": FLUSIGHT_LOCATIONS,
    "covid": COVID_HUB_LOCATIONS,
    "rsv": RSV_HUB_LOCATIONS,
}
