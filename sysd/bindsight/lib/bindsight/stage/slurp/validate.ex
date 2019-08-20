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
  @moduledoc """
  Slurp spigot consumer-producer to check for corrupt and greytoss frames.
  """

  use GenStage
  require Logger

  @defaults %{source: :producer_not_specified, camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{name: name} = Enum.into(opts, @defaults)
    GenStage.start_link(__MODULE__, opts, name: name)
  end

  def init(opts) do
    %{source: source, camera: camera} = Enum.into(opts, @defaults)
    {:producer_consumer, camera, subscribe_to: [source]}
  end

  def handle_events([{:batch, batch}], from, camera) do
    handle_events(batch, from, camera)
  end

  def handle_events(events, _from, camera) do
    fun = fn x -> validate_frame(x) == :ok end
    checks = events |> Task.async_stream(fun) |> Enum.map(fn {:ok, x} -> x end)

    good =
      events
      |> Enum.zip(checks)
      |> Enum.map(fn {evt, chk} -> if chk, do: evt end)
      |> Enum.filter(fn x -> x != nil end)

    discard = length(events) - length(good)

    if discard > 0 do
      Logger.warn("Discarding #{discard} bad frames from #{camera}")
    end

    {:noreply, good, camera}
  end

  @doc "Confirm binary is valid JPEG."
  def validate_frame(binary) do
    case ExImageInfo.info(binary) do
      {"image/jpeg", _, _, _} -> :ok
      _ -> :corrupt_frame
    end
  end
end
