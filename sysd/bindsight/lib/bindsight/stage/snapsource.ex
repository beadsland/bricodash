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
    GenStage.start_link(__MODULE__, [camera: camera, name: name], name: name)
  end

  def init(opts) do
    url = opts[:camera] |> BindSight.get_camera_url

    Task.Supervisor.start_child(BindSight.TaskSupervisor, fn ->
      task_cycle(opts[:name], url)
    end, name: "#{opts[:name]}:task" |> String.to_atom, restart: :permanent)

    {:producer, []}
  end

  def task_cycle(name, url) do
    Process.sleep(100)
    {:ok, data} = url |> BindSight.Snapshot.get_snapshot
    sync_notify(name, data)
    task_cycle(name, url)
  end

  def sync_notify(name, event, timeout \\ 5000) do
    GenStage.call(name, {:notify, event}, timeout)
  end

  def handle_call({:notify, event}, _from, state) do
    {:reply, :ok, [event], state} # Dispatch immediately
  end

  def handle_demand(_demand, state) do
    {:noreply, [], state} # We don't care about the demand
  end

end
