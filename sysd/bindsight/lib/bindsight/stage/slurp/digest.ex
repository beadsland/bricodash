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

  defstruct status: nil,
            boundary: "Lorem ipsum dolor sit amet",
            data: <<>>,
            done: false

  alias BindSight.Stage.Slurp.Digest

  def start_link(opts \\ []) do
    %{source: source, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, source, name: name)
  end

  def init(source) do
    {:producer_consumer, _state = %Digest{}, subscribe_to: [source]}
  end

  def handle_events([head | tail], from, state = %Digest{}) do
    status = state.status

    case head do
      {:status, _ref, status} ->
        handle_events(tail, from, _state = %{state | status: status})

      {:headers, _ref, _hdrs} when status == 200 ->
        handle_events(tail, from, state)

      {:headers, _ref, hdrs} ->
        Logger.warn("Request failed: #{state.status}: " <> inspect(hdrs))
        handle_events(tail, from, state)

      {:data, _ref, next} ->
        handle_events(tail, from, _state = %{state | data: state.data <> next})

      {:done, _ref} ->
        handle_events(tail, from, _state = %{state | done: true})
    end
  end

  def handle_events([], _from, state = %Digest{}) do
    cond do
      state.done and state.status == 200 ->
        {:noreply, [state.data], _state = %Digest{}}

      state.done ->
        {:noreply, [], _state = %Digest{}}

      true ->
        {:noreply, [], state}
    end
  end
end
