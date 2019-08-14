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

defmodule BindSight.Stage.Spew.Ripcord do
  @moduledoc "Spew spigot startpoint to serve client and arbitrary number of snoops."

  use GenStage, restart: :temporary

  @defaults %{source: :producer_not_specified, name: __MODULE__}

  def start_link(opts \\ []) do
    %{name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, opts, name: name)
  end

  def init(opts) do
    %{source: source, spigot: spigot} = Enum.into(opts, @defaults)
    dispatch = GenStage.BroadcastDispatcher

    {:producer_consumer, spigot, subscribe_to: [source], dispatcher: dispatch}
  end

  def handle_events(events, _from, spigot) do
    {:noreply, events, spigot}
  end

  def handle_cancel(_reason, _from, spigot) do
    Supervisor.stop(spigot)
    {:stop, :normal, :stateless}
  end
end
