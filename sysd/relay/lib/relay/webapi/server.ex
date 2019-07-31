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

defmodule Relay.WebAPI.Server do
  require Logger
  use Application

  def start(_type, _args) do
    {:ok, hostname} = :inet.gethostname()
    nodename = String.to_atom( "relay@#{hostname}" )
    {:ok, _pid} = :net_kernel.start([nodename])

    transport = if Mix.env == :dev, do: [num_acceptors: 5], else: []

    port = Application.get_env(:relay, :port)
    children = [
      { Plug.Cowboy, scheme: :http, plug: Relay.WebAPI.Router,
                     options: [port: port, transport_options: transport] }
    ]
    opts = [strategy: :one_for_one, name: Relay.WebAPI.Supervisor]

    Logger.info("Starting camera relay...")

    Supervisor.start_link(children, opts)
  end

end