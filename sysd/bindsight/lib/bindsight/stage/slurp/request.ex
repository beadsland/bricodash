####
## Copyright © 2019 Beads Land-Trujillo.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
####

defmodule BindSight.Stage.Slurp.Request do
  @moduledoc "Slurp spigot producer to request snapshots from a camera."

  use GenStage
  require Logger

  alias BindSight.Common.Library

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    url = camera |> Library.get_camera_url()
    GenStage.start_link(__MODULE__, url, name: name)
  end

  @impl true
  def init(url) do
    uri = url |> URI.parse()

    query = if uri.query, do: uri.query, else: ""
    query = query |> URI.decode_query(%{:action => :snapshot})
    uri = uri |> Map.put(:query, URI.encode_query(query))

    path = [uri.path, uri.query] |> Enum.join("?")

    scheme = uri.scheme |> String.to_existing_atom()
    parts = {scheme, uri, path}

    {:producer, _state = {parts, connect(parts)}}
  end

  defp connect(parts = {scheme, uri, _path}) do
    case mint_connect(scheme, uri.host, uri.port) do
      {:ok, conn} -> request(conn, parts)
      {:error, err} -> try_again(nil, parts, :connect, err)
    end
  end

  # Try ipv6 by default, but fail-over to ipv4 gracefully.
  defp mint_connect(scheme, host, port) do
    opts = [transport_opts: [{:tcp_module, :inet6_tcp}]]

    case Mint.HTTP.connect(scheme, host, port, opts) do
      {:ok, conn} -> {:ok, conn}
      _ -> Mint.HTTP.connect(scheme, host, port, [])
    end
  end

  defp request(conn, parts = {_scheme, _uri, path}) do
    case Mint.HTTP.request(conn, "GET", path, []) do
      {:ok, conn, _ref} -> conn
      {:error, conn, err} -> try_again(conn, parts, :request, err)
    end
  end

  defp try_again(conn, parts = {_scheme, uri, path}, call, err) do
    Logger.warn(fn ->
      "Failed #{call}: #{uri.host}:#{uri.port}/#{path}: " <> inspect(err)
    end)

    Mint.HTTP.close(conn)
    Process.sleep(1000)
    connect(parts)
  end

  @impl true
  def handle_info(message, state = {parts, conn}) do
    case Mint.HTTP.stream(conn, message) do
      {:ok, conn, resp} ->
        dispatch_responses(resp, _state = {parts, conn})

      :unknown ->
        Logger.error(fn -> "Received unknown message: " <> inspect(message) end)
        {:noreply, [], state}

      {:error, conn, err, resp} ->
        {:noreply, resp,
         _state = {parts, try_again(conn, parts, :response, err)}}
    end
  end

  defp dispatch_responses(resp, _state = {parts, conn}) do
    if Enum.reduce(resp, nil, fn x, accu -> find_done(x, accu) end) do
      Mint.HTTP.close(conn)
      # because snap
      Process.sleep(100)
      {:noreply, resp, _state = {parts, connect(parts)}}
    else
      {:noreply, resp, _state = {parts, conn}}
    end
  end

  defp find_done(x, accu) do
    case x do
      {:done, _ref} -> true
      _ -> accu
    end
  end

  @impl true
  def handle_demand(_demand, state) do
    {:noreply, [], state}
  end
end
