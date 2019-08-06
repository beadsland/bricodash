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

defmodule BindSight.Stage.Broadcast do
  use GenStage

  @defaults %{source: :producer_not_specified, name: __MODULE__}

  def start_link(opts \\ []) do
    %{source: source, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, source, name: name)
  end

  def init(source) do
    IO.inspect(source)
    {:producer_consumer, 0, subscribe_to: [source], #[{source, max_demand: 1}], #<----- problem
                              dispatcher: GenStage.BroadcastDispatcher}
  end

  def handle_events(events, _from, count) do
    IO.inspect("#{inspect self()} handle #{count}")
    IO.inspect(events)
    count = count + 1
    {:noreply, events, count}
  end
end
