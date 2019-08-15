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

defmodule BindSight.WebAPI.Router do
  @moduledoc "Router for BindSight WebAPI."

  use Plug.Router
  use Plug.ErrorHandler

  alias BindSight.Common.Library
  alias BindSight.WebAPI.Error
  alias BindSight.WebAPI.Frames
  alias BindSight.WebAPI.Home

  @cameras Library.get_env(:cameras) |> Map.keys()

  plug(BindSight.WebAPI.Verify, cameras: @cameras, actions: [:snapshot, :stream])

  plug(:match)
  plug(:dispatch)

  get "/" do
    Home.send(conn, cameras: @cameras)
  end

  get "/:camera/snapshot" do
    Frames.send(aggressive_nocache(conn), camera: camera, action: :snapshot)
  end

  get "/:camera/stream" do
    Frames.send(aggressive_nocache(conn), camera: camera, action: :stream)
  end

  match _ do
    send_resp(conn, 404, "Don't take any wooden nickels.")
  end

  defp handle_errors(conn, %{kind: kind, reason: reason, stack: stack}) do
    Error.send(conn, kind: kind, reason: reason, stack: stack)
  end

  # Note, cache-control defaults to "max-age=0, private, must-revalidate",
  # per https://hexdocs.pm/plug/Plug.Conn.html
  # But we want to be sure older, non-compliant browsers behave themselves.
  defp aggressive_nocache(conn) do
    cache =
      "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0"

    conn
    |> put_resp_header("cache-control", cache)
    |> put_resp_header("expires", "Thu, 9 Sep 1999 0:0:00 GMT")
    |> put_resp_header("pragma", "no-cache")
  end
end
