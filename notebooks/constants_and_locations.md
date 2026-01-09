# Constants & Hub Location Utilities


This notebook demonstrates the constants and hub location utilities
provided by `forecasttools`. These utilities standardize common values
used across CDC respiratory disease forecast hubs and simplify working
with hub-specific location requirements.

## Overview

The `forecasttools` package provides:

1.  **Constants** for hubverse workflows (quantile levels, horizons,
    disease mappings)
2.  **Hub-Specific Location Lists** for FluSight, COVID-19, and RSV hubs
3.  **Utility Functions** to retrieve and filter by hub locations

------------------------------------------------------------------------

## Setup

``` python
import forecasttools
import polars as pl
from rich import print
from rich.table import Table
from rich.console import Console

console = Console()
```

## Constants

### Hubverse Quantile Levels

The standard 23 quantile levels required for hubverse submissions:

``` python
table = Table(title="Hubverse Quantile Levels (23 levels)")
table.add_column("Index", style="dim")
table.add_column("Quantile", style="cyan")

for i, q in enumerate(forecasttools.HUBVERSE_QUANTILE_LEVELS, 1):
    table.add_row(str(i), str(q))

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic"> Hubverse Quantile  </span>
<span style="font-style: italic"> Levels (23 levels) </span>
┏━━━━━━━┳━━━━━━━━━━┓
┃<span style="font-weight: bold"> Index </span>┃<span style="font-weight: bold"> Quantile </span>┃
┡━━━━━━━╇━━━━━━━━━━┩
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 1     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.01     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 2     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.025    </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 3     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.05     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 4     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.1      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 5     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.15     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 6     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.2      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 7     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.25     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 8     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.3      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 9     </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.35     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 10    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.4      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 11    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.45     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 12    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.5      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 13    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.55     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 14    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.6      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 15    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.65     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 16    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.7      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 17    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.75     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 18    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.8      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 19    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.85     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 20    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.9      </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 21    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.95     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 22    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.975    </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 23    </span>│<span style="color: #008080; text-decoration-color: #008080"> 0.99     </span>│
└───────┴──────────┘
</pre>

### Standard Forecast Horizons

The standard forecast horizons for weekly submissions:

``` python
table = Table(title="Standard Forecast Horizons")
table.add_column("Horizon", style="cyan")
table.add_column("Meaning", style="green")

horizon_meanings = {
    -1: "nowcast (previous week)",
    0: "current week",
    1: "1 week ahead",
    2: "2 weeks ahead",
    3: "3 weeks ahead",
}

for h in forecasttools.STANDARD_HORIZONS:
    table.add_row(str(h), horizon_meanings[h])

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">     Standard Forecast Horizons      </span>
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Horizon </span>┃<span style="font-weight: bold"> Meaning                 </span>┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> -1      </span>│<span style="color: #008000; text-decoration-color: #008000"> nowcast (previous week) </span>│
│<span style="color: #008080; text-decoration-color: #008080"> 0       </span>│<span style="color: #008000; text-decoration-color: #008000"> current week            </span>│
│<span style="color: #008080; text-decoration-color: #008080"> 1       </span>│<span style="color: #008000; text-decoration-color: #008000"> 1 week ahead            </span>│
│<span style="color: #008080; text-decoration-color: #008080"> 2       </span>│<span style="color: #008000; text-decoration-color: #008000"> 2 weeks ahead           </span>│
│<span style="color: #008080; text-decoration-color: #008080"> 3       </span>│<span style="color: #008000; text-decoration-color: #008000"> 3 weeks ahead           </span>│
└─────────┴─────────────────────────┘
</pre>

### Disease Mappings

#### NHSN Column Names

Maps disease identifiers to the corresponding column names in NHSN
hospitalization data:

``` python
table = Table(title="Disease to NHSN Column Mapping")
table.add_column("Disease", style="cyan")
table.add_column("NHSN Column", style="green")

for disease, column in forecasttools.DISEASE_NHSN_COLUMNS.items():
    table.add_row(disease, column)

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic"> Disease to NHSN Column Mapping </span>
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Disease </span>┃<span style="font-weight: bold"> NHSN Column        </span>┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> flu     </span>│<span style="color: #008000; text-decoration-color: #008000"> totalconfflunewadm </span>│
│<span style="color: #008080; text-decoration-color: #008080"> covid   </span>│<span style="color: #008000; text-decoration-color: #008000"> totalconfc19newadm </span>│
│<span style="color: #008080; text-decoration-color: #008080"> rsv     </span>│<span style="color: #008000; text-decoration-color: #008000"> totalconfrsvnewadm </span>│
└─────────┴────────────────────┘
</pre>

#### Hubverse Target Names

Maps disease identifiers to the hubverse target strings used in
submissions. Each disease has two target types: `hosp` (NHSN
hospitalization data) and `ed` (NSSP ED visit proportion data).

``` python
table = Table(title="Disease Targets")
table.add_column("Disease", style="cyan")
table.add_column("Type", style="yellow")
table.add_column("Target String", style="green")

for disease, targets in forecasttools.DISEASE_TARGETS.items():
    for target_type, target in targets.items():
        table.add_row(disease, target_type, target)

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                Disease Targets                 </span>
┏━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Disease </span>┃<span style="font-weight: bold"> Type </span>┃<span style="font-weight: bold"> Target String               </span>┃
┡━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> flu     </span>│<span style="color: #808000; text-decoration-color: #808000"> hosp </span>│<span style="color: #008000; text-decoration-color: #008000"> wk inc flu hosp             </span>│
│<span style="color: #008080; text-decoration-color: #008080"> flu     </span>│<span style="color: #808000; text-decoration-color: #808000"> ed   </span>│<span style="color: #008000; text-decoration-color: #008000"> wk inc flu prop ed visits   </span>│
│<span style="color: #008080; text-decoration-color: #008080"> covid   </span>│<span style="color: #808000; text-decoration-color: #808000"> hosp </span>│<span style="color: #008000; text-decoration-color: #008000"> wk inc covid hosp           </span>│
│<span style="color: #008080; text-decoration-color: #008080"> covid   </span>│<span style="color: #808000; text-decoration-color: #808000"> ed   </span>│<span style="color: #008000; text-decoration-color: #008000"> wk inc covid prop ed visits </span>│
│<span style="color: #008080; text-decoration-color: #008080"> rsv     </span>│<span style="color: #808000; text-decoration-color: #808000"> hosp </span>│<span style="color: #008000; text-decoration-color: #008000"> wk inc rsv hosp             </span>│
│<span style="color: #008080; text-decoration-color: #008080"> rsv     </span>│<span style="color: #808000; text-decoration-color: #808000"> ed   </span>│<span style="color: #008000; text-decoration-color: #008000"> wk inc rsv prop ed visits   </span>│
└─────────┴──────┴─────────────────────────────┘
</pre>

#### Valid Diseases and Target Types

``` python
print(f"[bold]Valid disease identifiers:[/bold] {forecasttools.VALID_DISEASES}")
print(f"[bold]Valid target types:[/bold] {forecasttools.VALID_TARGET_TYPES}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Valid disease identifiers:</span> <span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'flu'</span>, <span style="color: #008000; text-decoration-color: #008000">'covid'</span>, <span style="color: #008000; text-decoration-color: #008000">'rsv'</span><span style="font-weight: bold">]</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Valid target types:</span> <span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'hosp'</span>, <span style="color: #008000; text-decoration-color: #008000">'ed'</span><span style="font-weight: bold">]</span>
</pre>

### Submission Column Order

The required column order for hubverse submission files:

``` python
table = Table(title="Hubverse Submission Columns (in order)")
table.add_column("#", style="dim")
table.add_column("Column Name", style="cyan")

for i, col in enumerate(forecasttools.HUBVERSE_SUBMISSION_COLUMNS, 1):
    table.add_row(str(i), col)

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">  Hubverse Submission  </span>
<span style="font-style: italic">  Columns (in order)   </span>
┏━━━┳━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> # </span>┃<span style="font-weight: bold"> Column Name     </span>┃
┡━━━╇━━━━━━━━━━━━━━━━━┩
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 1 </span>│<span style="color: #008080; text-decoration-color: #008080"> reference_date  </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 2 </span>│<span style="color: #008080; text-decoration-color: #008080"> target          </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 3 </span>│<span style="color: #008080; text-decoration-color: #008080"> horizon         </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 4 </span>│<span style="color: #008080; text-decoration-color: #008080"> target_end_date </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 5 </span>│<span style="color: #008080; text-decoration-color: #008080"> location        </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 6 </span>│<span style="color: #008080; text-decoration-color: #008080"> output_type     </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 7 </span>│<span style="color: #008080; text-decoration-color: #008080"> output_type_id  </span>│
│<span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> 8 </span>│<span style="color: #008080; text-decoration-color: #008080"> value           </span>│
└───┴─────────────────┘
</pre>

------------------------------------------------------------------------

## Hub Location Lists

Each CDC forecast hub accepts submissions for a specific set of
locations. These are provided as constants.

### Official Hub Location Specifications

The location requirements for each hub are defined in their respective
`hub-config/tasks.json` files. The hub URLs are available as constants:

``` python
table = Table(title="CDC Forecast Hub URLs")
table.add_column("Hub", style="cyan")
table.add_column("Repository URL", style="green")

for hub, url in forecasttools.HUB_URLS.items():
    table.add_row(hub, url)

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                    CDC Forecast Hub URLs                     </span>
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Hub      </span>┃<span style="font-weight: bold"> Repository URL                                  </span>┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> flusight </span>│<span style="color: #008000; text-decoration-color: #008000"> https://github.com/cdcepi/FluSight-forecast-hub </span>│
│<span style="color: #008080; text-decoration-color: #008080"> covid    </span>│<span style="color: #008000; text-decoration-color: #008000"> https://github.com/CDCgov/COVID-19-Forecast-Hub </span>│
│<span style="color: #008080; text-decoration-color: #008080"> rsv      </span>│<span style="color: #008000; text-decoration-color: #008000"> https://github.com/CDCgov/rsv-forecast-hub      </span>│
└──────────┴─────────────────────────────────────────────────┘
</pre>

**FluSight (Influenza) Hub**

> Locations are specified in the [FluSight-forecast-hub
> tasks.json](https://github.com/cdcepi/FluSight-forecast-hub/blob/main/hub-config/tasks.json).
> The hub accepts forecasts for 50 US states, the District of Columbia,
> Puerto Rico, and a national aggregate (US).

**COVID-19 Forecast Hub**

> Locations are specified in the [COVID-19-Forecast-Hub
> tasks.json](https://github.com/CDCgov/COVID-19-Forecast-Hub/blob/main/hub-config/tasks.json).
> The location set matches FluSight: 50 states + DC + PR + US national.

**RSV Forecast Hub**

> Locations are specified in the [rsv-forecast-hub
> tasks.json](https://github.com/CDCgov/rsv-forecast-hub/blob/main/hub-config/tasks.json).
> The location set matches FluSight and COVID-19: 50 states + DC + PR +
> US national.

------------------------------------------------------------------------

### All US Jurisdictions

All FIPS codes in `forecasttools` are derived programmatically from
`location_table.parquet` (Census data), not hardcoded. This ensures
consistency and makes it easy to update if jurisdictions change.

``` python
# the location_table is the source of truth for all FIPS codes
print("[bold]location_table structure:[/bold]")
print(forecasttools.location_table.head(5))
print(f"\n[bold]Total jurisdictions:[/bold] {len(forecasttools.location_table)}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">location_table structure:</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">shape: <span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">5</span>, <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">5</span><span style="font-weight: bold">)</span>
┌───────────────┬────────────┬───────────────┬────────────┬──────────┐
│ location_code ┆ short_name ┆ long_name     ┆ population ┆ is_state │
│ ---           ┆ ---        ┆ ---           ┆ ---        ┆ ---      │
│ str           ┆ str        ┆ str           ┆ i64        ┆ bool     │
╞═══════════════╪════════════╪═══════════════╪════════════╪══════════╡
│ US            ┆ US         ┆ United States ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">334735155</span>  ┆ false    │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">01</span>            ┆ AL         ┆ Alabama       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">5024279</span>    ┆ true     │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">02</span>            ┆ AK         ┆ Alaska        ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">733391</span>     ┆ true     │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">04</span>            ┆ AZ         ┆ Arizona       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">7151502</span>    ┆ true     │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">05</span>            ┆ AR         ┆ Arkansas      ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3011524</span>    ┆ true     │
└───────────────┴────────────┴───────────────┴────────────┴──────────┘
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
<span style="font-weight: bold">Total jurisdictions:</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">58</span>
</pre>

``` python
table = Table(title="All US Location Codes (from location_table)")
table.add_column("Constant", style="cyan")
table.add_column("Count", style="green")
table.add_column("Description", style="yellow")

table.add_row("ALL_LOCATION_CODES", str(len(forecasttools.ALL_LOCATION_CODES)), "All 58 US jurisdictions")
table.add_row("STATE_LOCATION_CODES", str(len(forecasttools.STATE_LOCATION_CODES)), "50 US states")
table.add_row("TERRITORY_LOCATION_CODES", str(len(forecasttools.TERRITORY_LOCATION_CODES)), "DC + 6 territories")

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">         All US Location Codes (from location_table)          </span>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Constant                 </span>┃<span style="font-weight: bold"> Count </span>┃<span style="font-weight: bold"> Description             </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> ALL_LOCATION_CODES       </span>│<span style="color: #008000; text-decoration-color: #008000"> 58    </span>│<span style="color: #808000; text-decoration-color: #808000"> All 58 US jurisdictions </span>│
│<span style="color: #008080; text-decoration-color: #008080"> STATE_LOCATION_CODES     </span>│<span style="color: #008000; text-decoration-color: #008000"> 50    </span>│<span style="color: #808000; text-decoration-color: #808000"> 50 US states            </span>│
│<span style="color: #008080; text-decoration-color: #008080"> TERRITORY_LOCATION_CODES </span>│<span style="color: #008000; text-decoration-color: #008000"> 7     </span>│<span style="color: #808000; text-decoration-color: #808000"> DC + 6 territories      </span>│
└──────────────────────────┴───────┴─────────────────────────┘
</pre>

``` python
print("[bold]Territories:[/bold]")
for code in forecasttools.TERRITORY_LOCATION_CODES:
    row = forecasttools.location_table.filter(pl.col("location_code") == code)
    name = row.get_column("long_name")[0]
    abbr = row.get_column("short_name")[0]
    print(f"  {code}: {abbr} ({name})")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Territories:</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">11</span>: DC <span style="font-weight: bold">(</span>District of Columbia<span style="font-weight: bold">)</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">60</span>: AS <span style="font-weight: bold">(</span>American Samoa<span style="font-weight: bold">)</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">66</span>: GU <span style="font-weight: bold">(</span>Guam<span style="font-weight: bold">)</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">69</span>: MP <span style="font-weight: bold">(</span>Northern Mariana Islands<span style="font-weight: bold">)</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">72</span>: PR <span style="font-weight: bold">(</span>Puerto Rico<span style="font-weight: bold">)</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">74</span>: UM <span style="font-weight: bold">(</span>U.S. Minor Outlying Islands<span style="font-weight: bold">)</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">78</span>: VI <span style="font-weight: bold">(</span>U.S. Virgin Islands<span style="font-weight: bold">)</span>
</pre>

------------------------------------------------------------------------

### Hub Location Summary

``` python
table = Table(title="Hub Location Lists")
table.add_column("Hub", style="cyan")
table.add_column("Count", style="green")
table.add_column("Description", style="yellow")

table.add_row("FluSight", str(len(forecasttools.FLUSIGHT_LOCATIONS)), "50 states + DC + PR + US")
table.add_row("COVID-19", str(len(forecasttools.COVID_HUB_LOCATIONS)), "50 states + DC + PR + US")
table.add_row("RSV", str(len(forecasttools.RSV_HUB_LOCATIONS)), "50 states + DC + PR + US")

console.print(table)

# check if all are the same
all_same = (
    forecasttools.FLUSIGHT_LOCATIONS
    == forecasttools.COVID_HUB_LOCATIONS
    == forecasttools.RSV_HUB_LOCATIONS
)
print(f"\n[bold]All hubs have identical location lists:[/bold] {all_same}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">              Hub Location Lists               </span>
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Hub      </span>┃<span style="font-weight: bold"> Count </span>┃<span style="font-weight: bold"> Description              </span>┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> FluSight </span>│<span style="color: #008000; text-decoration-color: #008000"> 53    </span>│<span style="color: #808000; text-decoration-color: #808000"> 50 states + DC + PR + US </span>│
│<span style="color: #008080; text-decoration-color: #008080"> COVID-19 </span>│<span style="color: #008000; text-decoration-color: #008000"> 53    </span>│<span style="color: #808000; text-decoration-color: #808000"> 50 states + DC + PR + US </span>│
│<span style="color: #008080; text-decoration-color: #008080"> RSV      </span>│<span style="color: #008000; text-decoration-color: #008000"> 53    </span>│<span style="color: #808000; text-decoration-color: #808000"> 50 states + DC + PR + US </span>│
└──────────┴───────┴──────────────────────────┘
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
<span style="font-weight: bold">All hubs have identical location lists:</span> <span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">True</span>
</pre>

### HUB_LOCATIONS Dictionary

Access location lists by hub name:

``` python
table = Table(title="HUB_LOCATIONS Dictionary")
table.add_column("Key", style="cyan")
table.add_column("Locations", style="green")

for hub, locations in forecasttools.HUB_LOCATIONS.items():
    table.add_row(hub, str(len(locations)))

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">HUB_LOCATIONS Dictionary</span>
┏━━━━━━━━━━┳━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Key      </span>┃<span style="font-weight: bold"> Locations </span>┃
┡━━━━━━━━━━╇━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> flusight </span>│<span style="color: #008000; text-decoration-color: #008000"> 53        </span>│
│<span style="color: #008080; text-decoration-color: #008080"> covid    </span>│<span style="color: #008000; text-decoration-color: #008000"> 53        </span>│
│<span style="color: #008080; text-decoration-color: #008080"> rsv      </span>│<span style="color: #008000; text-decoration-color: #008000"> 53        </span>│
└──────────┴───────────┘
</pre>

------------------------------------------------------------------------

## Utility Functions

### get_hub_locations()

Retrieve the list of valid location codes for a specific hub:

``` python
flusight_locs = forecasttools.get_hub_locations("flusight")
covid_locs = forecasttools.get_hub_locations("covid")
rsv_locs = forecasttools.get_hub_locations("rsv")

table = Table(title="get_hub_locations() Results")
table.add_column("Hub", style="cyan")
table.add_column("Count", style="green")

table.add_row("flusight", str(len(flusight_locs)))
table.add_row("covid", str(len(covid_locs)))
table.add_row("rsv", str(len(rsv_locs)))

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">get_hub_locations() </span>
<span style="font-style: italic">      Results       </span>
┏━━━━━━━━━━┳━━━━━━━┓
┃<span style="font-weight: bold"> Hub      </span>┃<span style="font-weight: bold"> Count </span>┃
┡━━━━━━━━━━╇━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> flusight </span>│<span style="color: #008000; text-decoration-color: #008000"> 53    </span>│
│<span style="color: #008080; text-decoration-color: #008080"> covid    </span>│<span style="color: #008000; text-decoration-color: #008000"> 53    </span>│
│<span style="color: #008080; text-decoration-color: #008080"> rsv      </span>│<span style="color: #008000; text-decoration-color: #008000"> 53    </span>│
└──────────┴───────┘
</pre>

The function is case-insensitive:

``` python
locs1 = forecasttools.get_hub_locations("flusight")
locs2 = forecasttools.get_hub_locations("FluSight")
locs3 = forecasttools.get_hub_locations("FLUSIGHT")
print(f"[bold]Case insensitive:[/bold] {locs1 == locs2 == locs3}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Case insensitive:</span> <span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">True</span>
</pre>

Invalid hub names raise a helpful error:

``` python
try:
    forecasttools.get_hub_locations("invalid_hub")
except ValueError as e:
    print(f"[red]ValueError:[/red] {e}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800000; text-decoration-color: #800000">ValueError:</span> Unknown hub <span style="color: #008000; text-decoration-color: #008000">'invalid_hub'</span>. Expected one of: <span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'flusight'</span>, <span style="color: #008000; text-decoration-color: #008000">'covid'</span>, <span style="color: #008000; text-decoration-color: #008000">'rsv'</span><span style="font-weight: bold">]</span>.
</pre>

### filter_to_hub_locations()

Filter a DataFrame to only include rows with valid hub locations:

``` python
# create sample data with various locations
sample_data = pl.DataFrame({
    "location": ["01", "02", "72", "78", "99", "US"],
    "value": [100, 200, 300, 400, 500, 600],
    "state_name": ["Alabama", "Alaska", "Puerto Rico", "Virgin Islands", "Invalid", "United States"]
})

print("[bold]Original data:[/bold]")
print(sample_data)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Original data:</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">shape: <span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">6</span>, <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3</span><span style="font-weight: bold">)</span>
┌──────────┬───────┬────────────────┐
│ location ┆ value ┆ state_name     │
│ ---      ┆ ---   ┆ ---            │
│ str      ┆ i64   ┆ str            │
╞══════════╪═══════╪════════════════╡
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">01</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">100</span>   ┆ Alabama        │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">02</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">200</span>   ┆ Alaska         │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">72</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">300</span>   ┆ Puerto Rico    │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">78</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">400</span>   ┆ Virgin Islands │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">99</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">500</span>   ┆ Invalid        │
│ US       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">600</span>   ┆ United States  │
└──────────┴───────┴────────────────┘
</pre>

``` python
# filter to FluSight locations
flusight_filtered = forecasttools.filter_to_hub_locations(
    sample_data,
    hub="flusight",
    location_col="location"
)

print("[bold]Filtered to FluSight locations:[/bold]")
print(flusight_filtered)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Filtered to FluSight locations:</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">shape: <span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4</span>, <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3</span><span style="font-weight: bold">)</span>
┌──────────┬───────┬───────────────┐
│ location ┆ value ┆ state_name    │
│ ---      ┆ ---   ┆ ---           │
│ str      ┆ i64   ┆ str           │
╞══════════╪═══════╪═══════════════╡
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">01</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">100</span>   ┆ Alabama       │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">02</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">200</span>   ┆ Alaska        │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">72</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">300</span>   ┆ Puerto Rico   │
│ US       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">600</span>   ┆ United States │
└──────────┴───────┴───────────────┘
</pre>

------------------------------------------------------------------------

## Example: Building a Submission Workflow

Here’s how these utilities can be used together in a forecast submission
workflow:

``` python
# 1. define the disease and hub
disease = "flu"
hub = "flusight"

# 2. get the target name and valid locations
target = forecasttools.DISEASE_TARGETS[disease]
valid_locations = forecasttools.get_hub_locations(hub)

print(f"[bold]Disease:[/bold] {disease}")
print(f"[bold]Hub:[/bold] {hub}")
print(f"[bold]Target:[/bold] {target}")
print(f"[bold]Valid locations:[/bold] {len(valid_locations)}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Disease:</span> flu
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Hub:</span> flusight
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Target:</span> <span style="font-weight: bold">{</span><span style="color: #008000; text-decoration-color: #008000">'hosp'</span>: <span style="color: #008000; text-decoration-color: #008000">'wk inc flu hosp'</span>, <span style="color: #008000; text-decoration-color: #008000">'ed'</span>: <span style="color: #008000; text-decoration-color: #008000">'wk inc flu prop ed visits'</span><span style="font-weight: bold">}</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Valid locations:</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">53</span>
</pre>

``` python
# 3. create a sample forecast DataFrame (in practice, from your model)
sample_forecast = pl.DataFrame({
    "location": ["01", "02", "06", "99"],  # includes one invalid
    "horizon": [0, 0, 0, 0],
    "quantile_level": [0.5, 0.5, 0.5, 0.5],
    "value": [100.0, 50.0, 500.0, 999.0]
})

# 4. filter to valid hub locations
filtered_forecast = forecasttools.filter_to_hub_locations(
    sample_forecast,
    hub=hub,
    location_col="location"
)

print(f"[bold]Original rows:[/bold] {len(sample_forecast)}")
print(f"[bold]After filtering:[/bold] {len(filtered_forecast)}")
print(filtered_forecast)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Original rows:</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">After filtering:</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">shape: <span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3</span>, <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4</span><span style="font-weight: bold">)</span>
┌──────────┬─────────┬────────────────┬───────┐
│ location ┆ horizon ┆ quantile_level ┆ value │
│ ---      ┆ ---     ┆ ---            ┆ ---   │
│ str      ┆ i64     ┆ f64            ┆ f64   │
╞══════════╪═════════╪════════════════╪═══════╡
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">01</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.5</span>            ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">100.0</span> │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">02</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.5</span>            ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">50.0</span>  │
│ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">06</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>       ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.5</span>            ┆ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">500.0</span> │
└──────────┴─────────┴────────────────┴───────┘
</pre>

``` python
# 5. verify quantile levels match hubverse requirements
model_quantiles = [0.01, 0.025, 0.05, 0.5, 0.95, 0.975, 0.99]
required_quantiles = forecasttools.HUBVERSE_QUANTILE_LEVELS

missing = set(required_quantiles) - set(model_quantiles)

table = Table(title="Quantile Level Verification")
table.add_column("Metric", style="cyan")
table.add_column("Value", style="green")

table.add_row("Required quantile levels", str(len(required_quantiles)))
table.add_row("Model quantile levels", str(len(model_quantiles)))
table.add_row("Missing quantiles", str(len(missing)))

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">    Quantile Level Verification     </span>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃<span style="font-weight: bold"> Metric                   </span>┃<span style="font-weight: bold"> Value </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> Required quantile levels </span>│<span style="color: #008000; text-decoration-color: #008000"> 23    </span>│
│<span style="color: #008080; text-decoration-color: #008080"> Model quantile levels    </span>│<span style="color: #008000; text-decoration-color: #008000"> 7     </span>│
│<span style="color: #008080; text-decoration-color: #008080"> Missing quantiles        </span>│<span style="color: #008000; text-decoration-color: #008000"> 16    </span>│
└──────────────────────────┴───────┘
</pre>

------------------------------------------------------------------------

## Summary

``` python
table = Table(title="forecasttools Constants & Functions Summary")
table.add_column("Name", style="cyan")
table.add_column("Description", style="green")

summary_data = [
    ("HUBVERSE_QUANTILE_LEVELS", "23 standard quantile levels"),
    ("STANDARD_HORIZONS", "[-1, 0, 1, 2, 3] forecast horizons"),
    ("DISEASE_NHSN_COLUMNS", "Maps disease to NHSN column names"),
    ("DISEASE_TARGETS", "Maps disease to hubverse target names (hosp + ed)"),
    ("HUBVERSE_SUBMISSION_COLUMNS", "Required column order"),
    ("HUB_URLS", "CDC forecast hub repository URLs"),
    ("HUB_TASKS_JSON_URLS", "Hub tasks.json URLs (location specs)"),
    ("ALL_LOCATION_CODES", "All 58 US jurisdiction FIPS codes (derived)"),
    ("STATE_LOCATION_CODES", "50 US state FIPS codes (derived)"),
    ("TERRITORY_LOCATION_CODES", "DC + 6 territory FIPS codes (derived)"),
    ("DC_FIPS", "District of Columbia FIPS code"),
    ("PR_FIPS", "Puerto Rico FIPS code"),
    ("FLUSIGHT_LOCATIONS", "53 FluSight hub locations"),
    ("COVID_HUB_LOCATIONS", "53 COVID-19 hub locations"),
    ("RSV_HUB_LOCATIONS", "53 RSV hub locations"),
    ("location_table", "DataFrame with all jurisdiction metadata"),
    ("get_hub_locations(hub)", "Get locations for a hub"),
    ("filter_to_hub_locations(df, hub)", "Filter DataFrame to hub locations"),
]

for name, desc in summary_data:
    table.add_row(name, desc)

console.print(table)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                      forecasttools Constants &amp; Functions Summary                       </span>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Name                             </span>┃<span style="font-weight: bold"> Description                                       </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│<span style="color: #008080; text-decoration-color: #008080"> HUBVERSE_QUANTILE_LEVELS         </span>│<span style="color: #008000; text-decoration-color: #008000"> 23 standard quantile levels                       </span>│
│<span style="color: #008080; text-decoration-color: #008080"> STANDARD_HORIZONS                </span>│<span style="color: #008000; text-decoration-color: #008000"> [-1, 0, 1, 2, 3] forecast horizons                </span>│
│<span style="color: #008080; text-decoration-color: #008080"> DISEASE_NHSN_COLUMNS             </span>│<span style="color: #008000; text-decoration-color: #008000"> Maps disease to NHSN column names                 </span>│
│<span style="color: #008080; text-decoration-color: #008080"> DISEASE_TARGETS                  </span>│<span style="color: #008000; text-decoration-color: #008000"> Maps disease to hubverse target names (hosp + ed) </span>│
│<span style="color: #008080; text-decoration-color: #008080"> HUBVERSE_SUBMISSION_COLUMNS      </span>│<span style="color: #008000; text-decoration-color: #008000"> Required column order                             </span>│
│<span style="color: #008080; text-decoration-color: #008080"> HUB_URLS                         </span>│<span style="color: #008000; text-decoration-color: #008000"> CDC forecast hub repository URLs                  </span>│
│<span style="color: #008080; text-decoration-color: #008080"> HUB_TASKS_JSON_URLS              </span>│<span style="color: #008000; text-decoration-color: #008000"> Hub tasks.json URLs (location specs)              </span>│
│<span style="color: #008080; text-decoration-color: #008080"> ALL_LOCATION_CODES               </span>│<span style="color: #008000; text-decoration-color: #008000"> All 58 US jurisdiction FIPS codes (derived)       </span>│
│<span style="color: #008080; text-decoration-color: #008080"> STATE_LOCATION_CODES             </span>│<span style="color: #008000; text-decoration-color: #008000"> 50 US state FIPS codes (derived)                  </span>│
│<span style="color: #008080; text-decoration-color: #008080"> TERRITORY_LOCATION_CODES         </span>│<span style="color: #008000; text-decoration-color: #008000"> DC + 6 territory FIPS codes (derived)             </span>│
│<span style="color: #008080; text-decoration-color: #008080"> DC_FIPS                          </span>│<span style="color: #008000; text-decoration-color: #008000"> District of Columbia FIPS code                    </span>│
│<span style="color: #008080; text-decoration-color: #008080"> PR_FIPS                          </span>│<span style="color: #008000; text-decoration-color: #008000"> Puerto Rico FIPS code                             </span>│
│<span style="color: #008080; text-decoration-color: #008080"> FLUSIGHT_LOCATIONS               </span>│<span style="color: #008000; text-decoration-color: #008000"> 53 FluSight hub locations                         </span>│
│<span style="color: #008080; text-decoration-color: #008080"> COVID_HUB_LOCATIONS              </span>│<span style="color: #008000; text-decoration-color: #008000"> 53 COVID-19 hub locations                         </span>│
│<span style="color: #008080; text-decoration-color: #008080"> RSV_HUB_LOCATIONS                </span>│<span style="color: #008000; text-decoration-color: #008000"> 53 RSV hub locations                              </span>│
│<span style="color: #008080; text-decoration-color: #008080"> location_table                   </span>│<span style="color: #008000; text-decoration-color: #008000"> DataFrame with all jurisdiction metadata          </span>│
│<span style="color: #008080; text-decoration-color: #008080"> get_hub_locations(hub)           </span>│<span style="color: #008000; text-decoration-color: #008000"> Get locations for a hub                           </span>│
│<span style="color: #008080; text-decoration-color: #008080"> filter_to_hub_locations(df, hub) </span>│<span style="color: #008000; text-decoration-color: #008000"> Filter DataFrame to hub locations                 </span>│
└──────────────────────────────────┴───────────────────────────────────────────────────┘
</pre>
