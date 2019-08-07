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

defmodule BindSight.Stage.Slurp.Spigot do
  @moduledoc "GenStage pipeline segment for processing a single camera feed."

  use Supervisor

  def start_link(camera \\ :test) do
    name = "spigot:#{camera}" |> String.to_atom()
    Supervisor.start_link(__MODULE__, camera, name: name)
  end

  @impl true
  def init(camera) do
    children = [
      {BindSight.Stage.Slurp.SnapSource, [camera: camera, name: name(:snapsource, camera)]},
      {BindSight.Stage.Slurp.Batch,
       [source: name(:snapsource, camera), camera: camera, name: name(:batch, camera)]},
      {BindSight.Stage.Slurp.Validate,
       [source: {name(:batch, camera), max_demand: 2}, name: name(:validate, camera)]},
      {BindSight.Stage.Slurp.Broadcast,
       [source: name(:validate, camera), name: name(:broadcast, camera)]}
    ]

    Supervisor.init(children, strategy: :rest_for_one)
  end

  def tap(camera), do: name(:broadcast, camera)

  defp name(mod, cam), do: "#{mod}:#{cam}" |> String.to_atom()
end
