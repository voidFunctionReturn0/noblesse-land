defmodule Service.Repo.Migrations.CreateOwnersBuidlings do
  use Ecto.Migration

  def change do
    create table(:owners_buildings) do
      add :owner_id, references(:owners)
      add :building_id, references(:buildings)
      add :created_at, :naive_datetime
    end

    create unique_index(:owners_buildings, [:owner_id, :building_id])
  end
end
