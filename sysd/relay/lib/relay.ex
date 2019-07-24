defmodule Relay do
  @moduledoc """
  Service to relay MJPEG camera streams to one or more clients as streams or
  snapshots. Proactively checks for corrupt frames and drops them before
  forwarding to clients.
  """

  @doc """
  Assemble camera URL.
  """

  def camera do
    camera = "http://rfid-access-building.lan:8080/"
    params = %{"action" => "stream"}
    camera = URI.parse(camera) |> Map.put(:query, URI.encode_query(params))
      |> URI.to_string()
    IO.puts(camera)
    :ok
  end

end
