defmodule Service.Repo.Migrations.CreateOwners do
  use Ecto.Migration

  def change do
    create table(:owners) do
      add :name, :string, null: false
      add :position, :string, null: false
      add :relation, :string, null: false
      add :organization, :string
      add :image_path, :string
    end
  end
end
