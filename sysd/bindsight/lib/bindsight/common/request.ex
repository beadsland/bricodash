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

defmodule BindSight.Common.Request do
  @moduledoc "Slosh spigot producer to request stream from a camera."

  use GenStage
  use BindSight.Common.Tasker

  alias BindSight.Common.Library

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    opts = [url: camera |> Library.get_camera_url()] ++ opts

    GenStage.start_link(__MODULE__, {nil, <<>>}, name: name)
    Tasker.start_task(__MODULE__, opts, name: name)
  end

  def init(_) do
    {:producer, :stateless}
  end

  def perform_task(name, opts) do
    %{url: url} = Enum.into(opts, @defaults)
    uri = url |> URI.parse()
    params = %{"action" => "snapshot"} |> URI.encode_query()
    scheme = uri.scheme |> String.to_existing_atom()
    path = [uri.path, params] |> Enum.join("?")

    do_perform_task(name, {scheme, uri, path})
  end

  defp do_perform_task(name, {scheme, uri, path}) do
    case mint_connect(scheme, uri.host, uri.port) do
      {:ok, conn} ->
        {:ok, conn, _req} = Mint.HTTP.request(conn, "GET", path, [])
        Tasker.sync_notify(name, recv_chunks(conn))

      {:error, err} ->
        Tasker.sync_notify(name, {:error, :mint, err})
        Process.sleep(100)
    end

    do_perform_task(name, {scheme, uri, path})
  end

  # Try ipv6 by default, but fail-over to ipv4 gracefully.
  defp mint_connect(scheme, host, port) do
    opts = [transport_opts: [{:tcp_module, :inet6_tcp}]]

    case Mint.HTTP.connect(scheme, host, port, opts) do
      {:ok, conn} -> {:ok, conn}
      _ -> Mint.HTTP.connect(scheme, host, port, [])
    end
  end

  # Receive messages responding to our request until done.
  defp recv_chunks(conn, status \\ nil, data \\ nil) do
    receive do
      message ->
        {:ok, conn, responses} = Mint.HTTP.stream(conn, message)

        case parse_responses(responses, status, data) do
          {:fail, status, headers} ->
            Mint.HTTP.close(conn)
            {:fail, status, headers}

          {:fail, status} ->
            recv_chunks(conn, status)

          {:ok, status, data} ->
            recv_chunks(conn, status, data)

          {:done, data} ->
            Mint.HTTP.close(conn)
            {:ok, data}
        end
    end
  end

  # Tail recurse over each response list until empty.
  defp parse_responses([], 200, data), do: {:ok, 200, data}
  defp parse_responses([], status, nil), do: {:fail, status}

  defp parse_responses([head | tail], status, data) do
    case head do
      {:status, _ref, status} ->
        parse_responses(tail, status, data)

      {:headers, _ref, headers}
      when status != 200 ->
        {:fail, status, headers}

      {:headers, _ref, _hdrs} ->
        parse_responses(tail, status, <<>>)

      {:data, _ref, next} ->
        # do sync_notify here only....
        parse_responses(tail, status, data <> next)

      {:done, _ref} ->
        {:done, data}
    end
  end

  def handle_call({:notify, event}, _from, :stateless) do
    {:reply, :ok, [event], :stateless}
  end

  def handle_demand(_demand, :stateless) do
    {:noreply, [], :stateless}
  end
end
