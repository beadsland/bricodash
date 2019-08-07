import Config

config :bindsight,
  cameras: %{
    space: "http://wrtnode-webcam.lan:8080/",
    door: "http://rfid-access-building.lan:8080/",
    cr10: "http://octoprint-main.lan:8080/",
    hydro: "http://hydrocontroller.lan:8081/"
  },
  cowboy_port: 2020

config :logger,
  backends: [:console],
  compile_time_purge_matching: [
    [level_lower_than: :info]
  ]

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
