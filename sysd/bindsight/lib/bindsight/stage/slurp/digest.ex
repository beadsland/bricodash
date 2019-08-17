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

defmodule BindSight.Stage.Slurp.Digest do
  @moduledoc "Slurp consumer-producer to frames from chunks."

  use GenStage
  require Logger

  @defaults %{source: :producer_not_specified, name: __MODULE__}

  def start_link(opts \\ []) do
    %{source: source, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, source, name: name)
  end

  def init(source) do
    {:producer_consumer, _state = {nil, <<>>, false}, subscribe_to: [source]}
  end

  def handle_events([head | tail], from, state = {status, data, _done}) do
    case head do
      {:status, _ref, status} ->
        handle_events(tail, from, _state = {status, data, false})

      {:headers, _ref, _hdrs} when status == 200 ->
        handle_events(tail, from, state)

      {:headers, _ref, hdrs} ->
        Logger.warn("Request failed: #{status}: " <> inspect(hdrs))
        handle_events(tail, from, state)

      {:data, _ref, next} ->
        handle_events(tail, from, _state = {status, data <> next, false})

      {:done, _ref} ->
        handle_events(tail, from, _state = {status, data, true})
    end
  end

  def handle_events([], _from, state = {status, data, done}) do
    cond do
      done and status == 200 -> {:noreply, [data], _state = {nil, <<>>, false}}
      done -> {:noreply, [], _state = {nil, <<>>, false}}
      true -> {:noreply, [], state}
    end
  end
end
