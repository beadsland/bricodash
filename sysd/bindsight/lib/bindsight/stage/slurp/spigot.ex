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

  alias BindSight.Common.Library

  def start_link(camera \\ :test) do
    Supervisor.start_link(__MODULE__, camera,
      name: name({:spigot, :slurp, camera})
    )
  end

  @impl true
  def init(camera) do
    children = [
      {Task.Supervisor,
       name: name({:tasks, :slurp, camera}), strategy: :one_for_one},
      {BindSight.Stage.Slurp.Request,
       [
         camera: camera,
         name: name({:request, camera})
       ]},
      {BindSight.Stage.Slurp.Chunk,
       [
         source: name({:request, camera}),
         name: name({:chunk, camera})
       ]},
      {BindSight.Stage.Slurp.Digest,
       [
         source: name({:chunk, camera}),
         name: name({:digest, camera})
       ]},
      {BindSight.Stage.Slurp.SnapSource,
       [
         camera: camera,
         name: name({:snapsource, camera}),
         tasks: name({:tasks, :slurp, camera})
       ]},
      {BindSight.Stage.Slurp.Batch,
       [
         source: name({:snapsource, camera}),
         camera: camera,
         name: name({:batch, camera}),
         tasks: name({:tasks, :slurp, camera})
       ]},
      {BindSight.Stage.Slurp.Validate,
       [
         source: {name({:batch, camera}), max_demand: 2},
         camera: camera,
         name: name({:validate, camera})
       ]},
      {BindSight.Stage.Slurp.Broadcast,
       [source: name({:validate, camera}), name: name({:broadcast, camera})]},
      {BindSight.Stage.SnoopSupervisor,
       [
         source: name({:broadcast, camera}),
         camera: camera,
         name: name({:snoops, camera}),
         always: [BindSight.Stage.Slurp.FlushSnoop],
         config: :slurp_snoops
       ]}
    ]

    Supervisor.init(children, strategy: :rest_for_one)
  end

  def tap(camera), do: name({:broadcast, camera})

  defp name(tup), do: Library.get_register_name(tup)
end
