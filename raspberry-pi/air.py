from sensors import Sensors
from airbrakes import Servo
import json
import time
import logging

# Log everything to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flight_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main flight loop - handles sensors and air brakes"""
    try:
        # Get everything ready
        sensors = Sensors()
        servo = Servo(pin=18)
        
        logger.info("Starting flight monitoring and air brake system...")
        logger.info("Sensor data collection and transmission initialized")
        
        # Keep track of where we are in flight
        flight_started = False
        apogee_detected = False
        last_altitude = 0
        altitude_samples = []
        loop_count = 0
        
        # Here we go!
        while True:
            try:
                loop_count += 1
                
                # Get all the sensor readings
                sensors.sensors_send()
                accX = sensors.getAccelerationX()
                accY = sensors.getAccelerationY()
                accZ = sensors.getAccelerationZ()
                altitude = sensors.getAltitude()
                temperature = sensors.getTemp()
                latitude = sensors.getLatitude()
                longitude = sensors.getLongitude()
                gps_fix = sensors.getGPSFix()
                
                # Remember recent altitudes so we can detect apogee
                altitude_samples.append(altitude)
                if len(altitude_samples) > 10:
                    altitude_samples.pop(0)
                
                # Did we launch yet?
                total_acceleration = (accX**2 + accY**2 + accZ**2)**0.5
                if not flight_started and (altitude > 1000 or total_acceleration > 15):
                    flight_started = True
                    logger.info(f"LIFTOFF! Alt: {altitude}ft, Accel: {total_acceleration}m/s²")
                
                # Open air brakes at 8000 feet
                if altitude >= 8000:
                    servo.open()
                    servo.close()
                
                # Don't spam the logs
                if loop_count % 10 == 0:
                    gps_status = f"GPS: {latitude:.4f},{longitude:.4f}" if gps_fix else "GPS: No fix"
                    logger.info(f"Alt: {altitude}ft, Temp: {temperature}°C, {gps_status}")
                
                # Are we at the top yet?
                if flight_started and len(altitude_samples) >= 5:
                    recent_avg = sum(altitude_samples[-3:]) / 3
                    older_avg = sum(altitude_samples[-6:-3]) / 3
                    
                    if not apogee_detected and recent_avg < older_avg - 10:
                        apogee_detected = True
                        max_alt = max(altitude_samples)
                        logger.info(f"APOGEE! Max altitude: {max_alt}ft")
                        
                        # Don't need brakes on the way down
                        servo.close()
                        logger.info("Brakes closed - coming down now")
                
                # Package up all our data
                flight_data = {
                    "timestamp": time.time(),
                    "altitude": altitude,
                    "temperature": temperature,
                    "acceleration": {
                        "x": accX,
                        "y": accY, 
                        "z": accZ,
                        "total": total_acceleration
                    },
                    "gps": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "has_fix": gps_fix
                    },
                    "flight_state": {
                        "started": flight_started,
                        "apogee_detected": apogee_detected,
                        "loop_count": loop_count
                    }
                }
                
                last_altitude = altitude
                time.sleep(0.1)  # run at 10Hz
                
            except KeyboardInterrupt:
                logger.info("User stopped the flight loop")
                break
            except Exception as e:
                logger.error(f"Something went wrong: {e}")
                # Close brakes if anything breaks
                try:
                    servo.close()
                except:
                    pass
                time.sleep(1)  # wait a bit before trying again
                
    except Exception as e:
        logger.error(f"Main function crashed: {e}")
    finally:
        try:
            servo.close()
            logger.info("Finished")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

if __name__ == "__main__":
    main()

