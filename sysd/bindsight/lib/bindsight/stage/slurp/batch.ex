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

defmodule BindSight.Stage.Slurp.Batch do
  @moduledoc "Consumer-producer to render events in batches. Assumes max_demand = 2."

  use GenStage
  require Logger

  @defaults %{source: :producer_not_specified, camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, opts, name: name)
  end

  def init(opts) do
    %{camera: camera} = Enum.into(opts, @defaults)

    visor = BindSight.TaskSupervisor
    fun = fn -> task_cycle(opts) end
    Task.Supervisor.start_child(visor, fun, restart: :permanent)

    # , subscribe_to: [source]}
    {:producer, {camera, Okasaki.Queue.new(), 0}}
  end

  defp task_cycle(opts) do
    %{name: name} = Enum.into(opts, @defaults)
    Process.register(self(), "#{name}:task" |> String.to_atom())
  rescue
    _ in ArgumentError ->
      Process.sleep(10)
      task_cycle(opts)
  else
    _ -> do_task_cycle(opts)
  end

  defp do_task_cycle(opts) do
    %{source: source, name: name} = Enum.into(opts, @defaults)
    [source] |> GenStage.stream() |> Enum.map(fn x -> sync_notify(name, x) end)
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

  def handle_call({:notify, event}, _from, {camera, queue, pending}) do
    queue = Okasaki.Queue.insert(queue, event)
    handle_demand(0, {camera, queue, pending})
  end

  def handle_demand(demand, {camera, queue, pending}) do
    demand = demand + pending
    onhold = Okasaki.Queue.size(queue)

    cond do
      demand == 0 ->
        {:noreply, [], {camera, queue, demand}}

      onhold == 0 ->
        {:noreply, [], {camera, queue, demand}}

      true ->
        size = min(demand, onhold)
        {batch, queue} = assemble_batch(queue, size, [])
        Logger.info("Batch of #{size} frames dispatched from #{camera}.")
        {:reply, :ok, [{:batch, batch}], {camera, queue, demand - size}}
    end
  end

  defp assemble_batch(queue, 0, batch), do: {Enum.reverse(batch), queue}

  defp assemble_batch(queue, size, batch) do
    {:ok, {item, queue}} = Okasaki.Queue.remove(queue)
    assemble_batch(queue, size - 1, [item | batch])
  end
end
