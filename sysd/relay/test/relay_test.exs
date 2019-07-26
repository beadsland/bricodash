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

defmodule RelayTest do
  use ExUnit.Case
  doctest Relay
  doctest Relay.Snapshot

  test "get :test camera path" do
    assert Relay.get_camera(:test) == "http://192.168.42.22:8080/"
  end

  test "grab a snapshot" do
    {:ok, data} = Relay.Snapshot.get_snapshot( Relay.get_camera(:test) )
    assert is_binary(data)
  end

  test "validate a snapshot" do
    {:ok, data} = Relay.Snapshot.get_valid_snapshot( Relay.get_camera(:test) )
    assert is_binary(data)
  end

end
