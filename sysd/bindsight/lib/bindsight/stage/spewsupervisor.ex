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

defmodule BindSight.Stage.SpewSupervisor do
  @moduledoc "Supervise spew spigot (client pipeline segment) for each client."

  use DynamicSupervisor
  require Logger

  alias BindSight.Stage.Spew.Spigot
  alias BindSight.Stage.SpewCounter

  @defaults %{camera: :test}

  def start_link(_) do
    Logger.info("Ready to spew clients...")
    DynamicSupervisor.start_link(__MODULE__, [], name: :spewsup)
  end

  @impl true
  def init(_) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end

  def start_session(opts) do
    %{camera: camera} = Enum.into(opts, @defaults)
    session = SpewCounter.next()

    DynamicSupervisor.start_child(
      :spewsup,
      {Spigot, camera: camera, session: session}
    )

    session
  end
end
