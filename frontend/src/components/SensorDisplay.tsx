import React from "react";
import { SensorData } from "../types/logTypes";

interface SensorDisplayProps {
  data: SensorData;
}

const SensorDisplay: React.FC<SensorDisplayProps> = ({ data }) => {
  return (
    <div className="max-w-2xl mx-auto mt-6 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">🌡️ Sensor Data</h2>
      <p className="text-gray-500 text-sm mb-4">
        Timestamp: {new Date(data.timestamp).toLocaleString()}
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {Object.entries(data.sensors).map(([key, value]) => (
          <div key={key} className="p-4 border rounded-lg bg-gray-100">
            <h3 className="text-lg font-medium capitalize">{key.replace(/_/g, " ")}</h3>

            {typeof value === "object" && !Array.isArray(value) ? (
              Object.entries(value).map(([subKey, subValue]) =>
                typeof subValue === "object" ? (
                  <p key={subKey} className="text-gray-600 ml-2">
                    <span className="font-semibold">{subKey.replace(/_/g, " ")}:</span>{" "}
                    {subValue.value} {subValue.unit}
                  </p>
                ) : (
                  <p key={subKey} className="text-gray-600">
                    <span className="font-semibold">{subKey.replace(/_/g, " ")}:</span>{" "}
                    {String(subValue)}
                  </p>
                )
              )
            ) : (
              <p className="text-gray-600">{String(value)}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SensorDisplay;
