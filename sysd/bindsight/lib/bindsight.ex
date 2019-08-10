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

defmodule BindSight do
  @moduledoc "Concurrent frame-scrubbing webcam broadcast gateway daemon."

  alias BindSight.Stage.SlurpSupervisor
  alias BindSight.WebAPI.Server

  def start(type, args) do
    Port.open({:spawn, "epmd -daemon"}, [:binary])
    {:ok, hostname} = :inet.gethostname()

    {:ok, _pid} =
      [String.to_atom("bindsight@#{hostname}")]
      |> :net_kernel.start()

    SlurpSupervisor.start_link([])
    Server.start(type, args)
  end

  @doc "Retrieve camera URL by name from config."
  def get_camera_url(name) do
    cameras = Application.fetch_env!(:bindsight, :cameras)
    cameras[name]
  end
end
