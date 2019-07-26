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

defmodule Relay do
  @moduledoc """
  Service to relay MJPEG camera streams to one or more clients as streams or
  snapshots. Proactively checks for corrupt frames and drops them before
  forwarding to clients.
  """

  @doc """
  Retrieve camera URL by name from config.
  """
  def get_camera(name) do
    cameras = Application.fetch_env!(:relay, :cameras)
    cameras[name]
  end

  @doc """
  Obtain snapshot JPEG from camera by name.
  """
  def get_snapshot(name) do
    uri = URI.parse( get_camera(name) )
    params = URI.encode_query( %{"action" => "snapshot"} )

    scheme = String.to_existing_atom( uri.scheme )
    path = Enum.join( [uri.path, params], "?" )

    {:ok, conn} = Mint.HTTP.connect(scheme, uri.host, uri.port)
    {:ok, conn, _request_ref} = Mint.HTTP.request(conn, "GET", path, [])

    recv_snapshot(conn)
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

  @doc """
  Obtain snapshot JPEG from camera by name, and confirm that it is valid.
  """
  def get_valid_snapshot(name) do
    snapshot = get_snapshot(name)
    case snapshot do
      {:fail, _, _} -> snapshot
      {:ok, data}   -> case ExImageInfo.info(data) do
                         {"image/jpeg", _, _, _} -> snapshot
                        _                        -> {:fail, :corrupt_frame}
                       end
    end
  end

end
