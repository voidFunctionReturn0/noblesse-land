defmodule Service.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      ServiceWeb.Telemetry,
      Service.Repo,
      {DNSCluster, query: Application.get_env(:service, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: Service.PubSub},
      # Start a worker by calling: Service.Worker.start_link(arg)
      # {Service.Worker, arg},
      # Start to serve requests, typically the last entry
      ServiceWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Service.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    ServiceWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
