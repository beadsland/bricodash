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
            boundsize: nil,
            eolex: nil,
            eohex: nil,
            data: [],
            done: false,
            frames: []

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
    boundsize = state.boundsize

    case head do
      {:status, _ref, status} ->
        handle_events(tail, from, _state = %{state | status: status})

      {:headers, _ref, hdrs} when status == 200 ->
        handle_headers(hdrs, tail, from, state)

      {:headers, _ref, hdrs} ->
        Logger.warn("Request failed: #{state.status}: " <> inspect(hdrs))
        handle_events(tail, from, state)

      {:frame_headers, _ref, _hdrs} ->
        frame = state.data |> Enum.reverse() |> Enum.join()
        frames = if frame == "", do: state.frames, else: [frame | state.frames]

        handle_events(tail, from, _state = %{state | frames: frames, data: []})

      {:text, _ref, text} when byte_size(text) > boundsize ->
        handle_text([head | tail], from, state)

      {:text, ref, text} ->
        handle_events([{:data, ref, text} | tail], from, state)

      {:data, _ref, ""} ->
        handle_events(tail, from, state)

      {:data, _ref, data} ->
        handle_events(tail, from, _state = %{state | data: [data | state.data]})

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

      state.frames ->
        {:noreply, Enum.reverse(state.frames),
         _state = %Digest{state | frames: []}}

      true ->
        {:noreply, [], state}
    end
  end

  defp handle_headers([], events, from, state),
    do: handle_events(events, from, state)

  defp handle_headers([{"content-type", ctype} | tail], events, from, state) do
    bound =
      "--" <> Regex.named_captures(~r/;boundary=(?<bound>.*)/, ctype)["bound"]

    boundsize = byte_size(bound)
    state = %Digest{state | bound: bound, boundsize: boundsize}

    handle_headers(tail, events, from, state)
  end

  defp handle_headers([_head | tail], events, from, state),
    do: handle_headers(tail, events, from, state)

  defp handle_text([head = {:text, ref, text} | tail], from, state) do
    if String.contains?(text, state.bound) do
      strip_boundary(head, tail, from, state)
    else
      handle_events([{:data, ref, text} | tail], from, state)
    end
  end

  defp strip_boundary({:text, ref, text}, tail, from, state) do
    [pre, post] = String.split(text, state.bound, parts: 2)

    state = if state.eohex == nil, do: determine_eol(text, state), else: state

    [headers, post] = Regex.split(state.eohex, post, parts: 2)

    events =
      [{:data, ref, pre}, {:frame_headers, ref, headers}, {:data, ref, post}] ++
        tail

    handle_events(events, from, state)
  end

  defp determine_eol(text, state) do
    [eol] = Regex.run(~r/[\n\r]+/, text, parts: 1)
    {:ok, eolex} = Regex.compile(eol)
    {:ok, eohex} = Regex.compile(eol <> eol)
    %Digest{state | eolex: eolex, eohex: eohex}
  end
end
