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

  use Supervisor
  require Logger

  alias BindSight.Common.Library

  def start_link(_) do
    Logger.info("Yeehaw cowboy...")

    Supervisor.start_link(__MODULE__, nil,
      name: Library.get_register_name(:wapisup)
    )
  end

  def init(_) do
    port = Library.get_env(:cowboy_port, 2020)
    acceptors = Library.get_env(:cowboy_acceptors, 100)
    transport = [num_acceptors: acceptors]

    children = [
      {Plug.Cowboy,
       scheme: :http,
       plug: BindSight.WebAPI.Router,
       options: [port: port, transport_options: transport]}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
