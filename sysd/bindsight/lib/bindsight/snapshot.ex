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

defmodule BindSight.Snapshot do
  @doc """
  Obtain snapshot JPEG from camera by name.
  """
  def snap(url), do: get_snapshot(url)

  # Make request for snapshot and begin reading incoming stream.
  def get_snapshot(url) do
    uri = URI.parse( url )
    params = URI.encode_query( %{"action" => "snapshot"} )
    scheme = String.to_existing_atom( uri.scheme )
    path = Enum.join( [uri.path, params], "?" )

    case mint_connect(scheme, uri.host, uri.port) do
      {:ok, conn} ->
          {:ok, conn, _req} = Mint.HTTP.request(conn, "GET", path, [])
          recv_snapshot(conn)
      {:error, err} ->
          {:fail, :mint, err}
    end
  end

  # Try ipv6 by default, but fail-over to ipv4 gracefully.
  defp mint_connect(scheme, host, port) do
    opts = [transport_opts: [{:tcp_module, :inet6_tcp}]]

    case Mint.HTTP.connect(scheme, host, port, opts) do
      {:ok, conn} -> {:ok, conn}
      _           -> Mint.HTTP.connect(scheme, host, port, [])
    end
  end

  # Receive messages responding to our request until done.
  defp recv_snapshot(conn, status \\ nil, data \\ nil) do
    receive do
      message ->
        {:ok, conn, responses} = Mint.HTTP.stream(conn, message)

        case parse_responses(responses, status, data) do
          {:fail, status, headers}  -> Mint.HTTP.close(conn)
                                       {:fail, status, headers}
          {:fail, status}           -> recv_snapshot(conn, status)
          {:ok, status, data}       -> recv_snapshot(conn, status, data)
          {:done, data}             -> Mint.HTTP.close(conn)
                                       {:ok, data}
        end
    end
  end

  # Tail recurse over each response list until empty.
  defp parse_responses([], 200, data), do:    {:ok, 200, data}
  defp parse_responses([], status, nil), do:  {:fail, status}

  defp parse_responses([head | tail], status, data) do
    case head do
      {:status, _ref, status}  -> parse_responses(tail, status, data)
      {:headers, _ref, headers}
          when status != 200   -> {:fail, status, headers}
      {:headers, _ref, _hdrs}  -> parse_responses(tail, status, <<>>)
      {:data, _ref, next}      -> parse_responses(tail, status, data <> next)
      {:done, _ref}            -> {:done, data}
    end
  end

end
