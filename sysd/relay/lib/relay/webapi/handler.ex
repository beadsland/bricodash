#Ref: https://angelika.me/2016/08/14/hello-world-web-app-in-elixir-part-1-cowboy/

defmodule Relay.WebAPI.Handler do
  def init(request, options) do
    if (:cowboy_req.method(request) == "GET") do
      name = :cowboy_req.binding(:name, request, "World")
      headers = [{"content-type", "text/plain"}]
      body = "Hello, #{String.capitalize(name)}!"

      request2 = :cowboy_req.reply(200, headers, body, request)
      {:ok, request2, options}
    else
#      Relay.WebAPI.Goodbye.init(options)
    end
  end
end
