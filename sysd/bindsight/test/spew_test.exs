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

defmodule SpewTest do
  @moduledoc "Test GenStage pipeline functionality."

  use ExUnit.Case

  doctest BindSight.Stage.SpewSupervisor
  doctest BindSight.Stage.Spew.Broadcast
  doctest BindSight.Stage.Spew.Spigot

  alias BindSight.Stage.Slurp.Validate
  alias BindSight.Stage.Spew.Spigot
  alias BindSight.Stage.SpewSupervisor

  test "grab snapshot from Spigot" do
    session = SpewSupervisor.start_session()
    subscriptions = [{Spigot.tap(session), max_demand: 1}]
    [data | _] = subscriptions |> GenStage.stream() |> Enum.take(1)

    assert Validate.validate_frame(data) == :ok
  end

  test "grab multiple Spigot snapshots" do
    sessions = 1..3 |> Enum.map(fn _ -> SpewSupervisor.start_session() end)
    subs = sessions |> Enum.map(fn x -> [{Spigot.tap(x), max_demand: 1}] end)
    [data0 | _] = subs |> Enum.at(0) |> GenStage.stream() |> Enum.take(1)
    [data1 | _] = subs |> Enum.at(1) |> GenStage.stream() |> Enum.take(1)
    [data2 | _] = subs |> Enum.at(2) |> GenStage.stream() |> Enum.take(1)

    assert Validate.validate_frame(data0) == :ok
    assert Validate.validate_frame(data1) == :ok
    assert Validate.validate_frame(data2) == :ok
    assert data0 <> data1
    assert data1 <> data2
  end

  @doc """

  test "grab broadcast frame across three clients" do
    subscriptions = [{Spigot.tap(:test), max_demand: 1}]

    t1 =
      Task.async(fn -> subscriptions |> GenStage.stream() |> Enum.take(5) end)

    t2 =
      Task.async(fn -> subscriptions |> GenStage.stream() |> Enum.take(5) end)

    t3 =
      Task.async(fn -> subscriptions |> GenStage.stream() |> Enum.take(5) end)

    data1 = Task.await(t1)
    data2 = Task.await(t2)
    data3 = Task.await(t3)

    assert length(data1 -- data2) < 2
    assert length(data2 -- data3) < 2
  end
  """
end