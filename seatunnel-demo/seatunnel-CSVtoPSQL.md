### Start Seatunnel Cluster
```
cd ~/seatunnel
./bin/seatunnel-cluster.sh
```

### Verify if Seatunnel running
```
ps aux | grep -i seatunnel | grep -v grep
```
```
ss -ltnp | grep 5801
```

### Create PostgreSQL DB
```
sudo -u postgres psql -c "CREATE DATABASE seatunnel_demo;"
```

#### Output:
```
CREATE DATABASE
```

### Create Sales Table
```
sudo -u postgres psql -d seatunnel_demo -c "
CREATE TABLE sales (
    id INTEGER,
    customer VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    price NUMERIC(10,2),
    total NUMERIC(12,2)
);"
```

#### Output:
```
CREATE TABLE
```

### Verify Table
```
sudo -u postgres psql -d seatunnel_demo -c "\dt"
```

#### Output
```
         List of relations
 Schema | Name  | Type  |  Owner   
--------+-------+-------+----------
 public | sales | table | postgres
(1 row)
```

### Demo Folder
```
mkdir -p ~/seatunnel-demo
cd ~/seatunnel-demo
```

### Create CSV
```
cat > sales.csv <<'EOF'
id,customer,product,quantity,price
1,Alice,Laptop,2,50000
2,Bob,Mouse,5,800
3,Charlie,Keyboard,2,1500
4,Alice,Monitor,1,12000
5,Bob,Mouse,3,800
6,Diana,Laptop,1,55000
7,Ethan,Keyboard,4,1800
8,Frank,Monitor,2,14000
9,Grace,Mouse,10,750
10,Hannah,Laptop,1,62000
11,Ian,Headphones,3,2500
12,Jack,Keyboard,2,1600
13,Karen,Monitor,1,13500
14,Liam,Mouse,8,700
15,Mia,Laptop,2,58000
16,Noah,Headphones,5,2200
17,Olivia,Monitor,2,12500
18,Paul,Mouse,6,850
19,Quinn,Keyboard,3,1750
20,Rachel,Laptop,1,60000
21,Sam,Monitor,3,13000
22,Tina,Mouse,12,750
23,Umar,Headphones,2,2800
24,Vera,Keyboard,5,1900
25,Will,Laptop,1,52000
26,Xavier,Monitor,2,14500
27,Yara,Mouse,7,800
28,Zack,Headphones,4,2400
29,Alice,Keyboard,2,1700
30,Bob,Laptop,1,57000
31,Charlie,Monitor,1,15000
32,Diana,Mouse,9,780
33,Ethan,Headphones,3,2600
34,Frank,Keyboard,4,1650
35,Grace,Laptop,2,61000
36,Hannah,Monitor,2,13800
37,Ian,Mouse,5,820
38,Jack,Headphones,2,2300
39,Karen,Keyboard,3,1800
40,Liam,Laptop,1,59000
41,Mia,Monitor,1,12800
42,Noah,Mouse,11,760
43,Olivia,Headphones,4,2700
44,Paul,Keyboard,2,1550
45,Quinn,Laptop,2,54000
46,Rachel,Monitor,3,14200
47,Sam,Mouse,6,810
48,Tina,Headphones,5,2500
49,Umar,Keyboard,3,1850
50,Vera,Laptop,1,63000
EOF
```

### Verify
```
wc -l sales.csv
```

#### Output
```
51 sales.csv
```

### Find Seatunnel Connectors
```
find ~ -type f -name "seatunnel.sh" 2>/dev/null
ls -1 /path-to-seatunnel-dir/connectors/ | grep -Ei 'jdbc|postgres|file|hadoop'
```

### Create Seatunnel Config
```
cd ~/seatunnel-demo

cat > csv_to_postgres.conf <<'EOF'
env {
    parallelism = 1
    job.mode = "BATCH"
}

source {
    LocalFile {
        path = "/home/abhi/seatunnel-demo/sales.csv"
        file_format_type = "csv"
        csv_use_header_line = true

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
cd ~/seatunnel-demo
~/seatunnel/bin/seatunnel.sh --config ./csv_to_postgres.conf
```

#### Output
```
2026-08-21 00:16:27,539 INFO  [o.a.s.a.t.f.FactoryUtil       ] [main] - Create sink 'Jdbc' with upstream input catalog-table[database: default, schema: default, table: default]
2026-08-21 00:16:27,619 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Start submit job, job id: 1142892421424611329, with plugin jar [file:/home/abhi/seatunnel/connectors/connector-file-local-2.3.13.jar, file:/home/abhi/seatunnel/connectors/connector-jdbc-2.3.13.jar]
2026-08-21 00:16:27,630 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Submit job finished, job id: 1142892421424611329, job name: SeaTunnel_Job
2026-08-21 00:16:27,642 WARN  [o.a.s.e.c.j.JobMetricsRunner  ] [job-metrics-runner-1142892421424611329] - Failed to get job metrics summary, it maybe first-run
2026-08-21 00:16:28,206 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Job (1142892421424611329) end with state FINISHED
2026-08-21 00:16:28,215 INFO  [s.c.s.s.c.ClientExecuteCommand] [main] - 
***********************************************
           Job Statistic Information
***********************************************
Start Time                : 2026-08-21 00:16:27
End Time                  : 2026-08-21 00:16:28
Total Time(s)             :                   1
Total Read Count          :                  50
Total Write Count         :                  50
Total Failed Count        :                   0
***********************************************
```

### PostgreSQL - Verification
```
psql -h localhost -U postgres -d seatunnel_demo
```
```
SELECT * FROM sales;
SELECT COUNT(*) FROM sales;
```

### PSql JDBC Driver Missing

##### Download
```
sudo apt update
sudo apt install libpostgresql-jdbc-java
```

##### Copy
```
sudo cp /usr/share/java/postgresql-42.7.2.jar ~/seatunnel/connectors/
sudo cp /usr/share/java/postgresql-42.7.2.jar ~/seatunnel/lib/
```

##### Restart Seatunnel
```
~/seatunnel/bin/stop-seatunnel-cluster.sh
~/seatunnel/bin/seatunnel-cluster.sh
```

##### Verify
```
ls ~/seatunnel/connectors/postgresql-42.7.2.jar
ls -lh ~/seatunnel/lib/postgresql-42.7.2.jar
```
