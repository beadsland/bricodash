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

defmodule BindSight.WebAPI.Home do
  import Plug.Conn
  import Phoenix.HTML
  import Phoenix.HTML.Tag
  use Memoize

  def send(conn, opts) do
    divs = links(opts[:cameras])
    body = content_tag(:body, [content_tag(:h1, "Howdy!"), divs])
    conn |> send_resp(200, body |> safe_to_string)
  end

  defp links([]), do: []
  defp links([head | tail]) do
    html = [camera(head), rest(head, :snapshot), rest(head, :stream), tag(:hr)]
    [html, links(tail)]
  end

  defp spacer(), do: raw(" &mdash; ")
  defp camera(text), do: content_tag(:h2, text, [style: "display:inline"])
  defp rest(camera, action), do: [spacer(), anchor(action, "#{camera}/#{action}")]
  defp anchor(text, url), do: content_tag(:a, text, [href: url])

end
