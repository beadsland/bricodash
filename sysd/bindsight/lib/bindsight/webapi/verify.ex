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

defmodule BindSight.WebAPI.Verify do
  import Plug.Conn

  def init(options), do: options

  def call(%Plug.Conn{request_path: path} = conn, opts) do
    components = path |> String.trim("/") |> String.split("/")
                      |> Enum.map(fn x -> atomize(x) end)

    if length(components) == 2 do
      verify_request(conn, opts[:cameras], opts[:actions], components)
    else
      conn
    end
  end

  defp atomize(s) do
    try do
      String.to_existing_atom(s)
    rescue
      _ in ArgumentError -> nil
    end
  end

  defp verify_request(conn, _cameras, _actions, components) do #[_cam, _act]) do
    if Enum.member?(components, nil) do
      conn |> send_resp(418, "That dog won't hunt (unknown camera).") |> halt
    else
      conn
    end
  end

end
