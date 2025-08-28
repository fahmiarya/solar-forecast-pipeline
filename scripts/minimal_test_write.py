from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

# Config
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "super-token-123"
ORG = "myorg"
BUCKET = "energy"

def test_write():
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    
    try:
        # Use synchronous write
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # Write a few test points with current timestamp
        now = datetime.now(timezone.utc)
        
        points = []
        for i in range(3):
            point = Point("weather") \
                .tag("location", "jakarta") \
                .field("ghi_kwh_m2", float(4.5 + i)) \
                .field("temp_c", float(28.0 + i)) \
                .field("rh_pct", float(80.0 + i)) \
                .field("wind_ms", float(2.0 + i * 0.1)) \
                .time(now)
            points.append(point)
        
        print(f"📤 Writing {len(points)} test points with current timestamp...")
        write_api.write(bucket=BUCKET, record=points)
        print("✅ Test points written successfully")
        
        # Immediate verification
        print("🔍 Immediate verification...")
        query_api = client.query_api()
        
        # Query recent data (last 1 hour)
        verify_query = f'''
        from(bucket: "{BUCKET}")
        |> range(start: -1h)
        |> limit(n: 10)
        '''
        
        try:
            result = query_api.query(verify_query)
            records = []
            for table in result:
                for record in table.records:
                    records.append(record)
            
            if records:
                print(f"✅ Verification successful! Found {len(records)} records")
                for i, record in enumerate(records[:3]):
                    print(f"   {i+1}. Time: {record.get_time()}")
                    print(f"      Field: {record.get_field()} = {record.get_value()}")
            else:
                print("❌ No records found in verification")
                
        except Exception as e:
            print(f"❌ Verification query failed: {e}")
            
    except Exception as e:
        print(f"❌ Write failed: {e}")
        
    finally:
        client.close()

if __name__ == "__main__":
    test_write()