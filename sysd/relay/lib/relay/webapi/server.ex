# Adapted from https://angelika.me/2016/08/14/hello-world-web-app-in-elixir-part-1-cowboy/
# Rewritten https://ninenines.eu/docs/en/cowboy/2.6/manual/cowboy.start_clear/
# Rewritten https://elixirschool.com/en/lessons/specifics/plug/

defmodule Relay.WebAPI.Server do
  require Logger
  use Application

  def start(_type, _args) do
    port = Application.get_env(:relay, :port)

    children = [
      {Plug.Cowboy, scheme: :http, plug: Relay.WebAPI.Goodbye, options: [port: port]}
    ]
    opts = [strategy: :one_for_one, name: Relay.WebAPI.Supervisor]

    Logger.info("Starting camera relay...")

    Supervisor.start_link(children, opts)
  end

end
