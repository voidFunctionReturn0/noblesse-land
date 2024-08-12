defmodule Service.Building do
  use Ecto.Schema
  import Ecto.Query
  alias Service.Repo
  alias Service.Building

  schema "buildings" do
    field :type, :string
    field :details, :string
    field :price, :integer
    field :note, :string
    field :coordinates, Service.Point
    many_to_many :owners, Service.Owner, join_through: "owners_buildings"
  end

  def get_building(id) do
    Repo.get(Building, id)
  end

  def get_buildings do
    Building
    |> where([b], not is_nil b.coordinates) # TODO: coordinate가 필수로 있도록 하기
    |> Repo.all()
  end
end
