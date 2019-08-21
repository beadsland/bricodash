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

defmodule BindSight.Stage.Slurp.Chunk do
  @moduledoc "Slurp consumer-producer to frames from chunks."

  use GenStage
  require Logger

  @defaults %{source: :producer_not_specified, name: __MODULE__}

  def start_link(opts \\ []) do
    %{source: source, name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, source, name: name)
  end

  def init(source) do
    {:producer_consumer, [], subscribe_to: [source]}
  end

  def handle_events([head | tail], from, rlist) do
    case head do
      {:data, _ref, _data} -> handle_data([head | tail], from, rlist)
      _ -> handle_events(tail, from, [head | rlist])
    end
  end

  def handle_events([], _from, rlist) do
    list = rlist |> Enum.reverse() |> adhere()
    [hold | rlist] = Enum.reverse(list)
    {:noreply, Enum.reverse(rlist), [hold]}
  end

  defp adhere([{:text, ref, x} | [{:text, ref, y} | tail]]),
    do: adhere([{:text, ref, x <> y} | tail])

  defp adhere([{:data, ref, x} | [{:data, ref, y} | tail]]),
    do: adhere([{:data, ref, x <> y} | tail])

  defp adhere([head | tail]), do: [head | adhere(tail)]
  defp adhere([]), do: []

  defp handle_data([{:data, ref, data} | tail], from, rlist) do
    chunks =
      Regex.split(~r/(?=[\r\n\-])/, data)
      |> Enum.map(fn x -> Regex.split(~r/(?<=[\r\n\-])/, x) end)
      |> List.flatten()
      |> Enum.map(fn x ->
        if String.printable?(x), do: {:text, ref, x}, else: {:data, ref, x}
      end)

    handle_events(tail, from, Enum.reverse(chunks) ++ rlist)
  end
end
