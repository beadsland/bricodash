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

defmodule BindSight.Common.Camera do
  @moduledoc "API interface definitions for common camera and server types."

  def build_request(uri, api, action) do
    case api do
      :mjpg_streamer -> mjpg_streamer(uri, action)
      _ -> raise("#{uri}: unknown camera interface: " <> inspect(api))
    end
  end

  def mjpg_streamer(uri, action) do
    case action do
      :snapshot -> uri |> query_put(:action, :snapshot)
      :stream -> uri |> query_put(:action, :stream)
    end
  end

  defp query_put(uri, key, value) do
    query = if uri.query, do: uri.query, else: ""
    query = query |> URI.decode_query(%{key => value})
    uri |> Map.put(:query, URI.encode_query(query))
  end
end
