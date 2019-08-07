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

  @cameras Application.get_env(:bindsight, :cameras) |> Map.keys()

  plug(BindSight.WebAPI.Verify, cameras: @cameras, actions: [:snapshot])
  plug(:match)
  plug(:dispatch)

  get "/" do
    BindSight.WebAPI.Home.send(conn, cameras: @cameras)
  end

  # Note, cache-control defaults to "max-age=0, private, must-revalidate",
  # per https://hexdocs.pm/plug/Plug.Conn.html -- so we needn't do anything.
  get "/:camera/snapshot" do
    {:ok, frame} =
      camera
      |> String.to_existing_atom()
      |> BindSight.get_camera_url()
      |> BindSight.Snapshot.get_snapshot()

    conn
    |> put_resp_content_type("image/jpg")
    |> send_resp(200, frame)
  end

  match _ do
    send_resp(conn, 404, "Don't take any wooden nickels.")
  end

  defp handle_errors(conn, %{kind: kind, reason: reason, stack: stack}) do
    BindSight.WebAPI.Error.send(conn, kind: kind, reason: reason, stack: stack)
  end
end
