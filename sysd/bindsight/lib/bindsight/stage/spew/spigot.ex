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

  use Supervisor

  alias BindSight.Common.Library
  alias BindSight.Stage.Slurp.Spigot

  @defaults %{camera: :test, clientid: :this_ought_to_be_unique}

  def start_link(opts) do
    %{camera: camera, clientid: clientid} = Enum.into(opts, @defaults)

    Supervisor.start_link(__MODULE__, camera,
      name: name(:spigot, "#{camera}:#{clientid}")
    )
  end

  @impl true
  def init(_camera) do
    children = []

    Supervisor.init(children, strategy: :one_for_one)
  end

  # name(:broadcast, camera)
  def tap(camera, _clientid), do: Spigot.tap(camera)

  defp name(mod, cam), do: Library.get_register_name(mod, cam)
end
