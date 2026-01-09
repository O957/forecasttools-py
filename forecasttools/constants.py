"""
Constants for hubverse forecasting workflows. This module
provides standard constants used across CDC respiratory
disease forecast hubs including quantile levels, forecast
horizons, disease-specific column mappings, target
definitions, and hub location lists.
"""

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

# hub tasks.json URLs (authoritative source for location 
# requirements)
HUB_TASKS_JSON_URLS: dict[str, str] = {
    "flusight": "https://github.com/cdcepi/FluSight-forecast-hub/blob/main/hub-config/tasks.json",
    "covid": "https://github.com/CDCgov/COVID-19-Forecast-Hub/blob/main/hub-config/tasks.json",
    "rsv": "https://github.com/CDCgov/rsv-forecast-hub/blob/main/hub-config/tasks.json",
}

# 50 US state FIPS codes (excludes DC and territories)
US_STATE_FIPS: list[str] = [
    "01",  # Alabama
    "02",  # Alaska
    "04",  # Arizona
    "05",  # Arkansas
    "06",  # California
    "08",  # Colorado
    "09",  # Connecticut
    "10",  # Delaware
    "12",  # Florida
    "13",  # Georgia
    "15",  # Hawaii
    "16",  # Idaho
    "17",  # Illinois
    "18",  # Indiana
    "19",  # Iowa
    "20",  # Kansas
    "21",  # Kentucky
    "22",  # Louisiana
    "23",  # Maine
    "24",  # Maryland
    "25",  # Massachusetts
    "26",  # Michigan
    "27",  # Minnesota
    "28",  # Mississippi
    "29",  # Missouri
    "30",  # Montana
    "31",  # Nebraska
    "32",  # Nevada
    "33",  # New Hampshire
    "34",  # New Jersey
    "35",  # New Mexico
    "36",  # New York
    "37",  # North Carolina
    "38",  # North Dakota
    "39",  # Ohio
    "40",  # Oklahoma
    "41",  # Oregon
    "42",  # Pennsylvania
    "44",  # Rhode Island
    "45",  # South Carolina
    "46",  # South Dakota
    "47",  # Tennessee
    "48",  # Texas
    "49",  # Utah
    "50",  # Vermont
    "51",  # Virginia
    "53",  # Washington
    "54",  # West Virginia
    "55",  # Wisconsin
    "56",  # Wyoming
]

# DC and territory FIPS codes
DC_FIPS: str = "11"
PR_FIPS: str = "72"

# build hub location lists: US national + states + DC + 
# PR (in FIPS order) DC (11) is inserted between states 
# 10 and 12
_STATES_AND_DC: list[str] = US_STATE_FIPS[:8] + [DC_FIPS] + US_STATE_FIPS[8:]

# all three hubs currently have the same 53 locations
FLUSIGHT_LOCATIONS: list[str] = ["US"] + _STATES_AND_DC + [PR_FIPS]
COVID_HUB_LOCATIONS: list[str] = ["US"] + _STATES_AND_DC + [PR_FIPS]
RSV_HUB_LOCATIONS: list[str] = ["US"] + _STATES_AND_DC + [PR_FIPS]

# mapping from hub name to location list
HUB_LOCATIONS: dict[str, list[str]] = {
    "flusight": FLUSIGHT_LOCATIONS,
    "covid": COVID_HUB_LOCATIONS,
    "rsv": RSV_HUB_LOCATIONS,
}
