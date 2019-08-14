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

defmodule BindSight.Stage.Spew.Spigot do
  @moduledoc "GenStage pipeline segment for processing a single client request."

  use Supervisor, restart: :temporary

  alias BindSight.Common.Library
  alias BindSight.Stage.Slurp.Spigot

  @defaults %{camera: :test, session: -1}

  def start_link(opts) do
    %{session: session} = Enum.into(opts, @defaults)
    spigot = {:spigot, {:session, session}}
    opts = [spigot: spigot] ++ opts
    Supervisor.start_link(__MODULE__, opts, name: name(spigot))
  end

  @impl true
  def init(opts) do
    %{camera: camera, spigot: spigot} = Enum.into(opts, @defaults)

    children = [
      {BindSight.Stage.Spew.Broadcast,
       [source: Spigot.tap(camera), name: name({:broadcast, spigot})]},
      {BindSight.Stage.Spew.Ripcord,
       [
         source: name({:broadcast, spigot}),
         name: name({:ripcord, spigot}),
         spigot: name(spigot)
       ]}
    ]

    Supervisor.init(children, strategy: :rest_for_one)
  end

  # name(:broadcast, camera)
  def tap(session), do: name({:ripcord, {:spigot, {:session, session}}})

  defp name(tup), do: Library.get_register_name(tup)
end
