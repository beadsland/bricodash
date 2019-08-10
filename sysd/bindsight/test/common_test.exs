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

  doctest BindSight
  doctest BindSight.Common.Snapshot
  doctest BindSight.Common.Tasker

  alias BindSight.Common.Snapshot

  test "get :test camera path" do
    assert BindSight.get_camera_url(:test) ==
             "http://rfid-access-building.lan:8080/"
  end

  test "grab a raw snapshot" do
    {:ok, data} = :test |> BindSight.get_camera_url() |> Snapshot.get_snapshot()

    assert is_binary(data)
  end

  test "validate a snapshot" do
    {:ok, data} = :test |> BindSight.get_camera_url() |> Snapshot.get_snapshot()

    assert BindSight.validate_frame(data) == :ok
  end
end
