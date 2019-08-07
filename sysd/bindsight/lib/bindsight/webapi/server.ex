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

defmodule BindSight.WebAPI.Server do
  @moduledoc "Cowboy server instance for BindSight WebAPI."

  require Logger
  use Application

  def start(_type, _args) do
    port = Application.get_env(:bindsight, :cowboy_port, 2020)
    acceptors = Application.get_env(:bindsight, :cowboy_acceptors, 100)
    transport = [num_acceptors: acceptors]

    children = [
      { Plug.Cowboy, scheme: :http, plug: BindSight.WebAPI.Router,
                     options: [port: port, transport_options: transport] }
    ]
    opts = [strategy: :one_for_one, name: BindSight.WebAPI.Supervisor]

    Logger.info("Starting camera relay...")

    Supervisor.start_link(children, opts)
  end

end
