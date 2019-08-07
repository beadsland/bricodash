import Config

config :bindsight,
  cameras: %{
    test: "http://rfid-access-building.lan:8080/",
    space: "http://wrtnode-webcam.lan:8080/",
    door: "http://rfid-access-building.lan:8080/",
    cr10: "http://octoprint-main.lan:8080/",
    hydro: "http://hydrocontroller.lan:8081/"
  },
  cowboy_acceptors: 5,
  cluck_errors: true
