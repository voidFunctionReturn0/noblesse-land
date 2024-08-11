defmodule Service.Owner do
  use Ecto.Schema
  alias Service.Repo
  alias Service.Owner

  schema "owners" do
    field :name, :string
    field :position, :string
    field :relation, :string
    field :organization, :string # nullable
    field :image_path, :string # nullable
    many_to_many :buildings, Service.Building, join_through: "owners_buildings"
  end

  def get_owner(id) do
    Repo.get(Owner, id)
  end

  def get_owners do
    Repo.all(Owner)
  end
end
