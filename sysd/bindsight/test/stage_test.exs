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
  use ExUnit.Case

  test "grab snapshot from SnapSource" do
    {:ok, _pid, name} = BindSight.Stage.SnapSource.start_link(:test)
    subscriptions = [{name, max_demand: 1}]
    [data | _] = subscriptions |> GenStage.stream |> Enum.take(1)

    assert BindSight.validate_frame(data) == :ok
  end
end
