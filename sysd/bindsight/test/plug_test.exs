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

defmodule PlugTest do
  use ExUnit.Case
  use Plug.Test

  doctest BindSight.WebAPI.Server
  doctest BindSight.WebAPI.Router
  doctest BindSight.WebAPI.Verify
  doctest BindSight.WebAPI.Error
  doctest BindSight.WebAPI.Home

  alias BindSight.WebAPI.Router

  @opts Router.init([])

  test "returns home page" do
    conn = :get |> conn("/", "") |> Router.call(@opts)

    assert conn.state == :sent
    assert conn.status == 200
    assert conn.resp_body =~ "<a href=\"test/snapshot\">snapshot</a>"
    assert conn.resp_body =~ "<a href=\"test/stream\">stream</a>"
  end

  test "returns jpg" do
    conn = :get |> conn("/test/snapshot", "") |> Router.call(@opts)

    assert conn.state == :sent
    assert conn.status == 200
    assert BindSight.validate_frame(conn.resp_body) == :ok
  end

  test "returns I'm a teapot" do
    conn = :get |> conn("/cuppa/snapshot", "") |> Router.call(@opts)

    assert conn.state == :sent
    assert conn.status == 418
  end

  test "returns Bad request" do
    conn = :get |> conn("/test/dance", "") |> Router.call(@opts)

    assert conn.state == :sent
    assert conn.status == 400
  end

  test "returns Not found" do
    conn = :get |> conn("/missing", "") |> Router.call(@opts)

    assert conn.state == :sent
    assert conn.status == 404
  end

end
