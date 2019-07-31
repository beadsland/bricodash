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

defmodule Relay.WebAPI.Router do
  use Plug.Router
  use Plug.ErrorHandler

  plug :match
  plug :dispatch

  get "/" do
    send_resp(conn, 200, "Howdy!")
  end

  get "/test/snapshot" do
    {:ok, frame} = Relay.Snapshot.get_snapshot( Relay.get_camera_url(:test) )
    conn
      |> put_resp_content_type("image/jpg")
      |> send_resp(200, frame)
  end

  match _ do
    send_resp(conn, 404, "Don't take any wooden nickels.")
  end

  defp handle_errors(conn, %{kind: kind, reason: reason, stack: stack}) do
    IO.inspect(kind, label: :kind)
    IO.inspect(reason, label: :reason)
    IO.inspect(stack, label: :stack)
    send_resp(conn, conn.status, "Ditty's gone catawampous, it has.")
  end

end
