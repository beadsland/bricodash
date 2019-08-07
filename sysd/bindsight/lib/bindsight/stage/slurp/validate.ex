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

defmodule BindSight.Stage.Slurp.Validate do
  use GenStage
  require Logger

  @defaults %{source: :producer_not_specified, name: __MODULE__}

  def start_link(opts \\ []) do
    %{source: source, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, source, name: name)
  end

  def init(source) do
    {:producer_consumer, 0, subscribe_to: [source]}
  end

  def handle_events(events, _from, count) do
    fun = fn x -> BindSight.validate_frame(x) == :ok end
    checks = events |> Task.async_stream(fun) |> Enum.map(fn({:ok, x}) -> x end)

    good = events |> Enum.zip(checks)
                  |> Enum.map(fn {evt, chk} -> if chk, do: evt end)
                  |> Enum.filter(fn x -> x != nil end)

    discard = length(events) - length(good)
    if discard > 0, do: Logger.warn("Discarding #{discard} bad frames")

    {:noreply, good, count}
  end


end
