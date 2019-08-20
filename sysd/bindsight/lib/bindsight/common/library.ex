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

defmodule BindSight.Common.Library do
  @moduledoc "Commonly used functions are functions used commonly."

  use Memoize

  @doc "Retrieve camera URL by name from config."
  def get_camera_url(name), do: name |> get_camera_info() |> elem(0)

  @doc "Retrieve camera API by name from config."
  def get_camera_api(name), do: name |> get_camera_info() |> elem(1)

  defp get_camera_info(name) do
    cameras = Application.fetch_env!(:bindsight, :cameras)

    case cameras[name] do
      {url, api} when is_binary(url) and is_atom(api) ->
        {url, api}

      url when is_binary(url) ->
        {url, get_env(:common_api, :no_api_configured)}

      input ->
        raise ArgumentError,
              "#{name} config expected string or string/atom tuple: " <>
                inspect(input)
    end
  end

  @doc "Return unique registerable name for process, shortname if dev/test."
  def get_register_name(tup) when is_tuple(tup) do
    list = tup |> Tuple.to_list()

    if Enum.all?(list, fn x -> is_atom(x) end) do
      list |> Enum.join(":") |> get_register_name()
    else
      {:via, Registry, {Registry.BindSight, tup}}
    end
  end

  def get_register_name(name) do
    if get_env(:register_shortnames, false) do
      "#{name}" |> String.to_atom()
    else
      "bindsight_#{name}" |> String.to_atom()
    end
  end

  @doc "Get config parameters for our application."
  def get_env(key, default \\ nil) do
    Application.get_env(:bindsight, key, default)
  end

  @doc "Return full path and query from a URI."
  def query_path(uri), do: [uri.path, uri.query] |> Enum.join("?")

  @doc "Return IOList interspersed with colons."
  def error_chain(list), do: Enum.intersperse(list, ": ")
end
