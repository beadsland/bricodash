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

  alias BindSight.Common.Library
  alias BindSight.Common.Snapshot

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    opts = [url: camera |> Library.get_camera_url()] ++ opts

    GenStage.start_link(__MODULE__, [], name: name)
    Tasker.start_task(__MODULE__, opts, name: name)
  end

  def init(_) do
    {:producer, :stateless}
  end

  def perform_task(name, opts) do
    %{url: url} = Enum.into(opts, @defaults)
    do_perform_task(name, url)
  end

  defp do_perform_task(name, url) do
    Process.sleep(100)

    case Snapshot.get_snapshot(url) do
      {:ok, data} -> Tasker.sync_notify(name, data)
      _ -> Process.sleep(60 * 1000)
    end

    do_perform_task(name, url)
  end

  def handle_call({:notify, event}, _from, :stateless) do
    {:reply, :ok, [event], :stateless}
  end

  def handle_demand(_demand, :stateless) do
    {:noreply, [], :stateless}
  end
end
