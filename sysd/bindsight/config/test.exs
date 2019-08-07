import Config

config :bindsight,
  ignore_noproc: true

config :logger,
  backends: [:console],
  compile_time_purge_matching: [
    [level_lower_than: :info]
  ]

import_config "dev.exs"
