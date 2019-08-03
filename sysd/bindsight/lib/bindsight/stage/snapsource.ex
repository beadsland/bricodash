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

defmodule BindSight.Stage.SnapSource do
  use GenStage

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, camera, name: name)
  end

  def init(camera), do: {:producer, camera}

  def handle_demand(_demand, camera) do
    task = Task.async(fn -> handler_task(camera) end)
    data = Task.await(task)
    {:noreply, [data], camera}
  end

  def handler_task(camera) do
    {:ok, data} = camera |> BindSight.get_camera_url
                         |> BindSight.Snapshot.get_snapshot
    data
  end

end
