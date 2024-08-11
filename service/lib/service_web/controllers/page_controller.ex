defmodule ServiceWeb.PageController do
  use ServiceWeb, :controller
  alias Service.{
    OwnerBuilding,
    Building,
    Owner,
    # Point,
  }

  def home(conn, _params) do
    _owners_buildings = OwnerBuilding.get_owners_buildings()
    buildings = Building.get_buildings()
    _owners = Owner.get_owners()
    render(conn, :home, layout: false, buildings: buildings)
  end
end
