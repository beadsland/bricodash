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
  require Logger

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, [camera: camera, name: name], name: name)
  end

  def init(opts) do
    url = opts[:camera] |> BindSight.get_camera_url

    fun = fn -> task_cycle(opts[:name], url) end
    Task.Supervisor.start_child(BindSight.TaskSupervisor, fun,
                                restart: :permanent)

    {:producer, []}
  end

  defp task_cycle(name, url) do
    try do
      Process.register(self(), "#{name}:task" |> String.to_atom)
    rescue
      _ in ArgumentError -> Process.sleep(10)
                            task_cycle(name, url)
    else
      _ -> do_task_cycle(name, url)
    end
  end

  defp do_task_cycle(name, url) do
    Process.sleep(100)
    case BindSight.Snapshot.get_snapshot(url) do
      {:ok, data} -> sync_notify(name, data)
      _           -> Process.sleep(60 * 1000)
    end

    do_task_cycle(name, url)
  end

  def sync_notify(name, event, timeout \\ 5000) do
    try do
      GenStage.call(name, {:notify, event}, timeout)
    catch
      :exit, {:noproc, msg} ->
        if Application.get_env(:bindsight, :ignore_noproc) do
          Logger.log(:debug, "Ignoring noproc race condition on #{name}")
        else
          throw({:exit, {:noproc, msg}})
        end
    end
  end

  def handle_call({:notify, event}, _from, state) do
    {:reply, :ok, [event], state} # Dispatch immediately
  end

  def handle_demand(_demand, state) do
    {:noreply, [], state} # We don't care about the demand
  end

end
