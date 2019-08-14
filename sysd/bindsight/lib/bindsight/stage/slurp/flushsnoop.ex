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

defmodule BindSight.Stage.Slurp.FlushSnoop do
  @moduledoc "Slurp snoop to keep camera feed flushing even when no spew clients."

  use GenStage

  alias BindSight.Common.Library

  @defaults %{source: :producer_not_specified, name: __MODULE__}

  def start_link(opts \\ []) do
    %{camera: camera, source: source} = Enum.into(opts, @defaults)

    GenStage.start_link(__MODULE__, source,
      name: Library.get_register_name({:flush, camera, :snoop})
    )
  end

  def init(source) do
    {:consumer, :stateless, subscribe_to: [source]}
  end

  def handle_events(_events, _from, :stateless) do
    {:noreply, [], :stateless}
  end
end
