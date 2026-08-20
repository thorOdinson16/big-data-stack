### Start HDFS
```
start-dfs.sh
```

#### Verify
```
jps
```

### Verify HDFS itself
```
hdfs dfs -ls /
```

### Create the destination
```
hdfs dfs -mkdir -p /seatunnel-demo/sales
```

#### Verify:
```
hdfs dfs -ls /seatunnel-demo
```

#### Output
```
Found 1 items
drwxr-xr-x   - abhi supergroup          0 2026-08-21 00:25 /seatunnel-demo/sales
```

### Check SeaTunnel connectors
```
ls -1 ~/seatunnel/connectors/ | grep -Ei 'hdfs|hadoop|file'
```

#### Output
```
connector-file-hadoop-2.3.13.jar
```

### Create HDFS Config
```
cd ~/seatunnel-demo

cat > csv_to_hdfs.conf <<'EOF'
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
    HdfsFile {
        path = "/seatunnel-demo/sales"
        file_format_type = "csv"
        field_delimiter = ","

        fs.defaultFS = "hdfs://localhost:9000"
    }
}
EOF
```

### Run Seatunnel Job
```
~/seatunnel/bin/seatunnel.sh --config ./csv_to_hdfs.conf
```

### Output
```
2026-08-21 00:30:13,146 INFO  [o.a.s.a.t.f.FactoryUtil       ] [main] - Create sink 'HdfsFile' with upstream input catalog-table[database: default, schema: default, table: default]
2026-08-21 00:30:13,225 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Start submit job, job id: 1142895884468486145, with plugin jar [file:/home/abhi/seatunnel/connectors/connector-file-hadoop-2.3.13.jar, file:/home/abhi/seatunnel/connectors/connector-file-local-2.3.13.jar]
2026-08-21 00:30:13,537 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Submit job finished, job id: 1142895884468486145, job name: SeaTunnel_Job
2026-08-21 00:30:13,546 WARN  [o.a.s.e.c.j.JobMetricsRunner  ] [job-metrics-runner-1142895884468486145] - Failed to get job metrics summary, it maybe first-run
2026-08-21 00:30:14,680 INFO  [o.a.s.e.c.j.ClientJobProxy    ] [main] - Job (1142895884468486145) end with state FINISHED
2026-08-21 00:30:14,686 INFO  [s.c.s.s.c.ClientExecuteCommand] [main] - 
***********************************************
           Job Statistic Information
***********************************************
Start Time                : 2026-08-21 00:30:12
End Time                  : 2026-08-21 00:30:14
Total Time(s)             :                   1
Total Read Count          :                  50
Total Write Count         :                  50
Total Failed Count        :                   0
***********************************************
```

### Verify
```
hdfs dfs -ls /seatunnel-demo/sales
```

```
hdfs dfs -cat /seatunnel-demo/sales/*
```

```
hdfs dfs -cat /seatunnel-demo/sales/* | awk 'END {print NR}'
```

#### Output
```
Found 1 items
-rw-r--r--   3 abhi supergroup       1280 2026-08-21 00:30 /seatunnel-demo/sales/T_1142895884468486145_2fc4f6cd7f_0_1_0.csv
```

```
1,Alice,Laptop,2,50000.0
2,Bob,Mouse,5,800.0
3,Charlie,Keyboard,2,1500.0
4,Alice,Monitor,1,12000.0
5,Bob,Mouse,3,800.0
6,Diana,Laptop,1,55000.0
7,Ethan,Keyboard,4,1800.0
8,Frank,Monitor,2,14000.0
9,Grace,Mouse,10,750.0
10,Hannah,Laptop,1,62000.0
11,Ian,Headphones,3,2500.0
12,Jack,Keyboard,2,1600.0
13,Karen,Monitor,1,13500.0
14,Liam,Mouse,8,700.0
15,Mia,Laptop,2,58000.0
16,Noah,Headphones,5,2200.0
17,Olivia,Monitor,2,12500.0
18,Paul,Mouse,6,850.0
19,Quinn,Keyboard,3,1750.0
20,Rachel,Laptop,1,60000.0
21,Sam,Monitor,3,13000.0
22,Tina,Mouse,12,750.0
23,Umar,Headphones,2,2800.0
24,Vera,Keyboard,5,1900.0
25,Will,Laptop,1,52000.0
26,Xavier,Monitor,2,14500.0
27,Yara,Mouse,7,800.0
28,Zack,Headphones,4,2400.0
29,Alice,Keyboard,2,1700.0
30,Bob,Laptop,1,57000.0
31,Charlie,Monitor,1,15000.0
32,Diana,Mouse,9,780.0
33,Ethan,Headphones,3,2600.0
34,Frank,Keyboard,4,1650.0
35,Grace,Laptop,2,61000.0
36,Hannah,Monitor,2,13800.0
37,Ian,Mouse,5,820.0
38,Jack,Headphones,2,2300.0
39,Karen,Keyboard,3,1800.0
40,Liam,Laptop,1,59000.0
41,Mia,Monitor,1,12800.0
42,Noah,Mouse,11,760.0
43,Olivia,Headphones,4,2700.0
44,Paul,Keyboard,2,1550.0
45,Quinn,Laptop,2,54000.0
46,Rachel,Monitor,3,14200.0
47,Sam,Mouse,6,810.0
48,Tina,Headphones,5,2500.0
49,Umar,Keyboard,3,1850.0
50,Vera,Laptop,1,63000.0
```

```
50
```

### Error
```
Sink in config file needs to have defaultFS
```