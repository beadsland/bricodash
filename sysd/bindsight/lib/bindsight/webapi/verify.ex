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
  @moduledoc "Plug to check syntax and terms of WebAPI requests."

  import Plug.Conn

  def init(options), do: options

  def call(%Plug.Conn{request_path: path} = conn, opts) do
    components = path |> String.trim("/") |> String.split("/")
                      |> Enum.map(fn x -> atomize(x) end)

    verify_request(conn, opts[:cameras], opts[:actions], components)
  end

  defp atomize(s) do
    try do
      String.to_existing_atom(s)
    rescue
      _ in ArgumentError -> nil
    end
  end

  defp verify_request(conn, _, _, comps) when length(comps) != 2, do: conn

  defp verify_request(conn, cameras, actions, [cam, act]) do
    cond do
      cam not in cameras ->
        conn |> send_resp(418, "That dog won't hunt (unknown camera).") |> halt
      act not in actions ->
        conn |> send_resp(400, "All down but nine (unknown action).") |> halt
      true ->
        conn
    end

  end

end
