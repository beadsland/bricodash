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
  Assemble camera URL.
  """

  def get_camera(name) do
    cameras = Application.fetch_env!(:relay, :cameras)
    IO.inspect(cameras)
    cameras[name]
  end

  def poke_camera do
    camera = "http://rfid-access-building.lan:8080/"
    params = %{"action" => "stream"}
    camera = URI.parse(camera) |> Map.put(:query, URI.encode_query(params))
      |> URI.to_string()
    IO.puts(camera)
    :ok
  end

end
