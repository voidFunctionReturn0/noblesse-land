defmodule Service.Repo do
  use Ecto.Repo,
    otp_app: :service,
    adapter: Ecto.Adapters.Postgres
end
