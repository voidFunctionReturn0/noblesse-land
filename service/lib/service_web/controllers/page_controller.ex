defmodule ServiceWeb.PageController do
  use ServiceWeb, :controller

  def home(conn, _params) do
    render(conn, :home, layout: false)
  end
end
