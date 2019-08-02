import Config

config :bindsight,
  cameras: %{
    test: "http://wrtnode-webcam.lan:8080/",
    space: "http://wrtnode-webcam.lan:8080/",
    door: "http://rfid-access-building.lan:8080/",
    cr10: "http://octoprint-main.lan:8080/",
    hydro: "http://hydrocontroller.lan:8081/"
  },
  port: 2020

config :logger,
  backends: [:console],
  compile_time_purge_matching: [
    [level_lower_than: :info]
  ]
