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
  defmodule BadDogError do
    defexception message: "That dog won't hunt (unknown camera).", type: :unknown_camera, plug_status: 404
  end

  def init(options), do: options

  def call(%Plug.Conn{request_path: path} = conn, opts) do
    try do
      components = path |> String.trim("/") |> String.split("/")
        |> Enum.map(fn x -> String.to_existing_atom(x) end)

      if length(components) == 2 do
        verify_request!(opts[:cameras], opts[:actions], components)
      end
      conn
    rescue
      _ -> raise(BadDogError)
    end
  end

  defp verify_request!(_cameras, _actions, [_cam, _act]) do
    nil # we can test for correct syntax on later iteration
  end

end
