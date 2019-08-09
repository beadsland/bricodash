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

defmodule BindSight.Common.Tasker do
  @moduledoc "Behavior for GenStage to launch a dedicated feeder task."

  defmacro __using__(_) do
    quote location: :keep do
      @behaviour BindSight.Common.Tasker
    end
  end

  @callback perform_task(opts :: [key: term]) :: term

  @defaults %{
    name: :need_a_unique_name,
    tasks: BindSight.TaskSupervisor,
    restart: :permanent,
  }

  def start_task(mod, opts) do
    %{tasks: tasks, restart: restart} = Enum.into(opts, @defaults)
    fun = fn -> launch_task(mod, opts) end
    Task.Supervisor.start_child(tasks, fun, restart: restart)
  end

  defp launch_task(mod, opts) do
    %{name: name} = Enum.into(opts, @defaults)
    register_task(name)
    mod.perform_task(opts)
  end

  defp register_task(name) do
    Process.register(self(), "#{name}:task" |> String.to_atom())
  rescue
    _ in ArgumentError ->
      Process.sleep(10)
      register_task(name)
  end

end
