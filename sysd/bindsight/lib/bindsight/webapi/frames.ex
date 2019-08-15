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

defmodule BindSight.WebAPI.Frames do
  @moduledoc "Plug to deliver snapshots and streams to client."

  import Plug.Conn

  alias BindSight.Stage.Spew.Spigot
  alias BindSight.Stage.SpewSupervisor

  @defaults %{camera: :test, action: :snapshot}
  @boundary "--SNAP-HACKLE-STOP--"

  def send(conn, opts) do
    %{camera: camera, action: action} = Enum.into(opts, @defaults)

    case action do
      :snapshot -> send_snapshot(camera, conn)
      :stream -> send_stream(camera, conn)
    end
  end

  defp send_snapshot(camera, conn) do
    [frame | _] = camera |> get_stream |> Enum.take(1)

    conn
    |> put_resp_content_type("image/jpg")
    |> send_resp(200, frame)
  end

  defp send_stream(camera, conn) do
    stream = get_stream(camera)

    contype = "multipart/x-mixed-replace;boundary=#{@boundary}"

    conn =
      conn
      |> put_resp_header("connection", "close")
      |> put_resp_content_type(contype)
      |> send_chunked(200)

    stream |> Stream.map(fn x -> send_frame(conn, x) end) |> Stream.run()
    conn
  end

  defp send_frame(conn, frame) do
    time = System.os_time()

    headers =
      ["", @boundary, "X-Timestamp: #{time}", "Content-Type: image/jpg", "\n"]
      |> Enum.join("\n")

    {:ok, conn} = chunk(conn, headers)
    {:ok, _conn} = chunk(conn, frame)
  end

  defp get_stream(camera) do
    camera = camera |> String.to_existing_atom()
    session = SpewSupervisor.start_session(camera: camera)
    [{Spigot.tap(session), mad_demand: 1}] |> GenStage.stream()
  end
end
