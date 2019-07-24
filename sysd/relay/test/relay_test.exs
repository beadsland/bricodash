defmodule RelayTest do
  use ExUnit.Case
  doctest Relay

  test "greets the world" do
    assert Relay.camera() == :ok
  end
end
