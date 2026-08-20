### Check HDFS Data
```
hdfs dfs -ls /seatunnel-demo/sales
```

#### Output
```
Found 1 items
-rw-r--r--   3 abhi supergroup       1280 2026-08-21 00:30 /seatunnel-demo/sales/T_1142895884468486145_2fc4f6cd7f_0_1_0.csv
```

### Truncate Table if data exists
```
psql -h localhost -U postgres -d seatunnel_demo -c "TRUNCATE TABLE sales;"
```

#### Output
```
TRUNCATE TABLE
```

### Verify Empty Table
```
psql -h localhost -U postgres -d seatunnel_demo -c "SELECT COUNT(*) FROM sales;"
```

#### Output
```
Password for user postgres: 
 count 
-------
     0
(1 row)
```

### Create Seatunnel Config
```
cd ~/seatunnel-demo

cat > hdfs_to_postgres.conf <<'EOF'
env {
    parallelism = 1
    job.mode = "BATCH"
}

source {
    HdfsFile {
        path = "/seatunnel-demo/sales"
        file_format_type = "csv"
        field_delimiter = ","
        fs.defaultFS = "hdfs://localhost:9000"

        schema {
            fields {
                id = int
                customer = string
                product = string
                quantity = int
                price = double
            }
        }
    }
}

sink {
    Jdbc {
        url = "jdbc:postgresql://localhost:5432/seatunnel_demo"
        driver = "org.postgresql.Driver"
        username = "postgres"
        password = "postgres"
        query = "INSERT INTO sales (id, customer, product, quantity, price) VALUES (?, ?, ?, ?, ?)"
    }
}
EOF
```

### Run Seatunnel Job
```
~/seatunnel/bin/seatunnel.sh --config ./hdfs_to_postgres.conf
```

#### Output
```
Create sink 'Jdbc' with upstream input catalog-table[database: default, schema: default, table: default]
2026-08-21 00:55:28,938 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Start submit job, job id: 1142902240852312065, with plugin jar [file:/home/abhi/seatunnel/connectors/connector-file-hadoop-2.3.13.jar, file:/home/abhi/seatunnel/connectors/connector-jdbc-2.3.13.jar]
2026-08-21 00:55:28,973 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Submit job finished, job id: 1142902240852312065, job name: SeaTunnel_Job
2026-08-21 00:55:28,985 WARN  [o.a.s.e.c.j.JobMetricsRunner  ] [job-metrics-runner-1142902240852312065] - Failed to get job metrics summary, it maybe first-run
2026-08-21 00:55:29,514 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Job (1142902240852312065) end with state FINISHED
2026-08-21 00:55:29,520 INFO  [s.c.s.s.c.ClientExecuteCommand] [main] - 
***********************************************
           Job Statistic Information
***********************************************
Start Time                : 2026-08-21 00:55:28
End Time                  : 2026-08-21 00:55:29
Total Time(s)             :                   1
Total Read Count          :                  50
Total Write Count         :                  50
Total Failed Count        :                   0
***********************************************
```

### Verify in Postgres
```
psql -h localhost -U postgres -d seatunnel_demo
SELECT COUNT(*) FROM sales;
SELECT * FROM sales ORDER BY id LIMIT 10;
```

#### Output
```
 count 
-------
    50
(1 row)
```
```
 id | customer | product  | quantity |  price   | total 
----+----------+----------+----------+----------+-------
  1 | Alice    | Laptop   |        2 | 50000.00 |      
  2 | Bob      | Mouse    |        5 |   800.00 |      
  3 | Charlie  | Keyboard |        2 |  1500.00 |      
  4 | Alice    | Monitor  |        1 | 12000.00 |      
  5 | Bob      | Mouse    |        3 |   800.00 |      
  6 | Diana    | Laptop   |        1 | 55000.00 |      
  7 | Ethan    | Keyboard |        4 |  1800.00 |      
  8 | Frank    | Monitor  |        2 | 14000.00 |      
  9 | Grace    | Mouse    |       10 |   750.00 |      
 10 | Hannah   | Laptop   |        1 | 62000.00 |      
(10 rows)
```