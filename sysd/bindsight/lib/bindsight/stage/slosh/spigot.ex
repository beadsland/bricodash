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

defmodule BindSight.Stage.Slosh.Spigot do
  @moduledoc "GenStage pipeline segment for processing a single camera feed."

  use Supervisor

  alias BindSight.Common.Library

  @defaults %{camera: :test, url: nil}

  def start_link(opts \\ []) do
    %{camera: camera} = Enum.into(opts, @defaults)

    Supervisor.start_link(__MODULE__, opts,
      name: name({:spigot, :slosh, camera})
    )
  end

  @impl true
  def init(opts) do
    %{camera: camera, url: url} = Enum.into(opts, @defaults)

    children = [
      {BindSight.Stage.Slosh.Request,
       [
         camera: camera,
         url: url,
         name: name({:request, camera})
       ]},
      {BindSight.Stage.Slosh.Chunk,
       [
         source: name({:request, camera}),
         name: name({:chunk, camera})
       ]},
      {BindSight.Stage.Slosh.Digest,
       [
         source: name({:chunk, camera}),
         name: name({:digest, camera})
       ]}
    ]

    Supervisor.init(children, strategy: :rest_for_one)
  end

  def tap(camera), do: name({:digest, camera})

  defp name(tup), do: Library.get_register_name(tup)
end
