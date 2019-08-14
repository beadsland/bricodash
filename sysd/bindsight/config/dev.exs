import Config

config :bindsight,
  cameras: %{
    test: "http://rfid-access-building.lan:8080/",
    space: "http://wrtnode-webcam.lan:8080/",
    door: "http://rfid-access-building.lan:8080/"
  },
  cowboy_acceptors: 5,
  cluck_errors: true,
  register_shortnames: true

config :logger, :console,
  format: "$time $metadata[$level] $levelpad$message\n",
  compile_time_purge_matching: [
    [level_lower_than: :info]
  ]
