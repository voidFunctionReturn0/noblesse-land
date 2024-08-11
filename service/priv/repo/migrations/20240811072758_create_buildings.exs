defmodule Service.Repo.Migrations.CreateBuildings do
  use Ecto.Migration

  def change do
    create table(:buildings) do
      add :type, :string, null: false
      add :details, :string, null: false
      add :price, :bigint, null: false
      add :note, :string
      add :coordinates, :point
    end

    create unique_index(:buildings, [:details])
  end
end
