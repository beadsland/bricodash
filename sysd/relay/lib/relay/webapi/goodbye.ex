#Ref: https://angelika.me/2016/08/14/hello-world-web-app-in-elixir-part-1-cowboy/
# Replae: https://elixirschool.com/en/lessons/specifics/plug/

defmodule Relay.WebAPI.Goodbye do
  require Logger
  import Plug.Conn

  def init(options), do: options

  def call(conn, _opts) do
    conn
    |> put_resp_content_type("text/plain")
    |> send_resp(404, "Goodbye!\n")
  end

end
