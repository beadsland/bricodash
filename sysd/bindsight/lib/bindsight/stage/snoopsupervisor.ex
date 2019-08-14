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

defmodule BindSight.Stage.SnoopSupervisor do
  @moduledoc "Supervise configured snoops on either slurp or spew spigot."

  use Supervisor

  alias BindSight.Common.Library

  @defaults %{source: :producer_not_specified, name: __MODULE__, always: []}

  def start_link(opts) do
    %{name: name} = Enum.into(opts, @defaults)
    Supervisor.start_link(__MODULE__, opts, name: name)
  end

  @impl true
  def init(opts) do
    %{always: always, config: config} = Enum.into(opts, @defaults)

    children =
      (always ++ Library.get_env(config, []))
      |> Enum.map(fn x -> speccer(x, opts) end)

    Supervisor.init(children, strategy: :one_for_one)
  end

  defp speccer(snoop, opts) do
    Supervisor.child_spec({snoop, opts}, [])
  end
end
