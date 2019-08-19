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

defmodule BindSight.Stage.Slurp.Request do
  @moduledoc "Slurp spigot producer to request snapshots from a camera."

  use BindSight.Common.MintJulep

  alias BindSight.Common.Camera
  alias BindSight.Common.Library

  @defaults %{camera: :test, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, name: name} = Enum.into(opts, @defaults)
    MintJulep.start_link(__MODULE__, camera, name: name)
  end

  @impl true
  def init(camera) do
    uri =
      camera
      |> Library.get_camera_url()
      |> URI.parse()
      |> Camera.build_request(Library.get_camera_api(camera), :stream)

    {:producer, _state = MintJulep.sip(__MODULE__, uri)}
  end

  @impl true
  def handle_mint(resp, state) do
    if Enum.reduce(resp, nil, fn x, accu -> find_done(x, accu) end) do
      # because snap
      Process.sleep(100)
      {:noreply, resp, _state = MintJulep.sip(state)}
    else
      {:noreply, resp, state}
    end
  end

  defp find_done(x, accu) do
    #    IO.inspect(x)

    case x do
      {:done, _ref} -> true
      _ -> accu
    end
  end

  @impl true
  def handle_demand(_demand, state) do
    {:noreply, [], state}
  end
end
