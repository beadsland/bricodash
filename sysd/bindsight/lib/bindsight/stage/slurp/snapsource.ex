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

defmodule BindSight.Stage.Slurp.SnapSource do
  @moduledoc "Slurp spigot producer to dispatch frames pulled via a task loop."

  use GenStage
  use BindSight.Common.Tasker
  require Logger

  alias BindSight.Common.Tasker

  @defaults %{camera: :test, name: __MODULE__, tasks: BindSight.TaskSupervisor}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    opts = [url: camera |> BindSight.get_camera_url()] ++ opts

    GenStage.start_link(__MODULE__, opts, name: name)
    Tasker.start_task(__MODULE__, opts)
  end

  def init(_opts) do
    {:producer, :stateless}
  end

  def perform_task(opts) do
    %{name: name, url: url} = Enum.into(opts, @defaults)
    Process.sleep(100)

    case BindSight.Snapshot.get_snapshot(url) do
      {:ok, data} -> sync_notify(name, data)
      _ -> Process.sleep(60 * 1000)
    end

    perform_task(opts)
  end

  def sync_notify(name, event, timeout \\ 5000) do
    GenStage.call(name, {:notify, event}, timeout)
  catch
    :exit, {:noproc, msg} ->
      if Application.get_env(:bindsight, :ignore_noproc) do
        Logger.log(:debug, "Ignoring noproc race condition on #{name}")
      else
        throw({:exit, {:noproc, msg}})
      end
  end

  def handle_call({:notify, event}, _from, :stateless) do
    # Dispatch immediately
    {:reply, :ok, [event], :stateless}
  end

  def handle_demand(_demand, :stateless) do
    # We don't care about the demand
    {:noreply, [], :stateless}
  end
end
