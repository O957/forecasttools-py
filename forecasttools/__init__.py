import importlib.resources

import arviz as az
import polars as pl

from forecasttools.constants import (
    ALL_LOCATION_CODES,
    COVID_HUB_LOCATIONS,
    DC_FIPS,
    DISEASE_NHSN_COLUMNS,
    DISEASE_TARGETS,
    FLUSIGHT_LOCATIONS,
    HUB_LOCATIONS,
    HUB_TASKS_JSON_URLS,
    HUB_URLS,
    HUBVERSE_QUANTILE_LEVELS,
    HUBVERSE_SUBMISSION_COLUMNS,
    PR_FIPS,
    RSV_HUB_LOCATIONS,
    STANDARD_HORIZONS,
    STATE_LOCATION_CODES,
    TERRITORY_LOCATION_CODES,
    VALID_DISEASES,
    VALID_TARGET_TYPES,
    location_table,
)
from forecasttools.daily_to_epiweekly import df_aggregate_to_epiweekly
from forecasttools.pull_data_cdc_gov import (
    data_cdc_gov_datasets,
    get_data_cdc_gov_dataset,
    get_dataset_info,
    get_nhsn,
)
from forecasttools.recode_locations import (
    filter_to_hub_locations,
    get_hub_locations,
    loc_abbr_to_hubverse_code,
    loc_hubverse_code_to_abbr,
    location_lookup,
    to_location_table_column,
)
from forecasttools.to_hubverse import get_hubverse_table
from forecasttools.trajectories_to_quantiles import trajectories_to_quantiles
from forecasttools.utils import (
    coalesce_common_columns,
    ensure_listlike,
    validate_and_get_idata_group,
    validate_and_get_idata_group_var,
    validate_idata_group_var_dim,
    validate_input_type,
    validate_iter_has_expected_types,
)

from . import arviz

# state names (for backwards compatibility)
united_states: list[str] = (
    location_table.filter(pl.col("is_state")).get_column("long_name").to_list()
)

# load example flusight submission
example_flusight_submission_path = importlib.resources.files(__package__).joinpath(
    "example_flusight_submission.parquet"
)
dtypes_d = {"location": pl.Utf8}
example_flusight_submission = pl.read_parquet(example_flusight_submission_path)

# load example fitting data for COVID
# (NHSN, as of 2024-09-26)
nhsn_hosp_COVID_path = importlib.resources.files(__package__).joinpath(
    "nhsn_hosp_COVID.parquet"
)
nhsn_hosp_COVID = pl.read_parquet(nhsn_hosp_COVID_path)

# load example fitting data for influenza
# (NHSN, as of 2024-09-26)
nhsn_hosp_flu_path = importlib.resources.files(__package__).joinpath(
    "nhsn_hosp_flu.parquet"
)
nhsn_hosp_flu = pl.read_parquet(nhsn_hosp_flu_path)

# load idata NHSN influenza forecast
# (NHSN, as of 2024-09-26) without dates
example_flu_forecast_wo_dates_path = importlib.resources.files(__package__).joinpath(
    "example_flu_forecast_wo_dates.nc"
)
nhsn_flu_forecast_wo_dates = az.from_netcdf(example_flu_forecast_wo_dates_path)

# load idata NHSN influenza forecast
# (NHSN, as of 2024-09-26) with dates
example_flu_forecast_w_dates_path = importlib.resources.files(__package__).joinpath(
    "example_flu_forecast_w_dates.nc"
)
nhsn_flu_forecast_w_dates = az.from_netcdf(example_flu_forecast_w_dates_path)


__all__ = [
    # data tables
    "location_table",
    "united_states",
    "example_flusight_submission",
    "nhsn_hosp_COVID",
    "nhsn_hosp_flu",
    "nhsn_flu_forecast_wo_dates",
    "nhsn_flu_forecast_w_dates",
    # constants
    "HUBVERSE_QUANTILE_LEVELS",
    "STANDARD_HORIZONS",
    "DISEASE_NHSN_COLUMNS",
    "DISEASE_TARGETS",
    "VALID_DISEASES",
    "VALID_TARGET_TYPES",
    "HUBVERSE_SUBMISSION_COLUMNS",
    "HUB_URLS",
    "HUB_TASKS_JSON_URLS",
    # location codes (derived from location_table)
    "ALL_LOCATION_CODES",
    "STATE_LOCATION_CODES",
    "TERRITORY_LOCATION_CODES",
    "DC_FIPS",
    "PR_FIPS",
    # hub location lists
    "FLUSIGHT_LOCATIONS",
    "COVID_HUB_LOCATIONS",
    "RSV_HUB_LOCATIONS",
    "HUB_LOCATIONS",
    # functions
    "trajectories_to_quantiles",
    "df_aggregate_to_epiweekly",
    "loc_abbr_to_hubverse_code",
    "loc_hubverse_code_to_abbr",
    "to_location_table_column",
    "location_lookup",
    "get_hub_locations",
    "filter_to_hub_locations",
    "get_hubverse_table",
    "validate_input_type",
    "validate_and_get_idata_group",
    "validate_and_get_idata_group_var",
    "validate_idata_group_var_dim",
    "validate_iter_has_expected_types",
    "ensure_listlike",
    "data_cdc_gov_datasets",
    "get_dataset_info",
    "get_data_cdc_gov_dataset",
    "get_nhsn",
    "coalesce_common_columns",
    "arviz",
]
