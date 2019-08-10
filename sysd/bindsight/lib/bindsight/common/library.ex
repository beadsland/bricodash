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

defmodule BindSight.Common.Library do
  @moduledoc "Commonly used functions are functions used commonly."

  @doc "Retrieve camera URL by name from config."
  def get_camera_url(name) do
    cameras = Application.fetch_env!(:bindsight, :cameras)
    cameras[name]
  end

  @doc "Return unique registerable name for process, shortname if dev/test."
  def get_register_name(mod, cam) do
    if Application.get_env(:bindsight, :register_shortnames, false) do
      "#{mod}:#{cam}" |> String.to_atom()
    else
      "bindsight_#{mod}:#{cam}" |> String.to_atom()
    end
  end
end
