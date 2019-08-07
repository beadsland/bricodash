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

defmodule StageTest do
  @moduledoc "Test GenStage pipeline functionality."
  
  use ExUnit.Case

  doctest BindSight.Stage.Slurp.SnapSource
  doctest BindSight.Stage.Slurp.Validate
  doctest BindSight.Stage.Slurp.Broadcast
  doctest BindSight.Stage.Slurp.Spigot

  test "grab snapshot from SnapSource" do
    {:ok, _pid} = BindSight.Stage.Slurp.SnapSource.start_link(camera: :test)
    subscriptions = [{BindSight.Stage.Slurp.SnapSource, max_demand: 1}]
    [data | _] = subscriptions |> GenStage.stream |> Enum.take(1)

    assert is_binary(data)
  end

  test "grab snapshot from Spigot" do
    subscriptions = [{BindSight.Stage.Slurp.Spigot.tap(:test), max_demand: 1}]
    [data | _] = subscriptions |> GenStage.stream |> Enum.take(1)

    assert BindSight.validate_frame(data) == :ok
  end

  test "grab multiple snapshots from Spigot" do
    subscriptions = [{BindSight.Stage.Slurp.Spigot.tap(:test), max_demand: 10}]
    result = subscriptions |> GenStage.stream |> Enum.take(10)
              |> Enum.map(fn x -> BindSight.validate_frame(x) end)

    assert result == List.duplicate(:ok, 10)
  end

  test "grab broadcast frame across three clients" do
    subscriptions = [{BindSight.Stage.Slurp.Spigot.tap(:test), max_demand: 1}]
    t1 = Task.async(fn -> subscriptions |> GenStage.stream |> Enum.take(5) end)
    t2 = Task.async(fn -> subscriptions |> GenStage.stream |> Enum.take(5) end)
    t3 = Task.async(fn -> subscriptions |> GenStage.stream |> Enum.take(5) end)
    data1 = Task.await t1
    data2 = Task.await t2
    data3 = Task.await t3

    assert length(data1 -- data2) < 2
    assert length(data2 -- data3) < 2
  end

end
