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
  Confirm binary is valid JPEG.
  """
  def validate_frame(binary) do
    case ExImageInfo.info(binary) do
      {"image/jpeg", _, _, _}   -> :ok
      _                         -> :corrupt_frame
    end
  end

end
