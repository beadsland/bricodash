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

defmodule BindSightTest do
  @moduledoc "Test basic utility functions used by other modules."

  use ExUnit.Case
  require Logger

  doctest BindSight
  doctest BindSight.Common.Camera
  doctest BindSight.Common.Library
  doctest BindSight.Common.MintJulep
  doctest BindSight.Common.Snapshot
  doctest BindSight.Common.Tasker

  alias BindSight.Common.Library
  alias BindSight.Common.Snapshot
  alias BindSight.Stage.Slurp.Validate

  test "get :test camera path" do
    assert Library.get_camera_url(:test) ==
             "http://rfid-access-building.lan:8080/"
  end

  test "grab a raw snapshot" do
    {:ok, data} = :test |> Library.get_camera_url() |> Snapshot.get_snapshot()

    assert is_binary(data)
  end

  test "validate a snapshot" do
    {:ok, data} = :test |> Library.get_camera_url() |> Snapshot.get_snapshot()

    assert Validate.validate_frame(data) == :ok
  end

  test "grab and validate a request/digest snapshot" do
    [data | _] =
      [:"digest:test"]
      |> GenStage.stream()
      |> Enum.take(1)

    assert Validate.validate_frame(data) == :ok
  end

  test "grab and validate multiple request/digest snapshots" do
    data =
      [:"digest:test"]
      |> GenStage.stream()
      |> Enum.take(3)

    assert Validate.validate_frame(Enum.at(data, 0)) == :ok
    assert Validate.validate_frame(Enum.at(data, 1)) == :ok
    assert Validate.validate_frame(Enum.at(data, 2)) == :ok
  end
end
