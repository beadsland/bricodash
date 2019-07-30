import Config

config :relay,
  cameras: %{
    test: "http://192.168.42.22:8080/",
    space: "http://192.168.42.22:8080/"
  },
  port: 2020

config :logger,
  backends: [:console],
  compile_time_purge_matching: [
    [level_lower_than: :info]
  ]
