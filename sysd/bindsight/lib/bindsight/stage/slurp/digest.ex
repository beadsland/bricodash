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
            bound: "Lorem ipsum dolor sit amet",
            data: <<>>,
            done: false,
            frame: <<>>

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

      {:headers, _ref, hdrs} when status == 200 ->
        handle_headers(hdrs, tail, from, state)

      {:headers, _ref, hdrs} ->
        Logger.warn("Request failed: #{state.status}: " <> inspect(hdrs))
        handle_events(tail, from, state)

      {:data, _ref, next} ->
        handle_data(next, tail, from, state)

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

      state.frame == "" ->
        {:noreply, [], _state = %Digest{state | frame: nil}}

      state.frame ->
        {:noreply, [state.frame], _state = %Digest{state | frame: nil}}

      true ->
        {:noreply, [], state}
    end
  end

  def handle_headers([], events, from, state),
    do: handle_events(events, from, state)

  def handle_headers([{"content-type", ctype} | tail], events, from, state) do
    bound = Regex.named_captures(~r/;boundary=(?<bound>.*)/, ctype)["bound"]

    bound =
      "^(?<frame>.*)--#{bound}([\x0d\x0a]{1,2}[[:print:]]+)+[\x0d\x0a]{1,2}[\x0d\x0a]{1,2}(?<data>.*)\z"

    {:ok, bound} = Regex.compile(bound, "ms")
    handle_headers(tail, events, from, _state = %Digest{state | bound: bound})
  end

  def handle_headers([_head | tail], events, from, state),
    do: handle_headers(tail, events, from, state)

  def handle_data(next, events, from, state) do
    data = state.data <> next
    match = Regex.named_captures(state.bound, data)

    #    if match, do: IO.inspect(match)

    if match do
      handle_events(events, from, %Digest{
        state
        | data: match["data"],
          frame: match["frame"]
      })
    else
      handle_events(events, from, %Digest{state | data: data})
    end
  end
end
