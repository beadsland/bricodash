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

    receive do
      message ->
        IO.inspect(message, label: :message)
        {:ok, _conn, responses} = Mint.HTTP.stream(conn, message)
        IO.inspect(responses, label: :responses)
    end

    :ok
  end

end
