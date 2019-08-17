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
  alias BindSight.Common.MintJulep

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    url = camera |> Library.get_camera_url()
    GenStage.start_link(__MODULE__, url, name: name)
  end

  @impl true
  def init(url) do
    uri = url |> URI.parse() |> query_put(:action, :snapshot)
    {:producer, _state = MintJulep.sip(uri)}
  end

  defp query_put(uri, key, value) do
    query = if uri.query, do: uri.query, else: ""
    query = query |> URI.decode_query(%{key => value})
    uri |> Map.put(:query, URI.encode_query(query))
  end

  @impl true
  def handle_info(message, state = {uri, conn}) do
    case Mint.HTTP.stream(conn, message) do
      {:ok, conn, resp} ->
        dispatch_responses(resp, _state = {uri, conn})

      :unknown ->
        Logger.error(fn -> "Received unknown message: " <> inspect(message) end)
        {:noreply, [], state}

      {:error, conn, err, resp} ->
        {:noreply, resp, _state = MintJulep.sip(uri, conn, :response, err)}
    end
  end

  defp dispatch_responses(resp, state = {uri, conn}) do
    if Enum.reduce(resp, nil, fn x, accu -> find_done(x, accu) end) do
      # because snap
      Process.sleep(100)
      {:noreply, resp, _state = MintJulep.sip(uri, conn)}
    else
      {:noreply, resp, state}
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
