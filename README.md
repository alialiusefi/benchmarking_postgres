This repo contains multiple benchmarking suites to evaluate and analyze postgres behavior against certain configurations.

1. Normal Suite
    * Normal concurrent updates of to a table.
    * Limited by 300 concurrent connections and 150 parallel tasks.
    * Using python, asyncio and psycopg3.
    * Dashboard to monitor metrics: 
      * Custom: http://localhost:3000/d/1/postgres-instance-statistics
        * This dashboard monitors specific metrics that are affected when rows get updated
        * Used sql_exporter to extract specific metrics that are not provided in existing libraries.
      * Imported from grafana dashboards library: http://localhost:3000/d/000000039/postgresql-database?orgId=1&refresh=10s
        * General metrics of postgres.
        * Source: https://grafana.com/grafana/dashboards/9628-postgresql-database/
    * Prometheus exporters:
      * https://github.com/free/sql_exporter for custom metrics.
      * https://github.com/prometheus-community/postgres_exporter for postgres general metrics.
