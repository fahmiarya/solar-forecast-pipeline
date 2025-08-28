from influxdb_client import InfluxDBClient, Point
from datetime import datetime, timezone

# Config
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "super-token-123"
ORG = "myorg"
BUCKET = "energy"

def debug_influxdb():
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    
    try:
        # 1. Test connection
        health = client.health()
        print(f"✅ InfluxDB Health: {health.status}")
        
        # 2. List buckets
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets()
        print(f"📦 Available buckets: {[b.name for b in buckets.buckets]}")
        
        # 3. Write one test point
        print("📤 Writing test point...")
        write_api = client.write_api()
        test_point = Point("test_measurement") \
            .tag("location", "test") \
            .field("test_field", 123.45) \
            .time(datetime.now(timezone.utc))
        
        write_api.write(bucket=BUCKET, record=test_point)
        print("✅ Test point written")
        
        # 4. Query test point
        print("🔍 Querying test point...")
        query_api = client.query_api()
        
        # Try different queries
        queries = [
            f'from(bucket: "{BUCKET}") |> range(start: -1h) |> limit(n: 10)',
            f'from(bucket: "{BUCKET}") |> range(start: -24h) |> limit(n: 10)',
            f'from(bucket: "{BUCKET}") |> range(start: -400d) |> limit(n: 10)',
            f'buckets()',
        ]
        
        for i, query_str in enumerate(queries):
            print(f"\n📋 Query {i+1}: {query_str}")
            try:
                result = query_api.query(query_str)
                records = []
                for table in result:
                    for record in table.records:
                        records.append(record)
                
                if records:
                    print(f"✅ Found {len(records)} records")
                    for j, record in enumerate(records[:3]):
                        if hasattr(record, 'get_time'):
                            print(f"   {j+1}. {record.get_time()}: {getattr(record, 'get_field', lambda: 'N/A')()} = {getattr(record, 'get_value', lambda: 'N/A')()}")
                        else:
                            print(f"   {j+1}. {record}")
                else:
                    print("❌ No records found")
                    
            except Exception as e:
                print(f"❌ Query failed: {e}")
        
        # 5. Check specific measurement
        print(f"\n🔍 Checking 'weather' measurement...")
        weather_query = f'''
        from(bucket: "{BUCKET}")
        |> range(start: -400d)
        |> filter(fn: (r) => r._measurement == "weather")
        |> limit(n: 5)
        '''
        
        try:
            result = query_api.query(weather_query)
            records = []
            for table in result:
                for record in table.records:
                    records.append(record)
            
            if records:
                print(f"✅ Found {len(records)} weather records")
            else:
                print("❌ No weather records found")
                
        except Exception as e:
            print(f"❌ Weather query failed: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        client.close()

if __name__ == "__main__":
    debug_influxdb()