defmodule Service.OwnerBuilding do
  use Ecto.Schema
  alias Service.Repo
  alias Service.OwnerBuilding

  schema "owner_buildings" do
    field :owner_id, :integer
    field :building_id, :integer
    field :created_at, :naive_datetime
  end

  def get_owner_building(id) do
    Repo.get(OwnerBuilding, id)
  end

  def get_owners_buildings do
    Repo.all(OwnerBuilding)
  end
end
