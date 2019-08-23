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

defmodule BindSight.Common.MintJulep do
  @moduledoc "Poll to obtain MJPEG snapshots as Mint messages."

  @type state() :: {mod :: atom(), uri :: %URI{}, conn :: :deferred | term()}

  @type genstage_return() ::
          {:noreply, [event :: term()], new_state :: state()}
          | {:noreply, [event :: term()], new_state :: state(), :hibernate}
          | {:stop, reason :: term(), new_state :: state()}

  @callback handle_normal_info(msg :: :timeout | term(), state()) ::
              genstage_return()

  @callback handle_mint(resp :: [term()], state()) ::
              genstage_return()

  @optional_callbacks handle_normal_info: 2

  defmacro __using__(_) do
    quote([]) do
      @behaviour BindSight.Common.MintJulep

      use GenStage
      require Logger

      alias BindSight.Common.Library
      alias BindSight.Common.MintJulep

      @impl true
      def handle_info(message, _state = {mod, uri, :deferred}),
        do:
          handle_info(message, _state = {mod, uri, MintJulep.connect(mod, uri)})

      def handle_info(:unfold_deferred_state, state),
        do: {:noreply, [], state}

      def handle_info(message, state = {mod, uri, conn}) do
        case Mint.HTTP.stream(conn, message) do
          :unknown ->
            apply(mod, :handle_normal_info, [message, state])

          # HACK When mint reads cowboy stream, it never flushes data_buffer,
          # but instead passes messages with empty response lists.
          #
          # This rule does what ought to be happening in
          # mint.http1.collapse_body_buffer/2 (lines 761-770).
          #
          # Possibly related to cowboy glitch of appending charset to boundary
          # in multipart content-type.

          {:ok, conn, []} ->
            buff = IO.iodata_to_binary(conn.request[:data_buffer])
            conn = %{conn | request: Map.put(conn.request, :data_buffer, [])}

            apply(mod, :handle_mint, [
              [{:data, nil, buff}],
              _state = {mod, uri, conn}
            ])

          {:ok, conn, resp} ->
            apply(mod, :handle_mint, [resp, _state = {mod, uri, conn}])

          {:error, conn, err, resp} ->
            {:noreply, resp,
             _state = MintJulep.sip(_state = {mod, uri, conn}, :response, err)}
        end
      end

      def handle_normal_info(resp, state = {mod, uri, conn}) do
        ["MintJulep", uri, "unknown info message", inspect(resp)]
        |> Library.error_chain()
        |> Logger.error()

        {:noreply, [], state}
      end

      defoverridable handle_normal_info: 2
    end
  end

  require Logger

  alias BindSight.Common.Library

  def start_link(mod, args, opts), do: GenStage.start_link(mod, args, opts)

  @doc "Return state for polling cameras, logging error if any."
  def sip(mod, uri = %URI{}) when is_atom(mod) do
    send(self(), :unfold_deferred_state)
    {mod, uri, :deferred}
  end

  def sip(_state = {mod, uri, conn}, call \\ nil, err \\ nil) do
    if conn, do: Mint.HTTP.close(conn)

    if err do
      path = Library.query_path(uri)

      [["Failed ", call], [uri.host, ":", uri.port, "/", path], inspect(err)]
      |> Library.error_chain()
      |> Logger.warn()

      Process.sleep(1000)
    end

    sip(mod, uri)
  end

  @doc "Callback to connect to camera host and issue a request thereto."
  def connect(mod, uri) do
    case mint_connect(uri.scheme |> String.to_atom(), uri.host, uri.port) do
      {:ok, conn} -> request(mod, uri, conn)
      {:error, err} -> sip({mod, uri, nil}, :connect, err)
    end
  end

  # Try ipv6 by default, but fail-over to ipv4 gracefully.
  defp mint_connect(scheme, host, port) do
    opts = [transport_opts: [{:tcp_module, :inet6_tcp}]]

    case Mint.HTTP.connect(scheme, host, port, opts) do
      {:ok, conn} -> {:ok, conn}
      _ -> Mint.HTTP.connect(scheme, host, port, [])
    end
  end

  defp request(mod, uri, conn) do
    case Mint.HTTP.request(conn, "GET", Library.query_path(uri), []) do
      {:ok, conn, _ref} -> conn
      {:error, conn, err} -> sip({mod, uri, conn}, :request, err)
    end
  end
end
