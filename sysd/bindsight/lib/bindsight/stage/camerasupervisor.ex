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

defmodule BindSight.Stage.CameraSupervisor do
  @moduledoc "Supervise slurp spigot (camera pipeline segment) for each camera."

  use Supervisor

  def start_link(_opts) do
    Supervisor.start_link(__MODULE__, nil, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    children =
      Application.get_env(:bindsight, :cameras)
      |> Map.keys()
      |> Enum.map(fn x -> speccer(x) end)

    Supervisor.init(children, strategy: :one_for_one)
  end

  defp speccer(camera) do
    Supervisor.child_spec({BindSight.Stage.Slurp.Spigot, camera}, id: camera)
  end
end
