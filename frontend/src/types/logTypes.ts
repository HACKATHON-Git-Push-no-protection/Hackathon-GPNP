export interface SensorData {
  timestamp: string;
  sensors: {
    temperature: { value: number; unit: string };
    humidity: { value: number; unit: string };
    soil_moisture: {
      sensor_1: { value: number; unit: string };
      sensor_2: { value: number; unit: string };
    };
    light_intensity: { value: number; unit: string };
    CO2_level: { value: number; unit: string };
    air_pressure: { value: number; unit: string };
    proximity_sensor: { object_detected: boolean };
    PIR_motion_sensor: { motion_detected: boolean };
    button_press: { button_1: boolean; button_2: boolean };
    servo_motor: { position: number; unit: string };
    "7_segment_display": { value: string };
    LED_status: { grow_light: string; indicator: string };
  };
}

  
  export interface LogEntry {
    topic: string;
    data: SensorData;
  }
  