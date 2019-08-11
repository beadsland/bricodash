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

defmodule BindSight.WebAPI.Error do
  @moduledoc "Plug for generic 500 status error message."

  import Plug.Conn
  import Phoenix.HTML
  import Phoenix.HTML.Tag

  alias BindSight.Common.Library

  @error_msg "Ditty's gone catawampous, it has."

  @cluck Library.get_env(:cluck_errors)

  def send(conn, opts) do
    error =
      if @cluck do
        IO.puts(cluck(opts))
        body = [content_tag(:h1, @error_msg), content_tag(:pre, cluck(opts))]
        content_tag(:body, body) |> safe_to_string
      else
        @error_msg
      end

    send_resp(conn, conn.status, error)
  end

  defp cluck(opts) do
    kind = spect(opts, :kind)
    reason = spect(opts, :reason)
    stack = spect(opts, :stack)
    "#{kind}\n#{reason}\n#{stack}\n"
  end

  defp spect(opts, label) do
    str = inspect(opts[label], label: label, pretty: true, limit: 7)
    "#{label}: #{str}"
  end
end
