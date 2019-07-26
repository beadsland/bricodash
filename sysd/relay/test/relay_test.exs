defmodule RelayTest do
  use ExUnit.Case
  doctest Relay

  test "get :test camera path" do
    assert Relay.get_camera(:test) == "http://192.168.42.22:8080/"
  end

  test "greets the world" do
    assert Relay.poke_camera() == :ok
  end
end
