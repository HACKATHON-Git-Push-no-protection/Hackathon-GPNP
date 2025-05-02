import React from "react";
import { LogEntry } from "../types/logTypes";
import SensorDisplay from "./SensorDisplay";

interface LogTableProps {
  logs: LogEntry[];
}

const LogTable: React.FC<LogTableProps> = ({ logs }) => {
  return (
    <div className="max-w-3xl mx-auto mt-6">
      <h2 className="text-2xl font-semibold mb-4">📜 MQTT Logs</h2>

      {logs.length === 0 ? (
        <p className="text-gray-500">No logs available.</p>
      ) : (
        <div className="space-y-6">
          {logs.map((log, index) => (
            <div key={index} className="p-4 border rounded-lg bg-gray-100 shadow-md">
              <h3 className="text-lg font-medium text-gray-700">Topic: {log.topic}</h3>
              <SensorDisplay data={log.data} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LogTable;
